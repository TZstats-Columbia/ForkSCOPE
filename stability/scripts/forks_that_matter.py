#!/usr/bin/env python3
"""Stability restricted to the forks results are actually reported on.

No model calls.

WHY RESTRICT
------------
Every stability number so far was computed over all 317 decision points. But no
result in this project is reported on all 317: the reported analyses cover
forks that enough runs reach for a proportion to mean anything, and that are
genuinely contested rather than settled. Measuring reproducibility over the
whole vocabulary answers a question nobody asks and is dominated by the rare
tail, where fork assignment is a coin flip on almost no evidence (64% of
options are singletons).

The honest question is: **do the forks we report on come back?**

THE FILTER
----------
    coverage        >= COV   runs reaching the fork / all runs
    effective opts   > EFF   1 / sum(p_i^2) over option shares at the fork

Effective options is the same 1/HHI used throughout: it reads as "how many
options this fork behaves like", so a 95/5 split scores 1.1 and is excluded as
a convention rather than a live degree of freedom.

THREE QUESTIONS, NOT ONE
------------------------
1. **Does the SET reproduce?** If build A says 18 forks matter and build B says
   22, and they are not the same 18, then no downstream result is stable no
   matter how well the matched ones agree. This is the primary question and it
   is asked first.
2. **Do the matched ones agree on membership?** Given a fork both builds
   consider important, do they mean the same thing by it?
3. **Do their statistics agree?** Coverage and effective options are what get
   reported; a fork can have shifting membership and stable statistics, and
   that distinction matters for what may be quoted.

Qualification is computed independently in each build, never by applying A's
list to B -- that would assume the answer to question 1.

Usage:
    python3 stability/scripts/forks_that_matter.py --a A.json --b B.json
        [--coverage 0.25] [--eff 1.5] [--json out.json] [--csv out.csv]
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import vocab                                                   # noqa: E402
import partition as P                                          # noqa: E402


def fork_stats(path):
    """{fork: {runs, n_runs, coverage, eff_options, n_options, members}}."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    keys = [(r["run"], r.get("line", -1), (r.get("text") or "")[:60])
            for r in dec]
    all_runs = {r["run"] for r in dec}

    per = defaultdict(lambda: {"opt_runs": defaultdict(set), "members": set()})
    for o in d["options"]:
        f = o["fork"]
        ms = [m for m in o.get("members", ()) if 0 <= m < len(keys)]
        if not ms:
            continue
        per[f]["members"].update(keys[m] for m in ms)
        per[f]["opt_runs"][o["option"]].update(dec[m]["run"] for m in ms)

    # Effective options from vocab.fork_stats -- the one definition.
    #
    # The code here previously summed run-set sizes per option, under a comment
    # saying shares are over runs and not decision records. That fixed half the
    # problem: an analysis recording the same option twice no longer counted
    # twice, but one holding TWO options at the same fork still voted in both,
    # and 86% of analyses do that somewhere. fork_stats gives each analysis
    # exactly one vote, its modal option there.
    #
    # `eff_options` stays `eff_reached` -- over analyses that reached the fork
    # -- because that is what this script's coverage x eff grid is about. The
    # pivotal definition uses `eff_all`, which is also carried here so a caller
    # can apply it without a second count.
    st = vocab.fork_stats(d, len(all_runs))

    out = {}
    for f, v in per.items():
        s = st.get(f)
        if not s or not s["reach"]:
            continue
        out[f] = {
            "runs": set().union(*v["opt_runs"].values()),
            "n_runs": s["reach"],
            "coverage": s["coverage"],
            "eff_options": s["eff_reached"],
            "eff_all": s["eff_all"],
            "n_options": s["options"],
            "members": v["members"],
        }
    return out, len(all_runs)


def qualify(stats, cov, eff):
    return {f: s for f, s in stats.items()
            if s["coverage"] >= cov and s["eff_options"] > eff}


