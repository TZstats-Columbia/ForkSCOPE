#!/usr/bin/env python3
"""ForkSCOPE — one viewer over the whole garden. No model calls.

THREE VIEWS, WHICH ARE THE THREE UNITS OF ANALYSIS
  The Garden      every decision fork at once, on the circle, with an
                  interactive side list; the top N are labelled
  Pivotal Forks   what makes a fork pivotal (the atlas panels) and what pivotal
                  forks do (coverage, option spectrum, Shapley)
  Corpus Viewer   one run at a time: its exon/intron map, the forks it visited,
                  and how it compares with the rest

TERMINOLOGY
The unit is a *decision fork*: a slot where an analyst must pick one
alternative. Elsewhere in the package it is called a decision point; the two
are the same object.

EXON AND INTRON ARE NOT IMPORTED FOR THIS VIEWER
`code_spans.json` types every line as `decision` or `intron` at distillation,
so % exon is `coverage.code.functional_share`. Silent decisions carry their own
line ranges and are drawn as a third colour: they are operations the code
performs and the write-up never mentions.

IT COMPUTES NO NEW STATISTIC
Coverage, effective options, stage and Shapley all come from the analysis files
that own them. A viewer that recomputed would be a second implementation to
keep in agreement with the first -- and the first thing this viewer did on its
first run was contradict a hand-written number in the README, which is the
failure mode it must not add to.

Usage:
    python3 scripts/forkscope.py [--tag TAG] [--top 10]
"""
import argparse
import html
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                  # noqa: E402

KIND = {"decision": 1, "intron": 0}
STAGES = ["problem_formulation", "data_collection", "data_cleaning",
          "eda", "modeling", "communication"]


