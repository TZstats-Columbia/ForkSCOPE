#!/usr/bin/env python3
"""Decompose fork disagreement into induction noise and inherited noise.

THE QUESTION A AND B COULD NOT ANSWER
-------------------------------------
Builds A and B agree well about options (ARI 0.85) and badly about forks
(by-option ARI 0.31). Two readings fit that equally:

    fork induction is unstable in itself -- it would disagree with itself even
    on byte-identical options
    fork induction inherits -- it is near-deterministic, and the disagreement
    is an options layer that already differed, amplified

A and B cannot separate these, because their options differ. Replicates that
FREEZE the options and re-run only fork formation can.

WHY THE WITHIN-PARENT COMPARISON IS EXACT
-----------------------------------------
Every replicate of one parent starts from the SAME options file, and the fork
chain never adds, removes or renumbers an option. So two replicates of one
parent are two labellings of one fixed set, and their agreement is a partition
comparison with no matching step at all -- no Jaccard threshold, no greedy
assignment, none of the machinery that makes the A-vs-B fork number arguable.
Whatever this measures, it is not an artifact of how options were paired.

The BETWEEN-parent comparison does need matching, and inherits every caveat
that applies to the original A-vs-B number. The two are reported separately and
must not be averaged together.

READING THE DECOMPOSITION
-------------------------
    within-parent HIGH, between LOW    induction is stable; the A/B fork
                                       disagreement is inherited from options
    within-parent LOW                  induction is unstable in itself, and no
                                       improvement upstream will fix forks
    within A != within B               the parents differ in how hard they are
                                       to fork, which is itself a finding

`sd` is reported with its degrees of freedom because that is the whole reason
this batch was sized as it was: at k replicates a parent contributes k-1 df,
and an sd on 2 df is compatible with almost anything.

WHAT THIS DOES NOT MEASURE
--------------------------
The replicates drop `merge_options` from the repair loop, so they are a
MODIFIED pipeline. This is fork-formation variance under frozen options, not
end-to-end pipeline variance. The parents' own fork layers were built by the
full loop and are therefore NOT exchangeable with the replicates -- they are
shown for reference and excluded from the variance statistics.

Usage:
    python3 stability/scripts/fork_variance.py --root replicates
        [--json out] [--csv out]
"""
import argparse
import csv
import itertools
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
from layer_agreement import load as load_opts, match_options       # noqa: E402


def final_vocab(root):
    """The vocabulary a fork replicate finished with, per its own manifest."""
    m = root / "manifest.json"
    if not m.exists():
        return None
    d = json.loads(m.read_text(encoding="utf-8"))
    tag = d.get("final_tag")
    if not tag:
        return None
    p = root / "data" / "vocabulary" / f"bottom_up_{tag}.json"
    return p if p.exists() else None


def fork_by_option(path):
    """option label -> fork, and the raw per-index fork list.

    Indexed comparison is only valid when both sides came from one options
    file, which is guaranteed within a parent and false across parents.
    """
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return ([o["fork"] for o in d["options"]],
            [o["option"] for o in d["options"]],
            len({o["fork"] for o in d["options"]}))


def pair_scores(fa, fb):
    return (round(float(adjusted_rand_score(fa, fb)), 4),
            round(float(adjusted_mutual_info_score(fa, fb)), 4))


