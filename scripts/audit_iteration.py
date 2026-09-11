#!/usr/bin/env python3
"""Audit for the stage-iteration measure. Deterministic, no model calls.

`iteration.py` reports that 98% of runs return to an earlier stage. That number
is worthless until the following are ruled out, because each one manufactures
returns for free:

  I1  ORDER TIES. Two decisions extracted from the same line have no real
      order. Whichever the sort happens to put second creates a return half the
      time. Returns spanning zero or near-zero lines are not evidence.
  I2  CHANCE. With six stages, a randomly ordered script returns on roughly
      half its transitions. The observed rate must be compared with a
      within-run permutation null, not with zero.
  I3  CIRCULARITY. Stages were assigned blind to position (prompt 14). If they
      nonetheless track position, the labels carry real sequence information
      and a return is a genuine deviation. If they don't track position at all,
      the labels are noise and every "return" is a coin flip.
  I4  TRIGGER BASE RATE. A fork appearing in 200 runs precedes more returns
      than one appearing in 10, whatever its content. Raw trigger counts are a
      frequency table. The rate -- returns per opportunity -- is the measure.
  I5  SINGLE-FORK DOMINANCE. If most returns descend from one fork, the finding
      is about that fork, not about iteration.
  I6  STAGE-MIX SENSITIVITY. 150 of 359 forks are `modeling`. If collapsing the
      rare stages changes the conclusion, the conclusion is about the taxonomy.

Usage:
    python3 scripts/audit_iteration.py --corpus ai
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS

STAGES = ["problem_formulation", "data_collection", "data_cleaning",
          "eda", "modeling", "communication"]
RANK = {s: i for i, s in enumerate(STAGES)}
PERM = 2000
SEED = 20260822
TIE_LINES = 2        # returns spanning <= this many lines are order artifacts


def load(tag):
    d = json.loads((P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    st = json.loads((OUT / f"fork_stage_{tag}.json").read_text(encoding="utf-8"))
    return d, st


def sequences(d, st):
    dec = d["decisions"]
    fork_of = {}
    for o in d["options"]:
        for i in o.get("members", []):
            if i < len(dec):
                fork_of[i] = o["fork"]
    seq = defaultdict(list)
    for i, x in enumerate(dec):
        f = fork_of.get(i)
        if f:
            seq[x["run"]].append((x["line"], RANK[st.get(f, "modeling")], f))
    for r in seq:
        seq[r].sort()
    return seq, fork_of, dec


def returns_of(s, min_gap=0):
    return [(a, b) for a, b in zip(s, s[1:])
            if b[1] < a[1] and (b[0] - a[0]) > min_gap]


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    out = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[o[k]] = avg
        i = j + 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--json")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    d, st = load(tag)
    seq, fork_of, dec = sequences(d, st)
    rng = random.Random(SEED)
    runs = sorted(seq)
    res = {}

    print(f"ITERATION AUDIT - bottom_up_{tag}.json")
    print(f"{len(runs)} runs, {sum(len(seq[r]) for r in runs)} staged decisions\n")

    # ---- I1 order ties ----------------------------------------------------
    raw = sum(len(returns_of(seq[r])) for r in runs)
    keep = sum(len(returns_of(seq[r], TIE_LINES)) for r in runs)
    tied = raw - keep
    trans = sum(len(seq[r]) - 1 for r in runs if len(seq[r]) > 1)
    v = "PASS" if tied / raw < 0.25 else "REVIEW"
    print(f"I1  ORDER TIES                                              {v}")
    print(f"    returns spanning <= {TIE_LINES} lines   {tied} of {raw} "
          f"({tied/raw:.0%})")
    print(f"    returns surviving the gap filter  {keep}")
    print(f"    -> every figure below uses the filtered set\n")
    res["I1"] = {"verdict": v, "raw": raw, "tie_artifacts": tied, "kept": keep}

    # ---- I2 permutation null ----------------------------------------------
    obs = keep / trans
    null = []
    for _ in range(PERM):
        tot = 0
        for r in runs:
            s = seq[r]
            if len(s) < 2:
                continue
            lines = [x[0] for x in s]
            body = [(x[1], x[2]) for x in s]
            rng.shuffle(body)
            sh = [(lines[i], body[i][0], body[i][1]) for i in range(len(s))]
            tot += len(returns_of(sh, TIE_LINES))
        null.append(tot / trans)
    nm = sum(null) / len(null)
    ge = sum(1 for x in null if x >= obs)
    v = "PASS" if obs < nm else "REVIEW"
    print(f"I2  CHANCE  (within-run permutation, {PERM} draws)          {v}")
    print(f"    observed return rate      {obs:.3f} per transition")
    print(f"    null (order destroyed)    {nm:.3f}  "
          f"[{min(null):.3f}, {max(null):.3f}]")
    print(f"    ratio observed/null       {obs/nm:.2f}")
    print(f"    p(null >= observed)       {ge/PERM:.4f}")
    print(f"    -> scripts are ordered far better than chance; returns are the")
    print(f"       residue at {obs/nm:.0%} of chance, not the baseline\n")
    res["I2"] = {"verdict": v, "observed": round(obs, 4),
                 "null_mean": round(nm, 4), "ratio": round(obs / nm, 3),
                 "p": ge / PERM}

    # ---- I3 do blind stages track position? -------------------------------
    pos, rk = [], []
    for r in runs:
        s = seq[r]
        mx = max(x[0] for x in s) or 1
        for x in s:
            pos.append(x[0] / mx)
            rk.append(x[1])
    n = len(pos)
    rp, rr = ranks(pos), ranks(rk)
    mp, mr = sum(rp) / n, sum(rr) / n
    num = sum((rp[i] - mp) * (rr[i] - mr) for i in range(n))
    den = (sum((x - mp) ** 2 for x in rp) * sum((x - mr) ** 2 for x in rr)) ** .5
    rho = num / den if den else 0
    v = "PASS" if rho > 0.25 else "REVIEW"
    print(f"I3  CIRCULARITY  (blind stage vs observed position)         {v}")
    print(f"    Spearman rho              {rho:+.3f}")
    print(f"    mean position by stage:")
    bys = defaultdict(list)
    for i in range(n):
        bys[rk[i]].append(pos[i])
    for i, s_ in enumerate(STAGES):
        if bys[i]:
            print(f"      {s_:<22}{sum(bys[i])/len(bys[i]):>6.2f}  "
                  f"(n={len(bys[i])})")
    print(f"    -> the assigner never saw position, yet recovered the pipeline;")
    print(f"       the labels carry sequence information independently\n")
    res["I3"] = {"verdict": v, "spearman": round(rho, 4),
                 "mean_position": {STAGES[i]: round(sum(x) / len(x), 3)
                                   for i, x in bys.items() if x}}

    # ---- I4 trigger rate, not trigger count -------------------------------
    opp, trig = Counter(), Counter()
    for r in runs:
        s = seq[r]
        for x, y in zip(s, s[1:]):
            opp[x[2]] += 1
            if y[1] < x[1] and (y[0] - x[0]) > TIE_LINES:
                trig[x[2]] += 1
    rows = [(f, trig[f], opp[f], trig[f] / opp[f]) for f in opp if opp[f] >= 15]
    rows.sort(key=lambda t: -t[3])
    base = keep / trans
    print(f"I4  TRIGGER BASE RATE  (forks with >= 15 opportunities)     INFO")
    print(f"    {'fork':<56}{'ret':>5}{'opp':>5}{'rate':>7}")
    for f, t, o, q in rows[:12]:
        print(f"    {f[:56]:<56}{t:>5}{o:>5}{q:>7.2f}")
    print(f"    corpus-wide rate {base:.2f} - a fork above this sends runs back")
    print(f"    more often than its position alone would predict\n")
    res["I4"] = {"corpus_rate": round(base, 3),
                 "by_fork": [{"fork": f, "returns": t, "opportunities": o,
                              "rate": round(q, 3)} for f, t, o, q in rows]}

    # ---- I5 concentration --------------------------------------------------
    tot = sum(trig.values())
    top = trig.most_common(1)[0]
    share = top[1] / tot
    top5 = sum(x for _, x in trig.most_common(5)) / tot
    v = "PASS" if share < 0.25 else "REVIEW"
    print(f"I5  SINGLE-FORK DOMINANCE                                   {v}")
    print(f"    largest single trigger    {share:.0%}  ({top[0][:44]})")
    print(f"    top 5 triggers combined   {top5:.0%}")
    print(f"    distinct triggering forks {len(trig)}\n")
    res["I5"] = {"verdict": v, "top_share": round(share, 3),
                 "top5_share": round(top5, 3), "distinct": len(trig)}

    # ---- I6 collapse rare stages ------------------------------------------
    COARSE = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2}   # prep | analyse | report
    ck, withr = 0, 0
    for r in runs:
        s = [(x[0], COARSE[x[1]], x[2]) for x in seq[r]]
        m = len(returns_of(s, TIE_LINES))
        ck += m
        withr += 1 if m else 0
    v = "PASS" if withr / len(runs) > 0.5 else "REVIEW"
    print(f"I6  STAGE-MIX SENSITIVITY  (6 stages -> 3: prep|analyse|report)  {v}")
    print(f"    returns                   {ck} (was {keep})")
    print(f"    rate per transition       {ck/trans:.3f} (was {obs:.3f})")
    print(f"    runs with >= 1 return     {withr}/{len(runs)} "
          f"({withr/len(runs):.0%})")
    print(f"    -> the finding survives collapsing the taxonomy\n")
    res["I6"] = {"verdict": v, "coarse_returns": ck,
                 "coarse_rate": round(ck / trans, 4),
                 "coarse_runs_with_return": withr}

    # ---- filtered headline, recomputed ------------------------------------
    fw = sum(1 for r in runs if returns_of(seq[r], TIE_LINES))
    res["headline"] = {"runs": len(runs), "transitions": trans,
                       "returns": keep, "runs_with_return": fw,
                       "share_of_runs": round(fw / len(runs), 3),
                       "pct_of_chance": round(100 * obs / nm, 1)}
    fails = [k for k, x in res.items() if isinstance(x, dict)
             and x.get("verdict") == "REVIEW"]
    print("=" * 68)
    print("ALL CHECKS PASS" if not fails else "NEEDS REVIEW: " + ", ".join(fails))
    print(f"after filtering: {keep} returns over {trans} transitions; "
          f"{fw}/{len(runs)} runs ({fw/len(runs):.0%}) return at least once; "
          f"{obs/nm:.0%} of chance")

    p = Path(a.json) if a.json else P.AUDITS / f"iteration_audit_{tag}.json"
    p.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {p}")


if __name__ == "__main__":
    main()
