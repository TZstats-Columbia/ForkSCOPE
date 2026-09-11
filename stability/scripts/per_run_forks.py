#!/usr/bin/env python3
"""Per run: do its own decisions group the same way in both builds?

No model calls. This is a different question from the corpus-wide partition
metrics, and a more direct one.

WHY PER RUN
-----------
Every measure so far is global: it compares two clusterings of all 3,946
decisions and asks how much the whole vocabulary agrees. That answers "is the
corpus vocabulary reproducible", which is the right question for a headline
number and the wrong one for a reader who wants to know what a *particular
analysis* looks like.

Restricting to one run removes the cross-run matching problem entirely. Run R's
decisions are the SAME instances in both builds. In build A they fall into some
set of forks; in build B into some set. Comparing those two groupings of one
run's own decisions needs no label matching, no threshold and no
correspondence: it is two partitions of one small set.

So this asks, for each run: **would this analysis's decision map look the
same?** That is the unit a reader actually consumes -- a run's path through the
garden -- and it is the unit an itinerary experiment would have to reproduce.

WHAT IS REPORTED, PER RUN
-------------------------
  ari          chance-corrected agreement on that run's own decisions
  n_forks_a/b  how many distinct forks the run touches in each build
  same_count   whether the run touches the same NUMBER of forks
  pairs_kept   of the decision pairs A put in one fork, the share B also did
               (recall on within-run co-membership -- the quantity an
               itinerary depends on)

A run with few decisions has few pairs and a noisy ARI, so the distribution is
reported alongside the mean and runs are bucketed by size.

Usage:
    python3 stability/scripts/per_run_forks.py --a A.json --b B.json
        [--level fork] [--json out.json] [--csv out.csv]
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import partition as P                                          # noqa: E402


def per_run(path, level):
    """{run: {instance_key: cluster}} using the shared instance identity."""
    lab, _ = P.labeling(path, level)
    out = defaultdict(dict)
    for k, c in lab.items():
        out[k[0]][k] = c          # k = (run, line, text-prefix)
    return out


def pair_recall(la, lb, keys):
    """Of the pairs A co-clusters, what share does B also co-cluster?

    This is the itinerary-relevant quantity: if two of a run's decisions were
    one decision point in A, would they still be one in B? Directional on
    purpose -- losing a grouping and inventing one are different errors.
    """
    kept = tot = 0
    n = len(keys)
    for i in range(n):
        for j in range(i + 1, n):
            if la[keys[i]] == la[keys[j]]:
                tot += 1
                if lb[keys[i]] == lb[keys[j]]:
                    kept += 1
    return (kept / tot if tot else None), tot


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--level", choices=["option", "fork"], default="fork")
    ap.add_argument("--json")
    ap.add_argument("--csv")
    x = ap.parse_args()

    ra, rb = per_run(x.a, x.level), per_run(x.b, x.level)
    runs = sorted(set(ra) & set(rb))

    rows = []
    for r in runs:
        keys = sorted(set(ra[r]) & set(rb[r]))
        if len(keys) < 2:
            continue
        la, lb = ra[r], rb[r]
        ari = P.adjusted_rand(la, lb, keys)
        pr, npairs = pair_recall(la, lb, keys)
        fa = len({la[k] for k in keys})
        fb = len({lb[k] for k in keys})
        rows.append({
            "run": r, "decisions": len(keys),
            "forks_a": fa, "forks_b": fb,
            "same_fork_count": fa == fb,
            "fork_count_delta": fb - fa,
            "ari": round(ari, 4) if ari == ari else None,
            "pair_recall": round(pr, 4) if pr is not None else None,
            "co_pairs": npairs,
        })

    def agg(sub):
        a = [r["ari"] for r in sub if r["ari"] is not None]
        p = [r["pair_recall"] for r in sub if r["pair_recall"] is not None]
        a.sort()
        p.sort()
        return {
            "runs": len(sub),
            "mean_ari": round(sum(a) / len(a), 4) if a else None,
            "median_ari": round(a[len(a) // 2], 4) if a else None,
            "mean_pair_recall": round(sum(p) / len(p), 4) if p else None,
            "median_pair_recall": round(p[len(p) // 2], 4) if p else None,
            "same_fork_count": sum(1 for r in sub if r["same_fork_count"]),
        }

    buckets = {
        "all": rows,
        "small (<12 decisions)": [r for r in rows if r["decisions"] < 12],
        "medium (12-19)": [r for r in rows if 12 <= r["decisions"] < 20],
        "large (20+)": [r for r in rows if r["decisions"] >= 20],
    }
    res = {"build_a": x.a, "build_b": x.b, "comparison_type": "replicate",
           "level": x.level, "runs_compared": len(rows),
           "buckets": {k: agg(v) for k, v in buckets.items()},
           "per_run": rows}

    print(f"PER-RUN {x.level.upper()} AGREEMENT  ({len(rows)} runs)\n")
    print(f"  {'bucket':<24}{'runs':>6}{'mean ARI':>10}{'med ARI':>9}"
          f"{'mean pairR':>12}{'med pairR':>11}{'same #':>8}")
    for k, v in ((k, agg(v)) for k, v in buckets.items()):
        print(f"  {k:<24}{v['runs']:>6}{str(v['mean_ari']):>10}"
              f"{str(v['median_ari']):>9}{str(v['mean_pair_recall']):>12}"
              f"{str(v['median_pair_recall']):>11}{v['same_fork_count']:>8}")
    print(f"\n  pair recall = of the decision pairs A grouped into one "
          f"{x.level},\n  the share B also grouped -- the quantity an "
          f"itinerary depends on.")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")
    if x.csv and rows:
        Path(x.csv).parent.mkdir(parents=True, exist_ok=True)
        with open(x.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"  wrote {x.csv}")


if __name__ == "__main__":
    main()