def describe(vals, label):
    if len(vals) < 2:
        return {"label": label, "n": len(vals),
                "mean": round(vals[0], 4) if vals else None,
                "sd": None, "df": max(0, len(vals) - 1)}
    return {"label": label, "n": len(vals),
            "mean": round(statistics.mean(vals), 4),
            "sd": round(statistics.stdev(vals), 4),
            "min": round(min(vals), 4), "max": round(max(vals), 4),
            "df": len(vals) - 1}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default="replicates")
    ap.add_argument("--json")
    ap.add_argument("--csv")
    a = ap.parse_args()

    root = Path(a.root)
    reps = defaultdict(list)          # parent -> [(name, path)]
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name in ("parents", "results"):
            continue
        v = final_vocab(d)
        if v:
            reps[d.name[0]].append((d.name, v))

    if not reps:
        sys.exit(f"no completed replicates under {root}")

    print("  COMPLETED REPLICATES")
    counts = {}
    for par in sorted(reps):
        for name, v in reps[par]:
            _, _, nf = fork_by_option(v)
            counts[name] = nf
            print(f"    {name:<6} {nf:>4} decision points   {v.name[-40:]}")
    print()

    res = {"root": str(root), "fork_counts": counts,
           "within": {}, "between": None,
           "note": "replicates freeze options and drop merge_options; this is "
                   "fork-formation variance, not pipeline variance"}
    rows = []

    # ---- within parent: exact, no matching --------------------------------
    print("  WITHIN PARENT  (same options file; indexed comparison, no matching)")
    for par in sorted(reps):
        aris, amis = [], []
        for (n1, p1), (n2, p2) in itertools.combinations(reps[par], 2):
            f1, o1, _ = fork_by_option(p1)
            f2, o2, _ = fork_by_option(p2)
            if o1 != o2:
                sys.exit(f"{n1} and {n2} do not share an options layer; "
                         f"a fork replicate must not alter options")
            ari, ami = pair_scores(f1, f2)
            aris.append(ari)
            amis.append(ami)
            rows.append({"kind": "within", "parent": par, "a": n1, "b": n2,
                         "ari": ari, "ami": ami})
        if aris:
            res["within"][par] = {"ari": describe(aris, f"within {par} ARI"),
                                  "ami": describe(amis, f"within {par} AMI")}
            d = res["within"][par]["ari"]
            print(f"    {par}: {d['n']:>2} pairs  ARI {d['mean']}"
                  f"  sd {d['sd']}  ({d['min']}-{d['max']})  df {d['df']}")

    # ---- between parents: needs matching ----------------------------------
    if len(reps) > 1:
        pa, pb = sorted(reps)[:2]
        aris, amis = [], []
        for n1, p1 in reps[pa]:
            for n2, p2 in reps[pb]:
                m1, _ = load_opts(str(p1))
                m2, _ = load_opts(str(p2))
                pairs = match_options(m1, m2, 0.5)
                if not pairs:
                    continue
                d1 = json.loads(Path(p1).read_text(encoding="utf-8"))
                d2 = json.loads(Path(p2).read_text(encoding="utf-8"))
                fa = [d1["options"][i]["fork"] for i, j, _ in pairs]
                fb = [d2["options"][j]["fork"] for i, j, _ in pairs]
                ari, ami = pair_scores(fa, fb)
                aris.append(ari)
                amis.append(ami)
                rows.append({"kind": "between", "parent": f"{pa}x{pb}",
                             "a": n1, "b": n2, "ari": ari, "ami": ami,
                             "matched": len(pairs)})
        if aris:
            res["between"] = {"ari": describe(aris, "between ARI"),
                              "ami": describe(amis, "between AMI")}
            d = res["between"]["ari"]
            print(f"\n  BETWEEN PARENTS  (options matched at Jaccard 0.5; "
                  f"inherits the A-vs-B caveats)")
            print(f"    {pa} x {pb}: {d['n']:>2} pairs  ARI {d['mean']}"
                  f"  sd {d['sd']}  ({d['min']}-{d['max']})")

    # ---- the decomposition -------------------------------------------------
    if res["between"] and len(res["within"]) == 2:
        w = statistics.mean([res["within"][p]["ari"]["mean"]
                             for p in res["within"]])
        b = res["between"]["ari"]["mean"]
        # Both shortfalls are reported as shares of the SAME total, because the
        # tempting reading -- "the gap is large, so the disagreement is
        # inherited" -- compares the wrong pair of numbers. What matters is how
        # far each stage falls short of perfect agreement, and a large gap is
        # entirely compatible with induction being the bigger contributor.
        own = 1.0 - w                      # induction's own noise
        inherited = w - b                  # what a differing options layer adds
        total = 1.0 - b
        res["decomposition"] = {
            "within_mean_ari": round(w, 4), "between_mean_ari": round(b, 4),
            "shortfall_from_induction": round(own, 4),
            "shortfall_from_options": round(inherited, 4),
            "induction_share": round(own / total, 4) if total else None}
        print(f"\n  DECOMPOSITION  (shortfall from perfect agreement)")
        print(f"    induction's own noise      {own:.3f}   "
              f"(identical options still give ARI {w:.3f})")
        print(f"    differing options add      {inherited:.3f}   "
              f"(ARI falls to {b:.3f})")
        print(f"    total                      {total:.3f}")
        print(f"\n    induction is {own / total:.0%} of the shortfall; "
              f"the options layer is {inherited / total:.0%}")
        if w < 0.75:
            print(f"\n    Fork induction does NOT reproduce itself: given "
                  f"byte-identical options it\n    still disagrees at ARI "
                  f"{w:.3f}. Fixing the options layer alone cannot make\n"
                  f"    forks reproducible.")

    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {a.json}")
    if a.csv and rows:
        Path(a.csv).parent.mkdir(parents=True, exist_ok=True)
        with open(a.csv, "w", newline="", encoding="utf-8") as fh:
            w_ = csv.DictWriter(fh, fieldnames=sorted({k for r in rows
                                                       for k in r}))
            w_.writeheader()
            w_.writerows(rows)
        print(f"  wrote {a.csv}")


if __name__ == "__main__":
    main()
