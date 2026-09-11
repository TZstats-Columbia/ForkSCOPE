#!/usr/bin/env python3
"""Are the trunk forks a tree, a graph, or 17 independent decisions?

A tree needs gates: B exists only because of a choice at A. `audit_garden.py`
G4 tested that and it did not survive a permutation null, so a tree drawn over
these forks would be drawing structure the data does not contain. That leaves
the weaker question -- is there a *graph*? -- and there are two kinds of edge
worth testing, which mean different things:

  CO-REACH   do two forks get faced together more than chance? An edge here says
             the decisions travel as a bundle: analysts who confront one
             confront the other.
  CO-CHOICE  among the runs facing both, does *which option* they take at A
             predict which they take at B? An edge here is a recipe -- the
             thing G6 looked for at the five universal nodes and did not find.

THE CONFOUND, AND WHY THE NULL IS A SWAP RANDOMISATION
------------------------------------------------------
A run recording 30 decisions reaches more forks than one recording 12. Under a
naive shuffle, that alone makes *every* pair of forks look positively
associated, and the graph comes out complete and meaningless. The null must
therefore hold two things fixed at once: how many forks each run reached, and
how many runs reached each fork.

That is a binary matrix with fixed row and column margins, and the standard way
to sample it is the curveball algorithm -- repeatedly pick two runs and swap a
random subset of the forks unique to each, which preserves both margins by
construction. It is the same null ecology uses for species co-occurrence, which
is the same problem: are these two things found together more often than their
individual commonness explains?

Co-choice is tested by shuffling option labels within the co-reaching subset,
which needs no margin trick because the subset is fixed.

Both are BH-FDR corrected over all 136 pairs.

Usage:
    python3 scripts/fork_graph.py --corpus ai
"""
import argparse
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402
import shapley_v2 as S                                          # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
OUT = P.ANALYSIS

PERM = 2000
BURN = 20000        # curveball mixing swaps before the first sample
STEP = 400          # swaps between samples
FDR = 0.05
SEED = 20260822
MIN_BOTH = 20       # runs reaching both forks, before co-choice is testable
CC_SCREEN = 600     # co-choice permutations, first pass
CC_DEEP = 40000     # ...and for anything that survives the screen


def bh(ps, q):
    if not ps:
        return 0.0
    s = sorted(ps)
    thr = 0.0
    for i, p in enumerate(s, 1):
        if p <= q * i / len(s):
            thr = p
    return thr


def curveball(M, rng, swaps):
    """In-place swap randomisation preserving row and column sums."""
    n = M.shape[0]
    for _ in range(swaps):
        i, j = rng.randrange(n), rng.randrange(n)
        if i == j:
            continue
        a, b = M[i], M[j]
        only_i = np.flatnonzero(a & ~b)
        only_j = np.flatnonzero(b & ~a)
        k = min(len(only_i), len(only_j))
        if k == 0:
            continue
        pool = np.concatenate([only_i, only_j])
        rng.shuffle(pool)
        take_i, take_j = pool[:len(only_i)], pool[len(only_i):]
        a[only_i] = False
        b[only_j] = False
        a[take_i] = True
        b[take_j] = True
    return M


def cramers_v(xs, ys):
    lx = sorted(set(xs))
    ly = sorted(set(ys))
    if len(lx) < 2 or len(ly) < 2:
        return 0.0
    ix = {v: k for k, v in enumerate(lx)}
    iy = {v: k for k, v in enumerate(ly)}
    T = np.zeros((len(lx), len(ly)))
    for a, b in zip(xs, ys):
        T[ix[a], iy[b]] += 1
    n = T.sum()
    if n == 0:
        return 0.0
    r = T.sum(1, keepdims=True)
    c = T.sum(0, keepdims=True)
    E = r @ c / n
    E[E == 0] = 1e-12
    chi2 = float(((T - E) ** 2 / E).sum())
    k = min(len(lx), len(ly)) - 1
    return math.sqrt(chi2 / (n * k)) if k > 0 else 0.0


SCOL = {"problem_formulation": "#8c6d31", "data_collection": "#7b9e5b",
        "data_cleaning": "#2f6fa8", "eda": "#c98a2b",
        "modeling": "#a3401f", "communication": "#6b4d8f"}


