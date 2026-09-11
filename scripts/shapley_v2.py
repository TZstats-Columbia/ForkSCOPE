#!/usr/bin/env python3
"""Shapley attribution over the v2 garden nodes.

An earlier version played the same game on the v1 vocabulary. This re-runs it
on v2, and differs in two ways that matter.

**Coarsening is algorithmic, not hand-written.** v1 mapped canonical labels onto
3-4 levels per player with bespoke functions (`lvl_skin`, `lvl_cov`, ...) that
encode a reading of what the options mean. That is the fixed-schema move this
project exists to avoid, and it is the step where a result can be authored
rather than measured. Here a level is just an option chosen by at least
MIN_LEVEL runs; everything rarer collapses into `other`. No option is read, only
counted.

**Not reaching a fork is a level, and that decides who plays.** v1 needed
complete rows and dropped runs that missed any player. In v2 that would leave 68
of 204 runs -- and worse, it would throw away the most common thing a run does at
a fork, which is not arrive at it. Not reaching a fork is a choice, the same
silent decision this project treats as a finding everywhere else.

Once `absent` is a level, coverage stops being the right admission test. A fork
where 20 runs dichotomised and 184 never went near it is a perfectly good binary
contrast. What Shapley needs is not coverage but *contrast*: two levels with
enough runs to estimate a contribution. So a fork plays when >= MIN_LEVELS of
its levels have >= MIN_LEVEL runs, counting `absent`, with at least one a named
option so nothing qualifies on "didn't do it" vs "did something miscellaneous".
Replacing the old coverage >= 0.25 gate with this roughly doubles the player set
(17 -> 29 AI, 16 -> 32 pooled).

Method, with two departures from v1:
  surrogate   ridge on one-hot levels, closed form, intercept unpenalised
  shapley     the surrogate is additive, so phi_j(x) = contrib_j(x_j) - mean_j
  payouts     verdict, log(OR), z, CI width
  bootstrap   B over runs, percentile 95% CI
  lambda      CHOSEN BY CROSS-VALIDATION per payout, not fixed at 1. On a
              204x83 design lambda=1 is essentially unregularised; it came from
              v1, where the hand-coarsened design had ~15 columns.

The additivity is an assumption, not a finding: an additive surrogate cannot
represent "dichotomizing only matters if you also cluster". `audit_shapley.py`
reports how much of each payout the surrogate actually explains, which is the
number that says whether these attributions are worth reading.

Usage:
    python3 scripts/shapley_v2.py --corpus ai
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
OUT = P.ANALYSIS
OUTCOMES = P.OUTCOMES

MIN_LEVEL = 10       # runs a level needs: to be its own option, and to count
                     # toward the two-level rule below
MIN_LEVELS = 2       # a fork is a player if this many of its levels clear
                     # MIN_LEVEL. Not reaching a fork is one of those levels.
B = 2000
LAM = 1.0            # v1's fixed value, kept only as the comparability baseline
LAM_GRID = [1, 3, 10, 30, 100, 300, 1000]
# Ridge penalty is now chosen by cross-validation per payout, not fixed. With
# the two-level player rule the design is 204x83, and lambda=1 on that is
# essentially unregularised -- it was inherited from v1, where the hand-coarsened
# design had ~15 columns and 1.0 was reasonable. Selecting on the same folds the
# score is read from is mildly optimistic; the number is reported as the ceiling
# it is, and it does not change the conclusion either way.
Z975 = 1.959964
SEED = 20260822
ABSENT = "(did not reach this fork)"
OTHER = "(other option)"


def pay_ci_width(o):
    """Log-ratio CI width. Defined only for a RATIO estimand.

    The positivity guard is not defensive tidying: a risk-difference interval
    routinely spans zero, `math.log` of a negative bound raises ValueError, and
    this crashed the whole Shapley stage on soccer-C -- after it had already
    computed and printed the results for the earlier payouts. The guard was
    `if not (ci_low and ci_high)`, which catches None and 0.0 and passes -0.04
    straight through.

    Returning None makes the payout skip itself, which is how every other
    inapplicable payout behaves. For difference-scale outcomes use
    `rd_ci_width`.
    """
    lo, hi = o.get("ci_low"), o.get("ci_high")
    if lo is None or hi is None or lo <= 0 or hi <= 0:
        return None
    return math.log(hi) - math.log(lo)


def pay_rd_ci_width(o):
    """CI width on the NATIVE scale: an arithmetic difference, not a log ratio.

    `pay_ci_width` below takes log(hi) - log(lo), which is right for a ratio
    estimand and wrong for a risk difference: an RD can be negative and its
    interval routinely spans zero, where the log is undefined. Using the
    OR-scale width on RD data silently drops every run whose interval crosses
    zero -- which is exactly the population a multiverse study is about.
    """
    lo, hi = o.get("ci_low"), o.get("ci_high")
    if lo is None or hi is None:
        return None
    return hi - lo


PAYOUTS = {
    "verdict": lambda o: 1.0 if o.get("conclusion") == "supported" else 0.0,
    # NATIVE-SCALE PAYOUTS. Every one of soccer-C's 206 extracted estimates is a
    # risk difference in percentage points -- checked across all 206 label
    # strings, with no odds ratio, rate ratio or log-odds coefficient anywhere.
    #
    # Build A converted everything onto an odds-ratio scale through a
    # baseline-rate assumption. The owner endorsed declining that: it inserts a
    # new analyst decision at the most consequential point in the study and
    # narrows the width by fiat at exactly the place it asked to see it. So the
    # estimate is used on the scale it was reported on, and `log_or`/`z` below
    # skip themselves when `or_scale_estimate` is absent.
    "rd": lambda o: o.get("primary_estimate"),
    "rd_ci_width": pay_rd_ci_width,
    "log_or": lambda o: (math.log(o["or_scale_estimate"])
                         if o.get("or_scale_estimate") else None),
    "z": lambda o: (math.log(o["or_scale_estimate"]) / (pay_ci_width(o) / (2 * Z975))
                    if o.get("or_scale_estimate") and pay_ci_width(o) else None),
    "ci_width": pay_ci_width,
}


def pivotal_set(tag, min_eff_all=1.5):
    """The forks the study reports on, from the ONE definition in vocab.

    `eff_all` counts "did not reach" as a level, so a single threshold carries
    both engagement and disagreement -- which is why there is no coverage
    argument here any more.
    """
    import vocab
    d = json.loads((P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    st = vocab.fork_stats(d)
    return {f for f, s in st.items() if vocab.is_pivotal(s, min_eff_all)}


NOVELTY = "how novel is this analysis (share of its decisions that are options nobody else took)?"


def add_novelty(tag, rows, players, levels, runs):
    """Add novelty as a player, binned, using novelty.py's own score.

    NOT a raw count. `novelty.py` normalises deliberately: an analysis
    recording 40 decisions has more chances to be unusual than one recording
    12, so a raw novel count would mostly measure verbosity and the attribution
    would read "writing more moves the answer". The stored `run_scores` are the
    share of an analysis's decisions that are options no other analysis took,
    at forks at least 10 analyses reached.

    Binned into levels rather than entered continuously, because the surrogate
    is one-hot throughout and a single continuous column would be the only
    place in the design where the effect is forced to be linear.
    """
    p = OUT / f"novelty_{tag}.json"
    if not p.exists():
        print(f"  no novelty file for {tag}; skipping the novelty player")
        return False
    sc = (json.loads(p.read_text(encoding="utf-8")) or {}).get("run_scores", {})
    vals = sorted(v for r, v in sc.items() if r in rows and v > 0)
    if len(vals) < 3 * MIN_LEVEL:
        print("  too few analyses with any novel option; skipping")
        return False
    lo, hi = vals[len(vals) // 3], vals[2 * len(vals) // 3]

    def lvl(v):
        if not v:
            return "no novel options"
        return ("novelty low" if v <= lo else
                "novelty medium" if v <= hi else "novelty high")

    seen = set()
    for r in rows:
        L = lvl(sc.get(r, 0.0))
        rows[r][NOVELTY] = L
        seen.add(L)
    counts = Counter(rows[r][NOVELTY] for r in rows)
    if sum(1 for c in counts.values() if c >= MIN_LEVEL) < MIN_LEVELS:
        print("  novelty has fewer than two estimable levels; skipping")
        for r in rows:
            rows[r].pop(NOVELTY, None)
        return False
    players.append(NOVELTY)
    levels[NOVELTY] = sorted(seen)
    print(f"  novelty player added: "
          + ", ".join(f"{k} {v}" for k, v in counts.most_common()))
    return True


def build_rows(tag, pivotal=None, novelty=False):
    """run -> {player node: level}, using the merged garden nodes."""
    gp = OUT / f"garden_{tag}.json"
    if not gp.exists():
        sys.exit(f"run `garden.py map --corpus {tag}` first")
    gm = json.loads(gp.read_text(encoding="utf-8"))
    d = json.loads((P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    dec = d["decisions"]

    cmap = {}
    for head, members in gm.get("sibling_groups", {}).items():
        for m in members:
            cmap[m] = head
    opts = defaultdict(lambda: defaultdict(set))
    runs = set()
    for o in d["options"]:
        node = cmap.get(o["fork"], o["fork"])
        for i in o.get("members", []):
            if i < len(dec):
                opts[node][o["option"]].add(dec[i]["run"])
                runs.add(dec[i]["run"])
    N = len(runs)

    # Which forks can be players.
    #
    # This used to gate on coverage (>= 25% of runs), which was wrong and
    # threw away most of the corpus. Not reaching a fork is not missing data --
    # it is a choice, the same "silent decision" this project treats as a
    # finding everywhere else, and it is already carried as the ABSENT level.
    # So a fork where 20 runs dichotomised and 184 never went near it is a
    # perfectly good binary contrast, and coverage is irrelevant to whether it
    # can be estimated.
    #
    # What Shapley actually needs is contrast: at least two levels with enough
    # runs to estimate a contribution. Hence the rule -- MIN_LEVELS levels of
    # >= MIN_LEVEL runs each, counting ABSENT as a level. At least one of them
    # must be a named option, so a fork cannot qualify on "didn't do it" versus
    # "did something miscellaneous" alone, which carries no interpretable
    # contrast.
    #
    # On this corpus the rule roughly doubles the player set (17 -> 29 for AI,
    # 16 -> 32 pooled) without inflating the design much, because options with
    # >= 10 runs are rare: most forks contribute one or two named levels plus
    # OTHER and ABSENT.
    rows = {r: {} for r in runs}
    levels, players = {}, []
    for f, om in opts.items():
        named = {o for o, rs in om.items() if len(rs) >= MIN_LEVEL}
        rare = sum(len(rs) for o, rs in om.items() if o not in named)
        absent = N - len(set().union(*om.values())) if om else N
        sizes = ([len(om[o]) for o in named]
                 + ([rare] if rare else []) + ([absent] if absent else []))
        if not named or sum(1 for s in sizes if s >= MIN_LEVEL) < MIN_LEVELS:
            continue
        # `--players pivotal` additionally restricts to the forks the study
        # REPORTS on, for coherence between the attribution and the results.
        # It is off by default because it reintroduces the coverage gate the
        # paragraph above argues against, and the two selections are compared
        # rather than assumed -- see data/analysis/shapley_players_*.json.
        if pivotal is not None and f not in pivotal:
            continue
        players.append(f)
        seen = set()
        for o, rs in om.items():
            lv = o if o in named else OTHER
            for r in rs:
                # a run recording the same fork twice keeps its first level, so
                # every run contributes exactly one observation per player
                if r not in seen:
                    rows[r][f] = lv
                    seen.add(r)
        for r in runs:
            rows[r].setdefault(f, ABSENT)
        levels[f] = sorted({rows[r][f] for r in runs})
    cov = {x["fork"]: x["coverage"] for x in gm["nodes_detail"]}
    players.sort(key=lambda f: -cov.get(f, 0))
    if novelty:
        add_novelty(tag, rows, players, levels, runs)
    return rows, players, levels, sorted(runs), N, opts


def design(rows, ids, players, levels):
    cols, meta = [], []
    for p in players:
        present = [lv for lv in levels[p] if any(rows[i][p] == lv for i in ids)]
        for lv in present[1:]:
            cols.append([1.0 if rows[i][p] == lv else 0.0 for i in ids])
            meta.append((p, lv))
    X = np.column_stack([np.ones(len(ids))] + cols) if cols else np.ones((len(ids), 1))
    return X, meta


def ridge(X, y, lam):
    d = X.shape[1]
    P = np.eye(d) * lam
    P[0, 0] = 0.0
    return np.linalg.solve(X.T @ X + P, X.T @ y)


def cv_r2(rows, ids, players, levels, y, lam, folds=5, seed=SEED):
    """Out-of-sample R2. Printed next to every attribution table because the
    in-sample figure is optimistic by construction -- 67 columns on 204 rows --
    and a decomposition of a surrogate that does not predict is a decomposition
    of noise. See audit_shapley.py H1."""
    # ONE design over all ids, then index rows by fold.
    #
    # Building a separate design per fold is wrong and was silently so.
    # `design()` emits only the levels PRESENT in the ids it is handed, so a
    # train fold and a test fold produce different column sets; truncating both
    # to min(width) and multiplying aligns them by POSITION, not identity. On
    # this study that misaligned 41-48 of ~50 columns in all five folds, so the
    # coefficient for one option was applied to the indicator of another and
    # `r2_cv` measured nothing. It is the number the "does not predict out of
    # sample" claim rests on, which is what made the bug expensive.
    #
    # With fixed columns, a level missing from a train fold simply gets a
    # coefficient shrunk to zero -- its column is all zeros there -- which is
    # the correct behaviour rather than a special case.
    X, _ = design(rows, ids, players, levels)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(ids))
    pred = np.zeros(len(ids))
    for f in range(folds):
        te = idx[f::folds]
        tr = np.array([j for j in idx if j not in set(te.tolist())])
        pred[te] = X[te] @ ridge(X[tr], y[tr], lam)
    return 1 - float(np.sum((y - pred) ** 2) /
                     max(1e-12, np.sum((y - y.mean()) ** 2)))


def phis(beta, meta, rows, ids, players):
    contrib = {p: defaultdict(float) for p in players}
    for (p, lv), b in zip(meta, beta[1:]):
        contrib[p][lv] = b
    out = {}
    for p in players:
        mean_p = float(np.mean([contrib[p][rows[i][p]] for i in ids]))
        out[p] = {lv: contrib[p][lv] - mean_p for lv in set(rows[i][p] for i in ids)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--bootstrap", type=int, default=B)
    ap.add_argument("--players", choices=["contrast", "pivotal"],
                   default="contrast",
                   help="contrast (default): any fork with two estimable "
                        "levels. pivotal: additionally restrict to reported "
                        "forks -- reintroduces the coverage gate")
    ap.add_argument("--pivotal-eff", type=float, default=1.5)
    ap.add_argument("--novelty", action="store_true",
                   help="add novelty as a binned player, from novelty.py's "
                        "normalised run_scores -- not a raw count")
    ap.add_argument("--out-suffix", default="")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))

    pivotal = pivotal_set(tag, a.pivotal_eff) if a.players == "pivotal" else None
    if pivotal is not None:
        print(f"restricting players to {len(pivotal)} pivotal forks "
              f"(eff_all > {a.pivotal_eff})\n")

    rows, players, levels, runs, N, opts = build_rows(tag, pivotal, a.novelty)
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
        print(f"SHAPLEY NOT COMPUTED -- no outcomes at {OUTCOMES}. Shapley "
              f"attributes movement in a reported estimate, so with no "
              f"estimates there is nothing to attribute. Owner decision D3.")
        return
    outcomes = {o["repo_id"]: o for o in
                json.loads(OUTCOMES.read_text(encoding="utf-8"))}
    rng = np.random.default_rng(SEED)

    print(f"SHAPLEY (v2 garden nodes) - corpus {tag}")
    print(f"{len(players)} players of {len(opts)} forks, {N} runs")
    print(f"a fork is a player when >= {MIN_LEVELS} of its levels have "
          f">= {MIN_LEVEL} runs;\nnot reaching the fork counts as a level\n")
    print(f"  {'cov':>5}{'lvls':>6}  player")
    for p in players:
        cov = sum(1 for r in runs if rows[r][p] != ABSENT) / N
        print(f"  {cov:>5.2f}{len(levels[p]):>6}  {p[:62]}")

    results = {}
    for name, fn in PAYOUTS.items():
        keep = [i for i in runs if i in outcomes and fn(outcomes[i]) is not None]
        if len(keep) < 30:
            continue
        y = np.array([fn(outcomes[i]) for i in keep])
        sweep = {lam: cv_r2(rows, keep, players, levels, y, lam)
                 for lam in LAM_GRID}
        lam = max(sweep, key=sweep.get)
        X, meta = design(rows, keep, players, levels)
        beta = ridge(X, y, lam)
        base = phis(beta, meta, rows, keep, players)
        r2 = 1 - float(np.sum((y - X @ beta) ** 2) /
                       max(1e-12, np.sum((y - y.mean()) ** 2)))
        strength = {p: float(np.mean([abs(base[p][rows[i][p]]) for i in keep]))
                    for p in players}

        boot = defaultdict(list)
        idx = np.arange(len(keep))
        for _ in range(a.bootstrap):
            s = rng.choice(idx, size=len(idx), replace=True)
            bids = [keep[j] for j in s]
            Xb, mb = design(rows, bids, players, levels)
            try:
                bb = ridge(Xb, y[s], lam)
            except np.linalg.LinAlgError:
                continue
            pb = phis(bb, mb, rows, bids, players)
            for p in players:
                boot[p].append(float(np.mean(
                    [abs(pb[p].get(rows[i][p], 0.0)) for i in bids])))

        r2cv = sweep[lam]
        order = sorted(players, key=lambda p: -strength[p])
        print(f"\n{'='*72}\nPAYOUT: {name}   n={len(keep)}   "
              f"R2 in-sample {r2:.3f}   R2 cross-validated {r2cv:+.3f}")
        if r2cv <= 0:
            print(f"  !! the surrogate predicts WORSE THAN THE MEAN out of "
                  f"sample. The table\n  !! below decomposes an in-sample fit "
                  f"that does not generalise; no lambda\n  !! fixes it (audit "
                  f"H1). Read it as description, not attribution.")
        print(f"  {'strength':>9}{'95% CI':>22}  player")
        for p in order[:12]:
            lo, hi = (np.percentile(boot[p], 2.5), np.percentile(boot[p], 97.5)) \
                if boot[p] else (0, 0)
            flag = " " if lo > 0.005 else "."
            print(f" {flag}{strength[p]:>9.4f}{f'[{lo:.4f}, {hi:.4f}]':>22}  "
                  f"{p[:44]}")
        top = order[0]
        print(f"\n  levels of the strongest player - {top[:60]}")
        lv_n = {lv: sum(1 for i in keep if rows[i][top] == lv)
                for lv in base[top]}
        for lv, v in sorted(base[top].items(), key=lambda t: -abs(t[1]))[:6]:
            print(f"    {v:>+8.4f}  n={lv_n[lv]:<4} {lv[:52]}")

        results[name] = {
            "n": len(keep), "r2": round(r2, 4), "r2_cv": round(r2cv, 4),
            "lambda": lam, "lambda_sweep": {str(k): round(v, 4) for k, v in sweep.items()},
            "players": {p: {
                "strength": round(strength[p], 5),
                "ci": [round(float(np.percentile(boot[p], 2.5)), 5),
                       round(float(np.percentile(boot[p], 97.5)), 5)]
                if boot[p] else None,
                "coverage": round(sum(1 for r in runs if rows[r][p] != ABSENT) / N, 3),
                "levels": {lv: round(v, 5) for lv, v in base[p].items()},
                "level_n": {lv: sum(1 for i in keep if rows[i][p] == lv)
                            for lv in base[p]},
            } for p in players},
        }

    payload = {"corpus": tag, "min_level": MIN_LEVEL, "min_levels": MIN_LEVELS,
               "lambda_grid": LAM_GRID, "bootstrap": a.bootstrap, "seed": SEED,
               "runs": N, "players": players, "payouts": results}
    p = OUT / f"shapley_{tag}{a.out_suffix}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"\n-> {p}")


if __name__ == "__main__":
    main()
