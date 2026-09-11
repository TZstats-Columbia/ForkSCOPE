#!/usr/bin/env python3
"""An atlas of the forks and their options, built to be read for insight.

The flow view answers "what did runs do". This answers "which decisions are
worth arguing about", which is a different question and needs different
pictures. Four panels, each chosen because it separates things the tables run
together:

  A  THE FAN. Every node ranked by coverage on a log axis. The claim in
     GARDEN.md -- five decisions almost everyone faces, 289 almost nobody --
     is one line here, and the shape (a short shoulder then a cliff) is the
     finding.

  B  THE MAP. Coverage against effective number of options. This is the panel
     that matters. A fork can be universal and settled (a convention: everyone
     does it, everyone does it the same way) or universal and split (a live
     researcher degree of freedom). Those are opposite situations and every
     summary statistic in the project so far reports them in the same column.
     Effective options is 1/HHI, which reads as "how many options this fork
     behaves like" -- a 95/5 split scores 1.1, not 2.

  C  THE SPECTRUM. For the highest-coverage forks, the option shares sorted
     descending, with the singleton tail marked. Distinguishes "one modal
     choice plus noise" from "genuinely divided", which panel B compresses to a
     single number.

  D  WHERE DISAGREEMENT LIVES. Effective options per DSLC stage. If the
     lifecycle has a contested phase, it shows here.

Everything is computed on the merged garden nodes, so the sibling under-merges
found in GARDEN.md are already collapsed. Forks reached by fewer than MIN_RUNS
runs are excluded from B, C and D: concentration measured on four runs is not a
measurement, and including them would fill the contested quadrant with noise.

Usage:
    python3 scripts/fork_atlas.py --corpus ai
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                              # noqa: E402
import vocab                                                   # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
OUT = P.ANALYSIS

MIN_RUNS = 10
STAGES = ["problem_formulation", "data_collection", "data_cleaning",
          "eda", "modeling", "communication"]
SCOL = {"problem_formulation": "#8c6d31", "data_collection": "#7b9e5b",
        "data_cleaning": "#2f6fa8", "eda": "#c98a2b",
        "modeling": "#a3401f", "communication": "#6b4d8f"}
W = 1180


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def clip(t, n):
    if len(t) <= n:
        return t
    cut = t[:n].rsplit(" ", 1)[0]
    return (cut if len(cut) > n * .6 else t[:n]).rstrip(",;/ ") + "…"


def load(tag):
    gm = json.loads((OUT / f"garden_{tag}.json").read_text(encoding="utf-8"))
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
    stg = {x["fork"]: x.get("stage") for x in gm["nodes_detail"]}
    pos = {x["fork"]: x.get("position") for x in gm["nodes_detail"]}

    # Effective options comes from vocab.fork_stats, which gives each analysis
    # exactly one vote per fork -- its modal option there. Summing run-set sizes
    # per option, as this did, counts an analysis once per option it holds, and
    # 86% of analyses hold two somewhere. `eff_all` additionally counts "did not
    # reach" as a level, which is what makes it the pivotal criterion.
    st = vocab.fork_stats(d, len(runs))

    nodes = []
    for f, om in opts.items():
        s = st.get(f, {})
        rs = set().union(*om.values())
        n = len(rs)
        counts = sorted((len(v) for v in om.values()), reverse=True)
        nodes.append({
            "fork": f, "runs": s.get("reach", n),
            "coverage": s.get("coverage", n / len(runs)),
            "options": len(om), "counts": counts,
            "modal_share": s.get("modal_share", counts[0] / n if n else 0),
            "eff": s.get("eff_reached", 0.0),
            "eff_all": s.get("eff_all", 0.0),
            "singletons": sum(1 for c in counts if c == 1),
            "stage": stg.get(f), "position": pos.get(f, 0),
        })
    nodes.sort(key=lambda x: -x["coverage"])
    return nodes, len(runs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    nodes, N = load(tag)
    meas = [x for x in nodes if x["runs"] >= MIN_RUNS]

    H = 1660
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
         f"viewBox='0 0 {W} {H}' font-family='ui-sans-serif,system-ui' "
         f"font-size='11'><rect width='{W}' height='{H}' fill='#fff'/>",
         "<style>.t{fill:#222;font-size:14px;font-weight:600}.d{fill:#666}"
         ".s{fill:#999;font-size:10px}.ax{stroke:#ccc}.gr{stroke:#f0f0f0}"
         ".lb{fill:#444;font-size:9.5px}</style>"]

    # ================= A : the fan =========================================
    X0, Y0, PW, PH = 62, 74, W - 320, 200
    s.append(f"<text x='40' y='34' class='t'>A &#183; The fan</text>")
    s.append(f"<text x='40' y='52' class='d'>all {len(nodes)} garden nodes "
             f"ranked by coverage. Log axis; the cliff is the point.</text>")
    mx = max(x["coverage"] for x in nodes)

    def fy(c):
        lo = math.log10(1 / N)
        return Y0 + PH - (math.log10(max(c, 1 / N)) - lo) / (0 - lo) * PH
    for gv in (1.0, 0.5, 0.25, 0.1, 0.05, 0.02, 1 / N):
        y = fy(gv)
        s.append(f"<line class='gr' x1='{X0}' y1='{y:.1f}' x2='{X0+PW}' "
                 f"y2='{y:.1f}'/>")
        s.append(f"<text x='{X0-6}' y='{y+3:.1f}' text-anchor='end' "
                 f"class='s'>{gv:.0%}</text>")
    for i, x in enumerate(nodes):
        px = X0 + PW * i / max(1, len(nodes) - 1)
        col = SCOL.get(x["stage"], "#999")
        s.append(f"<line x1='{px:.2f}' y1='{fy(x['coverage']):.1f}' "
                 f"x2='{px:.2f}' y2='{Y0+PH}' stroke='{col}' "
                 f"stroke-width='1.6' opacity='.55'/>")
    n_univ = sum(1 for x in nodes if x["coverage"] >= .6)
    n_rare = sum(1 for x in nodes if x["coverage"] < .05)
    xr = X0 + PW * (len(nodes) - n_rare) / len(nodes)
    s.append(f"<line class='ax' x1='{xr:.1f}' y1='{Y0}' x2='{xr:.1f}' "
             f"y2='{Y0+PH}' stroke-dasharray='3 3'/>")
    s.append(f"<text x='{xr+6:.1f}' y='{Y0+16}' class='lb'>&#8592; {n_rare} "
             f"nodes below 5% coverage ({n_rare/len(nodes):.0%} of the "
             f"garden)</text>")
    s.append(f"<text x='{X0+4}' y='{Y0-8}' class='lb'>{n_univ} nodes at "
             f"&#8805;60%</text>")
    # the head of the curve is four bars wide and any label placed on it
    # overlaps the next three; list them in the dead space past the cliff
    ax, ay = xr + 12, Y0 + 44
    s.append(f"<text x='{ax}' y='{ay}' class='lb' font-weight='600'>"
             f"the {n_univ} nodes at &#8805;60% coverage</text>")
    for k, x in enumerate(nodes[:n_univ]):
        ay += 15
        px = X0 + PW * k / max(1, len(nodes) - 1)
        s.append(f"<text x='{ax}' y='{ay}' class='lb'>"
                 f"{x['coverage']:.0%} &#183; {esc(clip(x['fork'], 52))}</text>")
        s.append(f"<line x1='{px:.1f}' y1='{fy(x['coverage']):.1f}' "
                 f"x2='{ax-4}' y2='{ay-3}' stroke='#ddd' stroke-width='.6'/>")
    s.append(f"<text x='{X0}' y='{Y0+PH+16}' class='s'>nodes, ranked</text>")
    lx, ly = X0 + PW + 26, Y0 + 6
    for st in STAGES:
        s.append(f"<rect x='{lx}' y='{ly-8}' width='9' height='9' "
                 f"fill='{SCOL[st]}'/>")
        s.append(f"<text x='{lx+14}' y='{ly}' class='s'>"
                 f"{st.replace('_',' ')}</text>")
        ly += 16

    # ================= B : the map =========================================
    BY = 340
    s.append(f"<text x='40' y='{BY}' class='t'>B &#183; Convention or live "
             f"disagreement?</text>")
    s.append(f"<text x='40' y='{BY+18}' class='d'>coverage &#215; effective "
             f"number of options (1/HHI) for the {len(meas)} nodes reached by "
             f"&#8805; {MIN_RUNS} runs. Circle area = options recorded.</text>")
    MX0, MY0, MW, MH = 62, BY + 42, W - 330, 300
    emax = max(x["eff"] for x in meas) * 1.08

    def mx_(c):
        return MX0 + (c - 0) / 1.0 * MW

    def my_(e):
        return MY0 + MH - (e / emax) * MH
    for gv in (0, .25, .5, .75, 1.0):
        s.append(f"<line class='gr' x1='{mx_(gv):.1f}' y1='{MY0}' "
                 f"x2='{mx_(gv):.1f}' y2='{MY0+MH}'/>")
        s.append(f"<text x='{mx_(gv):.1f}' y='{MY0+MH+16}' class='s' "
                 f"text-anchor='middle'>{gv:.0%}</text>")
    for gv in range(0, int(emax) + 1, 2):
        s.append(f"<line class='gr' x1='{MX0}' y1='{my_(gv):.1f}' "
                 f"x2='{MX0+MW}' y2='{my_(gv):.1f}'/>")
        s.append(f"<text x='{MX0-6}' y='{my_(gv)+3:.1f}' class='s' "
                 f"text-anchor='end'>{gv}</text>")
    s.append(f"<line class='ax' x1='{mx_(.5):.1f}' y1='{MY0}' "
             f"x2='{mx_(.5):.1f}' y2='{MY0+MH}' stroke-dasharray='4 4'/>")
    s.append(f"<line class='ax' x1='{MX0}' y1='{my_(3):.1f}' "
             f"x2='{MX0+MW}' y2='{my_(3):.1f}' stroke-dasharray='4 4'/>")
    s.append(f"<text x='{mx_(.52):.1f}' y='{MY0+14}' class='lb' "
             f"fill='#a3401f'>live degree of freedom &#8212; faced by most, "
             f"settled by none</text>")
    s.append(f"<text x='{mx_(.52):.1f}' y='{MY0+MH-8:.1f}' class='lb'>"
             f"convention &#8212; faced by most, everyone agrees</text>")
    s.append(f"<text x='{MX0+6}' y='{MY0+14}' class='lb'>idiosyncratic "
             f"&#8212; few reach it, those who do disagree</text>")
    for x in sorted(meas, key=lambda z: -z["options"]):
        r = 2.2 + 1.9 * math.sqrt(x["options"])
        col = SCOL.get(x["stage"], "#999")
        s.append(f"<circle cx='{mx_(x['coverage']):.1f}' "
                 f"cy='{my_(x['eff']):.1f}' r='{r:.1f}' fill='{col}' "
                 f"opacity='.42' stroke='{col}' stroke-width='.8'><title>"
                 f"{esc(x['fork'])}&#10;{x['runs']} runs, {x['options']} "
                 f"options&#10;effective {x['eff']:.1f}, modal share "
                 f"{x['modal_share']:.2f}</title></circle>")
    notable = sorted(meas, key=lambda z: -(z["eff"] * z["coverage"]))[:6]
    # de-collide labels vertically: two near-identical forks sit almost on top
    # of each other at coverage ~0.5 and their labels overprint
    placed = []
    for x in sorted(notable, key=lambda z: my_(z["eff"])):
        ly_ = my_(x["eff"]) + 3
        while any(abs(ly_ - q) < 12 for q in placed):
            ly_ += 12
        placed.append(ly_)
        lx_ = mx_(x["coverage"]) + 9
        s.append(f"<line x1='{mx_(x['coverage']):.1f}' "
                 f"y1='{my_(x['eff']):.1f}' x2='{lx_-3:.1f}' y2='{ly_-3:.1f}' "
                 f"stroke='#ccc' stroke-width='.6'/>")
        s.append(f"<text x='{lx_:.1f}' y='{ly_:.1f}' class='lb'>"
                 f"{esc(clip(x['fork'], 40))}</text>")
    s.append(f"<text x='{MX0+MW/2}' y='{MY0+MH+34}' class='s' "
             f"text-anchor='middle'>coverage (share of {N} runs reaching "
             f"the fork)</text>")
    s.append(f"<text transform='translate({MX0-40},{MY0+MH/2}) rotate(-90)' "
             f"class='s' text-anchor='middle'>effective options (1/HHI)</text>")

    # ================= C : the spectrum ====================================
    CY = 770
    s.append(f"<text x='40' y='{CY}' class='t'>C &#183; How each of the top "
             f"forks divides</text>")
    s.append(f"<text x='40' y='{CY+18}' class='d'>option shares, largest "
             f"first. Grey = the singleton tail (one run each) &#8212; the "
             f"private variation the clustering was built to keep.</text>")
    top = meas[:14]
    y = CY + 40
    BX, BW2 = 470, 470
    for x in top:
        s.append(f"<text x='40' y='{y+9}' class='d'>"
                 f"{esc(clip(x['fork'], 62))}</text>")
        cx = BX
        for k, c in enumerate(x["counts"]):
            w = BW2 * c / sum(x["counts"])
            single = c == 1
            col = "#d8d8d8" if single else SCOL.get(x["stage"], "#888")
            op = .30 if single else max(.30, .95 - k * .1)
            s.append(f"<rect x='{cx:.2f}' y='{y}' width='{max(w-0.4,0.3):.2f}' "
                     f"height='12' fill='{col}' opacity='{op:.2f}'/>")
            cx += w
        s.append(f"<text x='{BX+BW2+8}' y='{y+10}' class='s'>"
                 f"{x['runs']} runs &#183; {x['options']} opts &#183; "
                 f"eff {x['eff']:.1f} &#183; {x['singletons']} singletons"
                 f"</text>")
        y += 19

    # ================= D : where disagreement lives ========================
    DY = 1130
    s.append(f"<text x='40' y='{DY}' class='t'>D &#183; Where disagreement "
             f"lives</text>")
    s.append(f"<text x='40' y='{DY+18}' class='d'>every measurable node, "
             f"placed by effective options, grouped by DSLC stage. Diamond = "
             f"stage median.</text>")
    DX0, DY0, DW, DH = 190, DY + 40, W - 300, 300
    rowh = DH / len(STAGES)
    for i, st in enumerate(STAGES):
        yy = DY0 + rowh * (i + .5)
        got = [x for x in meas if x["stage"] == st]
        s.append(f"<line class='gr' x1='{DX0}' y1='{yy:.1f}' "
                 f"x2='{DX0+DW}' y2='{yy:.1f}'/>")
        s.append(f"<text x='{DX0-10}' y='{yy+4:.1f}' text-anchor='end' "
                 f"class='d'>{st.replace('_',' ')}</text>")
        s.append(f"<text x='{DX0+DW+8}' y='{yy+4:.1f}' class='s'>"
                 f"n={len(got)}</text>")
        for x in got:
            px = DX0 + (x["eff"] / emax) * DW
            s.append(f"<circle cx='{px:.1f}' cy='{yy:.1f}' r='4.5' "
                     f"fill='{SCOL[st]}' opacity='.4'><title>"
                     f"{esc(x['fork'])}&#10;eff {x['eff']:.1f}</title></circle>")
        if got:
            med = sorted(z["eff"] for z in got)[len(got) // 2]
            px = DX0 + (med / emax) * DW
            s.append(f"<path d='M{px:.1f},{yy-8} L{px+6:.1f},{yy:.1f} "
                     f"L{px:.1f},{yy+8} L{px-6:.1f},{yy:.1f} Z' "
                     f"fill='{SCOL[st]}'/>")
    for gv in range(0, int(emax) + 1, 5):
        px = DX0 + (gv / emax) * DW
        s.append(f"<text x='{px:.1f}' y='{DY0+DH+4}' class='s' "
                 f"text-anchor='middle'>{gv}</text>")
    s.append(f"<text x='{DX0+DW/2}' y='{DY0+DH+22}' class='s' "
             f"text-anchor='middle'>effective options (1/HHI)</text>")
    s.append("</svg>")

    p = P.FIGURES / "fork_atlas.svg"
    p.write_text("\n".join(s), encoding="utf-8")

    # ---- the numbers the panels are drawn from -----------------------------
    print(f"FORK ATLAS - {tag}")
    print(f"{len(nodes)} nodes, {len(meas)} measurable (>= {MIN_RUNS} runs), "
          f"{N} runs\n")
    live = [x for x in meas if x["coverage"] >= .5 and x["eff"] >= 3]
    conv = [x for x in meas if x["coverage"] >= .5 and x["eff"] < 3]
    idio = [x for x in meas if x["coverage"] < .5 and x["eff"] >= 3]
    print(f"QUADRANTS  (coverage 50%, effective options 3)")
    print(f"  live degree of freedom   {len(live):>3}")
    print(f"  convention               {len(conv):>3}")
    print(f"  idiosyncratic            {len(idio):>3}")
    print(f"  rare and settled         {len(meas)-len(live)-len(conv)-len(idio):>3}")
    print(f"\nLIVE DEGREES OF FREEDOM  (faced by most runs, settled by none)")
    print(f"  {'cov':>5}{'runs':>6}{'opts':>6}{'eff':>7}{'modal':>7}  fork")
    for x in sorted(live, key=lambda z: -z["eff"]):
        print(f"  {x['coverage']:>5.2f}{x['runs']:>6}{x['options']:>6}"
              f"{x['eff']:>7.1f}{x['modal_share']:>7.2f}  {x['fork'][:52]}")
    print(f"\nCONVENTIONS  (faced by most runs, everyone agrees)")
    for x in sorted(conv, key=lambda z: z["eff"]):
        print(f"  {x['coverage']:>5.2f}{x['runs']:>6}{x['options']:>6}"
              f"{x['eff']:>7.1f}{x['modal_share']:>7.2f}  {x['fork'][:52]}")
    print(f"\nBY STAGE  (median effective options among measurable nodes)")
    for st in STAGES:
        got = sorted(x["eff"] for x in meas if x["stage"] == st)
        if got:
            print(f"  {st:<22}{len(got):>4} nodes   median "
                  f"{got[len(got)//2]:>5.1f}   max {got[-1]:>5.1f}")
    print(f"\n-> {p}")


if __name__ == "__main__":
    main()
