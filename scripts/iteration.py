#!/usr/bin/env python3
"""How often does an analysis go back a stage, and what sends it back?

The lifecycle is drawn as a pipeline and everyone says it iterates, but the
iteration is rarely measured, because measuring it needs two things at once: a
stage label for every decision, and the order in which the decisions were
actually written. This corpus has both -- forks carry a DSLC stage (assigned by
job, blind to position, prompt 14) and every decision carries the line at which
it appears.

A **return** is a decision whose stage is earlier than the stage of the decision
before it in the script, separated by more than TIE_LINES lines. Walking each
run in written order and counting returns gives, per run: how many times it went
back, how far, and from where to where.

The **trigger** is the decision immediately preceding a return -- but as a
*rate*, not a count. A fork appearing in 200 runs precedes more returns than one
appearing in 10 whatever its content, so raw counts are a frequency table. The
rate is returns per opportunity, and it tells a different story: the largest raw
trigger is a common fork at 0.87, while the sharpest is a rarer one at 0.98.

WHAT THE FILTERS ARE FOR
------------------------
Two decisions extracted from the same line have no real order, and whichever the
sort puts second creates a return half the time. Returns spanning <= TIE_LINES
lines are dropped (4% of the raw count). `audit_iteration.py` establishes this
and five other checks, including the permutation null that says the observed
return rate is 44% of chance -- scripts are strongly forward-ordered, and the
returns are the residue, not the baseline.

TWO HONEST LIMITS, BOTH STRUCTURAL
----------------------------------
  * Writing order is not thinking order. A script is often reorganised before it
    is saved, so a clean forward script can hide iteration that happened, and a
    return can be tidying rather than rework. This measures the artifact, not
    the process, and it undercounts.
  * Stage assignment is a model judgement. It is made blind to position so it
    cannot be circular; audit check I3 confirms the labels nonetheless recover
    the pipeline order, which is evidence they carry real sequence information.

Usage:
    python3 scripts/iteration.py stages --corpus ai    # assign stages (LLM)
    python3 scripts/iteration.py run    --corpus ai    # measure iteration
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from math import log
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
OUTCOMES = P.OUTCOMES

STAGES = ["problem_formulation", "data_collection", "data_cleaning",
          "eda", "modeling", "communication"]
SHORT = ["formulation", "collection", "cleaning", "eda", "modeling", "reporting"]
RANK = {s: i for i, s in enumerate(STAGES)}
BATCH = 70
TIE_LINES = 2        # returns spanning <= this many lines are order artifacts
MIN_OPP = 15         # a fork needs this many successors for its rate to mean anything
BOOT = 4000
SEED = 20260822
STAGE_SCHEMA = {"type": "object", "required": ["assignments"]}


def load(tag):
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        cand = sorted(P.VOCAB.glob("bottom_up_*.json"))
        if not cand:
            sys.exit("no bottom_up_*.json; run cluster_up.py build first")
        p = cand[-1]
    return json.loads(p.read_text(encoding="utf-8")), p


# --------------------------------------------------------------------------
# stage assignment
# --------------------------------------------------------------------------
def assign_stages(tag):
    from llm import ask
    d, _ = load(tag)
    forks = sorted({o["fork"] for o in d["options"]})
    print(f"assigning DSLC stage to {len(forks)} forks")
    got = {}
    for k in range(0, len(forks), BATCH):
        chunk = forks[k:k + BATCH]
        want = set(range(k, k + len(chunk)))

        def check(o, want=want):
            ids = [a.get("id") for a in o.get("assignments", [])]
            missing = want - set(ids)
            if missing:
                raise ValueError(
                    f"{len(missing)} ids unassigned: {sorted(missing)[:8]}. "
                    f"Return every id exactly once.")
            bad = sorted({str(a.get("stage")) for a in o["assignments"]
                          if a.get("stage") not in RANK})
            if bad:
                raise ValueError(f"stage must be one of {STAGES}; got {bad[:5]}")

        out = ask("14_fork_stage",
                  {"forks": [{"id": k + j, "fork": f}
                             for j, f in enumerate(chunk)]},
                  schema=STAGE_SCHEMA, model="opus", run_id="fork_stage",
                  check=check)
        for a in out["assignments"]:
            i = a.get("id")
            if isinstance(i, int) and 0 <= i < len(forks):
                s = a.get("stage")
                got[forks[i]] = s if s in RANK else "modeling"
        print(f"  {min(k + BATCH, len(forks))}/{len(forks)}", flush=True)
    for f in forks:
        got.setdefault(f, "modeling")
    p = OUT / f"fork_stage_{tag}.json"
    p.write_text(json.dumps(got, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nstage mix: {dict(Counter(got.values()))}")
    print(f"-> {p}")


# --------------------------------------------------------------------------
# measurement
# --------------------------------------------------------------------------
def build_seq(d, stage):
    """run -> [(line, stage_rank, fork, decision_index)], in written order."""
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
            seq[x["run"]].append((x["line"], RANK[stage.get(f, "modeling")], f, i))
    for r in seq:
        seq[r].sort()
    return seq, dec


def outcome_check(per_run, seq):
    """Do runs that go back more often end up reporting something different?

    The outcome side is `data/outcomes/outcomes.json`, extracted from each
    report without reference to the decision vocabulary, so a correlation here
    is not the clustering marking its own homework. Rate, not count: a longer
    script has more transitions and so more chances to return.

    Observational. Runs were not assigned their iteration rate, and a persona
    brief plausibly drives both how much a run revisits and what it concludes.
    """
    if not OUTCOMES.exists():
        return []
    outc = {o["repo_id"]: o for o in
            json.loads(OUTCOMES.read_text(encoding="utf-8"))}
    rate = {r: per_run[r]["returns"] / max(1, len(seq[r]) - 1) for r in per_run}
    have = [r for r in sorted(per_run) if r in outc]
    if len(have) < 20:
        return []
    med = sorted(rate[r] for r in have)[len(have) // 2]
    hi = [r for r in have if rate[r] > med]
    lo = [r for r in have if rate[r] <= med]

    def eff(r):
        v = outc[r].get("or_scale_estimate")
        return log(v) if v and v > 0 else None

    def sup(r):
        return 1.0 if outc[r].get("conclusion") == "supported" else 0.0

    print(f"\nDOES ITERATING CHANGE THE ANSWER?  ({len(have)} runs with an "
          f"independently extracted outcome)")
    print(f"  split at the median return rate ({med:.2f} per transition): "
          f"{len(hi)} high, {len(lo)} low")
    rng = random.Random(SEED)
    rows = []
    for name, fn in (("log odds-ratio", eff), ("verdict = supported", sup)):
        A = [fn(r) for r in hi if fn(r) is not None]
        B = [fn(r) for r in lo if fn(r) is not None]
        if not A or not B:
            continue
        ma, mb = sum(A) / len(A), sum(B) / len(B)
        # bootstrap the difference; the measure is a bounded ratio, so no t-test
        dd = sorted(sum(rng.choice(A) for _ in A) / len(A) -
                    sum(rng.choice(B) for _ in B) / len(B) for _ in range(BOOT))
        lo_ci, hi_ci = dd[int(BOOT * .025)], dd[int(BOOT * .975)]
        crosses = lo_ci <= 0 <= hi_ci
        print(f"    {name:<22} high {ma:>7.3f}   low {mb:>7.3f}   "
              f"diff {ma-mb:>+7.3f}  95% CI [{lo_ci:+.3f}, {hi_ci:+.3f}]  "
              f"{'no detectable difference' if crosses else 'DIFFERENCE'}")
        rows.append({"measure": name, "high": round(ma, 4), "low": round(mb, 4),
                     "diff": round(ma - mb, 4),
                     "ci": [round(lo_ci, 4), round(hi_ci, 4)],
                     "detectable": not crosses})

    # guard: is the return rate just a proxy for script length?
    n = len(have)
    xs = [rate[r] for r in have]
    ys = [float(len(seq[r])) for r in have]
    mx, my = sum(xs) / n, sum(ys) / n
    den = ((sum((x - mx) ** 2 for x in xs) *
            sum((y - my) ** 2 for y in ys)) ** .5) or 1e-9
    rp = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / den
    print(f"    return rate vs decisions recorded: Pearson r = {rp:+.3f} "
          f"({'not ' if abs(rp) < 0.3 else ''}a length proxy)")
    return rows


def measure(tag):
    d, path = load(tag)
    sp = OUT / f"fork_stage_{tag}.json"
    if not sp.exists():
        sys.exit(f"run `iteration.py stages --corpus {tag}` first")
    stage = json.loads(sp.read_text(encoding="utf-8"))
    seq, dec = build_seq(d, stage)
    runs = sorted(seq)

    per_run, transitions, trig, opp = {}, Counter(), Counter(), Counter()
    back_pairs, distances = Counter(), []
    for r in runs:
        s = seq[r]
        span = (max(x[0] for x in s) - min(x[0] for x in s)) or 1
        rets, depth = 0, 0
        for a, b in zip(s, s[1:]):
            transitions[(a[1], b[1])] += 1
            opp[a[2]] += 1
            if b[1] < a[1] and (b[0] - a[0]) > TIE_LINES:
                rets += 1
                depth += a[1] - b[1]
                back_pairs[(a[1], b[1])] += 1
                trig[a[2]] += 1
                distances.append((b[0] - a[0]) / span)
        per_run[r] = {"decisions": len(s), "returns": rets, "total_depth": depth,
                      "returns_per_decision": round(rets / len(s), 3) if s else 0}

    tot_ret = sum(v["returns"] for v in per_run.values())
    tot_dec = sum(v["decisions"] for v in per_run.values())
    trans = sum(len(seq[r]) - 1 for r in runs if len(seq[r]) > 1)
    with_ret = sum(1 for v in per_run.values() if v["returns"])
    ordered = sorted(v["returns"] for v in per_run.values())

    print(f"STAGE ITERATION - {path.name}")
    print(f"{len(runs)} runs, {tot_dec} staged decisions, {trans} transitions")
    print(f"(returns spanning <= {TIE_LINES} lines excluded as order artifacts)\n")
    print(f"  runs with at least one return   {with_ret}/{len(runs)} "
          f"({with_ret/len(runs):.0%})")
    print(f"  total returns                   {tot_ret}")
    print(f"  returns per transition          {tot_ret/trans:.3f}")
    print(f"  median returns per run          {ordered[len(runs)//2]}")
    print(f"  max returns in one run          {ordered[-1]}")
    if distances:
        dsort = sorted(distances)
        print(f"  median jump back                "
              f"{abs(dsort[len(dsort)//2]):.0%} of the script")

    print(f"\nWHERE RUNS GO BACK TO")
    print(f"  {'from':<22}{'to':<22}{'n':>6}{'share':>8}")
    for (i, j), n in back_pairs.most_common(10):
        print(f"  {STAGES[i]:<22}{STAGES[j]:<22}{n:>6}{n/tot_ret:>8.0%}")

    print(f"\nWHAT TRIGGERS A RETURN  (rate = returns per opportunity; the "
          f"corpus rate is {tot_ret/trans:.2f})")
    print(f"  {'fork':<56}{'ret':>5}{'opp':>5}{'rate':>7}")
    rows = sorted([(f, trig[f], opp[f], trig[f] / opp[f])
                   for f in opp if opp[f] >= MIN_OPP], key=lambda t: -t[3])
    for f, t, o, q in rows[:12]:
        print(f"  {f[:56]:<56}{t:>5}{o:>5}{q:>7.2f}")

    arm = {x["run"]: x["arm"] for x in dec}
    by = defaultdict(lambda: [0, 0])
    for r in runs:
        by[arm.get(r, "?")][0] += per_run[r]["returns"]
        by[arm.get(r, "?")][1] += max(1, len(seq[r]) - 1)
    print(f"\nBY ARM")
    print(f"  {'arm':<30}{'returns':>9}{'transitions':>13}{'rate':>8}")
    arm_rows = []
    for a in sorted(by):
        rt, tr = by[a]
        arm_rows.append({"arm": a, "returns": rt, "transitions": tr,
                         "rate": round(rt / tr, 3)})
        print(f"  {a:<30}{rt:>9}{tr:>13}{rt/tr:>8.3f}")

    outcome_rows = outcome_check(per_run, seq)

    print(f"\nSTAGE TRANSITION MATRIX  (rows = from, cols = to; "
          f"below the diagonal = returns)")
    print(f"  {'':<20}" + "".join(f"{s:>12}" for s in SHORT))
    for i, a in enumerate(SHORT):
        print(f"  {a:<20}" +
              "".join(f"{transitions.get((i, j), 0):>12}"
                      for j in range(len(STAGES))))

    payload = {
        "source": path.name, "tie_lines": TIE_LINES, "runs": len(runs),
        "returns": tot_ret, "decisions": tot_dec, "transitions": trans,
        "runs_with_return": with_ret,
        "return_rate": round(tot_ret / trans, 4),
        "back_pairs": [{"from": STAGES[i], "to": STAGES[j], "n": n}
                       for (i, j), n in back_pairs.most_common()],
        "triggers": [{"fork": f, "returns": t, "opportunities": o,
                      "rate": round(q, 3)} for f, t, o, q in rows],
        "by_arm": arm_rows, "by_outcome": outcome_rows,
        "matrix": {f"{STAGES[i]}->{STAGES[j]}": n
                   for (i, j), n in transitions.items()},
        "per_run": per_run,
    }
    p = OUT / f"iteration_{tag}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"\n-> {p}")
    (P.FIGURES / "iteration.svg").write_text(
        render(seq, transitions, back_pairs, rows, tot_ret, len(runs), tot_dec),
        encoding="utf-8")
    print(f"-> {P.FIGURES / 'iteration.svg'}")


# --------------------------------------------------------------------------
# figure
# --------------------------------------------------------------------------
def clip(t, n):
    """Truncate at a word boundary; a label cut mid-word reads as a typo."""
    if len(t) <= n:
        return t
    cut = t[:n].rsplit(" ", 1)[0]
    return (cut if len(cut) > n * 0.7 else t[:n]).rstrip(",;/ ") + "…"


def render(seq, transitions, back_pairs, trig_rows, tot_ret, n_runs, n_dec):
    """Three panels: the pipeline is real / it is not obeyed / what breaks it."""
    W, BINS = 900, 24
    COL = ["#8c6d31", "#7b9e5b", "#2f6fa8", "#c98a2b", "#a3401f", "#6b4d8f"]
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='1010' "
         f"viewBox='0 0 {W} 1010' font-family='ui-sans-serif,system-ui' "
         f"font-size='11'><rect width='{W}' height='1010' fill='#fff'/>",
         "<style>.t{fill:#222;font-size:13px;font-weight:600}.d{fill:#666}"
         ".s{fill:#999;font-size:10px}.ax{stroke:#ccc}</style>"]

    # ---- A: stage composition across the script --------------------------
    s.append("<text x='40' y='26' class='t'>A &#183; Pipeline histogram</text>")
    # ponytail: subtitle parked, not deleted
#     s.append(f"<text x='40' y='42' class='d'>share of decisions at each stage, "
#              f"by position within the script ({n_runs} runs, "
#              f"{n_dec:,} decisions)</text>")
    comp = [[0] * len(STAGES) for _ in range(BINS)]
    for r, pts in seq.items():
        mx = max(p[0] for p in pts) or 1
        for p in pts:
            comp[min(BINS - 1, int(BINS * p[0] / mx))][p[1]] += 1
    X0, Y0, PW, PH = 40, 56, W - 200, 190
    for b in range(BINS):
        tot = sum(comp[b]) or 1
        y = Y0
        for k in range(len(STAGES)):
            h = PH * comp[b][k] / tot
            if h > 0.4:
                s.append(f"<rect x='{X0 + b*PW/BINS:.1f}' y='{y:.1f}' "
                         f"width='{PW/BINS - 0.6:.1f}' height='{h:.1f}' "
                         f"fill='{COL[k]}' opacity='.85'/>")
            y += h
    for k, nm in enumerate(SHORT):
        s.append(f"<rect x='{X0+PW+16}' y='{Y0 + k*20:.0f}' width='10' "
                 f"height='10' fill='{COL[k]}'/>")
        s.append(f"<text x='{X0+PW+32}' y='{Y0 + k*20 + 9:.0f}' class='d'>"
                 f"{nm}</text>")
    s.append(f"<text x='{X0}' y='{Y0+PH+14}' class='s'>start of script</text>")
    s.append(f"<text x='{X0+PW}' y='{Y0+PH+14}' class='s' "
             f"text-anchor='end'>end</text>")
    # ponytail: caption parked, not deleted
#     s.append(f"<text x='{X0}' y='{Y0+PH+34}' class='s'>stages overlap "
#              f"everywhere &#8212; no bin is pure, and cleaning is still running "
#              f"in the final tenth</text>")

    # ---- B: transition matrix -------------------------------------------
    BY = 330
    s.append(f"<text x='40' y='{BY}' class='t'>B &#183; Return-order heatmap"
             f"</text>")
    # ponytail: subtitle parked, not deleted
#     s.append(f"<text x='40' y='{BY+16}' class='d'>stage-to-stage transitions; "
#              f"cells below the diagonal are returns to an earlier stage</text>")
    CS, MX0, MY0 = 46, 190, BY + 40
    mxv = max(transitions.values())
    for j, nm in enumerate(SHORT):
        s.append(f"<text x='{MX0 + j*CS + CS/2:.0f}' y='{MY0-6}' class='s' "
                 f"text-anchor='middle'>{nm[:9]}</text>")
    for i, nm in enumerate(SHORT):
        s.append(f"<text x='{MX0-8}' y='{MY0 + i*CS + CS/2 + 4:.0f}' class='d' "
                 f"text-anchor='end'>{nm}</text>")
        for j in range(len(STAGES)):
            n = transitions.get((i, j), 0)
            o = (n / mxv) ** 0.45
            fill = "#a3401f" if j < i else ("#bbb" if i == j else "#2f6fa8")
            s.append(f"<rect x='{MX0 + j*CS:.0f}' y='{MY0 + i*CS:.0f}' "
                     f"width='{CS-2}' height='{CS-2}' fill='{fill}' "
                     f"opacity='{max(0.04, o):.2f}'/>")
            if n:
                s.append(f"<text x='{MX0 + j*CS + CS/2 - 1:.0f}' "
                         f"y='{MY0 + i*CS + CS/2 + 4:.0f}' text-anchor='middle' "
                         f"font-size='10' fill='{'#fff' if o > .6 else '#444'}'>"
                         f"{n}</text>")
    s.append(f"<text x='{MX0}' y='{MY0 + 6*CS + 24}' class='d'>"
             f"{tot_ret} returns over {sum(transitions.values()):,} transitions</text>")
    ry = MY0 + 6
    s.append(f"<text x='{MX0 + 6*CS + 24}' y='{ry}' class='d' "
             f"font-weight='600'>largest returns</text>")
    for (i, j), n in back_pairs.most_common(4):
        ry += 17
        s.append(f"<text x='{MX0 + 6*CS + 24}' y='{ry}' class='s'>"
                 f"{SHORT[i]} &#8594; {SHORT[j]}  ({n}, {n/tot_ret:.0%})</text>")

    # ---- C: trigger rates -------------------------------------------------
    CY = 700
    s.append(f"<text x='40' y='{CY}' class='t'>C &#183; Return rates of specific forks"
             f"</text>")
    # ponytail: subtitle parked, not deleted
#     s.append(f"<text x='40' y='{CY+16}' class='d'>of the times this decision has "
#              f"a successor, how often is that successor a return? "
#              f"(forks with &#8805; {MIN_OPP} opportunities)</text>")
    y = CY + 44
    base = tot_ret / max(1, sum(transitions.values()))
    BX, BW = 520, 300
    s.append(f"<line class='ax' x1='{BX + BW*base:.0f}' y1='{y-16}' "
             f"x2='{BX + BW*base:.0f}' y2='{y + 9*22 - 8}' "
             f"stroke-dasharray='3 3'/>")
    s.append(f"<text x='{BX + BW*base + 4:.0f}' y='{y-20}' class='s'>corpus "
             f"rate {base:.2f}</text>")
    for f, t, o, q in trig_rows[:9]:
        s.append(f"<text x='40' y='{y+10}' class='d'>{clip(f, 62)}</text>")
        s.append(f"<rect x='{BX}' y='{y}' width='{BW*q:.0f}' height='12' "
                 f"rx='2' fill='#a3401f' opacity='.8'/>")
        s.append(f"<text x='{BX + BW*q + 6:.0f}' y='{y+10}' class='s'>"
                 f"{q:.2f}  ({t}/{o})</text>")
        y += 22
    # ponytail: caption parked, not deleted
#     s.append(f"<text x='40' y='{y+18}' class='s'>the sharpest trigger is a "
#              f"diagnostic, not a failure: after checking inter-rater "
#              f"reliability, 48 of 49 runs went straight back to cleaning</text>")
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stages", "run"])
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    (assign_stages if a.cmd == "stages" else measure)(tag)
