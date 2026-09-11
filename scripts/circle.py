#!/usr/bin/env python3
"""The corpus as a circular map: stage sectors, forks as nodes, runs as routes.

Design follows the study owner's specification, and each element earns its place:

  CIRCLE + SECTORS   stages occupy angular sectors, sized by --sector-by (see
                     sectors()). A circle has no privileged end, which suits
                     a lifecycle ITERATION.md showed is 44%-of-chance forward.
  CLOSURE EDGE       each run's last fork is linked back to its first, so a run
                     is a closed tour rather than a line with two loose ends.
                     Drawn dashed: it is a device, not an observed transition.
  AREA = TRAFFIC     node radius is sqrt(runs), so *area* is proportional to the
                     runs passing through, as asked. Radius-proportional sizing
                     would exaggerate the big exhibits by squaring them twice.
  PATHS >= MIN_LINK  only routes walked by at least MIN_LINK runs are drawn,
                     width proportional to that count. Everything rarer is left
                     as an unconnected dot, which is honest: 84% of forks are
                     reached by under 5% of runs and connecting them all is a
                     hairball that hides the structure.
  COLOUR             stages are shades of one purple; personas get the hues.
                     Structure is monochrome so that traffic carries the only
                     colour signal in the picture.

THE ANALYSIS THE COLOURING MAKES POSSIBLE
-----------------------------------------
Once routes are coloured by persona, the obvious question is whether the
colours separate -- does a persona walk a route the others do not? Every
earlier persona comparison in this project asked what arms *chose*. This asks
where they *went*, which is a different question and is not answered by any of
them.

Tested per (route, persona): observed runs against the persona's share of the
corpus, with a null that permutes persona labels across runs while holding
every run's path fixed. That null is exact for this question -- it destroys the
association between brief and route while preserving route structure, run
length, and every fork's traffic. BH-FDR over all route x persona cells.

Usage:
    python3 scripts/circle.py --corpus ai [--min-link 5]
"""
import argparse
import html
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as PATHS                                             # noqa: E402
from fork_graph import bh                                       # noqa: E402

REPO = PATHS.ROOT
V2 = PATHS.ROOT
OUT = PATHS.ANALYSIS

STAGES = ["problem_formulation", "data_collection", "data_cleaning",
          "eda", "modeling", "communication"]
# stages: one hue, six values. structure should not compete with traffic.
PURPLE = {"problem_formulation": "#efeaf6", "data_collection": "#dcd0ea",
          "data_cleaning": "#c2aedb", "eda": "#a488c8",
          "modeling": "#8163ae", "communication": "#5d4288"}
PERSONA = {"standard": "#4c78a8", "positive": "#59a14f",
           "negative": "#e15759", "confirmation_seeking": "#f28e2b",
           "strong_confirmation_seeking": "#b07aa1", "human": "#17becf"}

MIN_NODE = 2
PERM = 4000
PERM_DEEP = 80000   # escalation for screen survivors; see persona_test()
FDR = 0.05
SEED = 20260822
ITERS = 1200
R_IN, R_OUT = 120, 355
LABEL_MIN = 0.12    # badge a fork reached by at least this share of runs
SEC_FS = 17.0       # one size for every stage name
JITTER = 16.0       # radial jitter on the rare rim, scaled by rarity
# rationale-cluster fill. Distinct hues, deliberately unlike the persona set
# so a cluster is never mistaken for an arm.
RAT_COL = ['#7fb3d5', '#f5b041', '#82c99a', '#d98cb3', '#b39ddb', '#e6a17a',
           '#9fd8cb', '#c9b458', '#a0a7d4', '#e0857f', '#8fbf9f', '#cfa3d1']
SECTOR_EXP = 0.75   # 1.0 = strictly proportional; below 1 compresses the range
MIN_SECTOR = 0.075  # floor: a thinner arc cannot hold a stage name at SEC_FS


def esc(s):
    return html.escape(str(s), quote=True)


def clip(t, k):
    if len(t) <= k:
        return t
    cut = t[:k].rsplit(" ", 1)[0]
    return (cut if len(cut) > k * .6 else t[:k]).rstrip(",;/ ") + "…"


