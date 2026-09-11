#!/usr/bin/env python3
"""Q1 -- distillation stability, per run. No model calls.

If two independent distillations of the same script and write-up agree, then
every later stage may reuse cached distillation without that reuse being an
unexamined assumption, and this question never has to be paid for again. That
is why it is worth measuring once, properly.

WHAT MAKES THIS EXACT
---------------------
The code segmentation is an exhaustive, exclusive partition of lines 1..n
(invariant enforced in the retry path, not checked afterwards). So two
segmentations of one script are two labelings of one fixed item set -- the
lines -- and agreement needs no matching heuristic at all. Per-line agreement
and ARI are computed directly.

Prose is exhaustive but NOT exclusive: one sentence may assert two things. Line
agreement is therefore not defined the same way, and the prose channel is
compared on counts and on span boundaries rather than on a partition.

FOUR THINGS ARE REPORTED, BECAUSE THEY MATTER DIFFERENTLY
---------------------------------------------------------
  line agreement    do the same lines get grouped into the same decision?
                    This is the structural question.
  count drift       decisions, claims, links, silent, misaligned. These are the
                    numbers the corpus tables are built from, so drift here
                    propagates directly into every headline.
  exon share        the fraction of lines judged analytically load-bearing. A
                    systematic shift here would move coverage claims.
  residue           silent decisions and misalignments are the FINDINGS, and
                    they are defined as what fails to align -- a residue is
                    more fragile than the thing it is left over from, so it is
                    reported separately and expected to be noisier.

Usage:
    python3 stability/scripts/q1_distill.py --a <baseline/data/distilled>
                                            --b <replicate/data/distilled>
                                            [--json out.json]
"""
import argparse
import json
from collections import Counter
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import partition as P                                          # noqa: E402
import spanmatch as SM                                         # noqa: E402


def load_run(d):
    """record.json plus the two span files, which live beside it.

    Spans are NOT inside record.json -- it carries counts, coverage, and the
    two residues (silent decisions, misalignments). The spans are in
    code_spans.json / prose_spans.json as {"n_lines": N, "spans": [...]}.
    """
    d = Path(d)
    rec = d / "record.json"
    if not rec.exists():
        return None
    out = {"record": json.loads(rec.read_text(encoding="utf-8"))}
    for ch in ("code", "prose"):
        p = d / f"{ch}_spans.json"
        out[ch] = (json.loads(p.read_text(encoding="utf-8"))
                   if p.exists() else {"spans": []})
    return out


def line_groups(spans):
    """{line: span_id} -- the GROUPING of lines into spans.

    Span ids are assigned per build and carry no meaning across builds, so
    these labels must never be compared for equality. They are only ever fed to
    ARI, which asks whether two lines are in the SAME span in both builds and
    is invariant to how the spans are named.
    """
    lab = {}
    for s in spans or ():
        sid = str(s.get("id", ""))
        for a, b in _ranges(s):
            for ln in range(a, b + 1):
                lab[ln] = sid
    return lab


def line_kinds(spans):
    """{line: kind} -- exon/intron typing, from a controlled vocabulary.

    Unlike span ids these labels ARE comparable across builds: `decision` and
    `intron` mean the same thing in every run. This is the question "did both
    builds judge this line analytically load-bearing?", which is separate from
    "did both builds group it with the same neighbours?" and can move
    independently.
    """
    lab = {}
    for s in spans or ():
        k = s.get("kind", "?")
        for a, b in _ranges(s):
            for ln in range(a, b + 1):
                lab[ln] = k
    return lab


def _ranges(span):
    if "lines" in span and isinstance(span["lines"], list):
        for x in span["lines"]:
            if isinstance(x, (list, tuple)) and len(x) == 2:
                yield int(x[0]), int(x[1])
            elif isinstance(x, int):
                yield x, x
    elif "line_start" in span:
        yield int(span["line_start"]), int(span.get("line_end",
                                                    span["line_start"]))


