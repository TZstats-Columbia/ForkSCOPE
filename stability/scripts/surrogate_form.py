#!/usr/bin/env python3
"""Does a non-additive surrogate predict the outcome better? No model calls.

THE QUESTION
------------
Shapley attribution here runs over a RIDGE surrogate on one-hot level
indicators. That is a deliberate choice with a stated cost, in
`shapley_v2.py`: an additive surrogate cannot represent "dichotomising only
matters if you also cluster", so where analysts' choices genuinely interact the
attribution spreads the interaction across main effects.

The obvious alternative is a tree model, which captures interactions natively.
Whether that is an improvement is an empirical question, and this answers it on
the same design, the same folds and the same seed.

THE CLEAN CONTRAST: STUMPS AGAINST DEPTH
----------------------------------------
Gradient boosting with `max_depth=1` -- stumps -- is ADDITIVE by construction:
each tree splits on one indicator, so the model is a sum of per-feature
functions and cannot express an interaction. `max_depth>=2` can.

So the stump-to-depth gap is the interaction contribution, isolated, without
confounding it with the difference between a linear and a tree fit. Comparing
ridge against a deep forest alone would confound the two.

WHY THE ANSWER MATTERS EITHER WAY
---------------------------------
  interactions add nothing   additivity is safe here, and the per-fork
                             attribution is not hiding structure. That is a
                             positive result for the method, not an absence.
  interactions add a lot     the additive attribution understates how choices
                             combine, and the report must say so -- the Shapley
                             numbers stay usable as main effects but stop being
                             a complete account.

WHAT THIS DOES NOT DO
---------------------
It does not replace the surrogate. Attribution over a tree needs TreeSHAP and
means something different -- interaction credit gets allocated among features,
so a per-fork number stops being "what this fork does" and becomes "this fork's
share of a joint effect". That is a modelling decision for the study owner, and
this script exists to inform it rather than to make it.

Usage:
    python3 stability/scripts/surrogate_form.py --corpus <tag> [--players pivotal]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import paths as P                                                  # noqa: E402
import shapley_v2 as S                                             # noqa: E402

FOLDS = 5


def folds_of(n, seed=S.SEED):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    return [(np.array([j for j in idx if j not in set(idx[f::FOLDS].tolist())]),
             idx[f::FOLDS]) for f in range(FOLDS)]


def cv_score(fit, X, y):
    """Pooled out-of-fold R2, on ONE design so columns cannot misalign.

    Rebuilding the design per fold is what broke `cv_r2` before: `design()`
    emits only the levels present in the ids it is given, so folds produced
    different column sets that were then aligned by position.
    """
    pred = np.zeros(len(y))
    for tr, te in folds_of(len(y)):
        pred[te] = fit(X[tr], y[tr]).predict(X[te])
    return 1 - float(np.sum((y - pred) ** 2) /
                     max(1e-12, np.sum((y - y.mean()) ** 2)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--players", choices=["contrast", "pivotal"],
                    default="pivotal")
    ap.add_argument("--pivotal-eff", type=float, default=1.5)
    ap.add_argument("--json")
    a = ap.parse_args()

    tag = "+".join(c.strip() for c in a.corpus.split(","))
    piv = (S.pivotal_set(tag, a.pivotal_eff)
           if a.players == "pivotal" else None)
    rows, players, levels, runs, N, opts = S.build_rows(tag, piv)
    outcomes = {o["repo_id"]: o for o in
                json.loads(P.OUTCOMES.read_text(encoding="utf-8"))}

    print(f"SURROGATE FORM — {tag}")
    print(f"  {len(players)} players ({a.players} selection), "
          f"{FOLDS}-fold, seed {S.SEED}\n")
    print(f"  {'payout':<10}{'ridge':>9}{'stumps':>9}{'depth 3':>9}"
          f"{'forest':>9}   {'interaction':>12}")

    res = {"corpus": tag, "players": a.players, "n_players": len(players),
           "folds": FOLDS, "payouts": {}}
    for name, fn in S.PAYOUTS.items():
        ids = [r for r in sorted(runs)
               if r in outcomes and fn(outcomes[r]) is not None]
        y = np.array([fn(outcomes[r]) for r in ids], dtype=float)
        X, _ = S.design(rows, ids, players, levels)

        # ridge at the lambda its own CV selects, so the comparison is against
        # the surrogate as actually used rather than an unregularised one
        best = max(S.LAM_GRID,
                   key=lambda lam: S.cv_r2(rows, ids, players, levels, y, lam))
        r_ridge = S.cv_r2(rows, ids, players, levels, y, best)

        def gb(depth):
            return lambda Xt, yt: GradientBoostingRegressor(
                max_depth=depth, n_estimators=300, learning_rate=0.05,
                subsample=0.9, random_state=S.SEED).fit(Xt, yt)

        r_stump = cv_score(gb(1), X, y)
        r_deep = cv_score(gb(3), X, y)
        r_rf = cv_score(
            lambda Xt, yt: RandomForestRegressor(
                n_estimators=400, min_samples_leaf=3, random_state=S.SEED,
                n_jobs=-1).fit(Xt, yt), X, y)

        gap = r_deep - r_stump
        print(f"  {name:<10}{r_ridge:>9.3f}{r_stump:>9.3f}{r_deep:>9.3f}"
              f"{r_rf:>9.3f}{gap:>+12.3f}")
        res["payouts"][name] = {
            "n": len(ids), "ridge_lambda": best, "ridge": round(r_ridge, 4),
            "stumps_additive": round(r_stump, 4),
            "depth3": round(r_deep, 4), "forest": round(r_rf, 4),
            "interaction_gain": round(gap, 4)}

    print("\n  stumps are ADDITIVE by construction; depth 3 is not, so the last")
    print("  column is the interaction contribution with the linear-vs-tree")
    print("  difference held out of it.")

    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {a.json}")


if __name__ == "__main__":
    main()
