#!/usr/bin/env python3
"""What novel options are, who uses them, and whether they move the answer.

A novel option is one chosen by exactly one run at a fork enough runs reached
for that to mean something. Three questions:

  WHAT   which forks do novel options concentrate in, and are they cosmetic
         variation or substantive divergence?
  WHO    does any persona arm reach for them more often, once you correct for
         the arm having more runs and longer scripts?
  SO WHAT does a run that takes unusual paths end up reporting a different
         answer?

The third is the one worth caring about and the one most easily overclaimed, so
the design is deliberately conservative:

  * The outcome side is `data/outcomes/outcomes.json`, an extraction that never
    touched the decision vocabulary. Effect size and verdict were read off each
    run's report independently of anything in this pipeline, so a correlation
    here is not the clustering marking its own homework.
  * Novelty is normalised per decision. A run that records 30 decisions has more
    chances to be unusual than one recording 12; raw novel counts would mostly
    measure script length.
  * The comparison is observational. Runs were not assigned their novelty, and
    a persona brief influences both the choices and the reported verdict, so
    arm is reported alongside rather than controlled away. Everything below is
    an association.
  * Uncertainty is a bootstrap over runs, not a parametric test, because the
    novelty score is a bounded ratio with a lumpy distribution.

Usage:
    python3 scripts/novelty.py --corpus ai [--json out.json]
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from math import log
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
OUTCOMES = P.OUTCOMES

MIN_RUNS = 10        # fork coverage gate, matching stability.py
B = 4000             # bootstrap resamples
SEED = 20260822


def load(tag):
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        cand = sorted(P.VOCAB.glob("bottom_up_*.json"))
        if not cand:
            sys.exit("no bottom_up_*.json; run cluster_up.py build first")
        p = cand[-1]
    return json.loads(p.read_text(encoding="utf-8")), p


def ci(vals, lo=2.5, hi=97.5):
    s = sorted(vals)
    if not s:
        return (0.0, 0.0)
    return (s[int(len(s) * lo / 100)], s[min(len(s) - 1, int(len(s) * hi / 100))])


def boot_mean_diff(a, b, rng):
    """Bootstrap CI for mean(a) - mean(b), resampling each group."""
    if not a or not b:
        return None
    d = []
    for _ in range(B):
        x = sum(rng.choice(a) for _ in a) / len(a)
        y = sum(rng.choice(b) for _ in b) / len(b)
        d.append(x - y)
    return (sum(d) / len(d),) + ci(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--json")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    d, path = load(tag)
    dec = d["decisions"]
    rng = random.Random(SEED)

    # ---- fork -> option -> runs, gated on coverage --------------------------
    forks = defaultdict(lambda: defaultdict(set))
    arm_of, opt_meta = {}, {}
    for o in d["options"]:
        for i in o.get("members", []):
            if i >= len(dec):
                continue
            r = dec[i]["run"]
            arm_of[r] = dec[i]["arm"]
            forks[o["fork"]][o["option"]].add(r)
            opt_meta[(o["fork"], o["option"])] = o
    well = {f for f, os_ in forks.items()
            if len(set().union(*os_.values())) >= MIN_RUNS}

    novel = {}            # (fork, option) -> the single run that chose it
    for f in well:
        for opt, rs in forks[f].items():
            if len(rs) == 1:
                novel[(f, opt)] = next(iter(rs))

    # ---- per-run novelty, normalised ---------------------------------------
    dec_per_run = Counter(x["run"] for x in dec)
    nov_per_run = Counter(novel.values())
    runs = sorted(dec_per_run)
    score = {r: nov_per_run.get(r, 0) / dec_per_run[r] for r in runs}

    print(f"NOVELTY — {path.name}")
    print(f"{len(novel)} novel options over {len(well)} measurable forks "
          f"(>= {MIN_RUNS} runs), {len(runs)} runs\n")

    # ---- WHAT: where novelty concentrates -----------------------------------
    byfork = Counter(f for f, _ in novel)
    tot_opt = {f: len(forks[f]) for f in well}
    print("WHERE NOVELTY CONCENTRATES  (measurable forks, most novel options)")
    print(f"  {'fork':<58}{'novel':>6}{'opts':>6}{'share':>7}")
    for f, n in byfork.most_common(12):
        print(f"  {f[:58]:<58}{n:>6}{tot_opt[f]:>6}{n/tot_opt[f]:>7.0%}")

    # ---- WHO: per-arm novelty rate -----------------------------------------
    print(f"\nWHO USES THEM  (novel options per decision recorded, "
          f"bootstrap 95% CI)")
    per_arm = defaultdict(list)
    for r in runs:
        per_arm[arm_of.get(r, "?")].append(score[r])
    print(f"  {'arm':<30}{'runs':>5}{'novel/decision':>16}{'95% CI':>20}")
    arm_rows = []
    for arm in sorted(per_arm):
        v = per_arm[arm]
        bs = [sum(rng.choice(v) for _ in v) / len(v) for _ in range(B)]
        lo, hi = ci(bs)
        m = sum(v) / len(v)
        arm_rows.append({"arm": arm, "runs": len(v), "mean": round(m, 4),
                         "ci": [round(lo, 4), round(hi, 4)]})
        print(f"  {arm:<30}{len(v):>5}{m:>16.3f}{f'[{lo:.3f}, {hi:.3f}]':>20}")

    # ---- SO WHAT: does novelty move the outcome? ---------------------------
    # A study may have no outcome side. study.json says so in as many words --
    # "omit this block entirely if the study has no outcome side" -- and
    # soccer-C has none by owner decision D3: the extractor must be written
    # and has not been. iteration.py already guards this exact read; these
    # three did not, so a deliberate absence crashed the build after the
    # repair chain and the whole analysis had run. The fork-side result is
    # independent of outcomes and should not be lost with the outcome-side
    # one.
    #
    # Skipping loudly, not silently: the owner parked K2 behind the
    # extractor, so "not computed, no outcomes" is the honest report and an
    # empty section that looks computed is not.
    if not OUTCOMES.exists():
        print()
        print(f"DOES IT MOVE THE ANSWER?  NOT COMPUTED -- no outcomes at "
              f"{OUTCOMES}. Owner decision D3: the extractor is unwritten.")
        return
    outc = {o["repo_id"]: o for o in
            json.loads(OUTCOMES.read_text(encoding="utf-8"))}
    have = [r for r in runs if r in outc]
    print(f"\nDOES IT MOVE THE ANSWER?  ({len(have)} runs with an "
          f"independently extracted outcome)")

    # split at the median novelty score
    med = sorted(score[r] for r in have)[len(have) // 2]
    hi_r = [r for r in have if score[r] > med]
    lo_r = [r for r in have if score[r] <= med]

    def eff(r):
        v = outc[r].get("or_scale_estimate")
        return log(v) if v and v > 0 else None

    def sup(r):
        return 1.0 if outc[r].get("conclusion") == "supported" else 0.0

    for name, fn, unit in (("log odds-ratio", eff, "log OR"),
                           ("verdict = supported", sup, "share")):
        A = [fn(r) for r in hi_r if fn(r) is not None]
        Bv = [fn(r) for r in lo_r if fn(r) is not None]
        if not A or not Bv:
            continue
        res = boot_mean_diff(A, Bv, rng)
        ma, mb = sum(A) / len(A), sum(Bv) / len(Bv)
        crosses = res[1] <= 0 <= res[2]
        print(f"\n  {name} ({unit})")
        print(f"    high-novelty runs (n={len(A)})  mean {ma:>7.3f}")
        print(f"    low-novelty  runs (n={len(Bv)})  mean {mb:>7.3f}")
        print(f"    difference {res[0]:>+7.3f}   95% CI "
              f"[{res[1]:+.3f}, {res[2]:+.3f}]   "
              f"{'no detectable difference' if crosses else 'DIFFERENCE'}")

    # ---- does a novel option coincide with an unusual outcome? -------------
    print(f"\n  Per-option check: for each novel option, how far is its run's "
          f"effect\n  from the corpus median? (|log OR - median| in MADs)")
    effs = [eff(r) for r in have if eff(r) is not None]
    m = sorted(effs)[len(effs) // 2]
    mad = sorted(abs(e - m) for e in effs)[len(effs) // 2] or 1e-9
    dev = []
    for (f, opt), r in novel.items():
        e = eff(r) if r in outc else None
        if e is not None:
            dev.append((abs(e - m) / mad, f, opt, r))
    base = sum(abs(e - m) / mad for e in effs) / len(effs)
    novmean = sum(x[0] for x in dev) / len(dev) if dev else 0
    print(f"    all runs        mean deviation {base:.2f} MAD")
    print(f"    novel-option runs             {novmean:.2f} MAD  "
          f"(n={len(dev)} option-run pairs)")
    print("\n  most deviant runs that took a novel option:")
    for z, f, opt, r in sorted(dev, reverse=True)[:6]:
        print(f"    {z:>5.1f} MAD  [{arm_of.get(r,'?')[:20]:<20}] {opt[:56]}")

    # Saving is the default. It used to need --json, so a direct run
    # printed the analysis and wrote nothing -- and the next reader
    # silently got an older tag's numbers.
    out = Path(a.json) if a.json else (
        P.ANALYSIS / f"novelty_{tag}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "source": path.name, "min_runs": MIN_RUNS,
        "n_novel": len(novel), "by_fork": byfork.most_common(),
        "by_arm": arm_rows,
        "run_scores": {r: round(score[r], 4) for r in runs},
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