def load(p, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:                                              # noqa: BLE001
        return default


from vocab import fork_stats, is_pivotal                           # noqa: E402
from circle import PERSONA                                         # noqa: E402


def build(tag, pivotal_eff=1.5):
    d = load(P.VOCAB / f"bottom_up_{tag}.json")
    if not d:
        sys.exit(f"no vocabulary for {tag}")
    dec = d["decisions"]
    runs_all = sorted({x["run"] for x in dec})

    fork_of, per = {}, defaultdict(
        lambda: {"opts": Counter(), "runs": set(), "arms": Counter(),
                 "lines": []})
    for o in d["options"]:
        for m in o.get("members", ()):
            if 0 <= m < len(dec):
                x = dec[m]
                fork_of[m] = o["fork"]
                f = per[o["fork"]]
                f["opts"][o["option"]] += 1
                f["runs"].add(x["run"])
                f["arms"][x["arm"]] += 1
                if x.get("line"):
                    f["lines"].append(x["line"])

    # authoritative coverage / stage / position, from the analysis that owns it
    gm = load(P.ANALYSIS / f"garden_{tag}.json", {}) or {}
    detail = {n["fork"]: n for n in gm.get("nodes_detail", [])}

    # Shapley, per payout. r2_cv travels with it: a negative one means the
    # model does not predict out of sample, and the attributions below it are
    # shares of a fit that does not generalise.
    # CONTRAST selection, not pivotal. Restricting attribution to the reported
    # forks looked like coherence and was a loss: of 15 attributions beating the
    # permutation null, NINE come from forks `eff_all > 1.5` excludes. Several
    # have eff_reached = 1.00 -- everyone who addressed the middle skin-tone
    # category did it the same way -- so the contrast carrying their signal is
    # ABSENT versus present, and eff_all scores exactly those lowest because
    # absent dominates the distribution.
    #
    # eff_all answers "is this fork contested". It is the wrong question for
    # "does this fork move the outcome", where not doing something is a choice
    # with an effect. Both files are kept; this reads the contrast one.
    shp = load(P.ANALYSIS / f"shapley_{tag}.json", {}) or {}
    shp_src = "contrast"
    # Permutation p per (payout, player) from the audit -- H2. garden.html shows
    # these and the first ForkSCOPE did not, which left the Shapley panel
    # unable to say which strengths survive a label shuffle. The audit must have
    # been run over the SAME player set, or the p-values describe a different
    # model; hence the .pivotal suffix on both.
    aud = load(P.AUDITS / f"shapley_audit_{tag}.json", {}) or {}
    perm = defaultdict(dict)
    for pay, lst in ((aud.get("H2") or {}).get("by_payout") or {}).items():
        for e in lst:
            if isinstance(e, dict) and e.get("player") is not None:
                perm[pay][e["player"]] = e.get("p")

    payouts = {}
    for name, blk in (shp.get("payouts") or {}).items():
        if isinstance(blk, dict) and isinstance(blk.get("players"), dict):
            payouts[name] = {"r2": blk.get("r2"), "r2_cv": blk.get("r2_cv"),
                             "n": blk.get("n"), "players": blk["players"],
                             "perm": perm.get(name, {})}

    # One definition, from vocab.fork_stats: each analysis votes once per fork
    # with its modal option. See the note there for why the two earlier
    # implementations both over-counted.
    stats = fork_stats(d, len(runs_all))

    forks = []
    for label, v in per.items():
        det = detail.get(label, {})
        st = stats.get(label, {})
        cov = st.get("coverage", det.get("coverage", 0.0))
        # `strength` with a bootstrap CI, not a bare number: a strength whose
        # interval straddles zero is not an attribution, and showing it without
        # the interval would read as one.
        sh = {}
        for k, b in payouts.items():
            pv = b["players"].get(label)
            if isinstance(pv, dict) and pv.get("strength") is not None:
                ci = pv.get("ci") or [None, None]
                sh[k] = {"s": round(float(pv["strength"]), 5),
                         "lo": ci[0], "hi": ci[1],
                         "p": b["perm"].get(label)}
        forks.append({
            "f": label,
            "stage": det.get("stage") or "modeling",
            "runs": st.get("reach", len(v["runs"])),
            "cov": cov,
            "eff": st.get("eff_all", 0.0),          # the pivotal criterion
            "effr": st.get("eff_reached", 0.0),     # among those who acted
            "piv": bool(is_pivotal(st, pivotal_eff)) if st else False,
            "nopt": len(v["opts"]),
            "pos": det.get("position", 0.5),
            # Per-ANALYSIS option counts plus the absent level, from the same
            # fork_stats the two eff numbers come from -- so panel C draws the
            # distribution those numbers were computed on, not a third count.
            "dist": sorted(st.get("dist", {}).items(), key=lambda kv: -kv[1])[:14],
            "absent": st.get("absent", 0),
            "opts": [[k, n] for k, n in v["opts"].most_common(14)],
            "arms": dict(v["arms"]),
            "shap": sh,
        })
    forks.sort(key=lambda r: -r["runs"])

    # Sector widths, following circle.py: a stage's arc is proportional to the
    # DECISIONS recorded in it, not to its fork count -- ground goes to where
    # the work happens. The 0.75 exponent compresses the range so cleaning does
    # not swallow the ring, and the floor keeps a thin stage labelable
    # (problem formulation is under 1% of decisions and would be a slit).
    SECTOR_EXP, MIN_SECTOR = 0.75, 0.075
    w = {}
    for st in STAGES:
        n = sum(sum(c for _, c in f["opts"]) for f in forks if f["stage"] == st)
        w[st] = max(1.0, n) ** SECTOR_EXP
    tot = sum(w.values())
    sh = {st: w[st] / tot for st in STAGES}
    short = {st: MIN_SECTOR - s for st, s in sh.items() if s < MIN_SECTOR}
    if short:
        debt = sum(short.values())
        pool = sum(s for st, s in sh.items() if s >= MIN_SECTOR)
        sh = {st: (MIN_SECTOR if st in short else s - debt * s / pool)
              for st, s in sh.items()}
    sectors, a0 = {}, 0.0
    for st in STAGES:
        sectors[st] = [round(a0, 6), round(a0 + sh[st], 6)]
        a0 += sh[st]

    # Placement: relax inside the stage sector.
    #
    # The starting position -- angle from position-in-script, radius from
    # coverage -- puts every fork where its properties say it belongs, and then
    # leaves overlapping nodes overlapping and connected nodes far apart. So
    # highways were drawn as long chords through the middle, which is a picture
    # of the layout rather than of the corpus.
    #
    # The relaxation keeps what the initial position encodes and fixes what it
    # does not: nodes repel by drawn radius so labels and discs stay legible,
    # highways attract in proportion to traffic so the routes shorten, and the
    # ANGULAR SECTOR IS A HARD CONSTRAINT -- a fork never leaves its stage,
    # because the sector is the one thing on this figure that carries meaning
    # rather than convenience. Seeded, so the same build draws the same garden.
    def relax(forks, links, iters=260, seed=20260822):
        import math
        import random
        rnd = random.Random(seed)
        C, R_IN, R_OUT = 310.0, 96.0, 258.0
        idx = {f["f"]: i for i, f in enumerate(forks)}
        ang, rad, rr = [], [], []
        for f in forks:
            s0, s1 = sectors.get(f["stage"], [0.0, 1.0])
            pad = min(0.02, (s1 - s0) * 0.12)
            a = -math.pi / 2 + 2 * math.pi * (
                s0 + pad + (s1 - s0 - 2 * pad) * (f.get("pos") or 0.5))
            ang.append(a)
            rad.append(R_IN + (R_OUT - R_IN) * (1.0 - min(1.0, f["cov"])))
            rr.append(max(2.2, math.sqrt(max(1, f["runs"])) * 0.85))
        lim = []
        for f in forks:
            s0, s1 = sectors.get(f["stage"], [0.0, 1.0])
            pad = min(0.02, (s1 - s0) * 0.12)
            lim.append((-math.pi / 2 + 2 * math.pi * (s0 + pad),
                        -math.pi / 2 + 2 * math.pi * (s1 - pad)))
        ed = [(idx[l["a"]], idx[l["b"]], l["n"]) for l in links
              if l["a"] in idx and l["b"] in idx]
        mx = max((n for _, _, n in ed), default=1)

        for it in range(iters):
            cool = 1.0 - it / iters
            fx = [0.0] * len(forks)
            fy = [0.0] * len(forks)
            px = [C + rad[i] * math.cos(ang[i]) for i in range(len(forks))]
            py = [C + rad[i] * math.sin(ang[i]) for i in range(len(forks))]
            for a_, b_, n in ed:                       # attraction along traffic
                dx, dy = px[b_] - px[a_], py[b_] - py[a_]
                w = 0.014 * (n / mx)
                fx[a_] += dx * w; fy[a_] += dy * w
                fx[b_] -= dx * w; fy[b_] -= dy * w
            for i in range(len(forks)):                # repulsion, near pairs
                for j in range(i + 1, len(forks)):
                    dx, dy = px[j] - px[i], py[j] - py[i]
                    d2 = dx * dx + dy * dy
                    want = rr[i] + rr[j] + 3.0
                    if d2 < want * want and d2 > 1e-9:
                        d = math.sqrt(d2)
                        push = (want - d) / d * 0.5
                        fx[i] -= dx * push; fy[i] -= dy * push
                        fx[j] += dx * push; fy[j] += dy * push
                    elif d2 <= 1e-9:
                        fx[i] += rnd.uniform(-1, 1); fy[i] += rnd.uniform(-1, 1)
            for i in range(len(forks)):
                nx, ny = px[i] + fx[i] * cool, py[i] + fy[i] * cool
                a = math.atan2(ny - C, nx - C)
                lo, hi = lim[i]
                while a < lo - math.pi:
                    a += 2 * math.pi
                while a > hi + math.pi:
                    a -= 2 * math.pi
                ang[i] = min(hi, max(lo, a))
                rad[i] = min(R_OUT, max(R_IN, math.hypot(nx - C, ny - C)))
        return {f["f"]: [round(C + rad[i] * math.cos(ang[i]), 1),
                         round(C + rad[i] * math.sin(ang[i]), 1)]
                for i, f in enumerate(forks)}

    # highways: consecutive fork-to-fork transitions, counted over runs.
    #
    # One entry per UNORDERED pair, carrying both directions in `dirs`. The
    # two directed chords used to draw on the same curve, so only the top one
    # could ever be clicked and the reverse direction was unreachable. A pair
    # is a highway if EITHER direction is walked by >= 3 analyses. `n` is the
    # distinct analyses on the pair in either direction -- the same unit as
    # circle.py's edge_total, so the panel header and the persona table agree
    # (an analysis that walks A->B and later B->A counts once).
    seq = defaultdict(list)
    for i, x in enumerate(dec):
        if i in fork_of:
            seq[x["run"]].append((x.get("line") or 0, fork_of[i]))
    arm = {x["run"]: x["arm"] for x in dec}
    # Persona share of the corpus, circle.py's definition: runs of that persona
    # over all runs in the vocabulary. Shipped so the panel can show expected
    # counts per ORDER with the same formula the undirected test uses -- the
    # arithmetic is the test's, not a new one. The p-value stays undirected:
    # no per-order permutation test exists and the viewer will not invent one.
    share = {p_: c / len(runs_all)
             for p_, c in Counter(arm[r] for r in runs_all).items()}
    dir_runs, walkers, visited = defaultdict(set), defaultdict(set), defaultdict(set)
    for r, items in seq.items():
        items.sort()
        chain = [f for _, f in items]
        visited[r] = set(chain)
        for a, b in zip(chain, chain[1:]):
            if a != b:
                dir_runs[(a, b)].add(r)
                walkers[frozenset((a, b))].add(r)
    hwy = []
    for pair, runs_ in walkers.items():
        x, y = sorted(pair)
        dirs = sorted(({"a": p, "b": q, "n": len(dir_runs[(p, q)]),
                        "arms": dict(Counter(arm[r] for r in dir_runs[(p, q)]))}
                       for p, q in ((x, y), (y, x))),
                      key=lambda d_: (-d_["n"], d_["a"]))
        if dirs[0]["n"] < 3:
            continue
        hwy.append({"a": dirs[0]["a"], "b": dirs[0]["b"], "n": len(runs_),
                    "dirs": dirs})
    hwy.sort(key=lambda h: (-h["n"], h["a"], h["b"]))
    hwy = hwy[:300]

    XY = relax(forks, hwy)

    # Lifecycle: where the work sits, whether analyses go back, and whether
    # inventing an option changes the answer. Read from the analyses that own
    # each question; the two SVGs are inlined so the viewer stays one file.
    it = load(P.ANALYSIS / f"iteration_{tag}.json", {}) or {}
    nv = load(P.ANALYSIS / f"novelty_{tag}.json", {}) or {}
    nov_shap = {}
    ns = load(P.ANALYSIS / f"shapley_{tag}.novelty.json", {})
    na = load(P.AUDITS / f"shapley_audit_{tag}.novelty.json", {})
    if ns and na:
        NOVK = ("how novel is this analysis (share of its decisions that are "
                "options nobody else took)?")
        pp = {}
        for pay, lst in ((na.get("H2") or {}).get("by_payout") or {}).items():
            for e in lst:
                if e.get("player") == NOVK:
                    pp[pay] = e.get("p")
        for pay, blk in (ns.get("payouts") or {}).items():
            pl = (blk.get("players") or {}).get(NOVK)
            if pl:
                nov_shap[pay] = {
                    "r2cv_with": blk.get("r2_cv"),
                    "r2cv_without": ((shp.get("payouts") or {})
                                     .get(pay, {}) or {}).get("r2_cv"),
                    "strength": pl.get("strength"), "p": pp.get(pay),
                    "levels": pl.get("levels", {}),
                    "level_n": pl.get("level_n", {})}

    def svg_inline(name):
        p = P.FIGURES / name
        if not p.exists():
            return ""
        t = p.read_text(encoding="utf-8")
        i = t.find("<svg")
        return t[i:] if i >= 0 else ""

    life = {"iteration": it, "novelty": nv, "nov_shap": nov_shap,
            "svg_iter": svg_inline("iteration.svg"),
            "svg_nov": svg_inline("novelty_curve.svg")}

    # Gate state, read from the locks rather than asserted. The About tab
    # reports an open gate as a correct state; a viewer that shows only what is
    # finished teaches its reader that everything is.
    gates = []
    for layer, name, what in (
            ("distill", "Distillation", "does extraction reproduce well "
                                        "enough to build on?"),
            ("chart", "Charting", "does the vocabulary reproduce well enough "
                                  "to report from?")):
        lk = load(P.ROOT / "locks" / f"{layer}.lock.json")
        gates.append({
            "name": name, "what": what, "settled": bool(lk),
            "note": ((lk or {}).get("decision", "")[:150] + "…") if lk else
                    "the evidence to close it does not exist yet"})

    # The persona association test, from circle.py: for each highway and each
    # persona, how many analyses of that persona used it against how many would
    # be expected from its share of the corpus, with a BH-corrected threshold.
    # Attached per edge so it can be read where the edge is, rather than as a
    # separate table nobody cross-references.
    cj = load(P.ANALYSIS / f"circle_{tag}.json", {}) or {}
    thr = cj.get("enrichment_threshold")
    enr = defaultdict(list)
    for e in (cj.get("enrichment") or []):
        ed = e.get("edge") or []
        if len(ed) == 2:
            enr[tuple(ed)].append(
                {"persona": e.get("persona"), "n": e.get("n"),
                 "tot": e.get("edge_total"), "exp": e.get("expected"),
                 "p": e.get("p")})
    for h in hwy:
        rows_ = enr.get((h["a"], h["b"])) or enr.get((h["b"], h["a"])) or []
        h["enr"] = sorted(rows_, key=lambda r: r["p"] if r["p"] is not None
                          else 1)[:6]

    # runs
    ndec = Counter(x["run"] for x in dec)
    outcomes = {o["repo_id"]: o for o in (load(P.OUTCOMES, []) or [])
                if isinstance(o, dict) and o.get("repo_id")}

    rows = []
    for rd in sorted(P.DISTILLED.glob("*/")):
        rid = rd.name
        rec = load(rd / "record.json")
        if not rec:
            continue
        cs = load(rd / "code_spans.json", {}) or {}
        cov = ((rec.get("coverage") or {}).get("code") or {})
        # `lines` is a LIST OF RANGES, not a range: a span may be disjoint --
        # a decision whose lines are separated by lines belonging to nothing.
        # Treating it as a single pair drops every span and draws an empty map,
        # which is how this shipped until someone looked at the picture.
        spans = []
        for s in cs.get("spans", []):
            k = KIND.get(s.get("kind"), 0)
            for ln in (s.get("lines") or []):
                if isinstance(ln, list) and len(ln) == 2:
                    spans.append([ln[0], ln[1], k])
        silent = []
        for sd in (rec.get("silent_decisions") or []):
            for ln in (sd.get("lines") or []):
                if isinstance(ln, list) and len(ln) == 2:
                    silent.append([ln[0], ln[1]])
        oc = outcomes.get(rid, {})
        rows.append({
            "id": rid, "arm": arm.get(rid) or rec.get("arm") or "?",
            "lines": cov.get("n_lines") or cs.get("n_lines") or 0,
            "exon": round(float(cov.get("functional_share") or 0), 4),
            "dec": ndec.get(rid, 0), "silent": len(rec.get("silent_decisions") or []),
            "est": oc.get("or_scale_estimate"), "concl": oc.get("conclusion") or "",
            "spans": spans, "sil": silent,
            "forks": sorted(visited.get(rid, ())),
        })
    return (d, forks, hwy, rows, runs_all, payouts, shp_src, sectors, thr, XY,
            life, gates, share)


PAGE = r"""<!doctype html><meta charset="utf-8">
<title>ForkSCOPE — {study}</title>
<style>
:root{{--bg:#fbfaf7;--ink:#1d2021;--mut:#6b7280;--line:#e3e0d8;--ac:#2f6f4e;
 --warn:#b45309;--card:#fff;--exon:#2f5fd0;--intron:#c9c5bc;--sil:#e08a3c}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
 font:13.5px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
header{{padding:16px 22px 0}} h1{{margin:0;font-size:18px}}
.sub{{color:var(--mut);font-size:12.5px;margin-top:2px}}
nav{{display:flex;gap:2px;padding:12px 22px 0;border-bottom:1px solid var(--line)}}
nav button{{border:1px solid var(--line);border-bottom:none;background:#f1efe9;
 padding:7px 14px;font:inherit;cursor:pointer;border-radius:5px 5px 0 0;color:var(--mut)}}
nav button[aria-selected=true]{{background:var(--card);color:var(--ink);font-weight:600}}
main{{padding:16px 22px 60px}}
.split{{display:grid;grid-template-columns:1fr 400px;gap:18px;align-items:start}}
@media(max-width:1100px){{.split{{grid-template-columns:1fr}}}}
.bar{{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:10px}}
input,select{{font:inherit;padding:5px 8px;border:1px solid var(--line);
 border-radius:5px;background:#fff}}
label{{color:var(--mut);font-size:12px}}
/* Persona toggles. A select allows one persona; the interesting comparisons are
   between two or three of them, so these are checkboxes and the filter is a
   union. Rendered from the corpus's own arms, not a fixed five -- this corpus
   pools the human teams in as a sixth. */
.atogs{{display:inline-flex;flex-wrap:wrap;gap:2px 10px;align-items:center;
 color:var(--mut);font-size:12px}}
.atog{{display:inline-flex;align-items:center;gap:4px;white-space:nowrap;
 cursor:pointer;padding:1px 7px 1px 5px;border:1px solid var(--line);
 border-radius:11px;background:var(--card)}}
.atog input{{cursor:pointer;accent-color:var(--pc);margin:0}}
/* A ticked character takes its own colour, the same hue circle.py draws its
   routes in, so the toggle and the ring agree on who is who. */
.atog:has(input:checked){{border-color:var(--pc);background:color-mix(in srgb,
 var(--pc) 12%, transparent);color:var(--pc);font-weight:600}}
#armall{{border:1px solid var(--line);background:#f4f2ec;border-radius:5px;
 padding:2px 8px;cursor:pointer;font:inherit;font-size:11.5px}}
table{{border-collapse:collapse;width:100%;background:var(--card)}}
th,td{{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);font-size:12.5px}}
th{{cursor:pointer;user-select:none;color:var(--mut);font-weight:600;position:sticky;
 top:0;background:#f6f4ef;white-space:nowrap}}
td.n,th.n{{text-align:right;font-variant-numeric:tabular-nums}}
.wrap{{max-height:62vh;overflow:auto;border:1px solid var(--line);border-radius:6px}}
.pill{{display:inline-block;padding:1px 6px;border-radius:9px;font-size:10.5px;
 background:#eef2ee;color:#33553f}}
.muted{{color:var(--mut)}} .note{{background:#fffdf5;border:1px solid #ecdfae;
 border-radius:6px;padding:8px 11px;font-size:12.5px;color:#6b5a2a;margin-bottom:12px}}
tr.sel{{background:#eef5f0}} tr:hover{{background:#f7f6f2;cursor:pointer}}
svg{{max-width:100%}} .cnt{{color:var(--mut);font-size:12px;margin:6px 0}}
/* Width alone lets a wide column push the ring past the fold, so cap its height
   against the viewport too. --chrome is measured at runtime by fitCircle rather
   than fixed here: the title and tag line wrap by window width, font size and
   corpus tag, so no single constant is right everywhere. The fallback only has
   to be sane for the case where that never runs. dvh, not vh, so mobile browser
   chrome does not eat the bottom of the ring. */
#circle{{max-height:calc(100dvh - var(--chrome,150px));height:auto}}
/* The ring is height-capped, so on a wide window its column is much wider than
   the ring itself. That leftover is where a selected fork's detail goes, rather
   than over the top of everything as a modal. `auto` lets the ring keep its own
   width and the detail take what is left; below the split's own breakpoint it
   stacks under the ring instead. */
/* The ring track is the ring's own height cap, not `auto`. Under `auto` the track
   takes the ring's *preferred* width while the ring renders at the smaller
   height-capped size, stranding the difference as blank inside the ring's column
   -- 88px of it on a 1920x1080 window. Pinning the track to the same expression
   that caps the ring means the detail absorbs everything left over.
   The floor scales with the window: a fixed one wide enough to be generous at
   1920 crushes the ring to 277px at 1200, where the whole left column is 738. */
.gmain{{display:grid;
 grid-template-columns:minmax(0,calc(100dvh - var(--chrome,150px)))
                      minmax(clamp(340px,30vw,520px),1fr);
 gap:16px;align-items:start}}
@media(max-width:1100px){{.gmain{{grid-template-columns:1fr}}}}
#gdetail{{border:1px solid var(--line);border-radius:9px;background:var(--card);
 padding:14px 16px;font-size:12.5px;position:sticky;top:8px;
 max-height:calc(100dvh - var(--chrome,150px));overflow:auto}}
#gdetail h2{{margin:0 0 2px;font-size:15px}}
#gdetail .hint{{color:var(--mut)}}
.chrom{{display:flex;height:11px;width:150px;border-radius:6px;overflow:hidden;
 background:#efece5;border:1px solid var(--line)}}
.chrom i{{display:block;height:100%}}
.ex{{background:var(--exon)}} .in{{background:var(--intron)}} .si{{background:var(--sil)}}
dialog{{border:1px solid var(--line);border-radius:9px;padding:0;max-width:880px;
 width:92vw;box-shadow:0 20px 60px rgba(0,0,0,.22)}}
dialog::backdrop{{background:rgba(20,20,20,.42)}}
.dlg{{padding:16px 20px 20px}} .dlg h2{{margin:0 0 2px;font-size:16px}}
.close{{float:right;border:1px solid var(--line);background:#f4f2ec;border-radius:5px;
 padding:3px 9px;cursor:pointer;font:inherit}}
.map{{width:100%;height:34px;border:1px solid var(--line);border-radius:5px;
 background:#f4f2ec;position:relative;overflow:hidden;margin:8px 0 4px}}
.map i{{position:absolute;top:50%;transform:translateY(-50%)}}
.map i.in{{height:3px}} .map i.ex{{height:20px;border-radius:2px}}
.map i.si{{height:26px;border-radius:2px;opacity:.92}}
.lg{{font-size:11.5px;color:var(--mut);margin-bottom:8px}}
.lg i{{display:inline-block;width:10px;height:10px;border-radius:2px;
 vertical-align:-1px;margin:0 4px 0 12px}}
.dtabs{{display:flex;gap:4px;margin:8px 0 2px}}
.dtab{{border:1px solid var(--line);border-radius:6px;background:#f1efe9;color:var(--mut);
 font:inherit;font-size:12px;padding:3px 9px;cursor:pointer}}
.dtab[aria-selected=true]{{background:var(--card);color:var(--ink);font-weight:600}}
.kv{{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;font-size:12.5px;margin:8px 0}}
.kv b{{color:var(--mut);font-weight:600}}
.fl{{max-height:150px;overflow:auto;border:1px solid var(--line);border-radius:5px;
 padding:6px 9px;font-size:12px;background:#fcfbf8}}
.panel h3{{margin:14px 0 4px;font-size:13.5px}}
.facts{{margin:0;padding-left:18px;font-size:12.5px;color:var(--mut)}}
.facts li{{margin:2px 0}} .facts b{{color:var(--ink);font-weight:600}}
.panel p{{margin:0 0 6px;color:var(--mut);font-size:12px}}
</style>
<header><h1>ForkSCOPE - Soccer Dataset</h1></header>
<nav>
 <button id="t0" aria-selected="true" onclick="tab(0)">The Garden</button>
 <button id="t1" aria-selected="false" onclick="tab(1)">Pivotal Forks</button>
 <button id="t2" aria-selected="false" onclick="tab(2)">Lifecycle</button>
 <button id="t3" aria-selected="false" onclick="tab(3)">Corpus Viewer</button>
</nav>
<main>

<section id="p0"><div class="split">
 <div class="gmain">
  <div>
  <svg id="circle" viewBox="0 0 620 620"></svg>
  <div class="cnt" id="gcount"></div>
  <div class="legend" style="margin-top:2px">
   <b>Sector</b> = DSLC stage, width proportional to decisions recorded in it.
   <b>Radius</b> = high coverage sits inward.
   <b>Node area</b> ∝ analyses that reached the fork; filled if it sits on a
   highway, hollow if not.
   <span style="color:#c2410c;font-weight:600">Orange chords</span> are
   <i>highways</i> = analyses that went from one fork to the other in order,
   drawn at 3 or more, thickness ∝ how many. <span style="color:#7c3aed;
   font-weight:600">Purple</span> ones carry a persona association that survives
   BH correction. Click any chord for its counts and persona test.
  </div>
  </div>
  <aside id="gdetail"><div class="hint">Click a fork on the ring, a row in the
   list, or a chord.</div></aside>
 </div>
 <div>
  <div class="bar">
   <input type="search" id="q" placeholder="filter forks…" size="18" oninput="drawG()">
   <span class="atogs">persona {armtoggles}
    <button type="button" id="armall" onclick="clearArms()">all</button></span>
   <select id="gsort" onchange="drawG()">
    <option value="runs">sort: analyses reached ↓</option>
    <option value="eff">sort: eff_all ↓</option>
    <option value="effr">sort: eff_reached ↓</option>
    <option value="shap">sort: |SHAP| ↓</option>
    <option value="nopt">sort: options recorded ↓</option>
    <option value="stage">group: lifecycle stage</option>
   </select>
  </div>
  <div class="bar">
   <label>label top <input id="topn" type="number" min="0" max="40" value="{top}"
     style="width:52px" oninput="drawG()"></label>
   <label><input type="checkbox" id="hw" onchange="drawG()"> highways only</label>
   <label><input type="checkbox" id="shf" onchange="drawG()"> has SHAP</label>
   <label>payout <select id="pay" onchange="drawG()">{payopts}</select></label>
  </div>
  <div class="wrap" style="max-height:56vh"><table id="gt"><tbody></tbody></table></div>
 </div>
</div></section>

<section id="p1" hidden>
 <div class="bar">
  <label>measure <select id="met" onchange="drawP()">
   <option value="effr">eff_reached</option>
   <option value="eff">eff_all</option>
  </select></label>
  <label>threshold &gt; <span id="efv">{peff}</span>
   <input type="range" id="ef" min="10" max="40" value="{peff10}" oninput="drawP()"></label>
  <label>coverage ≥ <span id="cvv">0%</span>
   <input type="range" id="cv" min="0" max="80" value="0" oninput="drawP()"></label>
  <label>persona <select id="parm" onchange="drawP()">
   <option value="">all</option>{arms}</select></label>
  <span class="cnt" id="pcount"></span>
 </div>
 <div class="panel">
  <h3>A · The fan</h3>
  <svg id="panA" viewBox="0 0 900 200" height="200"></svg>
  <h3>B · The map</h3>
  <svg id="panB" viewBox="0 0 900 340" height="340"></svg>
  <h3>C · The spectrum</h3>
  <svg id="panC" viewBox="0 0 900 300" height="300"></svg>
  <h3>D · Effective options by stage</h3>
  <svg id="panD" viewBox="0 0 900 210" height="210"></svg>
  <h3>Shapley</h3>
  <div id="shap"></div>
 </div>
</section>

<section id="p2" hidden>
 <div class="panel">
  <h3>Where the decisions are</h3>
  <div id="lstage"></div>

  <h3>Does the process go back?</h3>
  <div id="literm"></div>
  <div style="overflow-x:auto">{svg_iter}</div>

  <h3>Novelty against the reported effect</h3>
  <div style="overflow-x:auto">{svg_nov}</div>

  <h3>Novelty as an additional attribution player</h3>
  <div id="lnov"></div>
 </div>
</section>

<section id="p3" hidden>
 <div class="lg">Each run's script, line by line —
  <i class="ex"></i> exon (a decision) <i class="si"></i> silent decision
  <i class="in"></i> intron. Click a row for the full map.</div>
 <div class="bar">
  <input type="search" id="rq" placeholder="filter runs…" size="20" oninput="drawR()">
  <label>persona <select id="rarm" onchange="drawR()"><option value="">all</option>{arms}</select></label>
  <label>outcome <select id="rc" onchange="drawR()"><option value="">all</option>{concl}</select></label>
  <span class="cnt" id="rcount"></span>
 </div>
 <div class="wrap"><table id="rt"><thead><tr>
  <th onclick="sortR('id')">run</th><th onclick="sortR('arm')">persona</th>
  <th class="n" onclick="sortR('lines')">lines</th>
  <th class="n" onclick="sortR('exon')">% exon</th>
  <th>exon / intron</th>
  <th class="n" onclick="sortR('dec')">decisions</th>
  <th class="n" onclick="sortR('silent')">silent</th>
  <th class="n" onclick="sortR('est')">OR</th>
  <th onclick="sortR('concl')">conclusion</th></tr></thead><tbody></tbody></table></div>
</section>

</main>

<dialog id="dlg"><div class="dlg"></div></dialog>

<script>
const FORKS={forks}, RUNS={runs}, HWY={hwy}, PAY={pay}, STAGES={stages}, SHARE={share};
const SECT={sectors}, ENRTHR={enrthr}, XY={xy}, LIFE={life}, GATES={gates};
const HWSET=new Set(); HWY.forEach(h=>{{HWSET.add(h.a);HWSET.add(h.b);}});
const FIDX={{}}; FORKS.forEach((f,i)=>FIDX[f.f]=i);
const SC={{problem_formulation:"#7c6ee0",data_collection:"#2f8fbf",
 data_cleaning:"#2f6f4e",eda:"#c08a2e",modeling:"#c0532e",communication:"#8a4f7d"}};
const E=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({{"&":"&amp;","<":"&lt;",
 ">":"&gt;",'"':"&quot;"}})[c]);
function tab(i){{for(let k=0;k<5;k++){{const p_=document.getElementById("p"+k), t_=document.getElementById("t"+k);
  if(!p_||!t_) continue;   /* a tab with no panel or button is skipped */
  p_.hidden=k!=i;
  t_.setAttribute("aria-selected",k==i);}}
 if(i==0){{drawG();fitCircle();}} if(i==1)drawP(); if(i==2)drawL(); if(i==3)drawR();
  if(i==4&&document.getElementById("p4"))drawA();}}   /* only if an About panel exists */

/* How much page sits above the ring, measured rather than assumed -- the header
   wraps differently by width, font and corpus tag. Idempotent: the ring is below
   the chrome, so resizing the ring never moves its own top. Skipped while the
   tab is hidden, when the rect would read zero. */
function fitCircle(){{
 const c=document.getElementById("circle");
 if(!c||!c.getClientRects().length) return;
 const top=c.getBoundingClientRect().top+window.scrollY;
 document.documentElement.style.setProperty("--chrome",Math.round(top+28)+"px");}}
addEventListener("resize",fitCircle);
/* Not just window resizes: the h1 and the tag line wrap at widths that depend on
   the corpus name, and a late web font reflows both after first paint. Observing
   the two elements above the ring catches every such case, and fires once on
   observe, which is the initial measurement. */
if(window.ResizeObserver){{const ro=new ResizeObserver(fitCircle);
 ro.observe(document.querySelector("header")); ro.observe(document.querySelector("nav"));}}

/* Scroll to zoom, drag to pan -- both by moving the viewBox rather than
   transforming a group, so hit-testing, stroke widths and the click handlers
   all keep working in user units. drawG only replaces the svg's children, so
   the view survives a filter change. */
const VB=[0,0,620,620], MAXZ=12; let vb=VB.slice();
const CIRC=document.getElementById("circle");
const clampVB=(v,span)=>Math.min(Math.max(v,0),VB[2]-span);
function setVB(x,y,w){{
 vb=[clampVB(x,w),clampVB(y,w),w,w];
 CIRC.setAttribute("viewBox",vb.join(" "));
 const zoomed=w<VB[2];
 CIRC.style.cursor=zoomed?"grab":"";
 /* Only claim the touch gesture while there is somewhere to pan to, so at 1x
    a finger still scrolls the page over the ring. */
 CIRC.style.touchAction=zoomed?"none":"";}}
/* Anchored on the pointer: the point under the cursor is the one that stays. */
function zoomAt(ev,k){{
 const r=CIRC.getBoundingClientRect();
 const w=Math.min(VB[2],Math.max(VB[2]/MAXZ,vb[2]*k));
 if(Math.abs(w-vb[2])<0.01) return false;   /* already at a limit */
 const fx=(ev.clientX-r.left)/r.width, fy=(ev.clientY-r.top)/r.height;
 setVB(vb[0]+fx*(vb[2]-w), vb[1]+fy*(vb[3]-w), w); return true;}}
/* Only swallow the wheel when it actually zoomed. At full zoom-out a further
   scroll down is not ours, so the page scrolls normally instead of trapping
   the pointer over a ring that fills most of the window. */
CIRC.addEventListener("wheel",e=>{{
 if(zoomAt(e,e.deltaY>0?1.1:1/1.1)) e.preventDefault();}},{{passive:false}});

/* The ring is also 561 clickable chords and nodes, so a press only becomes a
   pan once it has travelled DEADZONE px. Under that it stays a click and the
   existing handlers fire untouched; over it, the click that follows pointerup
   is swallowed in the capture phase, so dragging never selects whatever
   happened to sit under the cursor when the drag ended. */
const DEADZONE=4; let drag=null, panned=false;
CIRC.addEventListener("pointerdown",e=>{{
 panned=false;
 if(e.button!==0||vb[2]>=VB[2]) return;     /* nothing to pan at 1x */
 drag={{x:e.clientX,y:e.clientY,vb:vb.slice(),id:e.pointerId}};}});
CIRC.addEventListener("pointermove",e=>{{
 if(!drag) return;
 const dx=e.clientX-drag.x, dy=e.clientY-drag.y;
 if(!panned&&Math.hypot(dx,dy)<DEADZONE) return;
 /* Capture only once this is definitely a drag. Capturing on pointerdown
    instead would retarget the click that follows to the svg, so the node under
    the cursor would never receive it and nothing would be selectable. */
 if(!panned){{panned=true; CIRC.setPointerCapture(drag.id);}}
 const r=CIRC.getBoundingClientRect();
 setVB(drag.vb[0]-dx*drag.vb[2]/r.width,
       drag.vb[1]-dy*drag.vb[3]/r.height, drag.vb[2]);
 CIRC.style.cursor="grabbing";   /* after setVB, which resets it to grab */}});
CIRC.addEventListener("pointerup",e=>{{
 if(drag&&CIRC.hasPointerCapture(drag.id)) CIRC.releasePointerCapture(drag.id);
 drag=null; CIRC.style.cursor=vb[2]<VB[2]?"grab":"";}});
CIRC.addEventListener("click",e=>{{
 if(panned){{e.stopPropagation(); e.preventDefault(); panned=false;}}}},true);

/* ---------- Tab 0: the circle ---------- */
let selFork=null, NUM={{}};
/* Every box ticked is the default and means the whole corpus. None ticked means
   the same thing -- there is no reading of "show me no personas" that anyone
   wants, so the empty selection falls back to everything rather than blanking
   the ring. `armsAll()` reports whether the current selection is one of those
   two cases, and the chord code below treats them identically so that
   unticking the last box changes nothing.
   A strict subset is a union: a fork survives if ANY ticked arm reached it, so
   ticking two answers "where did either of these go", not "where did both". */
function selArms(){{
 return [...document.querySelectorAll(".armchk:checked")].map(c=>c.value);}}
function armsAll(){{
 const n=document.querySelectorAll(".armchk").length;
 const k=document.querySelectorAll(".armchk:checked").length;
 return k===0||k===n;}}
function clearArms(){{
 document.querySelectorAll(".armchk").forEach(c=>c.checked=true); drawG();}}
function gfilter(){{
 const q=document.getElementById("q").value.toLowerCase().trim();
 const arms=selArms();
 const hw=document.getElementById("hw").checked;
 const sf=document.getElementById("shf").checked;
 let r=FORKS.filter(f=>(!arms.length||arms.some(a=>(f.arms[a]||0)>0))
   &&(!hw||HWSET.has(f.f))
   &&(!sf||(f.shap&&Object.keys(f.shap).length)));
 if(q)r=r.filter(f=>f.f.toLowerCase().includes(q)||
   f.opts.some(o=>o[0].toLowerCase().includes(q)));
 const k=document.getElementById("gsort").value;
 const pk=document.getElementById("pay").value;
 // Numeric keys sort DESCENDING -- biggest first is what every one of them
 // means. `stage` is not a magnitude, so it groups in lifecycle order with
 // analyses reached breaking ties inside each stage.
 if(k=="stage")return r.sort((a,b)=>
   (STAGES.indexOf(a.stage)-STAGES.indexOf(b.stage))||(b.runs-a.runs));
 const key=f=>k=="shap"?Math.abs(((f.shap||{{}})[pk]||{{}}).s||0):f[k];
 return r.sort((a,b)=>key(b)-key(a));
}}
const TAU=2*Math.PI, C=310;
function ang(f){{
 // Sectors are proportional to the decisions recorded in each stage, so a
 // stage's share of the ring is its share of the work. Within a sector the
 // fork sits at its position in the script.
 const s=SECT[f.stage]||[0,1], pad=0.02;
 return -Math.PI/2+TAU*(s[0]+pad+(s[1]-s[0]-2*pad)*(f.pos??0.5));
}}
function geom(f){{
 // Positions are relaxed in Python and shipped, so they are identical on every
 // load and do not shift when a filter changes -- a garden that rearranges
 // itself when you narrow it is unreadable.
 const p=XY[f.f];
 if(p)return p;
 const a=ang(f), R=90+165*(1-Math.min(1,f.cov));
 return [C+R*Math.cos(a),C+R*Math.sin(a)];
}}
function chord(A,B,lift){{
 // Bend TOWARD the centre in proportion to how far apart the endpoints are.
 // Bending every chord through the exact centre gives neighbouring nodes an
 // absurd bow that leaves the line nowhere near either of them; far pairs still
 // need the bow or they cut straight across the ring.
 //
 // `lift` (0 = none) bows a chord deeper still. It carries the light traffic
 // inward so it stops tracing the same arc as the highways. It MULTIPLIES the
 // distance term rather than adding to it, so a short chord between neighbours
 // is lifted a little and a long one a lot -- adding a constant would recreate
 // exactly the absurd bow the paragraph above avoids.
 // The base is clamped BEFORE the lift is applied, so a chord with lift 0
 // traces exactly the path it traced before lift existed -- the highways do not
 // move. Only the lifted chords are allowed past the old 0.85 ceiling, which is
 // what opens a gap between them and the heavy traffic on long spans, where
 // both would otherwise sit pinned at the same clamp.
 const mx=(A[0]+B[0])/2, my=(A[1]+B[1])/2;
 const d=Math.hypot(B[0]-A[0],B[1]-A[1]);
 const base=Math.min(0.85,d/380);           // 0 = straight, 1 = centre
 const t=Math.min(0.95,base*(1+(lift||0)));
 const cx=mx+(C-mx)*t, cy=my+(C-my)*t;
 return `M${{A[0].toFixed(1)}} ${{A[1].toFixed(1)}} Q${{cx.toFixed(1)}} ${{cy.toFixed(1)}} ${{B[0].toFixed(1)}} ${{B[1].toFixed(1)}}`;
}}
function arcPath(s0,s1,r,rev){{
 // `rev` draws the arc the other way round. Text on a path always runs along
 // the path, so a sector in the lower half reads upside down unless the path
 // itself is reversed -- which keeps the label on its arc instead of resorting
 // to a flat tangent line.
 const a0=-Math.PI/2+TAU*s0, a1=-Math.PI/2+TAU*s1;
 const big=(s1-s0)>0.5?1:0;
 const [p,q,sw]=rev?[a1,a0,0]:[a0,a1,1];
 return `M${{(C+r*Math.cos(p)).toFixed(1)}} ${{(C+r*Math.sin(p)).toFixed(1)}}`+
  ` A${{r}} ${{r}} 0 ${{big}} ${{sw}} ${{(C+r*Math.cos(q)).toFixed(1)}} ${{(C+r*Math.sin(q)).toFixed(1)}}`;
}}
function lowerHalf(s0,s1){{
 return Math.sin(-Math.PI/2+TAU*(s0+s1)/2)>0;   // below centre in SVG coords
}}
function drawG(){{
 const r=gfilter(), keep=new Set(r.map(f=>f.f));
 const top=+document.getElementById("topn").value||0;
 const pk=document.getElementById("pay").value;   // read here too: gfilter's
 // copy is function-scoped, and referencing it from drawG threw a ReferenceError
 // that silently killed the numbering and every click handler on this tab.
 NUM={{}}; r.forEach((f,i)=>NUM[f.f]=i+1);
 // Stage names ride their own arc. Long ones split on the underscore into two
 // stacked arcs so nothing is clipped by its sector, and lower-half sectors
 // reverse the path so the text is not upside down.
 let s=`<defs>`;
 STAGES.forEach((st,i)=>{{const sc=SECT[st]||[0,0], rev=lowerHalf(sc[0],sc[1]);
  const w=st.split("_"), R=rev?[302,287]:[287,302];
  w.forEach((_,j)=>{{s+=`<path id="arc${{i}}_${{j}}" fill="none"
   d="${{arcPath(sc[0]+0.006,sc[1]-0.006,R[j]||R[0],rev)}}"/>`;}});}});
 s+=`</defs>`;
 STAGES.forEach((st,i)=>{{const sc=SECT[st]||[0,0], rev=lowerHalf(sc[0],sc[1]);
  const a0=-Math.PI/2+TAU*sc[0];
  s+=`<line x1="${{C}}" y1="${{C}}" x2="${{(C+278*Math.cos(a0)).toFixed(1)}}"
   y2="${{(C+278*Math.sin(a0)).toFixed(1)}}" stroke="#e6e3db"/>`;
  s+=`<path d="${{arcPath(sc[0]+0.004,sc[1]-0.004,272)}}" fill="none"
   stroke="${{SC[st]}}" stroke-width="3" opacity=".5"/>`;
  st.split("_").forEach((word,j)=>{{
   s+=`<text font-size="13" font-weight="700" fill="${{SC[st]}}" letter-spacing=".2">
   <textPath href="#arc${{i}}_${{j}}" startOffset="50%" text-anchor="middle"
   >${{word}}</textPath></text>`;}});}});
 s+=`<circle cx="${{C}}" cy="${{C}}" r="88" fill="none" stroke="#e6e3db" stroke-dasharray="3 3"/>`;
 // Highways get their own colour rather than a heavier grey, so "which routes
 // does the corpus actually take" is answerable at a glance instead of by
 // comparing line weights. Nodes on no highway are drawn hollow.
 // With a persona selected, a highway is drawn at THAT persona's traversal
 // count, taken from the association test's per-persona n. Before this the
 // chords used the corpus-wide count and did not move when the persona
 // changed, so the control appeared to do nothing.
 // With personas ticked the count is summed over exactly those, and the edge
 // counts as enriched if any one of them is. Summing is right because the per
 // persona n partition the edge's traffic -- a run carries one persona.
 // A strict subset of arms filters; everything ticked is the same view as
 // nothing ticked and must render identically, or unticking the last box would
 // silently rescale every chord.
 const parms=selArms(), pf=!armsAll();
 // Draw light chords first so the heavy ones land on top of them. Before this
 // the paint order was the highway list's own, so a 3-analysis thread could sit
 // over a 50-analysis one and read as though it were the structure.
 const order=HWY.map((h,hi)=>hi).sort((x,y)=>HWY[x].n-HWY[y].n);
 order.forEach(hi=>{{const h=HWY[hi];
  if(!keep.has(h.a)||!keep.has(h.b))return;
  let n=h.n, es=null;
  if(pf){{es=(h.enr||[]).filter(e=>parms.includes(e.persona));
   n=es.reduce((t,e)=>t+(e.n||0),0); if(!n)return;}}
  const A=geom(FORKS[FIDX[h.a]]), B=geom(FORKS[FIDX[h.b]]);
  const sig=pf?es.some(e=>e.p!=null&&ENRTHR!=null&&e.p<=ENRTHR)
              :(h.enr||[]).some(e=>e.p!=null&&ENRTHR!=null&&e.p<=ENRTHR);
  // Scale the weight to how many personas are in view, so the chords stay
  // comparable instead of thickening just because more arms are ticked.
  const dv=pf?parms.length:0;
  const sw=Math.min(3.0,0.4+n/(pf?6*dv:20));
  // Separate the light traffic from the heavy by DEPTH, not just by weight.
  // Every chord used one curvature, so a hairline and a highway between nearby
  // nodes traced almost the same arc and the thin one read as fraying on the
  // thick one. `hv` is how close this chord is to the weight cap: heavy chords
  // keep exactly the old path, light ones bow further toward the centre and
  // vacate the band the highways occupy.
  const hv=Math.min(1,(sw-0.4)/2.6);
  s+=`<path d="${{chord(A,B,0.85*(1-hv))}}"
   fill="none" stroke="${{sig?"#7c3aed":"#c2410c"}}"
   stroke-width="${{sw}}"
   opacity="${{Math.min(.68,0.14+n/(pf?22*dv:70))}}" style="cursor:pointer"
   onclick="showHwy(${{hi}})"><title>${{n}} ${{pf?E(parms.join(" + "))+" ":""}}analyses on this pair${{sig?" · enriched":""}}
${{h.dirs[0].n}} →  ${{E(h.a.slice(0,50))}} → ${{E(h.b.slice(0,50))}}
${{h.dirs[1].n}} ←  the reverse order</title></path>`;}});
 FORKS.forEach(f=>{{const on=keep.has(f.f), hw=HWSET.has(f.f), [x,y]=geom(f);
  const rr=Math.max(2.2,Math.sqrt(f.runs)*0.85);
  s+=`<circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="${{rr.toFixed(1)}}"
   fill="${{!on?"#d8d5cd":(hw?SC[f.stage]||"#666":"#fff")}}"
   opacity="${{on?(selFork===f.f?1:.86):.3}}"
   stroke="${{selFork===f.f?"#1d2021":(on&&!hw?SC[f.stage]||"#666":"none")}}"
   stroke-width="${{selFork===f.f?1.6:1.2}}"
   style="cursor:pointer" onclick="pickI(${{FIDX[f.f]}})">
   <title>${{E(f.f)}}\n${{f.runs}} analyses · ${{(f.cov*100).toFixed(0)}}% coverage · eff_all ${{f.eff.toFixed(2)}}${{hw?"\non a highway":"\nnot on any highway"}}</title></circle>`;}});
 // Numbers, not labels: a ring of 317 labels is unreadable, and the number
 // ties the node to its row in the list, which carries the text.
 r.slice(0,top).forEach(f=>{{const [x,y]=geom(f);
  s+=`<circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="8.5" fill="#fff"
   stroke="${{SC[f.stage]}}" stroke-width="1.4" opacity=".95"/>
   <text x="${{x.toFixed(1)}}" y="${{(y+3.2).toFixed(1)}}" font-size="9.5"
   font-weight="700" fill="${{SC[f.stage]}}" text-anchor="middle"
   style="cursor:pointer" onclick="pickI(${{FIDX[f.f]}})"
   >${{NUM[f.f]}}</text>`;}});
 document.getElementById("circle").innerHTML=s;
 // Only announce a persona filter when one is actually narrowing the view.
 // With every box ticked -- the default -- this said "standard + positive +
 // ... : forks any of them reached", which is every fork, dressed up as a
 // selection.
 const a0=armsAll()?[]:selArms();
 document.getElementById("gcount").innerHTML=
  `${{r.length}} of ${{FORKS.length}} decision forks`
  +(a0.length?` · <b>${{E(a0.join(" + "))}}</b>: forks ${{a0.length>1?"any of them":"it"}}
   reached, chords at their combined traversal count. Node size stays
   corpus-wide.`:"");
 // Which payout the SHAP column shows is a CHOICE, and three of the four do
 // not predict out of sample. The note says which is selected and whether it
 // generalises, so a sort by |SHAP| cannot silently rank on a fit that does not.
 const pb=PAY[pk]||{{}}, cv=pb.r2_cv;
 const pn_=document.getElementById("paynote"); if(pn_) pn_.innerHTML= cv==null?"":
  `SHAP column: <b>${{E(pk)}}</b> · cross-validated R² `+
  `<b style="color:${{cv>0?'#2f6f4e':'#b45309'}}">${{cv.toFixed(4)}}</b>`+
  (cv>0?"":
   " — <b>does not predict out of sample</b>; these attributions are shares of a fit that does not generalise");
 document.getElementById("gt").tBodies[0].innerHTML=r.map(f=>{{
  const sh=f.shap&&f.shap[pk], n=NUM[f.f];
  return `<tr id="row-${{n}}" class="${{selFork===f.f?'sel':''}}"
   onclick="pickI(${{FIDX[f.f]}})">
   <td style="width:26px;text-align:right;color:${{n<=top?SC[f.stage]:'#9aa79f'}};
    font-weight:${{n<=top?700:400}}">${{n}}</td>
   <td><b>${{E(f.f.slice(0,60))}}</b><div class="muted" style="font-size:11.5px">
   <span class="pill" style="background:${{SC[f.stage]}}22;color:${{SC[f.stage]}}">${{f.stage.replace(/_/g," ")}}</span>
   ${{f.runs}} analyses · ${{(f.cov*100).toFixed(0)}}% · ${{f.eff.toFixed(2)}} eff · ${{f.nopt}} opts
   ${{sh?` · SHAP ${{sh.s>=0?"+":""}}${{sh.s.toFixed(4)}}`:""}}</div></td></tr>`;}}).join("");
 if(selFork&&NUM[selFork]){{const el=document.getElementById("row-"+NUM[selFork]);
  if(el)el.scrollIntoView({{block:"nearest"}});}}
}}
/* Handlers carry the fork's index, not its text. Passing the text meant building
   a JS string literal inside an HTML attribute, and the escape used for the
   apostrophe (&#39;) is decoded by the parser back to a bare ' that closes the
   string early -- so every fork whose wording contains one threw a syntax error
   on click and simply did not respond. Twenty of the 317 do. An index needs no
   escaping at all. */
function pickI(i){{const f=FORKS[i]; if(f)pick(f.f);}}
function pick(f){{selFork=(selFork===f?null:f);drawG();
 if(selFork){{const o=FORKS[FIDX[selFork]];if(o)showFork(o);}} else panelClear();}}

/* Tab 0's detail goes in the gap beside the ring, not over the whole screen.
   dlgOpen stays for the Corpus Viewer, whose run detail has no such gap to
   live in. */
const PANEL_HINT='<div class="hint">Click a fork on the ring, a row in the '
 +'list, or a chord.</div>';
function panelOpen(h){{const p=document.getElementById("gdetail");
 p.innerHTML='<button class="close" onclick="panelClear();selFork=null;drawG()"'
  +'>close</button>'+h; p.scrollTop=0;}}
function panelClear(){{document.getElementById("gdetail").innerHTML=PANEL_HINT;}}
/* `k` picks the direction tab: 0 = the busier order (the entry's a->b),
   1 = the reverse. The persona table is shared below the tabs, because the
   test behind it is undirected -- putting it inside each tab would imply it
   changes with the arrow, and it does not. */
function showHwy(i,k){{
 const h=HWY[i]; if(!h)return;
 k=k===1?1:0;
 const d=(h.dirs||[])[k]||{{a:h.a,b:h.b,n:h.n}};
 const A=FORKS[FIDX[d.a]], B=FORKS[FIDX[d.b]];
 const dtabs=(h.dirs||[]).map((x,j)=>`<button class="dtab" aria-selected="${{j===k}}"
   onclick="showHwy(${{i}},${{j}})">${{j===0?"→":"←"}} ${{x.n}} analyses</button>`).join("");
 // The persona association test from circle.py: for this edge and each
 // persona, analyses that used it against analyses expected from that
 // persona's share of the corpus, with a BH-corrected threshold.
 // Counts, expected and lift follow the selected ORDER: used is the persona's
 // distinct analyses walking a->b, expected is that order's total times the
 // persona's corpus share (circle.py's formula). p cannot follow the order --
 // the test behind it is undirected -- so it is shown as what it is.
 const pmap={{}}; (h.enr||[]).forEach(e=>pmap[e.persona]=e.p);
 const order=[...(h.enr||[]).map(e=>e.persona),
              ...Object.keys(SHARE).filter(p=>!(p in pmap))];
 const rows=order.map(p=>{{
  const used=(d.arms||{{}})[p]||0, tot=d.n||0, exp=tot*(SHARE[p]||0);
  const lift=exp?used/exp:null, pv=pmap[p];
  const sig=pv!=null&&ENRTHR!=null&&pv<=ENRTHR;
  return `<tr><td>${{E(p)}}</td><td class=n>${{used}} / ${{tot}}</td>
   <td class=n>${{exp.toFixed(1)}}</td>
   <td class=n>${{lift==null?"—":lift.toFixed(2)+"×"}}</td>
   <td class="n" style="color:${{sig?"#7c3aed":"#6b7280"}};font-weight:${{sig?700:400}}">
   ${{pv==null?"—":pv.toExponential(1)}}${{sig?" ✓":""}}</td></tr>`;}}).join("");
 panelOpen(`<h2>Highway · ${{h.n}} analyses</h2>
  <div class="muted" style="font-size:11.5px">distinct analyses that walked this pair in either order</div>
  <div class="dtabs">${{dtabs}}</div>
  <div class="kv"><b>from</b><span>${{E(d.a)}}</span>
   <b></b><span class="muted">${{A?`${{A.runs}} analyses · ${{A.stage.replace(/_/g," ")}}`:""}}</span>
   <b>to</b><span>${{E(d.b)}}</span>
   <b></b><span class="muted">${{B?`${{B.runs}} analyses · ${{B.stage.replace(/_/g," ")}}`:""}}</span>
   <b>traversed by</b><span>${{d.n}} analyses in this order</span></div>
  <h3 style="margin:12px 0 4px;font-size:13px">Persona association
   <span class="muted" style="font-weight:400">· this order, ${{d.n}} analyses</span></h3>
  ${{rows?`<table><thead><tr><th>persona</th><th class="n">used / total</th>
   <th class="n">expected</th><th class="n">lift</th><th class="n">p · both orders</th></tr></thead>
   <tbody>${{rows}}</tbody></table>
   <div class="muted" style="font-size:11.5px;margin-top:5px">Used, expected and
   lift are for the selected order. Expected is that order's total times the
   persona's share of the corpus, so lift is use against availability, not raw
   popularity. <b>p</b> is the permutation test over both orders
   (${{h.n}} analyses) — no per-order test exists. ✓ survives the BH-corrected
   threshold (p ≤ ${{ENRTHR==null?"—":ENRTHR.toExponential(1)}}).</div>`
   :`<p class="muted">no persona test recorded for this edge</p>`}}`);
}}
function showFork(f){{
 const tot=f.opts.reduce((a,o)=>a+o[1],0)||1;
 const sh=Object.entries(f.shap||{{}}).map(([k,v])=>`${{E(k)}} ${{v.s>=0?"+":""}}${{v.s.toFixed(4)}}`).join(" · ");
 panelOpen(`<h2>${{E(f.f)}}</h2><div class="muted">${{f.stage.replace(/_/g," ")}}</div>
  <div class="kv"><b>runs</b><span>${{f.runs}} (${{(f.cov*100).toFixed(1)}}% coverage)</span>
  <b>effective options</b><span>${{f.eff.toFixed(2)}} of ${{f.nopt}}</span>
  ${{sh?`<b>Shapley</b><span>${{sh}}</span>`:""}}</div>
  <h3 style="margin:10px 0 4px;font-size:13px">Options</h3>
  <div class="fl">${{f.opts.map(o=>
   `<div>${{(100*o[1]/tot).toFixed(0)}}% &nbsp;${{E(o[0])}} <span class="muted">(${{o[1]}})</span></div>`).join("")}}</div>`);
}}

/* ---------- Tab 1: the atlas ---------- */
function drawP(){{
 const ef=+document.getElementById("ef").value/10;
 const cv=+document.getElementById("cv").value/100;
 document.getElementById("cvv").textContent=(cv*100).toFixed(0)+"%";
 const MET=document.getElementById("met").value;   // "effr" or "eff"
 const MLAB=MET=="eff"?"eff_all":"eff_reached";
 const pa=document.getElementById("parm").value;
 const FK=pa?FORKS.filter(f=>(f.arms[pa]||0)>0):FORKS;
 document.getElementById("efv").textContent=ef.toFixed(1);
 const piv=FK.filter(f=>f[MET]>ef&&f.cov>=cv);
 document.getElementById("pcount").textContent=
  `${{piv.length}} of ${{FK.length}} decision forks`;
 // A · fan
 const rk=FK.slice().sort((a,b)=>b.cov-a.cov), W=900;
 let a=`<line x1="46" y1="170" x2="${{W-8}}" y2="170" stroke="#ccc"/>`;
 rk.forEach((f,i)=>{{const x=46+(W-58)*i/Math.max(1,rk.length-1);
  const h=150*Math.log10(1+9*f.cov);
  a+=`<line x1="${{x.toFixed(1)}}" y1="170" x2="${{x.toFixed(1)}}" y2="${{(170-h).toFixed(1)}}"
   stroke="${{f.eff>ef?SC[f.stage]:"#d6d3ca"}}" stroke-width="1.6"><title>${{E(f.f)}}
${{f.runs}} runs · ${{(f.cov*100).toFixed(0)}}%</title></line>`;}});
 a+=`<text x="46" y="192" font-size="11" fill="#6b7280">forks ranked by coverage (log)</text>`;
 document.getElementById("panA").innerHTML=a;
 // B · map
 // x = coverage, y = effective options. The pivotal threshold is on eff_all,
 // so it is a HORIZONTAL line: everything above it is pivotal.
 const mx=Math.max(...FK.map(f=>f[MET]),2), L=56,H=340,B=42;
 const px=v=>L+(W-L-16)*Math.min(1,v), py=v=>H-B-(H-B-16)*Math.min(v,mx)/mx;
 let b=`<line x1="${{L}}" y1="${{H-B}}" x2="${{W-8}}" y2="${{H-B}}" stroke="#ccc"/>
  <line x1="${{L}}" y1="12" x2="${{L}}" y2="${{H-B}}" stroke="#ccc"/>
  <line x1="${{L}}" y1="${{py(ef).toFixed(1)}}" x2="${{W-8}}" y2="${{py(ef).toFixed(1)}}"
   stroke="#b45309" stroke-dasharray="4 3"/>
  <text x="${{W-10}}" y="${{(py(ef)-5).toFixed(1)}}" font-size="10.5" fill="#b45309"
   text-anchor="end">above this line</text>
  ${{cv>0?`<line x1="${{px(cv).toFixed(1)}}" y1="12" x2="${{px(cv).toFixed(1)}}" y2="${{H-B}}"
   stroke="#b45309" stroke-dasharray="4 3"/>`:""}}
  <text x="${{L-8}}" y="16" font-size="10.5" fill="#6b7280" text-anchor="end">${{mx.toFixed(1)}}</text>
  <text x="${{L-8}}" y="${{H-B}}" font-size="10.5" fill="#6b7280" text-anchor="end">1</text>
  <text x="${{L}}" y="${{H-24}}" font-size="10.5" fill="#6b7280">0%</text>
  <text x="${{W-8}}" y="${{H-24}}" font-size="10.5" fill="#6b7280" text-anchor="end">100%</text>
  <text x="${{W/2}}" y="${{H-8}}" font-size="11" fill="#6b7280" text-anchor="middle">coverage — analyses that reached the fork</text>
  <text x="14" y="${{H/2}}" font-size="11" fill="#6b7280" text-anchor="middle" transform="rotate(-90 14 ${{H/2}})">effective options (${{MLAB}})</text>`;
 FK.forEach(f=>{{const on=f[MET]>ef&&f.cov>=cv;
  b+=`<circle cx="${{px(f.cov).toFixed(1)}}" cy="${{py(f[MET]).toFixed(1)}}"
   r="${{on?5:2.6}}" fill="${{on?SC[f.stage]||"#2f6f4e":"#cfccc3"}}"
   opacity="${{on?.88:.5}}" style="cursor:pointer"
   onclick="showFork(FORKS[${{FIDX[f.f]}}])"><title>${{E(f.f)}}
${{f.runs}} analyses · ${{(f.cov*100).toFixed(1)}}% coverage · eff_all ${{f.eff.toFixed(2)}} (eff_reached ${{f.effr.toFixed(2)}}) of ${{f.nopt}} options
stage ${{f.stage.replace(/_/g," ")}}</title></circle>`;}});
 document.getElementById("panB").innerHTML=b;
 // C · spectrum
 // C follows B. Under eff_reached the bar is the options only; under eff_all it
 // also carries the "did not visit" band, because that is the level which
 // separates the two numbers and a spectrum without it cannot explain the gap.
 const top=FK.slice().sort((x,y)=>y.cov-x.cov).slice(0,14);
 let c="", rowh=19;
 top.forEach((f,i)=>{{
  const dist=(f.dist&&f.dist.length)?f.dist:f.opts;
  const abs_=MET=="eff"?(f.absent||0):0;
  const tot=(dist.reduce((s,o)=>s+o[1],0)||1)+abs_;
  let x=330;
  c+=`<text x="322" y="${{i*rowh+22}}" font-size="10.5" fill="#1d2021"
   text-anchor="end">${{E(f.f.slice(0,46))}}</text>`;
  dist.forEach((o,j)=>{{const w=(W-350)*o[1]/tot;
   c+=`<rect x="${{x.toFixed(1)}}" y="${{i*rowh+12}}" width="${{Math.max(0.6,w).toFixed(1)}}"
    height="12" fill="${{o[1]===1?"#e2ded4":SC[f.stage]}}" opacity="${{o[1]===1?.9:0.9-j*0.06}}">
    <title>${{E(o[0])}} — ${{o[1]}} analyses</title></rect>`;x+=w;}});
  if(abs_>0){{const w=(W-350)*abs_/tot;
   c+=`<rect x="${{x.toFixed(1)}}" y="${{i*rowh+12}}" width="${{Math.max(0.6,w).toFixed(1)}}"
    height="12" fill="none" stroke="#9aa79f" stroke-width="1"
    style="fill:url(#hatch)"><title>did not visit — ${{abs_}} analyses</title></rect>`;}}}});
 c=`<defs><pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse"
   patternTransform="rotate(45)"><rect width="5" height="5" fill="#f2f0ea"/>
   <line x1="0" y1="0" x2="0" y2="5" stroke="#b9b5ab" stroke-width="1.4"/></pattern></defs>`+c;
 c+=`<text x="330" y="${{top.length*rowh+26}}" font-size="10.5" fill="#6b7280">pale = singleton options (the novel tail)`
  +(MET=="eff"?` · hatched = did not visit, the level that separates eff_all from eff_reached`:"")+`</text>`;
 document.getElementById("panC").innerHTML=c;
 // D · effective options by stage
 let d="",bw=(W-90)/STAGES.length;
 STAGES.forEach((st,i)=>{{const v=FORKS.filter(f=>f.stage===st&&f.runs>=10).map(f=>f.eff);
  const x0=56+i*bw;
  d+=`<text x="${{(x0+bw/2).toFixed(1)}}" y="196" font-size="10" fill="${{SC[st]}}"
   text-anchor="middle">${{st.replace(/_/g," ").slice(0,16)}}</text>`;
  v.forEach(e=>{{const y=175-(e-1)/3*150;
   d+=`<circle cx="${{(x0+bw/2+(Math.random()-.5)*bw*0.5).toFixed(1)}}" cy="${{Math.max(12,y).toFixed(1)}}"
    r="3" fill="${{SC[st]}}" opacity=".62"/>`;}});
  if(v.length){{const m=v.reduce((a,b)=>a+b,0)/v.length, y=175-(m-1)/3*150;
   d+=`<line x1="${{(x0+bw*0.18).toFixed(1)}}" y1="${{Math.max(12,y).toFixed(1)}}"
    x2="${{(x0+bw*0.82).toFixed(1)}}" y2="${{Math.max(12,y).toFixed(1)}}" stroke="${{SC[st]}}" stroke-width="2"/>`;}}}});
 d+=`<text x="14" y="100" font-size="11" fill="#6b7280" text-anchor="middle" transform="rotate(-90 14 100)">effective options</text>`;
 document.getElementById("panD").innerHTML=d;
 // Shapley
 let s="";
 for(const [name,blk] of Object.entries(PAY)){{
  const pm=blk.perm||{{}};
  const rows=Object.entries(blk.players)
   .map(([k,v])=>[k,(v&&v.strength)||0,(v&&v.ci)||[null,null],pm[k]])
   .sort((x,y)=>Math.abs(y[1])-Math.abs(x[1])).slice(0,12);
  const mx2=Math.max(...rows.map(r=>Math.abs(r[1])),1e-9);
  const bad=(blk.r2_cv??0)<=0;
  s+=`<div style="margin:10px 0 4px"><b>${{E(name)}}</b>
   <span class="muted">· n=${{blk.n}} · R² ${{(blk.r2??0).toFixed(3)}} ·
   cross-validated R² <b style="color:${{bad?"#b45309":"#2f6f4e"}}">${{(blk.r2_cv??0).toFixed(4)}}</b></span></div>`;
  if(bad)s+=`<div class="note" style="margin:4px 0 8px">Cross-validated R² is not positive:
   this model does not predict out of sample. The attributions below are shares of a fit that
   does not generalise, and must not be read as "this fork drives the conclusion".</div>`;
  s+=`<table><tbody>`+rows.map(([k,v,ci])=>{{
   // Significance is the PERMUTATION p, never the CI. `strength` is mean|phi|,
   // non-negative by construction, so a percentile bootstrap interval on it
   // essentially cannot contain zero -- 44 of 44 exclude it here while only 8
   // reach p < 0.05. Greying on "CI straddles zero" encoded a test that can
   // never fire and implied the CI was one.
   const pv=blk.perm&&blk.perm[k], sig=pv!=null&&pv<0.05;
   const zero=pv!=null&&!sig;
   const cis=ci[0]==null?"":` · bootstrap 95% ${{ci[0].toFixed(4)}} to ${{ci[1].toFixed(4)}}`;
   return `<tr title="${{E(k)}}${{cis}}"><td style="width:56%">${{E(k.slice(0,72))}}</td>
    <td><div style="background:${{zero?"#cfccc3":(v>=0?"#2f6f4e":"#b45309")}};height:9px;
     border-radius:2px;width:${{(100*Math.abs(v)/mx2).toFixed(1)}}%"></div></td>
    <td class="n" style="width:78px">${{v>=0?"+":""}}${{v.toFixed(4)}}</td>
    <td class="n" style="width:72px;color:${{sig?"#2f6f4e":"#6b7280"}};
     font-weight:${{sig?700:400}}">${{pv==null?"—":"p "+pv.toFixed(3)}}</td></tr>`;}}
   ).join("")+`</tbody></table>`;
 }}
 document.getElementById("shap").innerHTML=s||'<p class="muted">no Shapley file for this tag</p>';
}}

/* ---------- Tab 2: lifecycle ---------- */
function drawL(){{
 const it=LIFE.iteration||{{}}, nv=LIFE.novelty||{{}}, ns=LIFE.nov_shap||{{}};
 // stages
 const cnt={{}}, dec={{}};
 STAGES.forEach(s=>{{cnt[s]=0;dec[s]=0;}});
 FORKS.forEach(f=>{{if(cnt[f.stage]==null)return;
  cnt[f.stage]++; dec[f.stage]+=f.opts.reduce((a,o)=>a+o[1],0);}});
 const mxd=Math.max(...Object.values(dec),1);
 document.getElementById("lstage").innerHTML=
  `<table><thead><tr><th>stage</th><th class="n">forks</th>
   <th class="n">decisions</th><th></th></tr></thead><tbody>`+
  STAGES.map(s=>`<tr><td><span class="pill" style="background:${{SC[s]}}22;
   color:${{SC[s]}}">${{s.replace(/_/g," ")}}</span></td>
   <td class=n>${{cnt[s]}}</td><td class=n>${{dec[s]}}</td>
   <td><div style="background:${{SC[s]}};height:9px;border-radius:2px;
    width:${{(100*dec[s]/mxd).toFixed(1)}}%"></div></td></tr>`).join("")+
  `</tbody></table>`;
 // iteration
 const bp=(it.back_pairs||[]).slice(0,8);
 const mxb=Math.max(...bp.map(b=>b.n),1);
 document.getElementById("literm").innerHTML= it.runs==null?"":
  `<div class="kv"><b>analyses</b><span>${{it.runs}}</span>
   <b>with at least one return</b><span><b>${{it.runs_with_return}}</b> of
    ${{it.runs}}</span>
   <b>returns / transitions</b><span>${{it.returns}} of ${{it.transitions}}</span></div>
   <table><thead><tr><th>from</th><th>to</th><th class="n">n</th><th></th></tr>
   </thead><tbody>`+bp.map(b=>
   `<tr><td>${{E(b.from.replace(/_/g," "))}}</td>
    <td>${{E(b.to.replace(/_/g," "))}}</td><td class=n>${{b.n}}</td>
    <td><div style="background:#8a4f7d;height:9px;border-radius:2px;
     width:${{(100*b.n/mxb).toFixed(1)}}%"></div></td></tr>`).join("")+
   `</tbody></table>`;
 // novelty shapley
 const pays=Object.keys(ns);
 document.getElementById("lnov").innerHTML= !pays.length?
  `<p class="muted">no novelty Shapley run for this tag — build it with
   <code>shapley_v2.py --novelty --out-suffix .novelty</code></p>` :
   `
   <table><thead><tr><th>payout</th><th class="n">CV without</th>
   <th class="n">CV with</th><th class="n">gain</th><th class="n">strength</th>
   <th class="n">p</th></tr></thead><tbody>`+
  pays.map(k=>{{const b=ns[k], g=(b.r2cv_with||0)-(b.r2cv_without||0),
   sig=b.p!=null&&b.p<0.05;
   return `<tr><td>${{E(k)}}</td><td class=n>${{(b.r2cv_without||0).toFixed(3)}}</td>
    <td class=n>${{(b.r2cv_with||0).toFixed(3)}}</td>
    <td class=n style="color:${{g>0?'#2f6f4e':'#6b7280'}}">${{g>=0?"+":""}}${{g.toFixed(3)}}</td>
    <td class=n>${{(b.strength||0).toFixed(4)}}</td>
    <td class="n" style="color:${{sig?'#2f6f4e':'#6b7280'}};font-weight:${{sig?700:400}}">
    ${{b.p==null?"—":b.p.toFixed(3)}}</td></tr>`;}}).join("")+`</tbody></table>`;
}}

/* ---------- Tab 4: about ---------- */
function drawA(){{
 // Gate state is read from the locks, not asserted. An open gate is a correct
 // state and the tab says so: a viewer that reports only what is finished
 // teaches its reader that everything is.
 const g=GATES||[];
 document.getElementById("agates").innerHTML=
  `<table><thead><tr><th>gate</th><th>state</th><th>what it rests on</th></tr>
   </thead><tbody>`+g.map(x=>
   `<tr><td><b>${{E(x.name)}}</b><div class="muted" style="font-size:12px">
    ${{E(x.what)}}</div></td>
    <td><span class="pill" style="background:${{x.settled?"#e8f2ec":"#fdf0dd"}};
     color:${{x.settled?"#2f6f4e":"#b45309"}}">${{x.settled?"settled":"open"}}</span></td>
    <td style="font-size:12.5px;color:#555">${{E(x.note)}}</td></tr>`).join("")
   +`</tbody></table>`;
}}

/* ---------- Tab 3: corpus ---------- */
let rs={{k:"exon",d:-1}};
function sortR(k){{rs.d=(rs.k==k)?-rs.d:-1;rs.k=k;drawR();}}
function chrom(r){{
 if(!r.spans.length||!r.lines)return '<span class="muted">no script</span>';
 const sil=new Set(); r.sil.forEach(s=>{{for(let i=s[0];i<=s[1];i++)sil.add(i);}});
 return `<div class="chrom" title="${{r.lines}} lines">`+
  r.spans.slice().sort((a,b)=>a[0]-b[0]).map(s=>{{
   const k=s[2]?(sil.has(s[0])?"si":"ex"):"in";
   return `<i class="${{k}}" style="flex:${{Math.max(1,s[1]-s[0]+1)}}"></i>`;}}).join("")+`</div>`;
}}
function drawR(){{
 const q=document.getElementById("rq").value.toLowerCase().trim();
 const a=document.getElementById("rarm").value, c=document.getElementById("rc").value;
 let r=RUNS.filter(x=>(!a||x.arm==a)&&(!c||x.concl==c)&&(!q||x.id.toLowerCase().includes(q)));
 r.sort((x,y)=>{{let u=x[rs.k],v=y[rs.k];if(u==null)u=-1;if(v==null)v=-1;
  return (typeof u=="string"?u.localeCompare(v):u-v)*rs.d;}});
 document.getElementById("rcount").textContent=`${{r.length}} of ${{RUNS.length}} runs`;
 document.getElementById("rt").tBodies[0].innerHTML=r.map(x=>
  `<tr onclick="showRun('${{x.id}}')"><td>${{E(x.id)}}</td>
   <td><span class="pill">${{E(x.arm)}}</span></td><td class=n>${{x.lines}}</td>
   <td class=n>${{(x.exon*100).toFixed(1)}}%</td><td>${{chrom(x)}}</td>
   <td class=n>${{x.dec}}</td><td class=n>${{x.silent}}</td>
   <td class=n>${{x.est==null?"—":x.est.toFixed(3)}}</td>
   <td>${{E(x.concl||"—")}}</td></tr>`).join("");
}}
function pct(arr,v){{const s=arr.filter(x=>x!=null).sort((a,b)=>a-b);
 if(!s.length)return null;let i=s.findIndex(x=>x>=v);if(i<0)i=s.length;
 return Math.round(100*i/s.length);}}
function showRun(id){{
 const r=RUNS.find(x=>x.id==id); if(!r)return;
 const sil=new Set(); r.sil.forEach(s=>{{for(let i=s[0];i<=s[1];i++)sil.add(i);}});
 const bars=r.spans.slice().sort((a,b)=>a[0]-b[0]).map(s=>{{
  const k=s[2]?(sil.has(s[0])?"si":"ex"):"in";
  const l=100*(s[0]-1)/Math.max(1,r.lines), w=100*(s[1]-s[0]+1)/Math.max(1,r.lines);
  return `<i class="${{k}}" style="left:${{l.toFixed(2)}}%;width:${{Math.max(0.25,w).toFixed(2)}}%"></i>`;
 }}).join("");
 const pe=pct(RUNS.map(x=>x.exon),r.exon), pd=pct(RUNS.map(x=>x.dec),r.dec);
 const med=a=>{{const s=a.filter(x=>x!=null).sort((x,y)=>x-y);
  return s.length?s[Math.floor(s.length/2)]:0;}};
 dlgOpen(`<h2>${{E(r.id)}}</h2>
  <div class="muted">${{E(r.arm)}} · ${{r.lines}} lines · ${{r.forks.length}} decision forks visited</div>
  <div class="map">${{bars}}</div>
  <div class="lg"><i class="ex"></i> exon <i class="si"></i> silent decision <i class="in"></i> intron</div>
  <div class="kv">
   <b>% exon</b><span>${{(r.exon*100).toFixed(1)}}% — ${{pe}}th percentile (median ${{(med(RUNS.map(x=>x.exon))*100).toFixed(1)}}%)</span>
   <b>decisions</b><span>${{r.dec}} — ${{pd}}th percentile (median ${{med(RUNS.map(x=>x.dec))}})</span>
   <b>silent decisions</b><span>${{r.silent}}</span>
   <b>odds ratio</b><span>${{r.est==null?"—":r.est.toFixed(3)}} ${{r.concl?"· "+E(r.concl):""}}</span></div>
  <h3 style="margin:10px 0 4px;font-size:13px">Decision forks visited</h3>
  <div class="fl">${{r.forks.map(f=>{{const o=FORKS[FIDX[f]];
   return `<div>${{E(f.slice(0,74))}} <span class="muted">${{o?`· ${{o.runs}} runs`:""}}</span></div>`;}}).join("")||"<span class=muted>none</span>"}}</div>`);
}}
function dlgOpen(h){{const d=document.getElementById("dlg");
 d.querySelector(".dlg").innerHTML=`<button class="close" onclick="dlg.close()">close</button>`+h;
 d.showModal();}}
drawG(); fitCircle();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tag", default=None)
    ap.add_argument("--top", type=int, default=10,
                    help="forks labelled on the circle")
    ap.add_argument("--pivotal-eff", type=float, default=1.5,
                   help="eff_all above which a fork is pivotal. One criterion: "
                        "eff_all already carries coverage and disagreement")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    tag = a.tag or P.FINAL_TAG
    (d, forks, hwy, rows, runs_all, payouts, shp_src, sectors, enr_thr,
     xy, life, gates, share) = build(tag, a.pivotal_eff)
    arms = sorted({r["arm"] for r in rows if r["arm"] and r["arm"] != "?"})
    concl = sorted({r["concl"] for r in rows if r["concl"]})
    piv = [f for f in forks if f["piv"]]

    # Payouts ordered by cross-validated R2, best first, each labelled with it.
    # A payout that does not predict out of sample must not become the default
    # silently, so the best cross-validated fit leads.
    order = sorted(payouts.items(),
                   key=lambda kv: -(kv[1].get("r2_cv") or -9))
    payopts = "".join(
        f'<option value="{html.escape(k)}">{html.escape(k)} '
        f'(CV R² {b.get("r2_cv", 0):+.4f})</option>' for k, b in order)

    page = PAGE.format(
        study=P.STUDY_NAME,
        title=html.escape(str(P.STUDY.get("title") or P.STUDY_NAME)),
        tag=html.escape(tag), nrun=len(runs_all), ndec=len(d["decisions"]),
        nopt=len(d["options"]), nfork=len(forks), top=a.top,
        arms="".join(f'<option>{html.escape(x)}</option>' for x in arms),
        # One toggle per arm present in the corpus, in the palette's own order
        # rather than alphabetical, and carrying that arm's colour so the
        # control reads against circle.py's routes. `human` is included: it is a
        # corpus rather than a persona, but it is an arm a reader wants to
        # isolate, and excluding it left the 19 human teams with no filter at
        # all while their routes were still drawn.
        #
        # All boxes start ticked, which reads as "everything is shown" -- the
        # honest default, since everything is. All-ticked and none-ticked are
        # made identical downstream rather than merely equivalent in the filter,
        # so toggling the last box off does not change the picture.
        armtoggles="".join(
            f'<label class="atog" style="--pc:{PERSONA[x]}">'
            f'<input type="checkbox" class="armchk" value="{html.escape(x)}" '
            f'checked onchange="drawG()">{html.escape(x.replace("_", " "))}</label>'
            for x in PERSONA if x in arms),
        concl="".join(f'<option>{html.escape(x)}</option>' for x in concl),
        peff=f"{a.pivotal_eff:.1f}", peff10=int(a.pivotal_eff * 10),
        payopts=payopts,
        forks=json.dumps(forks, ensure_ascii=False),
        runs=json.dumps(rows, ensure_ascii=False),
        hwy=json.dumps(hwy, ensure_ascii=False),
        share=json.dumps(share),
        pay=json.dumps(payouts, ensure_ascii=False),
        stages=json.dumps(STAGES), shpsrc=shp_src,
        sectors=json.dumps(sectors), enrthr=json.dumps(enr_thr),
        xy=json.dumps(xy),
        life=json.dumps({k: v for k, v in life.items()
                         if not k.startswith("svg_")}),
        svg_iter=life["svg_iter"], svg_nov=life["svg_nov"],
        gates=json.dumps(gates))

    out = Path(a.out) if a.out else P.FIGURES / "forkscope.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")

    # Runs with no script have no exon share -- 11 human teams deposited none,
    # and `float(cov.get("functional_share") or 0)` above turns that absence
    # into a literal 0.0 for the row. Zero-filling them dragged this median to
    # 38.5% where the runs that actually have code sit at 39.0%. A team with no
    # script is not a team whose code is 0% functional; it is not in the
    # denominator at all.
    ex = sorted(r["exon"] for r in rows if r["exon"])
    print(f"ForkSCOPE — {P.STUDY_NAME}")
    print(f"  {len(runs_all)} runs · {len(d['decisions'])} decisions · "
          f"{len(d['options'])} options · {len(forks)} decision forks")
    print(f"  {len(piv)} pivotal · {len(hwy)} highways · "
          f"{len(payouts)} Shapley payouts")
    print(f"  median % exon {ex[len(ex)//2]:.1%}")
    print(f"\n  wrote {out}  ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
