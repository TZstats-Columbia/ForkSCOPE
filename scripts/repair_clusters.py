#!/usr/bin/env python3
"""Split over-merged options along the discriminant that proves the merge wrong.

The audit finds options whose members disagree on a number in a comparison slot
-- one option holding `dichotomize at 0.25`, `at 0.5` and `at 0.75`. That is an
over-merge, and it is the failure mode that matters: it is invisible downstream
and it inflates apparent agreement between runs, which is precisely the quantity
a multiverse study is trying to measure.

The repair is deterministic and needs no model. The audit already knows *why*
each option is wrong -- the members carry different threshold values -- so the
split is just a regroup by that value. Asking a model to re-decide would
reintroduce the judgement that caused the error.

What it does NOT do: merge anything. Under-merge (the 4.6% near-duplicate rate)
is left alone, because a wrongly split option stays visible and countable while
a wrongly merged one does not. When the two errors cannot both be fixed, the
audit's asymmetry says to prefer splitting.

Members that carry no threshold at all stay with the option's modal value
rather than becoming their own group: they are not evidence of a distinct
choice, only of a description that omitted the number.

Usage:
    python3 scripts/repair_clusters.py --corpus ai
    python3 scripts/repair_clusters.py --corpus ai --dry-run
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402
import audit_clusters as A                                     # noqa: E402

OUT = A.OUT


def _fallback_corpus():
    """Defensive only: records written by the current distill.py carry
    `corpus`. Named from the study rather than from one study's data."""
    cs = P.corpora()
    return cs[0] if cs else "corpus"


def fmt(v):
    return f"{v:g}"


def repair(tag, dry=False):
    src = P.VOCAB / f"bottom_up_{tag}.json"
    if not src.exists():
        sys.exit(f"no {src.name}; run cluster_up.py build first")
    d = json.loads(src.read_text(encoding="utf-8"))
    dec = d["decisions"]

    new_opts, split_log = [], []
    for o in d["options"]:
        mem = o.get("members", [])
        if len(mem) < 2:
            new_opts.append(o)
            continue
        # Group by the FULL value set, not by any single value. An extreme-
        # groups rule is one choice described sometimes as "<=0.25", sometimes
        # as ">=0.75", sometimes as both; splitting on the raw value would make
        # three options out of one. Two members conflict only when neither
        # value set contains the other -- {2} vs {3} conflict, {0.25} vs
        # {0.25, 0.75} do not, because the first is a partial description of
        # the second.
        groups = defaultdict(list)
        for i in mem:
            if i >= len(dec):
                continue
            vals = frozenset(A.slot_nums(dec[i]["text"]))
            groups[vals].append(i)
        real = {k: v for k, v in groups.items() if k}
        if len(real) < 2:
            new_opts.append(o)
            continue

        # absorb every value set that is a subset of a larger one
        keys = sorted(real, key=lambda k: (-len(k), sorted(k)))
        merged_keys = {}
        for k in keys:
            host = next((h for h in merged_keys if k < h), None)
            merged_keys.setdefault(host or k, []).extend(real[k])
        real = {"|".join(fmt(v) for v in sorted(k)): ids
                for k, ids in merged_keys.items()}
        if len(real) < 2:
            new_opts.append(o)
            continue

        # members with no threshold join the largest thresholded group: an
        # omitted number is a vaguer description, not a different choice
        modal = max(real, key=lambda k: len(real[k]))
        if frozenset() in groups:
            real[modal] = real[modal] + groups[frozenset()]

        for val, ids in sorted(real.items()):
            runs = sorted({dec[i]["run"] for i in ids})
            new_opts.append({
                "option": f"{o['option']} [{val}]",
                "fork": o["fork"], "question": o["question"],
                "n": len(ids), "runs": runs,
                "arms": dict(Counter(dec[i]["arm"] for i in ids)),
                "corpora": dict(Counter(dec[i].get("corpus", _fallback_corpus())
                                        for i in ids)),
                "members": ids,
                "split_from": o["option"], "split_on": val,
            })
        split_log.append({"option": o["option"], "n": o["n"],
                          "into": {k: len(v) for k, v in sorted(real.items())}})

    print(f"{len(d['options'])} options -> {len(new_opts)} after splitting "
          f"{len(split_log)} over-merged")
    for s in split_log[:12]:
        print(f"  {s['option'][:62]!r}")
        print(f"     n={s['n']} -> " +
              ", ".join(f"{k}:{v}" for k, v in s['into'].items()))
    if dry:
        print("\n(dry run; nothing written)")
        return

    d["options"] = new_opts
    d["n_options"] = len(new_opts)
    d["repair"] = {"split_over_merged": len(split_log), "detail": split_log}
    src.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {src}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    repair("+".join(c.strip() for c in a.corpus.split(",")), a.dry_run)