def match(qa, qb, allb):
    """Match each qualifying A-fork to its best B-fork by CONTAINMENT.

    Matched against ALL of B's forks, not only B's qualifying ones: a fork that
    exists in B but failed the filter is a different event from a fork that is
    not there at all, and collapsing them would hide a real failure mode.

    Containment (|A n B| / |A|), not Jaccard, decides the match. Jaccard
    punishes a MERGE: when B unites two of A's forks into one, each A-fork
    overlaps only part of the larger B-fork and scores ~0.3, even though the
    correspondence is exact and nothing was lost. That happens here -- two
    pairs of A's qualifying forks map onto single B forks -- and reading those
    as failures would report a merge as a disappearance.

    Jaccard is still recorded, because the two together say WHICH event
    occurred: high containment with low Jaccard is a merge, low containment is
    genuine scatter.
    """
    out = {}
    for f, s in qa.items():
        best, bc, bj = None, 0.0, 0.0
        for g, t in allb.items():
            inter = len(s["members"] & t["members"])
            if not inter:
                continue
            c = inter / len(s["members"])
            if c > bc:
                best, bc = g, c
                bj = inter / len(s["members"] | t["members"])
        out[f] = (best, round(bj, 4), best in qb if best else False,
                  round(bc, 4))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--coverage", type=float, default=0.25)
    ap.add_argument("--eff", type=float, default=1.5)
    ap.add_argument("--tau", type=float, default=0.5,
                    help="Jaccard floor for calling two forks the same fork")
    ap.add_argument("--json")
    ap.add_argument("--csv")
    x = ap.parse_args()

    sa, na = fork_stats(x.a)
    sb, nb = fork_stats(x.b)
    qa, qb = qualify(sa, x.coverage, x.eff), qualify(sb, x.coverage, x.eff)
    m = match(qa, qb, sb)

    both = [f for f, (g, j, isq, c) in m.items() if isq and c >= x.tau]
    present_not_q = [f for f, (g, j, isq, c) in m.items()
                     if g and c >= x.tau and not isq]
    weak = [f for f, (g, j, isq, c) in m.items() if c < x.tau]
    merged = [f for f, (g, j, isq, c) in m.items()
              if c >= x.tau and j < 0.5]

    rows = []
    for f in sorted(qa, key=lambda k: -qa[k]["coverage"]):
        g, j, isq, c = m[f]
        t = sb.get(g) if g else None
        rows.append({
            "fork_a": f[:110],
            "cov_a": round(qa[f]["coverage"], 3),
            "eff_a": round(qa[f]["eff_options"], 2),
            "nopt_a": qa[f]["n_options"],
            "jaccard": j, "containment": c,
            "event": ("merged into a larger B fork" if c >= x.tau and j < 0.5
                      else "matched" if c >= x.tau else "scattered"),
            "in_b_qualifying": isq,
            "cov_b": round(t["coverage"], 3) if t else None,
            "eff_b": round(t["eff_options"], 2) if t else None,
            "nopt_b": t["n_options"] if t else None,
            "cov_delta": round(t["coverage"] - qa[f]["coverage"], 3) if t else None,
            "eff_delta": round(t["eff_options"] - qa[f]["eff_options"], 2) if t else None,
        })

    # Membership agreement restricted to the qualifying, matched forks.
    keys, la, lb = [], {}, {}
    for f in both:
        g = m[f][0]
        for k in (qa[f]["members"] & sb[g]["members"]):
            keys.append(k)
            la[k] = f
            lb[k] = g
    keys = sorted(set(keys))
    ari = P.adjusted_rand(la, lb, keys) if len(keys) > 1 else None

    covd = [r["cov_delta"] for r in rows if r["cov_delta"] is not None]
    effd = [r["eff_delta"] for r in rows if r["eff_delta"] is not None]

    def med(v):
        v = sorted(v)
        return round(v[len(v) // 2], 3) if v else None

    res = {
        "build_a": x.a, "build_b": x.b, "comparison_type": "replicate",
        "filter": {"coverage_min": x.coverage, "eff_options_min": x.eff,
                   "match_tau": x.tau},
        "forks_total": {"a": len(sa), "b": len(sb)},
        "forks_qualifying": {"a": len(qa), "b": len(qb)},
        "set_reproducibility": {
            "matched_and_qualifying_in_b": len(both),
            "matched_but_not_qualifying_in_b": len(present_not_q),
            "no_confident_match": len(weak),
            "merged_into_larger_b_fork": len(merged),
            "recall": round(len(both) / len(qa), 4) if qa else None,
            "precision": round(len(both) / len(qb), 4) if qb else None,
        },
        "membership_ari_on_qualifying": round(ari, 4) if ari is not None else None,
        "statistic_drift": {
            "median_coverage_delta": med(covd),
            "median_eff_options_delta": med(effd),
            "max_abs_coverage_delta": round(max((abs(v) for v in covd),
                                                default=0), 3),
            "max_abs_eff_delta": round(max((abs(v) for v in effd),
                                           default=0), 2),
        },
        "forks": rows,
    }

    s = res["set_reproducibility"]
    print(f"FORKS THAT MATTER  (coverage >= {x.coverage:.0%}, "
          f"effective options > {x.eff})\n")
    print(f"  forks in vocabulary        {len(sa)} A / {len(sb)} B")
    print(f"  qualifying                 {len(qa)} A / {len(qb)} B\n")
    print(f"  Q1 does the SET reproduce?")
    print(f"    qualifying in both       {s['matched_and_qualifying_in_b']}")
    print(f"    present in B, not qual.  {s['matched_but_not_qualifying_in_b']}")
    print(f"    of those, B merged 2->1  {s['merged_into_larger_b_fork']}")
    print(f"    scattered (no match)     {s['no_confident_match']}")
    print(f"    recall / precision       {s['recall']} / {s['precision']}\n")
    print(f"  Q2 do the matched agree on membership?")
    print(f"    ARI on qualifying forks  {res['membership_ari_on_qualifying']}\n")
    print(f"  Q3 do their statistics agree?")
    print(f"    median coverage delta    {res['statistic_drift']['median_coverage_delta']}")
    print(f"    median eff-options delta {res['statistic_drift']['median_eff_options_delta']}")
    print(f"    max |coverage delta|     {res['statistic_drift']['max_abs_coverage_delta']}")
    print(f"    max |eff-options delta|  {res['statistic_drift']['max_abs_eff_delta']}")

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
        print(f"  wrote {x.csv}  ({len(rows)} qualifying forks)")


if __name__ == "__main__":
    main()