def load(tag):
    gm = json.loads((OUT / f"garden_{tag}.json").read_text(encoding="utf-8"))
    d = json.loads((PATHS.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    dec = d["decisions"]
    cmap = {}
    for head, members in gm.get("sibling_groups", {}).items():
        for m in members:
            cmap[m] = head
    fork_of = {}
    for o in d["options"]:
        node = cmap.get(o["fork"], o["fork"])
        for i in o.get("members", []):
            if i < len(dec):
                fork_of[i] = node
    seq, arm = defaultdict(list), {}
    for i, x in enumerate(dec):
        if i in fork_of:
            seq[x["run"]].append((x["line"], fork_of[i]))
            arm[x["run"]] = x["arm"]
    for r in seq:
        seq[r].sort()
    stg = {x["fork"]: x.get("stage") or "modeling" for x in gm["nodes_detail"]}
    return seq, arm, stg


def silent_by_fork(tag, seq):
    """How many runs took each fork without saying so anywhere in the report.

    A silent decision is one the code makes and the write-up never mentions --
    the residue of the S2 link, and one of the few things this pipeline finds
    that a reader of the paper could not. Joined to forks on (run, operation
    text), which is exact: the operation string in the record is the same
    string the clustering consumed. Within a corpus every silent decision
    matches; the AI-only tag misses the human ones because those runs are not
    in it, which is correct rather than a join failure.
    """
    gm = json.loads((OUT / f"garden_{tag}.json").read_text(encoding="utf-8"))
    d = json.loads((PATHS.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    dec = d["decisions"]
    cmap = {}
    for head, members in gm.get("sibling_groups", {}).items():
        for m in members:
            cmap[m] = head
    fork_of = {}
    for o in d["options"]:
        node = cmap.get(o["fork"], o["fork"])
        for i in o.get("members", []):
            if i < len(dec):
                fork_of[i] = node
    by_run = defaultdict(dict)
    for i, x in enumerate(dec):
        if i in fork_of:
            by_run[x["run"]][(x.get("text") or "").strip()] = fork_of[i]
    sil = Counter()
    for rp in sorted(PATHS.DISTILLED.glob("*/record.json")):
        run = rp.parent.name
        if run not in seq:
            continue
        rec = json.loads(rp.read_text(encoding="utf-8"))
        for s in rec.get("silent_decisions", []):
            f = by_run.get(run, {}).get((s.get("operation") or "").strip())
            if f:
                sil[f] += 1
    return sil


def fork_sizes(tag):
    """Per merged fork: distinct options, and decisions recorded."""
    gm = json.loads((OUT / f"garden_{tag}.json").read_text(encoding="utf-8"))
    d = json.loads((PATHS.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    dec = d["decisions"]
    cmap = {}
    for head, members in gm.get("sibling_groups", {}).items():
        for m in members:
            cmap[m] = head
    opt, cnt = defaultdict(set), Counter()
    for o in d["options"]:
        node = cmap.get(o["fork"], o["fork"])
        for i in o.get("members", []):
            if i < len(dec):
                opt[node].add(o["option"])
                cnt[node] += 1
    return {f: len(v) for f, v in opt.items()}, cnt


def routes(seq):
    """Consecutive fork-to-fork moves per run, plus the closing edge."""
    per_run = {}
    for r, s in seq.items():
        path = []
        for a, b in zip(s, s[1:]):
            if a[1] != b[1]:
                path.append((a[1], b[1]))
        if len(s) >= 2 and s[0][1] != s[-1][1]:
            close = (s[-1][1], s[0][1])
        else:
            close = None
        per_run[r] = (path, close)
    return per_run


def undirected(per_run, arm, closing=True):
    """edge -> {persona: runs}. Undirected: the map is about adjacency."""
    E = defaultdict(lambda: defaultdict(set))
    for r, (path, close) in per_run.items():
        moves = list(path) + ([close] if (closing and close) else [])
        for a, b in moves:
            E[tuple(sorted((a, b)))][arm.get(r, "?")].add(r)
    return E


# --------------------------------------------------------------------------
def persona_test(per_run, arm, E, min_link):
    """Does any route carry more of one persona than its corpus share?"""
    runs = sorted(per_run)
    arms = sorted({arm.get(r, "?") for r in runs})
    share = {a: sum(1 for r in runs if arm.get(r) == a) / len(runs)
             for a in arms}
    keep = {e: v for e, v in E.items()
            if sum(len(s) for s in v.values()) >= min_link}
    # observed
    obs = {}
    for e, v in keep.items():
        tot = sum(len(s) for s in v.values())
        for a in arms:
            obs[(e, a)] = (len(v.get(a, ())), tot)
    # Null: shuffle persona labels across runs; paths stay put.
    #
    # Two stages, and the reason is the failure mode that has now bitten this
    # project three times. A permutation p cannot go below 1/(B+1). With 550
    # cells the BH threshold for the smallest is 0.05/550 = 9.1e-5, well under
    # the 2.5e-4 floor of a 4,000-draw screen -- so a one-stage test returns
    # "nothing significant" by construction, whatever the data contain. B has
    # to be set against the *corrected* threshold, not against 0.05.
    rng = np.random.default_rng(SEED)
    labels = [arm.get(r, "?") for r in runs]
    edge_runs = {e: sorted(set().union(*v.values())) for e, v in keep.items()}

    def run_perms(cells, B):
        ge = Counter()
        by_edge = defaultdict(list)
        for e, a in cells:
            by_edge[e].append(a)
        for _ in range(B):
            lab = dict(zip(runs, rng.permutation(labels)))
            for e, as_ in by_edge.items():
                c = Counter(lab[r] for r in edge_runs[e])
                for a in as_:
                    if c[a] >= obs[(e, a)][0]:
                        ge[(e, a)] += 1
        return ge

    cells = [k for k, (n, tot) in obs.items() if tot > 0]
    ge = run_perms(cells, PERM)
    pv = {k: (ge[k] + 1) / (PERM + 1) for k in cells}
    nB = {k: PERM for k in cells}
    deep = [k for k in cells if pv[k] < 0.02]
    if deep:
        ge2 = run_perms(deep, PERM_DEEP)
        for k in deep:
            pv[k] = (ge[k] + ge2[k] + 1) / (PERM + PERM_DEEP + 1)
            nB[k] = PERM + PERM_DEEP

    rows = []
    for (e, a) in cells:
        n, tot = obs[(e, a)]
        rows.append({"edge": list(e), "persona": a, "n": n, "edge_total": tot,
                     "expected": round(tot * share[a], 2),
                     "p": pv[(e, a)], "perms": nB[(e, a)]})
    thr = bh([r["p"] for r in rows], FDR)
    for r in rows:
        r["enriched"] = r["p"] <= thr
    rows.sort(key=lambda r: r["p"])
    return rows, thr, share, arms


# --------------------------------------------------------------------------
def sectors(nodes, stg, weight):
    """Angular width per stage, from a chosen weight, with a floor.

    Basis matters and is not obvious. Sizing by fork count crowds data
    cleaning, whose 67 forks are each revisited far more often than
    modelling's 92. Sizing by *options* does not fix it -- modelling holds 462
    options to cleaning's 368, because the 72-option adjustment set lives
    there -- so that basis grows both stages and changes nothing about the
    crowding. Sizing by *decisions recorded* is the one that reallocates: 1,567
    in cleaning against 1,055 in modelling. It is also the most defensible
    reading of a garden, where ground goes to where the work happens.

    A floor keeps thin stages labelable: problem formulation is 0.7% of
    decisions and would otherwise be a slit.
    """
    w = {st: max(1.0, sum(weight.get(f, 0) for f in nodes
                          if stg.get(f) == st)) ** SECTOR_EXP
         for st in STAGES}
    tot = sum(w.values())
    sh = {st: w[st] / tot for st in STAGES}
    # raise anything under the floor, take it proportionally from the rest
    short = {st: MIN_SECTOR - s for st, s in sh.items() if s < MIN_SECTOR}
    if short:
        debt = sum(short.values())
        donors = {st: s for st, s in sh.items() if s >= MIN_SECTOR}
        pool = sum(donors.values())
        sh = {st: (MIN_SECTOR if st in short
                   else sh[st] - debt * sh[st] / pool) for st in STAGES}
    ang, a0 = {}, -math.pi / 2
    for st in STAGES:
        span = 2 * math.pi * sh[st]
        ang[st] = (a0 + 0.035, a0 + span - 0.035)
        a0 += span
    return ang, sh


def layout(nodes, stg, traffic, E, min_link, weight):
    """Force iteration inside angular sectors, with radius carrying traffic.

    Free force layout put the rare forks everywhere. They have no edges above
    the draw threshold, so nothing pulls them anywhere and repulsion alone
    spreads them across the whole annulus -- 289 near-private forks then occupy
    most of the picture while the handful of nodes that carry the corpus get
    squeezed into a thin inner ring.

    Two constraints fix it:

    RADIUS ENCODES TRAFFIC. Each node gets a target radius from sqrt(traffic),
    busiest at the inner edge and rarest at the outer. That is not decoration:
    the busy nodes are the ones with edges, and edges are drawn across the
    middle, so putting them innermost also shortens every ribbon. The rare tail
    packs into a thin outer band where it reads as a rim rather than as
    structure.

    STRETCH AND CENTRE PER STAGE. After each pass the angles within a stage are
    rescaled to fill the sector and re-centred on it. Without this a stage's
    nodes drift to whichever edge its neighbours pull them toward and leave
    dead space on the other side -- which is what made data cleaning look
    clustered even after its arc was widened.
    """
    rng = np.random.default_rng(SEED)
    idx = {f: i for i, f in enumerate(nodes)}
    n = len(nodes)
    ang, sh = sectors(nodes, stg, weight)
    mx_t = max(traffic.values())

    # busiest -> R_IN, rarest -> R_OUT, on a sqrt scale so the long thin tail
    # does not consume the whole radial range
    tgt = np.array([R_IN + (R_OUT - R_IN) *
                    (1.0 - math.sqrt(traffic.get(f, 1) / mx_t)) for f in nodes])
    # Jitter the rim. Hundreds of forks with near-identical traffic get
    # near-identical target radii, and the separation pass then lays them out
    # as tidy concentric arcs -- a lattice the data does not contain, which
    # reads as though the rim were ordered. The jitter scales with how rare a
    # node is, so the busy inner nodes keep their meaningful radius.
    rarity = np.array([1.0 - math.sqrt(traffic.get(f, 1) / mx_t) for f in nodes])
    tgt = tgt + rng.normal(0.0, 1.0, len(nodes)) * (JITTER * rarity)
    P = np.zeros((n, 2))
    for f, i in idx.items():
        lo, hi = ang[stg.get(f, "modeling")]
        th = rng.uniform(lo, hi)
        P[i] = [tgt[i] * math.cos(th), tgt[i] * math.sin(th)]

    W = np.zeros((n, n))
    for e, v in E.items():
        t = sum(len(s) for s in v.values())
        if t < min_link:
            continue
        a, b = e
        if a in idx and b in idx:
            W[idx[a], idx[b]] = W[idx[b], idx[a]] = t
    if W.max() > 0:
        W = W / W.max()
    rad = np.array([2.0 + 15 * math.sqrt(traffic.get(f, 1) / mx_t)
                    for f in nodes])
    by_stage = defaultdict(list)
    for f, i in idx.items():
        by_stage[stg.get(f, "modeling")].append(i)

    for it in range(ITERS):
        t = 1.0 - 0.85 * it / ITERS
        D = P[:, None, :] - P[None, :, :]
        dist = np.sqrt((D ** 2).sum(-1)) + 1e-6
        F = -(W * (dist - 40) / dist)[:, :, None] * D * 0.030
        over = np.clip((rad[:, None] + rad[None, :] + 3.5) - dist, 0, None)
        np.fill_diagonal(over, 0.0)
        F += ((over / dist)[:, :, None] * D) * 1.15
        P += F.sum(1) * t
        # radial spring toward the traffic-implied radius
        rr = np.sqrt((P ** 2).sum(1)) + 1e-9
        P += (P / rr[:, None]) * ((tgt - rr) * 0.55)[:, None]
        for _ in range(4):
            D = P[:, None, :] - P[None, :, :]
            dist = np.sqrt((D ** 2).sum(-1)) + 1e-6
            over = np.clip((rad[:, None] + rad[None, :] + 3.5) - dist, 0, None)
            np.fill_diagonal(over, 0.0)
            P += (((over / dist)[:, :, None] * D) * 0.62).sum(1)
            _clamp(P, idx, stg, ang, rad)
        if it % 25 == 24:
            _stretch(P, by_stage, ang, stg, nodes)
            _clamp(P, idx, stg, ang, rad)
    cost = float((W * np.sqrt(((P[:, None] - P[None]) ** 2).sum(-1))).sum() / 2)
    return P, idx, ang, rad, W, cost, sh


def _stretch(P, by_stage, ang, stg, nodes):
    """Rescale each stage's angles to fill its sector, centred."""
    for st, ids in by_stage.items():
        if len(ids) < 3:
            continue
        lo, hi = ang[st]
        mid = (lo + hi) / 2
        th = np.array([math.atan2(P[i, 1], P[i, 0]) for i in ids])
        # unwrap onto the sector's branch before measuring spread
        th = np.where(th < mid - math.pi, th + 2 * math.pi, th)
        th = np.where(th > mid + math.pi, th - 2 * math.pi, th)
        span = th.max() - th.min()
        want = (hi - lo) * 0.94
        if span < 1e-6:
            continue
        k = min(want / span, 2.5)          # stretch, never violently
        th2 = mid + (th - th.mean()) * k
        rr = np.sqrt((P[ids] ** 2).sum(1))
        for j, i in enumerate(ids):
            a = min(max(th2[j], lo), hi)
            P[i] = [rr[j] * math.cos(a), rr[j] * math.sin(a)]


def _clamp(P, idx, stg, ang, rad):
    for f, i in idx.items():
        x, y = P[i]
        th = math.atan2(y, x)
        rr = math.hypot(x, y)
        lo, hi = ang[stg.get(f, "modeling")]
        # unwrap to the sector's branch before clamping
        while th < lo - math.pi:
            th += 2 * math.pi
        while th > hi + math.pi:
            th -= 2 * math.pi
        th = min(max(th, lo), hi)
        rr = min(max(rr, R_IN + rad[i]), R_OUT - rad[i])
        P[i] = [rr * math.cos(th), rr * math.sin(th)]


# --------------------------------------------------------------------------
def render(nodes, P, idx, ang, rad, stg, traffic, E, per_run, arm,
           silent, rat_of, rat_name,
           sector_by, sh,
           enrich, min_link, N, cost, tag):
    CX, CY, S = 545, 545, 1090
    H = 1090
    arms = sorted({arm.get(r, "?") for r in per_run})
    s = [f"<svg id='map' width='{S}' height='{H}' viewBox='0 0 {S} {H}'>"]
    # sectors
    for st in STAGES:
        lo, hi = ang[st]
        x0, y0 = CX + (R_OUT + 26) * math.cos(lo), CY + (R_OUT + 26) * math.sin(lo)
        x1, y1 = CX + (R_OUT + 26) * math.cos(hi), CY + (R_OUT + 26) * math.sin(hi)
        xi, yi = CX + (R_IN - 16) * math.cos(hi), CY + (R_IN - 16) * math.sin(hi)
        xj, yj = CX + (R_IN - 16) * math.cos(lo), CY + (R_IN - 16) * math.sin(lo)
        big = 1 if (hi - lo) > math.pi else 0
        s.append(f"<path d='M{x0:.1f},{y0:.1f} A{R_OUT+26},{R_OUT+26} 0 "
                 f"{big},1 {x1:.1f},{y1:.1f} L{xi:.1f},{yi:.1f} "
                 f"A{R_IN-16},{R_IN-16} 0 {big},0 {xj:.1f},{yj:.1f} Z' "
                 f"fill='{PURPLE[st]}' opacity='.55'/>")
        # stage name follows the outer arc. Text on the lower half would read
        # upside down, so the path is swept the other way round for it.
        mid = (lo + hi) / 2
        up = math.sin(mid) < 0
        RL = R_OUT + (20 if up else 30)
        ax0, ay0 = CX + RL * math.cos(lo), CY + RL * math.sin(lo)
        ax1, ay1 = CX + RL * math.cos(hi), CY + RL * math.sin(hi)
        pid = f"arc-{st}"
        d = (f"M{ax0:.1f},{ay0:.1f} A{RL},{RL} 0 {big},1 {ax1:.1f},{ay1:.1f}"
             if up else
             f"M{ax1:.1f},{ay1:.1f} A{RL},{RL} 0 {big},0 {ax0:.1f},{ay0:.1f}")
        # shrink to fit the arc: problem_formulation holds 4% of the circle and
        # at a fixed size its name is silently clipped to "M FORMU"
        # One size for every stage, so the type does not imply a hierarchy the
        # data does not have. A sector too narrow for its full name drops to
        # the distinguishing word rather than shrinking: problem formulation
        # holds 4% of the circle and would otherwise render as "M FORMU".
        # 0.70em per glyph plus the 0.09em CSS letter-spacing -- omitting the
        # tracking is what left it clipped after the first fix.
        fs = SEC_FS
        label = st.replace("_", " ").upper()
        need = len(label) * 0.79 * fs
        span = (hi - lo) * 0.92                # leave the arc ends clear
        if need > RL * span:
            # an arc is longer further out, so push before abbreviating: this
            # keeps the full name wherever a modest push can hold it. Clamped
            # BELOW as well as above -- without the lower clamp an abbreviated
            # label is pulled back inside the disc, which is what turned
            # "DATA COLLECTION" into "OLLECTION" sitting over the sector fill.
            RL = min(max(need / span, RL), R_OUT + 145)
            if need > RL * span:
                label = label.split()[-1]
        ax0, ay0 = CX + RL * math.cos(lo), CY + RL * math.sin(lo)
        ax1, ay1 = CX + RL * math.cos(hi), CY + RL * math.sin(hi)
        d = (f"M{ax0:.1f},{ay0:.1f} A{RL},{RL} 0 {big},1 {ax1:.1f},{ay1:.1f}"
             if up else
             f"M{ax1:.1f},{ay1:.1f} A{RL},{RL} 0 {big},0 {ax0:.1f},{ay0:.1f}")
        s.append(f"<path id='{pid}' d='{d}' fill='none'/>")
        # inline style, not a font-size attribute: the .sec rule in the
        # stylesheet outranks a presentation attribute, which silently kept
        # every stage at 17px and clipped this one to "M FORMU"
        s.append(f"<text class='sec' style='font-size:{fs:.1f}px'>"
                 f"<textPath href='#{pid}' startOffset='50%' "
                 f"text-anchor='middle'>{label}</textPath></text>")
    enriched_cells = {(tuple(sorted(r["edge"])), r["persona"])
                      for r in enrich if r["enriched"]}
    # edges, one sub-path per persona so they can be toggled
    drawn = 0
    mxw = max((sum(len(x) for x in v.values()) for v in E.values()), default=1)
    for e, v in sorted(E.items(), key=lambda kv: sum(len(x) for x in kv[1].values())):
        tot = sum(len(x) for x in v.values())
        if tot < min_link or e[0] not in idx or e[1] not in idx:
            continue
        drawn += 1
        i, j = idx[e[0]], idx[e[1]]
        x1, y1 = CX + P[i, 0], CY + P[i, 1]
        x2, y2 = CX + P[j, 0], CY + P[j, 1]
        # bend toward the middle: chord-style, keeps the disc readable
        mxp, myp = (x1 + x2) / 2, (y1 + y2) / 2
        cx = mxp + (CX - mxp) * 0.32
        cy = myp + (CY - myp) * 0.32
        off = 0
        for a in arms:
            k = len(v.get(a, ()))
            if not k:
                continue
            w = 0.35 + 6.2 * (k / mxw)
            d = (f"M{x1:.1f},{y1:.1f} Q{cx+off:.1f},{cy+off:.1f} "
                 f"{x2:.1f},{y2:.1f}")
            hot = (tuple(sorted(e)), a) in enriched_cells
            if hot:
                # the finding should be findable in the picture, not only the
                # table underneath it
                s.append(f"<path class='ed p-{esc(a)}' d='{d}' fill='none' "
                         f"stroke='#222' stroke-width='{w+2.4:.2f}' "
                         f"opacity='.55'/>")
            s.append(f"<path class='ed p-{esc(a)}' d='{d}' "
                     f"fill='none' stroke='{PERSONA.get(a,'#888')}' "
                     f"stroke-width='{w:.2f}' "
                     f"opacity='{0.95 if hot else 0.42}'><title>"
                     f"{esc(clip(e[0],46))}  &#8596;  {esc(clip(e[1],46))}"
                     f"&#10;{a}: {k} of {tot} runs"
                     f"{'  — ENRICHED' if hot else ''}</title></path>")
            off += 3.0
    # nodes
    enr = {tuple(r["edge"]) for r in enrich if r["enriched"]}
    # Fill is the rationale cluster where one exists, otherwise the stage. The
    # outline is a second, independent channel: a dashed amber ring whose width
    # grows with how many runs took this fork WITHOUT mentioning it anywhere in
    # their write-up. Dashed so it cannot be read as part of the node, and on a
    # separate visual channel from fill because silence is orthogonal to both
    # what a decision is about and what it rests on.
    mxs = max(silent.values()) if silent else 1
    for f in sorted(nodes, key=lambda z: traffic.get(z, 0)):
        i = idx[f]
        x, y = CX + P[i, 0], CY + P[i, 1]
        cl = rat_of.get(f)
        fill = RAT_COL[cl % len(RAT_COL)] if cl is not None \
            else PURPLE[stg.get(f, "modeling")]
        nsil = silent.get(f, 0)
        s.append(f"<circle class='nd{f' rc-{cl}' if cl is not None else ''}' "
                 f"cx='{x:.1f}' cy='{y:.1f}' "
                 f"r='{rad[i]:.1f}' fill='{fill}' "
                 f"stroke='#6b4d8f' stroke-width='.7'><title>{esc(f)}&#10;"
                 f"{traffic.get(f,0)} runs&#10;{stg.get(f)}"
                 f"{f'&#10;{rat_name.get(cl)}' if cl is not None else ''}"
                 f"{f'&#10;{nsil} silent' if nsil else ''}</title></circle>")
        if nsil:
            w = 1.0 + 3.4 * (nsil / mxs) ** 0.6
            s.append(f"<circle class='sil' cx='{x:.1f}' cy='{y:.1f}' "
                     f"r='{rad[i] + 2.6 + w / 2:.1f}' fill='none' "
                     f"stroke='#c9761f' stroke-width='{w:.2f}' "
                     f"stroke-dasharray='3.2 2.4' opacity='.9'/>")
    # Fork labels run along the radius through their own node and outward, so
    # a label can never be mistaken for belonging to a neighbour. Text on the
    # left half is flipped end-for-end so it still reads left-to-right.
    # Two labels on nearby rays overlap however they are anchored, and the
    # densest part of the map is exactly where the labelled nodes are. Nudge
    # each one outward along its OWN ray until it clears the ones already
    # placed -- so a label still points at its node, which is the whole reason
    # for putting them on radii.
    # All labels sit on one ring just outside the disc and radiate outward like
    # spokes, each on the ray through its own node, with a leader line back to
    # it. Radiating from a common radius is what makes them legible: two spokes
    # a few degrees apart diverge as they extend, whereas labels started at
    # their own node radius overlap along their whole length wherever the nodes
    # are dense -- which is exactly the data-cleaning fan.
    # Labels begin at their own node and run outward along its ray. A common
    # outer ring reads more tidily but detaches the name from the thing it
    # names behind a long leader; starting at the node keeps the association
    # immediate, and running over the sector fill costs nothing because the
    # fill is a flat wash. Overlaps are pushed outward along the same ray, so
    # a label never leaves its node's radius.
    # Numbered badges, keyed to a list beside the figure. Spelling the names
    # out on the map cost far more space than they were worth: the text had to
    # be truncated to fit, it crowded the very region worth reading, and a
    # 34-character stub of a 90-character question is not much of a label. A
    # badge is small enough that many more forks can be annotated, and the
    # legend can carry the question in full.
    #
    # Numbered clockwise from twelve o'clock so the list reads in the order the
    # eye travels, not in rank order, which would scatter the numbers.
    lab = sorted((f for f in nodes if traffic.get(f, 0) >= LABEL_MIN * N),
                 key=lambda f: (math.atan2(P[idx[f], 0], -P[idx[f], 1])) % (2 * math.pi))
    key, spots = [], []
    for k, f in enumerate(lab, 1):
        i = idx[f]
        th = math.atan2(P[i, 1], P[i, 0])
        r0 = math.hypot(P[i, 0], P[i, 1]) + rad[i] + 8
        # slide outward along the node's own ray until the badge is clear of
        # the ones already placed; the busiest forks sit closest together, so
        # without this the numbers pile up exactly where they are needed
        rr = r0
        for _ in range(60):
            bx, by = CX + rr * math.cos(th), CY + rr * math.sin(th)
            if all((bx - px) ** 2 + (by - py) ** 2 > 20 ** 2
                   for px, py in spots):
                break
            rr += 6
        bx, by = CX + rr * math.cos(th), CY + rr * math.sin(th)
        spots.append((bx, by))
        if rr - r0 > 4:
            s.append(f"<line x1='{CX + r0*math.cos(th):.1f}' "
                     f"y1='{CY + r0*math.sin(th):.1f}' x2='{bx:.1f}' "
                     f"y2='{by:.1f}' stroke='#b9b0c8' stroke-width='.6'/>")
        s.append(f"<circle class='bdg' data-k='{k}' cx='{bx:.1f}' "
                 f"cy='{by:.1f}' r='8.5'/>")
        s.append(f"<text class='bn' data-k='{k}' x='{bx:.1f}' y='{by:.1f}' "
                 f"text-anchor='middle' dominant-baseline='central'>{k}</text>")
        key.append((k, f, traffic.get(f, 0), stg.get(f)))
    s.append("</svg>")

    chips = "".join(
        f"<button class='chip on' data-p='{esc(a)}' "
        f"style='--c:{PERSONA.get(a,'#888')}'>{esc(a)} "
        f"({sum(1 for r in per_run if arm.get(r)==a)})</button>" for a in arms)

    # built in a loop, not a comprehension: nested quotes and backslashes
    # inside f-string expressions are a syntax error before Python 3.12
    rows = []
    for k, f, t, st in key:
        rc = rat_of.get(f)
        attr = f" data-rc='{rc}'" if rc is not None else ""
        meta = f"{t} runs &#183; {esc((st or '').replace('_', ' '))}"
        if rc is not None:
            meta += f" &#183; {esc(rat_name.get(rc, ''))}"
        if silent.get(f):
            meta += f" &#183; <b>{silent[f]} silent</b>"
        rows.append(f"<li data-k='{k}'{attr}><span class='num'>{k}</span>"
                    f"<span class='q'>{esc(f)}</span>"
                    f"<span class='meta'>{meta}</span></li>")
    keylist = "".join(rows)

    rc_counts = Counter(rat_of.values())
    rchips = "".join(
        f"<button class='rchip on' data-rc='{c}' "
        f"style='--c:{RAT_COL[c % len(RAT_COL)]}'>"
        f"{esc(rat_name.get(c, c))} ({rc_counts[c]})</button>"
        for c in sorted(rc_counts, key=lambda c: -rc_counts[c])) if rat_of \
        else "<span class='muted'>no rationale clusters — run " \
             "<code>scripts/rationale.py</code></span>"

    er = [r for r in enrich if r["enriched"]]
    if er:
        body = "".join(
            f"<tr><td>{esc(clip(r['edge'][0],44))} &#8596; "
            f"{esc(clip(r['edge'][1],44))}</td>"
            f"<td style='color:{PERSONA.get(r['persona'],'#888')}'>"
            f"{esc(r['persona'])}</td><td class='n'>{r['n']}</td>"
            f"<td class='n'>{r['expected']}</td>"
            f"<td class='n'>{r['edge_total']}</td>"
            f"<td class='n'>{r['p']:.4f}</td></tr>" for r in er[:25])
        etab = (f"<table><thead><tr><th>route</th><th>persona</th><th>runs</th>"
                f"<th>expected</th><th>route total</th><th>p</th></tr></thead>"
                f"<tbody>{body}</tbody></table>")
    else:
        top = "".join(
            f"<tr><td>{esc(clip(r['edge'][0],44))} &#8596; "
            f"{esc(clip(r['edge'][1],44))}</td>"
            f"<td style='color:{PERSONA.get(r['persona'],'#888')}'>"
            f"{esc(r['persona'])}</td><td class='n'>{r['n']}</td>"
            f"<td class='n'>{r['expected']}</td>"
            f"<td class='n'>{r['edge_total']}</td>"
            f"<td class='n'>{r['p']:.4f}</td></tr>" for r in enrich[:8])
        etab = (f"<p class='none'><b>No route is persona-enriched.</b> "
                f"Permuting persona labels across runs, holding every path "
                f"fixed, reproduces the observed colour mix on every one of "
                f"the {len(set(tuple(r['edge']) for r in enrich))} drawn "
                f"routes. The briefs changed what runs concluded; they did not "
                f"change where runs went.</p>"
                f"<p class='muted'>Closest eight, none surviving BH-FDR "
                f"{FDR}:</p><table><thead><tr><th>route</th><th>persona</th>"
                f"<th>runs</th><th>expected</th><th>route total</th><th>p</th>"
                f"</tr></thead><tbody>{top}</tbody></table>")

    return f"""<!doctype html><meta charset="utf-8">
<title>The circle — {esc(tag)}</title>
<style>
 body{{font:13px/1.55 ui-sans-serif,system-ui,sans-serif;margin:0;
  padding:24px 30px;color:#222;background:#fff}}
 h1{{font-size:19px;margin:0 0 4px}} h2{{font-size:15px;margin:26px 0 6px}}
 .muted{{color:#777}} code{{background:#f2f2f2;padding:1px 4px;border-radius:3px}}
 .sec{{font-size:17px;fill:#5d4288;font-weight:700;letter-spacing:.09em;opacity:.9}}
 .bdg{{fill:#fff;stroke:#5d4288;stroke-width:1.3}}
 .lg{{max-width:1050px}}
 .nd.dim{{opacity:.10}} .key li.dim{{opacity:.28}}
 .rchip{{font:inherit;font-size:12px;border:1.5px solid var(--c);
  color:#333;background:var(--c);padding:2px 10px;border-radius:4px;
  cursor:pointer;margin:0 5px 5px 0;opacity:.45}}
 .rchip.on{{opacity:1}}
 .bn{{font-size:10px;font-weight:700;fill:#5d4288}}
 .bdg.hi{{fill:#5d4288}} .bn.hi{{fill:#fff}}
 .row{{display:flex;gap:22px;align-items:flex-start}}
 .key{{list-style:none;margin:0;padding:0;font-size:12px;max-width:430px;
  columns:1}}
 .key li{{display:grid;grid-template-columns:26px 1fr;gap:2px 8px;
  padding:4px 6px;border-radius:4px;border-bottom:1px solid #f0eef4}}
 .key li:hover{{background:#f4f1f8}}
 .key li.hi{{background:#ece5f5}}
 .key .num{{grid-row:span 2;font-weight:700;color:#5d4288;text-align:right;
  font-variant-numeric:tabular-nums}}
 .key .q{{color:#222;line-height:1.35}}
 .key .meta{{color:#8b8b8b;font-size:11px}}
 .key .hdr{{display:block;color:#777;font-size:11.5px;border:0;
  padding:0 0 8px 0;max-width:430px}}
 .ed{{transition:opacity .12s}} .ed.off{{display:none}}
 .nd{{cursor:default}}
 .chip{{font:inherit;border:1.5px solid var(--c);color:var(--c);
  background:#fff;padding:3px 11px;border-radius:13px;cursor:pointer;
  margin:0 5px 5px 0}}
 .chip.on{{background:var(--c);color:#fff}}
 table{{border-collapse:collapse;font-size:12px;width:100%;margin-top:6px}}
 th,td{{border-bottom:1px solid #eee;padding:3px 8px;text-align:left}}
 th{{color:#666}} td.n{{text-align:right;font-variant-numeric:tabular-nums}}
 .none{{background:#f4f1f8;border-left:3px solid #5d4288;padding:9px 13px;
  border-radius:0 4px 4px 0}}
</style>
<h1>The circle — {esc(tag)} corpus</h1>
<p class="muted">{len(nodes)} forks in six stage sectors. Arc width &#8733;
 <b>{esc(sector_by)}</b><sup>{SECTOR_EXP}</sup> recorded in that stage
 ({' · '.join(f'{st.replace("_"," ")} {sh[st]:.0%}' for st in STAGES)}),
 floored at {MIN_SECTOR:.0%} so thin stages stay labelable.
 Node <b>area</b> &#8733; runs passing through. {drawn} routes drawn
 (&#8805; {min_link} runs), width &#8733; runs, coloured by persona. Each run's
 last fork is linked back to its first, so every route is a closed tour.
 Placement is force-directed inside each sector; traffic&#215;distance
 {cost:,.0f}.</p>
<div>{chips}</div>
<p class="muted lg">Node fill = <b>rationale cluster</b> &#8212; forks grouped by
 what they rest on rather than what they are about
 (<code>scripts/rationale.py</code>: elicited assumptions &#8594; tag families
 &#8594; Jaccard + average-linkage hclust). Click a cluster to isolate it.
 A dashed amber ring marks forks taken <b>silently</b>: width &#8733; runs that
 made the choice in code and never mentioned it in the write-up.</p>
<div>{rchips}</div>
<div class="row">
  <div>{''.join(s)}</div>
  <ol class="key">
    <li class="hdr">the {len(key)} forks reached by &#8805; {LABEL_MIN:.0%} of
      runs, numbered clockwise from twelve o'clock</li>
    {keylist}
  </ol>
</div>
<h2>Do personas walk different routes?</h2>
<p class="muted">Null permutes persona labels across runs while holding every
 run's path fixed &#8212; it destroys the link between brief and route while
 preserving route structure, run length and every fork's traffic.
 BH-FDR {FDR} over {len(enrich)} route&#215;persona cells.</p>
{etab}
<script>
// isolating a rationale cluster: dim every node and list entry outside it,
// so the question "where does this kind of reasoning live?" is answered by
// looking at which sectors keep their colour
document.querySelectorAll('.rchip').forEach(c=>c.addEventListener('click',()=>{{
 const all=[...document.querySelectorAll('.rchip')];
 const wasSolo=c.classList.contains('on')&&all.every(x=>x===c||!x.classList.contains('on'));
 all.forEach(x=>x.classList.toggle('on', wasSolo ? true : x===c));
 const on=all.filter(x=>x.classList.contains('on')).map(x=>x.dataset.rc);
 const showAll=on.length===all.length;
 document.querySelectorAll('.nd').forEach(n=>{{
  const rc=[...n.classList].find(k=>k.startsWith('rc-'));
  n.classList.toggle('dim', !showAll && !(rc && on.includes(rc.slice(3))));
 }});
 document.querySelectorAll('.key li[data-k]').forEach(li=>{{
  li.classList.toggle('dim', !showAll && !on.includes(li.dataset.rc));
 }});
}}));
// hovering either the badge or its list entry lights both
function mark(k,on){{
 document.querySelectorAll('[data-k="'+k+'"]').forEach(
   e=>e.classList.toggle('hi',on));
}}
document.querySelectorAll('.key li[data-k], .bdg, .bn').forEach(e=>{{
 e.addEventListener('mouseenter',()=>mark(e.dataset.k,true));
 e.addEventListener('mouseleave',()=>mark(e.dataset.k,false));
}});
document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{{
 c.classList.toggle('on');
 const on=[...document.querySelectorAll('.chip.on')].map(x=>x.dataset.p);
 document.querySelectorAll('.ed').forEach(e=>{{
  const p=[...e.classList].find(k=>k.startsWith('p-'));
  e.classList.toggle('off', !on.includes(p.slice(2)));
 }});
}}));
</script>"""


def main():
    ap = argparse.ArgumentParser()
    # PATHS, not P -- identical to the bug in grounds.py, and for the same
    # reason: this module imports paths as PATHS and uses `P` for the numpy
    # positions matrix. A default is evaluated when the parser is built, so
    # this raised UnboundLocalError before parsing and the stage has never run.
    ap.add_argument("--corpus", default=PATHS.FINAL_TAG)
    ap.add_argument("--min-link", type=int, default=3)
    ap.add_argument("--sector-by", default="decisions",
                    choices=["forks", "options", "decisions", "traffic"],
                    help="what stage arc width is proportional to")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    seq, arm, stg = load(tag)
    N = len(seq)
    per_run = routes(seq)
    E = undirected(per_run, arm)
    traffic = Counter()
    for r, s_ in seq.items():
        for f in {x[1] for x in s_}:
            traffic[f] += 1
    nodes = sorted([f for f, c in traffic.items() if c >= MIN_NODE],
                   key=lambda f: -traffic[f])

    print(f"THE CIRCLE - {tag}")
    print(f"{len(nodes)} forks, {N} runs, min-link {a.min_link}\n")
    drawn = [(e, sum(len(x) for x in v.values())) for e, v in E.items()
             if sum(len(x) for x in v.values()) >= a.min_link
             and e[0] in set(nodes) and e[1] in set(nodes)]
    print(f"routes: {len(E)} distinct, {len(drawn)} at >= {a.min_link} runs")
    print(f"\nBUSIEST ROUTES (undirected, closure edge included)")
    for e, t in sorted(drawn, key=lambda kv: -kv[1])[:10]:
        print(f"  {t:>4}  {clip(e[0],42):<42} <-> {clip(e[1],42)}")

    silent = silent_by_fork(tag, seq)
    rat_of, rat_name = {}, {}
    rc = OUT / f"rationale_clusters_{tag}.json"
    if rc.exists():
        j = json.loads(rc.read_text(encoding="utf-8"))
        rat_of = {f: int(c) for f, c in j["assignment"].items() if f in traffic}
        rat_name = {int(c["cluster"]): c["name"] for c in j["clusters"]}
        print(f"\nRATIONALE CLUSTERS  ({len(rat_name)} groups, silhouette "
              f"{j['silhouette']})")
        for c in j["clusters"]:
            n_here = sum(1 for f in rat_of if rat_of[f] == c["cluster"])
            print(f"  [{c['cluster']}] {c['name'][:34]:<34}{n_here:>4} drawn "
                  f"forks   {c['dominant_stage']} {c['stage_share']:.0%}")
    print(f"\nSILENT DECISIONS  (chosen in code, never mentioned in the "
          f"write-up)")
    print(f"  {sum(silent.values())} over {len(silent)} forks")
    for f, n in silent.most_common(6):
        print(f"  {n:>3}  {clip(f, 66)}")

    n_opt, n_dec = fork_sizes(tag)
    weight = {"forks": {f: 1 for f in nodes},
              "options": n_opt, "decisions": n_dec, "traffic": traffic
              }[a.sector_by]
    P, idx, ang, rad, W, cost, sh = layout(nodes, stg, traffic, E,
                                           a.min_link, weight)
    print(f"\nSECTOR WIDTHS  (basis: {a.sector_by}, exponent {SECTOR_EXP}, "
          f"floor {MIN_SECTOR:.0%})")
    for st in STAGES:
        raw = sum(weight.get(f, 0) for f in nodes if stg.get(f) == st)
        print(f"  {st:<22}{raw:>7} {a.sector_by:<10}{sh[st]:>7.1%} of the "
              f"circle")
    print(f"\nplacement traffic x distance {cost:,.0f}")

    enrich, thr, share, arms = persona_test(per_run, arm, E, a.min_link)
    ne = sum(1 for r in enrich if r["enriched"])
    print(f"\nDO PERSONAS WALK DIFFERENT ROUTES?")
    print(f"  persona shares: " +
          ", ".join(f"{k} {v:.0%}" for k, v in sorted(share.items())))
    print(f"  {len(enrich)} route x persona cells; BH-FDR {FDR} -> "
          f"p <= {thr:.2g}; {ne} enriched")
    print(f"  {'obs':>4}{'exp':>7}{'tot':>5}{'p':>9}  persona / route")
    for r in enrich[:10]:
        mark = "*" if r["enriched"] else " "
        print(f" {mark}{r['n']:>4}{r['expected']:>7.1f}{r['edge_total']:>5}"
              f"{r['p']:>9.4f}  {r['persona'][:24]:<24} "
              f"{clip(r['edge'][0],26)} <-> {clip(r['edge'][1],26)}")

    doc = render(nodes, P, idx, ang, rad, stg, traffic, E, per_run, arm,
                 silent, rat_of, rat_name,
                 a.sector_by, sh,
                 enrich, a.min_link, N, cost, tag)
    p = PATHS.FIGURES / "circle.html"
    p.write_text(doc, encoding="utf-8")
    jp = OUT / f"circle_{tag}.json"
    jp.write_text(json.dumps({
        "corpus": tag, "runs": N, "nodes": len(nodes), "min_link": a.min_link,
        "routes_drawn": len(drawn), "placement_cost": cost,
        "persona_share": share, "enrichment": enrich,
        "enrichment_threshold": thr,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {p}\n-> {jp}")


if __name__ == "__main__":
    main()
