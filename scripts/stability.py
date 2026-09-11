#!/usr/bin/env python3
"""Stability and novelty over the clustered decision corpus. No model calls.

An option's frequency -- how many runs chose it -- is the quantity this whole
pipeline exists to produce. Two things are read off it:

  STABILITY  at a fork, how concentrated are the runs? A fork where 95% of runs
             take one option is not a fork in practice, whatever the option
             count says. A fork split 40/35/25 is a live researcher degree of
             freedom.
  NOVELTY    an option chosen by exactly one run. The rare tail is the point of
             a multiverse study, and the reason the clustering was built with no
             cap on option count.

The population-genetics framing the study owner proposed is apt and is used here
directly: the option frequency spectrum is a site frequency spectrum, singletons
are the rare-variant tail, and options confined to one persona arm are private
alleles. The analogy also brings its own correction -- ascertainment bias --
which is why nothing below is reported without rarefaction.

THE THREE THINGS THAT WOULD OTHERWISE GO WRONG
----------------------------------------------

1. Runs, not decisions. A run that dichotomizes twice in one script must not
   count twice toward an option's frequency. Every count here is over distinct
   run ids.

2. Rarefaction, always. Novel-option count grows with sample size, so the arm
   with 51 runs will show more novelty than the arm with 31 for arithmetic
   reasons alone. Every richness figure is reported at a common subsample size,
   computed exactly by the hypergeometric complement rather than simulated.

3. Coverage before comparison. 227 of 359 forks are reached by fewer than 5
   runs. Concentration on 3 runs is not a measurement. Forks below MIN_RUNS are
   excluded from every stability statistic and reported separately as coverage.

Usage:
    python3 scripts/stability.py --corpus ai
    python3 scripts/stability.py --corpus ai --json out.json
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402
import vocab                                                   # noqa: E402
from vocab import split_by_provenance                          # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS

MIN_RUNS = 10        # a fork needs this many runs before concentration means anything
STABLE_SHARE = 0.10  # an option is "stable" at >= this share of the fork's runs
STABLE_FLOOR = 3     # ...and at least this many runs, so 1-of-4 is not "stable"


def rarefy(counts, n, k):
    """Expected distinct options in a random subsample of k of n runs.

    Exact, via the hypergeometric complement: an option is absent from the
    subsample with probability C(n-c, k)/C(n, k).
    """
    if k <= 0 or n <= 0:
        return 0.0
    if k >= n:
        return float(len(counts))
    d = comb(n, k)
    return sum(1.0 - (comb(n - c, k) / d if n - c >= k else 0.0) for c in counts)


def load(tag):
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        cand = sorted(P.VOCAB.glob("bottom_up_*.json"))
        if not cand:
            sys.exit("no bottom_up_*.json; run cluster_up.py build first")
        p = cand[-1]
    return json.loads(p.read_text(encoding="utf-8")), p


def build_tables(d):
    """fork -> {option -> set(runs)}, and run -> arm."""
    dec = d["decisions"]
    arm_of = {}
    forks = defaultdict(lambda: defaultdict(set))
    for o in d["options"]:
        for i in o.get("members", []):
            if i >= len(dec):
                continue
            r = dec[i]["run"]
            arm_of[r] = dec[i]["arm"]
            forks[o["fork"]][o["option"]].add(r)
    return forks, arm_of


def fork_stats(forks, vstats=None):
    """Per-fork concentration. `vstats` is vocab.fork_stats for this tag.

    Effective options comes from there rather than from these run sets: summing
    set sizes per option counts an analysis once per option it holds, and 86%
    of analyses hold two at some fork. Without `vstats` the old figure is kept
    so a caller that has no vocabulary still runs, but it is the inflated one.
    """
    rows = []
    for fk, opts in forks.items():
        runs = set().union(*opts.values()) if opts else set()
        n = len(runs)
        counts = sorted((len(v) for v in opts.values()), reverse=True)
        tot = sum(counts)
        if not tot:
            continue
        shares = [c / tot for c in counts]
        hhi = sum(s * s for s in shares)
        vs = (vstats or {}).get(fk, {})
        rows.append({
            "fork": fk, "runs": n, "options": len(opts),
            "modal_share": round(counts[0] / n, 3) if n else 0,
            # effective number of options: 1/HHI. Reads as "how many options
            # this fork behaves like", so a 95/5 split reads ~1.1 not 2.
            "effective_options": vs.get("eff_reached",
                                        round(1 / hhi, 2) if hhi else 0),
            "eff_all": vs.get("eff_all"),
            "stable_options": sum(
                1 for c in counts if c >= max(STABLE_FLOOR, STABLE_SHARE * n)),
            "novel_options": sum(1 for c in counts if c == 1),
            "novel_share": round(sum(1 for c in counts if c == 1) / len(counts), 3),
            "counts": counts,
        })
    return rows


def spectrum(forks):
    """The option frequency spectrum: how many options were chosen by k runs."""
    spec = Counter()
    for opts in forks.values():
        for v in opts.values():
            spec[len(v)] += 1
    return spec


def _summarise(forks, well, keep=None):
    """Mean concentration over measurable forks, optionally on a subset of runs."""
    mods, effs, n = [], [], 0
    for fk in well:
        counts = [len(rs if keep is None else [r for r in rs if r in keep])
                  for rs in forks[fk].values()]
        tot = sum(counts)
        if tot < MIN_RUNS:
            continue
        n += 1
        mods.append(max(counts) / tot)
        effs.append(1.0 / sum((c / tot) ** 2 for c in counts))
    return {"mean_modal_share": sum(mods) / len(mods) if mods else 0.0,
            "mean_effective": sum(effs) / len(effs) if effs else 0.0,
            "n_measurable": float(n)}


def provenance_delta(forks, well):
    """The same statistics with and without assembled runs.

    Every run counts -- an itinerary run is a human's choice, executed. What
    this reports is whether including them moves the headline, because a
    number that drifts silently as paths are walked is the real hazard.
    """
    runs = {r for f in well for rs in forks[f].values() for r in rs}
    corpus, other = split_by_provenance(runs)
    allr = _summarise(forks, well)
    con = _summarise(forks, well, keep=corpus) if other else allr
    return {"corpus_runs": len(corpus), "other_runs": len(other),
            "all": allr, "corpus": con,
            "delta": {k: round(allr[k] - con[k], 4) for k in allr}}


def by_arm(forks, arm_of, well):
    """Per-arm richness, rarefied to the smallest arm so the counts compare."""
    arms = sorted(set(arm_of.values()))
    runs_per_arm = Counter(arm_of.values())
    k = min(runs_per_arm.values())
    rows = []
    for a in arms:
        # counts of runs-per-option, restricted to this arm and to well-covered forks
        counts = []
        private = 0
        for fk in well:
            for opt, rs in forks[fk].items():
                mine = sum(1 for r in rs if arm_of.get(r) == a)
                if mine:
                    counts.append(mine)
                    if all(arm_of.get(r) == a for r in rs):
                        private += 1
        n = runs_per_arm[a]
        rows.append({
            "arm": a, "runs": n,
            "options_touched": len(counts),
            "rarefied_to_min": round(rarefy(counts, n, k), 1),
            "singletons": sum(1 for c in counts if c == 1),
            "private_options": private,
            "private_per_run": round(private / n, 2),
        })
    return rows, k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--json")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    d, path = load(tag)
    forks, arm_of = build_tables(d)
    rows = fork_stats(forks, vocab.fork_stats(d))
    well = [r["fork"] for r in rows if r["runs"] >= MIN_RUNS]

    print(f"STABILITY AND NOVELTY — {path.name}")
    print(f"{d['n_decisions']} decisions, {len(d['options'])} options, "
          f"{len(forks)} forks, {len(arm_of)} runs\n")

    print(f"COVERAGE GATE  (a fork needs >= {MIN_RUNS} runs to be measurable)")
    print(f"  measurable forks    {len(well)} of {len(rows)}")
    print(f"  excluded            {len(rows)-len(well)} "
          f"(reported as coverage, never as disagreement)")
    print(f"  decisions covered   "
          f"{sum(sum(r['counts']) for r in rows if r['runs'] >= MIN_RUNS)}"
          f" of {sum(sum(r['counts']) for r in rows)}\n")

    print("OPTION FREQUENCY SPECTRUM  (options chosen by exactly k runs)")
    spec = spectrum({f: forks[f] for f in well})
    tot = sum(spec.values())
    for k in sorted(spec)[:10]:
        bar = "#" * max(1, round(46 * spec[k] / max(spec.values())))
        print(f"  {k:>3} run(s)  {spec[k]:>4}  {spec[k]/tot:>5.1%}  {bar}")
    hi = sum(v for k, v in spec.items() if k > 10)
    if hi:
        print(f"  >10 runs   {hi:>4}  {hi/tot:>5.1%}")
    print(f"  singleton (novel) share of options: "
          f"{spec.get(1,0)/tot:.0%}\n")

    print(f"MOST CONTESTED FORKS  (measurable, lowest modal share = most divided)")
    print(f"  {'fork':<56}{'runs':>5}{'opts':>5}{'modal':>7}{'eff':>6}{'novel':>6}")
    for r in sorted([r for r in rows if r["runs"] >= MIN_RUNS],
                    key=lambda r: r["modal_share"])[:12]:
        print(f"  {r['fork'][:56]:<56}{r['runs']:>5}{r['options']:>5}"
              f"{r['modal_share']:>7.2f}{r['effective_options']:>6.1f}"
              f"{r['novel_options']:>6}")

    print(f"\nMOST SETTLED FORKS  (highest modal share = everyone did the same)")
    for r in sorted([r for r in rows if r["runs"] >= MIN_RUNS],
                    key=lambda r: -r["modal_share"])[:8]:
        print(f"  {r['fork'][:56]:<56}{r['runs']:>5}{r['options']:>5}"
              f"{r['modal_share']:>7.2f}{r['effective_options']:>6.1f}"
              f"{r['novel_options']:>6}")

    prov = provenance_delta(forks, well)
    if prov["other_runs"]:
        d = prov["delta"]
        print(f"\nPROVENANCE  ({prov['corpus_runs']} corpus, "
              f"{prov['other_runs']} assembled)")
        print(f"  {'':<30}{'all runs':>10}{'corpus only':>14}{'delta':>9}")
        for k2, lab in (("mean_modal_share", "mean modal share"),
                        ("mean_effective", "mean effective options"),
                        ("n_measurable", "measurable forks")):
            print(f"  {lab:<30}{prov['all'][k2]:>10.3f}"
                  f"{prov['corpus'][k2]:>14.3f}{d[k2]:>+9.3f}")
        print("  Assembled runs are counted. This says whether they move the")
        print("  headline -- drift must be visible, not prevented.")

    arows, k = by_arm(forks, arm_of, well)
    print(f"\nBY PERSONA ARM  (measurable forks only; rarefied to {k} runs)")
    print(f"  {'arm':<30}{'runs':>5}{'opts':>6}{'rarefied':>10}"
          f"{'singl':>7}{'private':>9}{'priv/run':>10}")
    for r in arows:
        print(f"  {r['arm']:<30}{r['runs']:>5}{r['options_touched']:>6}"
              f"{r['rarefied_to_min']:>10.1f}{r['singletons']:>7}"
              f"{r['private_options']:>9}{r['private_per_run']:>10.2f}")
    print("\n  private = option chosen by runs of this arm and no other arm")
    print("  rarefied = expected distinct options at a common subsample size;")
    print("             raw counts favour whichever arm has more runs")

    # Saving is the default. It used to need --json, so a direct run
    # printed the analysis and wrote nothing -- and the next reader
    # silently got an older tag's numbers.
    out = Path(a.json) if a.json else (
        P.ANALYSIS / f"stability_{tag}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "source": path.name, "min_runs": MIN_RUNS,
        "stable_share": STABLE_SHARE, "stable_floor": STABLE_FLOOR,
        "rarefied_to": k, "forks": rows, "by_arm": arows,
        "by_provenance": prov,
        "spectrum": {str(k): v for k, v in sorted(spec.items())},
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
