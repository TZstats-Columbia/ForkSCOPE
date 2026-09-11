#!/usr/bin/env python3
"""Apply the stability rule: a merge two builds disagree about is undone.

No model calls. This is the implementation of the rule the audit has been
*reporting* since S4 existed but nothing applied.

THE RULE
--------
The pipeline's governing asymmetry (docs/METHODS.md, and every repair pass) is
that over-merge is invisible in the output and unrecoverable, while under-merge
is visible and fixable later. Replication gives a new way to detect a suspect
merge: if build A puts two decisions in one cluster and build B does not, the
pipeline has answered "are these the same?" both ways, and neither answer is
privileged.

So the arbitrated vocabulary keeps two decisions together **only if every build
kept them together**. Formally that is the *meet* of the partitions -- their
coarsest common refinement -- and it is exactly "default to unmerged".

WHY NOT MAJORITY VOTE
---------------------
With K=3 a majority rule would retain any merge 2 builds of 3 made. That
silently keeps merges one build rejected, which is the over-merge the whole
design exists to prevent, and it does so at the moment we have the clearest
possible evidence the merge is disputed. Majority vote is the right rule when
errors are symmetric. Here they are not.

The cost is real and is stated rather than hidden: the meet is finer than any
input, so the arbitrated vocabulary has MORE clusters than any single build.
That is the intended direction -- a split is recoverable by a later human
merge; the merge it replaces was not recoverable at all.

WHAT COMES OUT
--------------
  arbitrated vocabulary   same schema, safe to feed to any analysis
  review queue (CSV)      every disputed group, worst-first, for a human to
                          adjudicate -- because the meet is a safe default,
                          not an answer

Usage:
    python3 stability/scripts/arbitrate.py --vocab A.json B.json [C.json ...]
        --level option --out arbitrated.json --queue review.csv
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import partition as P                                          # noqa: E402


def meet(labelings, keys):
    """Coarsest common refinement: group by the TUPLE of labels across builds.

    Two instances land together only if every build agreed. This is O(n) and
    exact -- no pairwise comparison, no threshold, nothing to tune.
    """
    groups = defaultdict(list)
    for k in keys:
        groups[tuple(lab[k] for lab in labelings)].append(k)
    return groups


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vocab", nargs="+", required=True,
                    help="two or more build vocabularies; the first is the "
                         "one whose labels and metadata are carried forward")
    ap.add_argument("--level", choices=["option", "fork"], default="option")
    ap.add_argument("--out", help="write the arbitrated vocabulary here")
    ap.add_argument("--queue", help="write the human review queue here (CSV)")
    x = ap.parse_args()

    if len(x.vocab) < 2:
        sys.exit("arbitration needs at least two builds")

    labs = []
    for p in x.vocab:
        lab, _ = P.labeling(p, x.level)
        labs.append(lab)
    keys = sorted(set(labs[0]).intersection(*[set(l) for l in labs[1:]]))
    if not keys:
        sys.exit("no decision instances shared by all builds")

    groups = meet(labs, keys)

    # A cluster of build 1 is DISPUTED when the meet breaks it up: the other
    # builds separated instances it held together.
    by_first = defaultdict(set)
    for gk, members in groups.items():
        by_first[gk[0]].add(gk)
    disputed = {c: gs for c, gs in by_first.items() if len(gs) > 1}

    sizes = Counter(len(v) for v in groups.values())
    n_first = len(set(labs[0][k] for k in keys))

    print(f"ARBITRATION -- {x.level} level, {len(x.vocab)} builds, "
          f"{len(keys)} instances\n")
    for i, p in enumerate(x.vocab, 1):
        n = len(set(labs[i - 1][k] for k in keys))
        print(f"  build {i}  {n:>5} clusters   {Path(p).name}")
    print(f"\n  arbitrated (meet)      {len(groups):>5} clusters")
    print(f"  clusters of build 1 broken up  {len(disputed)} of {n_first}"
          f"  ({len(disputed)/n_first:.1%})")
    print(f"  singletons created     {sizes[1]}")
    print(f"\n  -> a merge any build rejected is undone. The result is finer")
    print(f"     than every input, by design: a split is recoverable, the")
    print(f"     over-merge it replaces was not.")

    if x.out:
        d = json.loads(Path(x.vocab[0]).read_text(encoding="utf-8"))
        dec = d["decisions"]
        # Rebuild the instance key -> index map the same way partition.py
        # derives its keys, so membership survives the rewrite intact.
        idx = {}
        for i, rec in enumerate(dec):
            idx[(rec["run"], rec.get("line", -1),
                 (rec.get("text") or "")[:60])] = i

        # One option record per arbitrated group, inheriting the first build's
        # labels for the group's largest original cluster.
        old = {o_i: o for o_i, o in enumerate(d["options"])}
        owner = {}
        for o_i, o in old.items():
            for m in o.get("members", ()):
                owner[m] = o_i

        out_opts = []
        for gk, members in sorted(groups.items(), key=lambda t: -len(t[1])):
            mi = sorted(idx[k] for k in members if k in idx)
            if not mi:
                continue
            src = Counter(owner.get(m) for m in mi).most_common(1)[0][0]
            base = dict(old[src]) if src is not None else {}
            base["members"] = mi
            base["n"] = len(mi)
            base["runs"] = sorted({dec[m]["run"] for m in mi})
            base["arbitrated_from"] = list(gk)
            out_opts.append(base)

        d["options"] = out_opts
        d["arbitration"] = {
            "builds": [str(p) for p in x.vocab], "level": x.level,
            "rule": "meet of partitions; a merge any build rejected is undone",
            "clusters_before": n_first, "clusters_after": len(groups),
            "disputed_clusters": len(disputed),
        }
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parents[2]
                                   / "scripts"))
            from vocab import sync_counts
            sync_counts(d)
        except Exception:                                       # noqa: BLE001
            d["n_options"] = len(out_opts)
            d["n_forks"] = len({o["fork"] for o in out_opts if "fork" in o})
        Path(x.out).parent.mkdir(parents=True, exist_ok=True)
        Path(x.out).write_text(json.dumps(d, ensure_ascii=False, indent=1),
                               encoding="utf-8")
        print(f"\n  wrote {x.out}")

    if x.queue:
        rows = []
        for c, gs in disputed.items():
            parts = sorted((groups[g] for g in gs), key=len, reverse=True)
            rows.append({
                "cluster": str(c)[:160],
                "n_instances": sum(len(p) for p in parts),
                "split_into": len(parts),
                "part_sizes": "|".join(str(len(p)) for p in parts),
                "largest_share": round(len(parts[0])
                                       / sum(len(p) for p in parts), 3),
                "reviewer_verdict": "", "reviewer_note": "",
            })
        # Worst-first: the most evenly split are the least resolvable by any
        # rule and the most worth a human's attention.
        rows.sort(key=lambda r: (r["largest_share"], -r["n_instances"]))
        Path(x.queue).parent.mkdir(parents=True, exist_ok=True)
        with open(x.queue, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"  wrote {x.queue}  ({len(rows)} disputed clusters, "
              f"worst-first)")


if __name__ == "__main__":
    main()