def clip(t, k):
    if len(t) <= k:
        return t
    cut = t[:k].rsplit(" ", 1)[0]
    return (cut if len(cut) > k * .6 else t[:k]).rstrip(",;/ ") + "…"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def render(order, posn, stg, rows, runs, ABSENT, pairs, thr, cc, thr2, N):
    """Arc diagram plus the full matrix.

    The matrix is here on purpose. An arc diagram showing six edges invites the
    reading "here is the structure"; the matrix shows the 130 pairs where there
    is none, which is the actual result.
    """
    n = len(order)
    W, H = 1180, 960
    X0, XW = 250, W - 330
    AY = 215
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
         f"viewBox='0 0 {W} {H}' font-family='ui-sans-serif,system-ui' "
         f"font-size='11'><rect width='{W}' height='{H}' fill='#fff'/>",
         "<style>.t{fill:#222;font-size:14px;font-weight:600}.d{fill:#666}"
         ".s{fill:#999;font-size:10px}.lb{fill:#444;font-size:9.5px}</style>"]
    xs = {p: X0 + XW * i / max(1, n - 1) for i, p in enumerate(order)}
    cov = {p: sum(1 for r in runs if rows[r][p] != ABSENT) / N for p in order}

    s.append("<text x='40' y='30' class='t'>Is the trunk a graph?</text>")
    s.append(f"<text x='40' y='48' class='d'>17 forks on the script-position "
             f"axis. Arcs above = co-reach (faced together or never together); "
             f"below = co-choice (the option at one predicts the other). Only "
             f"edges surviving BH-FDR 0.05 are drawn.</text>")

    def arc(a, b, up, col, wd, dash=""):
        x1, x2 = xs[a], xs[b]
        r = abs(x2 - x1) / 2
        y = AY - 6 if up else AY + 6
        sweep = 1 if up else 0
        return (f"<path d='M{x1:.1f},{y} A{r:.1f},{min(r*0.62,150):.1f} 0 0,"
                f"{sweep} {x2:.1f},{y}' fill='none' stroke='{col}' "
                f"stroke-width='{wd:.1f}' opacity='.65' {dash}/>")

    for q in pairs:
        if q["p"] > thr:
            continue
        col = "#2f6fa8" if q["dir"] == "together" else "#a3401f"
        dash = "" if q["dir"] == "together" else "stroke-dasharray='5 3'"
        s.append(arc(q["a"], q["b"], True, col, 2.6, dash))
    for q in cc:
        if q["p"] > thr2:
            continue
        s.append(arc(q["a"], q["b"], False, "#6b4d8f", 2.6))
    for i, p in enumerate(order):
        x = xs[p]
        s.append(f"<circle cx='{x:.1f}' cy='{AY}' r='{3+9*cov[p]:.1f}' "
                 f"fill='{SCOL.get(stg.get(p),'#999')}' opacity='.8'>"
                 f"<title>{esc(p)}&#10;coverage {cov[p]:.2f}</title></circle>")
        s.append(f"<text x='{x:.1f}' y='{AY+36}' class='lb' "
                 f"transform='rotate(58 {x:.1f} {AY+36})'>"
                 f"{i+1}. {esc(clip(p, 30))}</text>")
    s.append(f"<text x='{X0-10}' y='{AY+4}' text-anchor='end' class='s'>"
             f"earlier</text>")
    ly = 90
    for lab, col, d in (("faced together more than chance", "#2f6fa8", ""),
                        ("never faced together (see below)", "#a3401f",
                         "dashed"),
                        ("choice predicts choice", "#6b4d8f", "")):
        s.append(f"<line x1='40' y1='{ly}' x2='70' y2='{ly}' stroke='{col}' "
                 f"stroke-width='2.6' "
                 f"{'stroke-dasharray=\"5 3\"' if d else ''}/>")
        s.append(f"<text x='78' y='{ly+4}' class='s'>{lab}</text>")
        ly += 18

    # ---- matrix -----------------------------------------------------------
    MY = 470
    s.append(f"<text x='40' y='{MY}' class='t'>…mostly not. All "
             f"{n*(n-1)//2} pairs</text>")
    s.append(f"<text x='40' y='{MY+18}' class='d'>upper triangle co-reach, "
             f"lower co-choice. Shade = how far from the null; ring = survives "
             f"FDR. The white is the finding.</text>")
    CS, MX0, MY0 = 19, 330, MY + 36
    pm = {(q["i"], q["j"]): q for q in pairs}
    cm = {(q["i"], q["j"]): q for q in cc}
    for i in range(n):
        s.append(f"<text x='{MX0-6}' y='{MY0+i*CS+13}' text-anchor='end' "
                 f"class='lb'>{i+1}. {esc(clip(order[i], 28))}</text>")
        s.append(f"<text x='{MX0+i*CS+CS/2:.0f}' y='{MY0-6}' class='lb' "
                 f"text-anchor='middle'>{i+1}</text>")
        for j in range(n):
            if i == j:
                s.append(f"<rect x='{MX0+j*CS}' y='{MY0+i*CS}' "
                         f"width='{CS-2}' height='{CS-2}' fill='#f4f4f4'/>")
                continue
            k = (min(i, j), max(i, j))
            up = j > i
            q = pm.get(k) if up else cm.get(k)
            if not q:
                continue
            if up:
                mag = min(1.0, abs(math.log10(max(q["p"], 1e-4))) / 4)
                col = "#2f6fa8" if q["dir"] == "together" else "#a3401f"
                ok = q["p"] <= thr
            else:
                mag = min(1.0, abs(math.log10(max(q["p"], 1e-4))) / 4)
                col = "#6b4d8f"
                ok = q["p"] <= thr2
            s.append(f"<rect x='{MX0+j*CS}' y='{MY0+i*CS}' width='{CS-2}' "
                     f"height='{CS-2}' fill='{col}' opacity='{mag*.85:.2f}'/>")
            if ok:
                s.append(f"<rect x='{MX0+j*CS}' y='{MY0+i*CS}' "
                         f"width='{CS-2}' height='{CS-2}' fill='none' "
                         f"stroke='#111' stroke-width='1.4'/>")
    s.append("</svg>")
    p = P.FIGURES / "fork_graph.svg"
    p.write_text("\n".join(s), encoding="utf-8")
    print(f"-> {p}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    rows, players, levels, runs, N, _ = S.build_rows(tag)
    gm = json.loads((OUT / f"garden_{tag}.json").read_text(encoding="utf-8"))
    posn = {x["fork"]: x["position"] for x in gm["nodes_detail"]}
    stg = {x["fork"]: x.get("stage") for x in gm["nodes_detail"]}
    order = sorted(players, key=lambda p: posn.get(p, 0))
    n = len(order)
    rng = random.Random(SEED)
    nprng = np.random.default_rng(SEED)

    # incidence: runs x forks, True = reached
    M = np.array([[rows[r][p] != S.ABSENT for p in order] for r in runs],
                 dtype=bool)
    obs = (M.astype(np.int32).T @ M.astype(np.int32))

    print(f"FORK GRAPH - {tag}")
    print(f"{n} trunk forks, {N} runs, {n*(n-1)//2} pairs\n")
    print(f"reach per run: median {int(np.median(M.sum(1)))}, "
          f"range {M.sum(1).min()}-{M.sum(1).max()}")
    print(f"-> a naive null would call almost every pair associated; using "
          f"curveball\n   swap randomisation (both margins fixed, {PERM} "
          f"samples)\n")

    # ---- co-reach null ----------------------------------------------------
    W = M.copy()
    curveball(W, rng, BURN)
    ge = np.zeros((n, n))
    le = np.zeros((n, n))
    acc = np.zeros((n, n))
    for _ in range(PERM):
        curveball(W, rng, STEP)
        C = (W.astype(np.int32).T @ W.astype(np.int32))
        ge += (C >= obs)
        le += (C <= obs)
        acc += C
    exp = acc / PERM
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            p_hi = (ge[i, j] + 1) / (PERM + 1)
            p_lo = (le[i, j] + 1) / (PERM + 1)
            pairs.append({
                "a": order[i], "b": order[j], "i": i, "j": j,
                "both": int(obs[i, j]), "expected": round(float(exp[i, j]), 1),
                "p": float(min(p_hi, p_lo)),
                "dir": "together" if obs[i, j] > exp[i, j] else "apart",
            })
    thr = bh([q["p"] for q in pairs], FDR)
    sig = [q for q in pairs if q["p"] <= thr]
    print(f"CO-REACH  (do two forks get faced together more/less than "
          f"chance?)")
    print(f"  BH-FDR {FDR} -> p <= {thr:.4g};  {len(sig)} of {len(pairs)} "
          f"pairs significant")
    for q in sorted(sig, key=lambda z: z["p"])[:14]:
        print(f"    {q['dir']:<9} obs {q['both']:>3} vs exp "
              f"{q['expected']:>5}  p={q['p']:.4f}")
        print(f"      {q['a'][:64]}")
        print(f"      {q['b'][:64]}")

    # ---- co-choice --------------------------------------------------------
    print(f"\nCO-CHOICE  (among runs facing both, does the option at A predict "
          f"the option at B?)")
    cc = []
    for i in range(n):
        for j in range(i + 1, n):
            A, Bk = order[i], order[j]
            sub = [r for r in runs
                   if rows[r][A] != S.ABSENT and rows[r][Bk] != S.ABSENT]
            if len(sub) < MIN_BOTH:
                continue
            xs = [rows[r][A] for r in sub]
            ys = [rows[r][Bk] for r in sub]
            v = cramers_v(xs, ys)
            # Two stages, because a permutation p cannot go below 1/(B+1) and
            # the BH threshold over 126 tests is ~4e-4. Screening at B=600
            # floors every p at 1.7e-3, which is ABOVE the threshold -- the
            # test would return "nothing significant" by construction, whatever
            # the data said. Survivors are re-tested at B=CC_DEEP.
            null = [cramers_v(xs, list(nprng.permutation(ys)))
                    for _ in range(CC_SCREEN)]
            pv = (sum(1 for z in null if z >= v) + 1) / (CC_SCREEN + 1)
            deep = False
            if pv < 0.05:
                extra = [cramers_v(xs, list(nprng.permutation(ys)))
                         for _ in range(CC_DEEP)]
                null = null + extra
                pv = (sum(1 for z in null if z >= v) + 1) / (len(null) + 1)
                deep = True
            cc.append({"a": A, "b": Bk, "i": i, "j": j, "n": len(sub),
                       "v": round(v, 3), "perms": len(null), "deep": deep,
                       "null_v": round(float(np.mean(null)), 3), "p": pv})
    thr2 = bh([q["p"] for q in cc], FDR)
    sig2 = [q for q in cc if q["p"] <= thr2]
    print(f"  {len(cc)} pairs testable (>= {MIN_BOTH} runs facing both); "
          f"BH-FDR -> p <= {thr2:.4g}; {len(sig2)} significant")
    for q in sorted(cc, key=lambda z: z["p"])[:10]:
        mark = "*" if q["p"] <= thr2 else " "
        print(f"   {mark} V={q['v']:.2f} (null {q['null_v']:.2f}) n={q['n']:>3} "
              f"p={q['p']:.5f} (B={q['perms']:,})")
        print(f"      {q['a'][:64]}")
        print(f"      {q['b'][:64]}")

    # ---- do the mutual-exclusion edges look like missed siblings? ---------
    import garden as G
    print(f"\nMUTUAL EXCLUSION AS A SIBLING DETECTOR")
    print(f"  garden.py screened sibling candidates on label Jaccard "
          f">= {G.LABEL_J}.\n  These pairs are mutually exclusive in the data. "
          f"Did the lexical screen see them?")
    miss = []
    for q in sorted(sig, key=lambda z: z["p"]):
        if q["dir"] != "apart":
            continue
        j = G.jac(G.toks(q["a"]), G.toks(q["b"]))
        seen = j >= G.LABEL_J and q["both"] <= G.CO_MAX
        miss.append({**q, "label_jaccard": round(j, 3), "screened": seen})
        print(f"    J={j:.2f}  {'screened' if seen else 'MISSED BY SCREEN':<16} "
              f"obs {q['both']} vs exp {q['expected']}")
        print(f"      {q['a'][:66]}")
        print(f"      {q['b'][:66]}")
    nmiss = sum(1 for m in miss if not m["screened"])
    if nmiss:
        print(f"  -> {nmiss} of {len(miss)} invisible to a lexical screen. "
              f"Mutual exclusivity\n     is the stronger signal: it is a "
              f"property of the runs, not the wording.")

    render(order, posn, stg, rows, runs, S.ABSENT, pairs, thr, cc, thr2, N)

    payload = {"corpus": tag, "forks": order, "runs": N, "perm": PERM,
               "exclusion_vs_screen": miss,
               "stage": {p: stg.get(p) for p in order},
               "position": {p: posn.get(p) for p in order},
               "co_reach": pairs, "co_reach_threshold": thr,
               "co_choice": cc, "co_choice_threshold": thr2}
    p = OUT / f"fork_graph_{tag}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"\nSUMMARY")
    print(f"  tree?  no gate survives its null (audit G4) - a tree would be "
          f"invented")
    print(f"  graph? co-reach edges {len(sig)}/{len(pairs)}, "
          f"co-choice edges {len(sig2)}/{len(cc)}")
    print(f"\n-> {p}")


if __name__ == "__main__":
    main()
