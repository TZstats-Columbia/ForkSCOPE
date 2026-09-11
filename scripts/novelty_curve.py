#!/usr/bin/env python3
"""Is the novelty-outcome relation non-linear, and does pipeline stage matter?

Two questions the median split in novelty.py could not answer.

**Shape.** A median split reports one contrast and hides everything else. If the
relation is U-shaped, or flat until a threshold, or driven by a handful of
extreme runs, a two-group comparison shows nothing and is read as "no effect".
So the runs are binned into novelty quintiles and the outcome is reported per
bin with a bootstrap interval, alongside Pearson (linear) and Spearman
(monotone) correlations. A Spearman clearly larger than Pearson is the
signature of a monotone-but-curved relation; both near zero with a visibly
non-flat curve points to non-monotonicity.

**Stage.** v2 records no DSLC stage -- the segmentation prompt never asked for
one, deliberately. What every decision does carry is the line at which it
appears, and that is the better variable here: the observed position is an
artifact property, while a DSLC label is a scheme laid over it. Earlier in this
project the median code line put `analytic posture` at line 109 and `primary
estimand choice` at 159, i.e. the problem-formulation decisions are physically
written in the middle of the modelling code, so the two orderings genuinely
disagree.

Position is normalised by each script's own length before binning, because
scripts run from 164 to 507 lines and raw line numbers are not comparable.

Everything here is observational. Runs were not assigned their novelty.

Usage:
    python3 scripts/novelty_curve.py --corpus ai [--svg out.svg] [--json out.json]
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from math import log, sqrt
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
OUT = P.ANALYSIS
OUTCOMES = P.OUTCOMES

MIN_RUNS = 10
NBINS = 5
B = 3000
SEED = 20260822


def ci(v, lo=2.5, hi=97.5):
    s = sorted(v)
    return (s[int(len(s) * lo / 100)], s[min(len(s) - 1, int(len(s) * hi / 100))])


def boot_mean(v, rng):
    if not v:
        return (0, 0, 0)
    bs = [sum(rng.choice(v) for _ in v) / len(v) for _ in range(B)]
    return (sum(v) / len(v),) + ci(bs)


def pearson(x, y):
    n = len(x)
    if n < 3:
        return 0.0
    mx, my = sum(x) / n, sum(y) / n
    sx = sqrt(sum((a - mx) ** 2 for a in x))
    sy = sqrt(sum((b - my) ** 2 for b in y))
    if not sx or not sy:
        return 0.0
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def load(tag):
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        cand = sorted(P.VOCAB.glob("bottom_up_*.json"))
        if not cand:
            sys.exit("no bottom_up_*.json")
        p = cand[-1]
    return json.loads(p.read_text(encoding="utf-8")), p


def script_lengths():
    out = {}
    for r in P.DISTILLED.glob("*/record.json"):
        d = json.loads(r.read_text(encoding="utf-8"))
        c = d.get("coverage", {}).get("code")
        if c:
            out[d["run_id"]] = c["n_lines"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--svg", default=str(P.FIGURES / "novelty_curve.svg"))
    ap.add_argument("--json")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    d, path = load(tag)
    dec, rng = d["decisions"], random.Random(SEED)
    lens = script_lengths()

    forks = defaultdict(lambda: defaultdict(set))
    arm_of = {}
    memb = {}
    for o in d["options"]:
        for i in o.get("members", []):
            if i >= len(dec):
                continue
            forks[o["fork"]][o["option"]].add(dec[i]["run"])
            arm_of[dec[i]["run"]] = dec[i]["arm"]
            memb.setdefault((o["fork"], o["option"]), []).append(i)
    well = {f for f, os_ in forks.items()
            if len(set().union(*os_.values())) >= MIN_RUNS}

    novel_idx = []          # decision indices that instantiate a novel option
    for f in well:
        for opt, rs in forks[f].items():
            if len(rs) == 1:
                novel_idx.extend(memb.get((f, opt), []))
    novel_idx = set(novel_idx)

    dec_per_run = Counter(x["run"] for x in dec)
    nov_per_run = Counter(dec[i]["run"] for i in novel_idx)
    runs = sorted(dec_per_run)
    score = {r: nov_per_run.get(r, 0) / dec_per_run[r] for r in runs}

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
        print(f"novelty curve NOT COMPUTED -- no outcomes at {OUTCOMES}. "
              f"Owner decision D3: the extractor is unwritten.")
        return
    outc = {o["repo_id"]: o for o in
            json.loads(OUTCOMES.read_text(encoding="utf-8"))}

    def eff(r):
        v = outc.get(r, {}).get("or_scale_estimate")
        return log(v) if v and v > 0 else None

    def sup(r):
        return 1.0 if outc.get(r, {}).get("conclusion") == "supported" else None

    have = [r for r in runs if eff(r) is not None]
    print(f"NOVELTY DOSE-RESPONSE — {path.name}")
    print(f"{len(novel_idx)} novel-option decisions, {len(have)} runs with an "
          f"outcome\n")

    # ---------- shape ----------
    xs = [score[r] for r in have]
    ys = [eff(r) for r in have]
    vs = [1.0 if outc[r].get("conclusion") == "supported" else 0.0 for r in have]
    print("SHAPE OF THE RELATION")
    print(f"  log OR   Pearson {pearson(xs, ys):+.3f}   "
          f"Spearman {spearman(xs, ys):+.3f}")
    print(f"  verdict  Pearson {pearson(xs, vs):+.3f}   "
          f"Spearman {spearman(xs, vs):+.3f}")
    print("  (Spearman >> Pearson would mean monotone but curved; both ~0 with a\n"
          "   non-flat curve below would mean non-monotone)\n")

    order = sorted(have, key=lambda r: score[r])
    bins, per = [], max(1, len(order) // NBINS)
    for b in range(NBINS):
        chunk = order[b * per:(b + 1) * per] if b < NBINS - 1 else order[b * per:]
        if not chunk:
            continue
        e = [eff(r) for r in chunk]
        v = [1.0 if outc[r].get("conclusion") == "supported" else 0.0
             for r in chunk]
        me, le, he = boot_mean(e, rng)
        mv, lv, hv = boot_mean(v, rng)
        bins.append({"bin": b + 1, "n": len(chunk),
                     "novelty_lo": round(score[chunk[0]], 3),
                     "novelty_hi": round(score[chunk[-1]], 3),
                     "logOR": round(me, 4), "logOR_ci": [round(le, 4), round(he, 4)],
                     "supported": round(mv, 3),
                     "supported_ci": [round(lv, 3), round(hv, 3)]})
    print(f"  {'bin':<5}{'n':>4}{'novelty range':>18}{'mean log OR':>14}"
          f"{'95% CI':>20}{'supported':>11}")
    for b in bins:
        rng_s = "{:.2f}-{:.2f}".format(b["novelty_lo"], b["novelty_hi"])
        ci_s = "[{:+.3f}, {:+.3f}]".format(*b["logOR_ci"])
        print(f"  {b['bin']:<5}{b['n']:>4}{rng_s:>18}{b['logOR']:>14.3f}"
              f"{ci_s:>20}{b['supported']:>11.2f}")

    # ---------- stage ----------
    print(f"\nDOES STAGE MATTER?  (position normalised by each script's length)")
    stage_rows = []
    for b in range(NBINS):
        lo, hi = b / NBINS, (b + 1) / NBINS
        # novel decisions in this position band, per run
        cnt = Counter()
        tot = Counter()
        for i, x in enumerate(dec):
            L = lens.get(x["run"])
            if not L:
                continue
            p = x["line"] / L
            if lo <= p < hi or (b == NBINS - 1 and p >= hi):
                tot[x["run"]] += 1
                if i in novel_idx:
                    cnt[x["run"]] += 1
        rr = [r for r in have if tot.get(r)]
        if len(rr) < 20:
            continue
        s = {r: cnt.get(r, 0) / tot[r] for r in rr}
        x2 = [s[r] for r in rr]
        y2 = [eff(r) for r in rr]
        v2 = [1.0 if outc[r].get("conclusion") == "supported" else 0.0
              for r in rr]
        stage_rows.append({
            "band": f"{lo:.0%}-{hi:.0%}", "runs": len(rr),
            "decisions": sum(tot[r] for r in rr),
            "novel_rate": round(sum(cnt.values()) / sum(tot[r] for r in rr), 3),
            "r_logOR": round(spearman(x2, y2), 3),
            "r_verdict": round(spearman(x2, v2), 3)})
    print(f"  {'position':<12}{'runs':>5}{'decisions':>11}{'novel rate':>12}"
          f"{'rho(logOR)':>12}{'rho(verdict)':>14}")
    for s in stage_rows:
        print(f"  {s['band']:<12}{s['runs']:>5}{s['decisions']:>11}"
              f"{s['novel_rate']:>12.3f}{s['r_logOR']:>12.3f}"
              f"{s['r_verdict']:>14.3f}")
    print("  rho = Spearman between a run's novelty rate in that band and its "
          "outcome")

    svg = render(bins, stage_rows)
    Path(a.svg).write_text(svg, encoding="utf-8")
    print(f"\n-> {a.svg}")
    # Saving is the default. It used to need --json, so a direct run
    # printed the analysis and wrote nothing -- and the next reader
    # silently got an older tag's numbers.
    out = Path(a.json) if a.json else (
        P.ANALYSIS / f"novelty_curve_{tag}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(
        {"source": path.name, "bins": bins, "stages": stage_rows,
         "pearson_logOR": round(pearson(xs, ys), 4),
         "spearman_logOR": round(spearman(xs, ys), 4),
         "pearson_verdict": round(pearson(xs, vs), 4),
         "spearman_verdict": round(spearman(xs, vs), 4)},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {out}")


def render(bins, stages):
    """Two small panels: the dose-response curve with CIs, and stage rho."""
    W, H, P = 760, 300, 52
    if not bins:
        return "<svg xmlns='http://www.w3.org/2000/svg'/>"
    los = [b["logOR_ci"][0] for b in bins] + [b["logOR"] for b in bins]
    his = [b["logOR_ci"][1] for b in bins] + [b["logOR"] for b in bins]
    ymin, ymax = min(los), max(his)
    pad = (ymax - ymin) * 0.25 or 0.05
    ymin, ymax = ymin - pad, ymax + pad
    def X(i): return P + i * (W - 2 * P) / max(1, len(bins) - 1)
    def Y(v): return H - P - (v - ymin) / (ymax - ymin) * (H - 2 * P)
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H*2+20}' "
         f"viewBox='0 0 {W} {H*2+20}' font-family='ui-sans-serif,system-ui' "
         f"font-size='11'>",
         "<style>.ax{stroke:#bbb;stroke-width:1}.gr{stroke:#eee}"
         ".pt{fill:#2f5fa8}.eb{stroke:#2f5fa8;stroke-width:2}"
         ".ln{stroke:#2f5fa8;stroke-width:2;fill:none}"
         ".t{fill:#333}.d{fill:#777}.bar{fill:#8a5a2b}</style>"]
    s.append(f"<text x='{P}' y='22' class='t' font-size='13' "
             f"font-weight='600'>Novelty vs reported effect, by quintile</text>")
    # ponytail: subtitle parked, not deleted
#     s.append(f"<text x='{P}' y='38' class='d'>mean log odds-ratio with "
#              f"bootstrap 95% CI; flat line = novelty does not move the answer</text>")
    for k in range(5):
        v = ymin + k * (ymax - ymin) / 4
        s.append(f"<line class='gr' x1='{P}' y1='{Y(v):.1f}' x2='{W-P}' "
                 f"y2='{Y(v):.1f}'/>")
        s.append(f"<text x='{P-8}' y='{Y(v)+4:.1f}' text-anchor='end' "
                 f"class='d'>{v:+.2f}</text>")
    pts = " ".join(f"{X(i):.1f},{Y(b['logOR']):.1f}" for i, b in enumerate(bins))
    s.append(f"<polyline class='ln' points='{pts}'/>")
    for i, b in enumerate(bins):
        s.append(f"<line class='eb' x1='{X(i):.1f}' y1='{Y(b['logOR_ci'][0]):.1f}' "
                 f"x2='{X(i):.1f}' y2='{Y(b['logOR_ci'][1]):.1f}'/>")
        s.append(f"<circle class='pt' cx='{X(i):.1f}' cy='{Y(b['logOR']):.1f}' r='4'/>")
        s.append(f"<text x='{X(i):.1f}' y='{H-P+18}' text-anchor='middle' "
                 f"class='d'>{b['novelty_lo']:.2f}-{b['novelty_hi']:.2f}</text>")
        s.append(f"<text x='{X(i):.1f}' y='{H-P+32}' text-anchor='middle' "
                 f"class='d'>n={b['n']}</text>")
    s.append(f"<line class='ax' x1='{P}' y1='{H-P}' x2='{W-P}' y2='{H-P}'/>")
    s.append(f"<text x='{W//2}' y='{H-6}' text-anchor='middle' class='d'>"
             f"novel options per decision recorded</text>")

    if stages:
        O = H + 20
        s.append(f"<text x='{P}' y='{O+22}' class='t' font-size='13' "
                 f"font-weight='600'>Spearman correlation barchart</text>")
        # ponytail: subtitle parked, not deleted
#         s.append(f"<text x='{P}' y='{O+38}' class='d'>Spearman rho between a "
#                  f"run's novelty rate in each position band and its log OR</text>")
        mx = max(0.2, max(abs(t["r_logOR"]) for t in stages))
        mid = O + (H) / 2 + 10
        bw = (W - 2 * P) / len(stages)
        for i, t in enumerate(stages):
            h = t["r_logOR"] / mx * (H / 2 - 60)
            x = P + i * bw + bw * 0.2
            y = mid - max(h, 0)
            s.append(f"<rect class='bar' x='{x:.1f}' y='{y:.1f}' "
                     f"width='{bw*0.6:.1f}' height='{abs(h):.1f}' rx='2'/>")
            s.append(f"<text x='{x+bw*0.3:.1f}' y='{mid+ (18 if h>=0 else -8):.1f}' "
                     f"text-anchor='middle' class='d'>{t['band']}</text>")
            s.append(f"<text x='{x+bw*0.3:.1f}' y='{y-5 if h>=0 else y+abs(h)+14:.1f}' "
                     f"text-anchor='middle' class='d'>{t['r_logOR']:+.2f}</text>")
        s.append(f"<line class='ax' x1='{P}' y1='{mid}' x2='{W-P}' y2='{mid}'/>")
        s.append(f"<text x='{W//2}' y='{O+H-8}' text-anchor='middle' class='d'>"
                 f"position within the script (0% = first line, 100% = last)</text>")
    s.append("</svg>")
    return "\n".join(s)


if __name__ == "__main__":
    main()