def counts(run):
    """The numbers the corpus tables are built from.

    Read from record.json's own `counts`/`coverage` blocks rather than
    recomputed from the spans, so that what is compared here is exactly what
    every downstream stage consumes.
    """
    rec = run["record"]
    c = rec.get("counts", {})
    cov = (rec.get("coverage") or {}).get("code", {})
    return {
        "decisions": c.get("decisions", 0),
        "claims": c.get("claims", 0),
        "links": c.get("links", 0),
        "silent": len(rec.get("silent_decisions", [])),
        "misaligned": len(rec.get("misalignments", [])),
        "code_lines": cov.get("n_lines"),
        "exon_share": cov.get("functional_share"),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True, help="baseline data/distilled")
    ap.add_argument("--b", required=True, help="replicate data/distilled")
    ap.add_argument("--tau", type=float, default=SM.TAU,
                    help="lenient-match Jaccard floor on line sets")
    ap.add_argument("--json")
    x = ap.parse_args()
    tau = x.tau

    da, db = Path(x.a), Path(x.b)
    shared = sorted({p.name for p in da.iterdir() if p.is_dir()} &
                    {p.name for p in db.iterdir() if p.is_dir()})
    if not shared:
        sys.exit("no runs present in both trees")

    rows, agg = [], Counter()
    deltas = {k: [] for k in ("decisions", "claims", "links", "silent",
                              "misaligned")}
    aris, kagr, paris = [], [], []
    for name in shared:
        ra, rb = load_run(da / name), load_run(db / name)
        if not ra or not rb:
            continue
        ga, gb = line_groups(ra["code"]["spans"]), line_groups(rb["code"]["spans"])
        ka, kb = line_kinds(ra["code"]["spans"]), line_kinds(rb["code"]["spans"])
        keys = sorted(set(ga) & set(gb))
        # Grouping: ARI only -- span ids are not comparable across builds.
        ari = P.adjusted_rand(ga, gb, keys) if len(keys) > 1 else float("nan")
        # Typing: raw agreement is meaningful, the vocabulary is controlled.
        kk = sorted(set(ka) & set(kb))
        kag = (sum(1 for k in kk if ka[k] == kb[k]) / len(kk)) if kk else None
        # Prose is exhaustive but NOT exclusive, so it is compared on grouping
        # only, and reported separately -- one sentence may assert two things,
        # and a line can legitimately belong to two prose spans.
        pa, pb = (line_groups(ra["prose"]["spans"]),
                  line_groups(rb["prose"]["spans"]))
        pk = sorted(set(pa) & set(pb))
        pari = P.adjusted_rand(pa, pb, pk) if len(pk) > 1 else float("nan")

        # The lenient level: match DECISIONS across builds allowing boundaries
        # to move. This is the question downstream work depends on, and the gap
        # against the verbatim level is how much apparent instability is jitter.
        dec_a = [s for s in ra["code"]["spans"] if s.get("kind") == "decision"]
        dec_b = [s for s in rb["code"]["spans"] if s.get("kind") == "decision"]
        sm = SM.compare_spans(dec_a, dec_b, tau)

        ca, cb = counts(ra), counts(rb)
        row = {"run": name, "lines_shared": len(keys),
               "code_group_ari": round(ari, 4) if ari == ari else None,
               "code_kind_agreement": round(kag, 4) if kag is not None else None,
               "prose_group_ari": round(pari, 4) if pari == pari else None,
               "exon_share_a": ca["exon_share"], "exon_share_b": cb["exon_share"],
               "decision_verbatim_f1": sm["verbatim_f1"],
               "decision_lenient_f1": sm["lenient_f1"],
               "decision_core_f1": sm["core_f1"],
               "jitter_lines": sm["median_boundary_jitter_lines"],
               "text_overlap": sm["median_text_overlap_matched"],
               "_sm": sm}
        for k in deltas:
            row[f"{k}_a"], row[f"{k}_b"] = ca[k], cb[k]
            row[f"{k}_delta"] = (cb[k] or 0) - (ca[k] or 0)
            deltas[k].append(row[f"{k}_delta"])
        rows.append(row)
        if ari == ari:
            aris.append(ari)
        if kag is not None:
            kagr.append(kag)
        if pari == pari:
            paris.append(pari)
        agg["runs"] += 1

    def med(v):
        v = sorted(x for x in v if x is not None)
        return v[len(v) // 2] if v else None

    # Pool the decision-level matching over all runs rather than averaging
    # per-run F1s: a run with 30 decisions should weigh more than one with 8,
    # and averaging ratios silently equalises them.
    tot = {k: sum(r["_sm"][k] for r in rows)
           for k in ("n_a", "n_b", "verbatim_matched", "lenient_matched",
                     "core_matched")}
    vp, vr, vf = SM.prf(tot["verbatim_matched"], tot["n_a"], tot["n_b"])
    lp, lr, lf = SM.prf(tot["lenient_matched"], tot["n_a"], tot["n_b"])
    cp, cr, cf = SM.prf(tot["core_matched"], tot["n_a"], tot["n_b"])

    res = {
        "build_a": str(da), "build_b": str(db),
        "comparison_type": "replicate",
        "runs_compared": agg["runs"],
        "code_group_ari_mean": round(sum(aris) / len(aris), 4) if aris else None,
        "code_group_ari_median": med([r["code_group_ari"] for r in rows]),
        "code_group_ari_min": round(min(aris), 4) if aris else None,
        "code_kind_agreement_mean": round(sum(kagr) / len(kagr), 4) if kagr else None,
        "code_kind_agreement_median": med([r["code_kind_agreement"] for r in rows]),
        "prose_group_ari_mean": round(sum(paris) / len(paris), 4) if paris else None,
        "prose_group_ari_median": med([r["prose_group_ari"] for r in rows]),
        "decisions": {
            "tau": tau,
            "n_a": tot["n_a"], "n_b": tot["n_b"],
            "verbatim": {"matched": tot["verbatim_matched"],
                         "precision": vp, "recall": vr, "f1": vf},
            "lenient": {"matched": tot["lenient_matched"],
                        "precision": lp, "recall": lr, "f1": lf},
            "core": {"matched": tot["core_matched"],
                     "precision": cp, "recall": cr, "f1": cf},
            "jitter_share": (round((tot["lenient_matched"] -
                                    tot["verbatim_matched"])
                                   / tot["lenient_matched"], 4)
                             if tot["lenient_matched"] else None),
            "median_boundary_jitter_lines": med(
                [r["_sm"]["median_boundary_jitter_lines"] for r in rows]),
            "median_text_overlap": med([r["text_overlap"] for r in rows]),
        },
        "count_drift": {k: {"median_delta": med(v),
                            "mean_abs_delta": round(
                                sum(abs(d) for d in v) / len(v), 3) if v else None,
                            "runs_unchanged": sum(1 for d in v if d == 0),
                            "runs_changed": sum(1 for d in v if d != 0),
                            "total_a": sum(r[f"{k}_a"] or 0 for r in rows),
                            "total_b": sum(r[f"{k}_b"] or 0 for r in rows)}
                        for k, v in deltas.items()},
        "per_run": rows,
    }

    d = res["decisions"]
    print("Q1  DISTILLATION STABILITY")
    print(f"    runs compared                 {res['runs_compared']}\n")
    print(f"    DECISIONS  {d['n_a']} in A, {d['n_b']} in B "
          f"(tau={d['tau']})")
    print(f"      {'level':<10}{'matched':>9}{'prec':>8}{'recall':>8}{'F1':>8}"
          f"   {'question answered'}")
    for lvl, q in (("verbatim", "identical line sets"),
                   ("lenient", "same decision, boundary may move"),
                   ("core", "same decision, allowing split/absorb")):
        v = d[lvl]
        print(f"      {lvl:<10}{v['matched']:>9}{v['precision']:>8}"
              f"{v['recall']:>8}{v['f1']:>8}   {q}")
    print(f"      jitter share of lenient matches   {d['jitter_share']}"
          f"   <- apparent instability that is only boundary movement")
    print(f"      median boundary jitter (lines)    "
          f"{d['median_boundary_jitter_lines']}")
    print(f"      median text overlap, matched      "
          f"{d['median_text_overlap']}\n")
    print("    CODE channel (exhaustive + exclusive partition of lines)")
    print(f"      grouping ARI  mean/med/min  {res['code_group_ari_mean']} / "
          f"{res['code_group_ari_median']} / {res['code_group_ari_min']}")
    print(f"      exon/intron typing agree    {res['code_kind_agreement_mean']} "
          f"(median {res['code_kind_agreement_median']})")
    print("    PROSE channel (exhaustive, NOT exclusive)")
    print(f"      grouping ARI  mean/median   {res['prose_group_ari_mean']} / "
          f"{res['prose_group_ari_median']}\n")
    print(f"    {'field':<14}{'total A':>9}{'total B':>9}{'median d':>10}"
          f"{'mean |d|':>10}{'same':>7}{'moved':>7}")
    for k, v in res["count_drift"].items():
        print(f"    {k:<14}{v['total_a']:>9}{v['total_b']:>9}"
              f"{str(v['median_delta']):>10}{str(v['mean_abs_delta']):>10}"
              f"{v['runs_unchanged']:>7}{v['runs_changed']:>7}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n    wrote {x.json}")


if __name__ == "__main__":
    main()
