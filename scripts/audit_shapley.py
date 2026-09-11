#!/usr/bin/env python3
"""Audit for the v2 Shapley attribution. Deterministic apart from seeded draws.

The production script reports a `strength` per player with a bootstrap CI, and
that CI is not the test a reader will assume it is. Six checks, of which the
first three can each invalidate the table:

  H1  OVERFIT. The surrogate has ~50 free parameters on 204 rows. In-sample R2
      is therefore optimistic by construction. Cross-validated R2 is the number
      that says whether the surrogate predicts anything, and if it is near zero
      the attributions are a decomposition of noise.
  H2  THE CI CANNOT COVER ZERO. `strength` is a mean of absolute values, so
      bootstrapping it produces an interval bounded away from zero no matter
      what the data say -- a player with no relationship to the payout still
      gets a CI excluding 0. The honest null is a permutation: shuffle the
      payout across runs and re-run the whole pipeline.
  H3  LENGTH ARTIFACT. `absent` is a level, and a run that recorded few
      decisions is absent at many players at once. If attribution is carried by
      the absent levels, the table is measuring how much a run wrote, not what
      it chose -- the same trap checked for in the iteration analysis.
  H4  COLLINEARITY. Absent indicators are correlated across players for the
      same reason. A near-singular design makes ridge split credit arbitrarily
      between correlated players.
  H5  REGULARISATION. If the player ranking moves with lambda, the ranking is a
      property of the penalty.
  H6  PAYOUT AGREEMENT. Verdict and log(OR) measure related things. Rankings
      that disagree completely would mean the attribution is unstable.

Usage:
    python3 scripts/audit_shapley.py --corpus ai
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shapley_v2 as S                                          # noqa: E402
import paths as P                                             # noqa: E402

PERM = 400
FOLDS = 5
SEED = 20260822


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    out = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            out[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = (sum((x - ma) ** 2 for x in ra) * sum((x - mb) ** 2 for x in rb)) ** .5
    return num / den if den else 0.0


def strengths(rows, ids, players, levels, y, lam):
    X, meta = S.design(rows, ids, players, levels)
    beta = S.ridge(X, y, lam)
    ph = S.phis(beta, meta, rows, ids, players)
    return ({p: float(np.mean([abs(ph[p][rows[i][p]]) for i in ids]))
             for p in players}, X, beta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--json")
    ap.add_argument("--players", choices=["contrast", "pivotal"],
                   default="contrast",
                   help="must match the shapley run being audited, or the "
                        "p-values describe a different player set")
    ap.add_argument("--pivotal-eff", type=float, default=1.5)
    ap.add_argument("--novelty", action="store_true")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    piv = (S.pivotal_set(tag, a.pivotal_eff)
           if a.players == "pivotal" else None)
    rows, players, levels, runs, N, opts = S.build_rows(tag, piv, a.novelty)
    # An audit of a result that was not produced has nothing to check. Shapley
    # itself now skips when there are no outcomes -- owner decision D3, the
    # extractor is unwritten -- so its audit must skip for the same reason
    # rather than crash one stage later on the same missing file.
    if not S.OUTCOMES.exists():
        print(f"H1-H6 NOT RUN -- no outcomes at {S.OUTCOMES}, so shapley was "
              f"not computed and there is nothing to audit. Owner decision D3.")
        return
    outcomes = {o["repo_id"]: o for o in
                json.loads(S.OUTCOMES.read_text(encoding="utf-8"))}
    rng = np.random.default_rng(SEED)
    res = {}

    print(f"SHAPLEY AUDIT - corpus {tag}")
    print(f"{len(players)} players, {N} runs\n")

    # lambda is CV-selected per payout in production, so the audit must use the
    # same value or H1 and H2 grade a model nobody reports
    per_payout = {}
    for name, fn in S.PAYOUTS.items():
        keep = [i for i in runs if i in outcomes and fn(outcomes[i]) is not None]
        if len(keep) < 30:
            continue
        y = np.array([fn(outcomes[i]) for i in keep])
        sweep = {lm: S.cv_r2(rows, keep, players, levels, y, lm)
                 for lm in S.LAM_GRID}
        per_payout[name] = (keep, y, max(sweep, key=sweep.get), sweep)

    # ---- H1 overfit --------------------------------------------------------
    print(f"H1  OVERFIT  (in-sample vs {FOLDS}-fold cross-validated R2)")
    print(f"    {'payout':<12}{'lambda':>8}{'in-sample':>11}{'CV':>9}{'gap':>9}")
    h1 = {}
    worst_cv = 1.0
    for name, (keep, y, lam, sweep) in per_payout.items():
        X, _ = S.design(rows, keep, players, levels)
        beta = S.ridge(X, y, lam)
        r2in = 1 - float(np.sum((y - X @ beta) ** 2) /
                         max(1e-12, np.sum((y - y.mean()) ** 2)))
        idx = rng.permutation(len(keep))
        pred = np.zeros(len(keep))
        for f in range(FOLDS):
            te = idx[f::FOLDS]
            tr = np.array([j for j in idx if j not in set(te.tolist())])
            Xtr, _ = S.design(rows, [keep[j] for j in tr], players, levels)
            Xte, _ = S.design(rows, [keep[j] for j in te], players, levels)
            if Xtr.shape[1] != Xte.shape[1]:      # a level vanished from a fold
                m = min(Xtr.shape[1], Xte.shape[1])
                Xtr, Xte = Xtr[:, :m], Xte[:, :m]
            b = S.ridge(Xtr, y[tr], lam)
            pred[te] = Xte @ b
        r2cv = sweep[lam]
        worst_cv = min(worst_cv, r2cv)
        h1[name] = {"lambda": lam, "in_sample": round(r2in, 4), "cv": round(r2cv, 4)}
        print(f"    {name:<12}{lam:>8}{r2in:>11.3f}{r2cv:>9.3f}{r2in-r2cv:>9.3f}")
    v = "PASS" if worst_cv > 0.05 else "REVIEW"
    print(f"    verdict {v} - a surrogate that does not predict out of sample")
    print(f"    cannot support an attribution table\n")
    res["H1"] = {"verdict": v, "r2": h1}

    # ---- H2 permutation null ------------------------------------------------
    print(f"H2  PERMUTATION NULL  ({PERM} draws; the bootstrap CI in the")
    print(f"    production table is a mean of absolute values and cannot "
          f"cover 0)")
    h2 = {}
    any_sig = False
    for name, (keep, y, lam, sweep) in per_payout.items():
        obs, _, _ = strengths(rows, keep, players, levels, y, lam)
        null = defaultdict(list)
        for _ in range(PERM):
            ys = rng.permutation(y)
            st, _, _ = strengths(rows, keep, players, levels, ys, lam)
            for p in players:
                null[p].append(st[p])
        rowsout = []
        for p in players:
            ge = sum(1 for x in null[p] if x >= obs[p]) / PERM
            rowsout.append((ge, obs[p], float(np.mean(null[p])), p))
        rowsout.sort()
        sig = [r for r in rowsout if r[0] < 0.05]
        any_sig = any_sig or bool(sig)
        h2[name] = [{"player": p, "strength": round(o, 5),
                     "null_mean": round(nm, 5), "p": pv}
                    for pv, o, nm, p in rowsout]
        print(f"\n    {name}  ({len(sig)} of {len(players)} players beat the "
              f"null at p<0.05)")
        print(f"      {'p':>7}{'strength':>10}{'null':>9}  player")
        for pv, o, nm, p in rowsout[:6]:
            mark = "*" if pv < 0.05 else " "
            print(f"     {mark}{pv:>6.3f}{o:>10.4f}{nm:>9.4f}  {p[:44]}")
    v = "PASS" if any_sig else "REVIEW"
    print(f"\n    verdict {v}\n")
    res["H2"] = {"verdict": v, "by_payout": h2}

    # ---- H3 length artifact -------------------------------------------------
    nabs = {r: sum(1 for p in players if rows[r][p] == S.ABSENT)
            for r in runs}
    d = json.loads((S.P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    ndec = defaultdict(int)
    for x in d["decisions"]:
        ndec[x["run"]] += 1
    rr = sorted(runs)
    cor = spearman([nabs[r] for r in rr], [ndec[r] for r in rr])
    print(f"H3  LENGTH ARTIFACT")
    print(f"    Spearman(absent count, decisions recorded)  {cor:+.3f}")
    h3 = {}
    for name, (keep, y, lam, sweep) in per_payout.items():
        X, meta = S.design(rows, keep, players, levels)
        beta = S.ridge(X, y, lam)
        ph = S.phis(beta, meta, rows, keep, players)
        tot = sum(abs(ph[p][rows[i][p]]) for i in keep for p in players)
        abs_share = sum(abs(ph[p][rows[i][p]]) for i in keep for p in players
                        if rows[i][p] == S.ABSENT) / max(1e-12, tot)
        n_abs = sum(1 for i in keep for p in players if rows[i][p] == S.ABSENT)
        base = n_abs / (len(keep) * len(players))
        h3[name] = {"absent_share_of_attribution": round(abs_share, 4),
                    "absent_share_of_cells": round(base, 4)}
        print(f"    {name:<12} absent carries {abs_share:>6.1%} of "
              f"attribution on {base:.1%} of cells")
    v = "PASS" if abs(cor) < 0.8 else "REVIEW"
    print(f"    verdict {v} - if absent carried far more than its cell share,")
    print(f"    the table would be about how much a run wrote\n")
    res["H3"] = {"verdict": v, "absent_vs_length_spearman": round(cor, 4),
                 "by_payout": h3}

    # ---- H4 collinearity ----------------------------------------------------
    keep, y, vlam, _ = per_payout["verdict"]
    X, meta = S.design(rows, keep, players, levels)
    sv = np.linalg.svd(X, compute_uv=False)
    cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")
    v = "PASS" if cond < 100 else "REVIEW"
    print(f"H4  COLLINEARITY                                            {v}")
    print(f"    design {X.shape[0]} x {X.shape[1]}, condition number {cond:.1f}")
    print(f"    (ridge lambda={S.LAM} is what keeps this solvable)\n")
    res["H4"] = {"verdict": v, "condition": round(cond, 2),
                 "shape": list(X.shape)}

    # ---- H5 lambda sensitivity ----------------------------------------------
    print(f"H5  REGULARISATION  (player ranking vs lambda, payout = verdict)")
    ref, _, _ = strengths(rows, keep, players, levels, y, vlam)
    refv = [ref[p] for p in players]
    h5 = {}
    worst = 1.0
    for lam in (x for x in S.LAM_GRID if x != vlam):
        st, _, _ = strengths(rows, keep, players, levels, y, lam)
        rho = spearman(refv, [st[p] for p in players])
        worst = min(worst, rho)
        h5[str(lam)] = round(rho, 4)
        print(f"    lambda {lam:<5} Spearman vs selected {vlam}: {rho:+.3f}")
    v = "PASS" if worst > 0.7 else "REVIEW"
    print(f"    verdict {v}\n")
    res["H5"] = {"verdict": v, "spearman_vs_default": h5}

    # ---- H6 payout agreement -------------------------------------------------
    print(f"H6  PAYOUT AGREEMENT  (Spearman between player rankings)")
    sts = {}
    for name, (kp, yy, lm, _) in per_payout.items():
        st, _, _ = strengths(rows, kp, players, levels, yy, lm)
        sts[name] = [st[p] for p in players]
    names = list(sts)
    h6 = {}
    lo = 1.0
    print(f"    {'':<12}" + "".join(f"{n:>11}" for n in names))
    for i in names:
        line = f"    {i:<12}"
        for j in names:
            r = spearman(sts[i], sts[j])
            line += f"{r:>11.2f}"
            if i != j:
                lo = min(lo, r)
                h6[f"{i}|{j}"] = round(r, 3)
        print(line)
    v = "PASS" if lo > 0.2 else "REVIEW"
    print(f"    weakest pair {lo:+.2f} - verdict {v}\n")
    res["H6"] = {"verdict": v, "pairs": h6, "weakest": round(lo, 3)}

    fails = [k for k, x in res.items() if isinstance(x, dict)
             and x.get("verdict") == "REVIEW"]
    print("=" * 68)
    print("ALL CHECKS PASS" if not fails else "NEEDS REVIEW: " + ", ".join(fails))
    p = Path(a.json) if a.json else P.AUDITS / f"shapley_audit_{tag}.json"
    p.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {p}")


if __name__ == "__main__":
    main()
