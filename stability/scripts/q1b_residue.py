#!/usr/bin/env python3
"""Does boundary jitter reach the residues and the option layer? No model calls.

The natural hope, once boundary jitter is understood, is that it stops at the
segmentation: option merging and silent-decision detection are both SEMANTIC
steps -- they compare descriptions, not line numbers -- so jitter ought to wash
out before it reaches them.

That hope is right about the mechanism and can still be wrong about the effect,
for two different reasons, and this script tests each separately.

  OPTION LAYER.  Merging never reads a line number, so jitter cannot affect it
  directly. But merging consumes the decision's DESCRIPTION, and a description
  describes whatever lines the span covers. Move the boundary and the sentence
  can change -- ``average the two raters'' becomes ``average the two raters and
  drop incomplete dyads''. The input to the semantic step is therefore not
  invariant to jitter even though the step itself is. Measured here as the text
  agreement of decisions that matched on lines.

  RESIDUES.  Silent decisions and misalignments are not extracted; they are
  what is LEFT OVER after aligning two channels. A residue inherits the
  instability of both channels and of the alignment, and it has a structural
  sensitivity the extraction does not: split one decision in two and only one
  half aligns to a claim, and a silent decision appears that no one's judgement
  changed to create. So a residue can move even when both channels are stable.

Both are reported at the same verbatim/lenient levels used for decisions, so
the numbers are comparable across layers.

Usage:
    python3 stability/scripts/q1b_residue.py --a <A/data/distilled>
                                             --b <B/data/distilled> [--json out]
"""
import argparse
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import spanmatch as SM                                         # noqa: E402


def load(d):
    d = Path(d)
    if not (d / "record.json").exists():
        return None
    out = {"record": json.loads((d / "record.json").read_text(encoding="utf-8"))}
    for ch in ("code", "prose"):
        p = d / f"{ch}_spans.json"
        out[ch] = (json.loads(p.read_text(encoding="utf-8"))
                   if p.exists() else {"spans": []})
    return out


def as_spans(items, line_key="lines", text_keys=("operation", "note", "claim")):
    """Coerce residue records into the shape spanmatch expects."""
    out = []
    for it in items or ():
        s = {}
        if isinstance(it.get(line_key), list):
            s["lines"] = it[line_key]
        elif "line_start" in it:
            s["line_start"] = it["line_start"]
            s["line_end"] = it.get("line_end", it["line_start"])
        elif isinstance(it.get("lines"), int):
            s["lines"] = [[it["lines"], it["lines"]]]
        for k in text_keys:
            if it.get(k):
                s["note"] = it[k]
                break
        out.append(s)
    return out


def text_only_match(items_a, items_b, tau=0.4):
    """Match on description alone, for residues that carry no line reference.

    Lexical, so it is a floor rather than an estimate: two records describing
    the same operation in different words score low here and would be matched
    by a human or a model. Reported as such.
    """
    ta = [SM.tokens((i.get("operation") or i.get("note") or
                     i.get("claim") or "")) for i in items_a or ()]
    tb = [SM.tokens((i.get("operation") or i.get("note") or
                     i.get("claim") or "")) for i in items_b or ()]
    cand = []
    for i, A in enumerate(ta):
        for j, B in enumerate(tb):
            if A and B and (A & B):
                s = len(A & B) / len(A | B)
                if s >= tau:
                    cand.append((-s, i, j))
    cand.sort()
    ua, ub, n = set(), set(), 0
    for neg, i, j in cand:
        if i in ua or j in ub:
            continue
        ua.add(i)
        ub.add(j)
        n += 1
    return n, len(ta), len(tb)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--tau", type=float, default=SM.TAU)
    ap.add_argument("--json")
    x = ap.parse_args()

    da, db = Path(x.a), Path(x.b)
    shared = sorted({p.name for p in da.iterdir() if p.is_dir()} &
                    {p.name for p in db.iterdir() if p.is_dir()})

    agg = {k: 0 for k in
           ("runs", "dec_a", "dec_b", "dec_lenient", "dec_text_agree",
            "sil_a", "sil_b", "sil_match", "sil_match_lines", "sil_match_core",
            "mis_a", "mis_b", "mis_match")}
    txt_scores = []

    for name in shared:
        ra, rb = load(da / name), load(db / name)
        if not ra or not rb:
            continue
        agg["runs"] += 1

        # --- option-layer input: do line-matched decisions describe the same
        #     operation? This is what merging actually reads.
        dec_a = [s for s in ra["code"]["spans"] if s.get("kind") == "decision"]
        dec_b = [s for s in rb["code"]["spans"] if s.get("kind") == "decision"]
        pairs, _, _ = SM.greedy_match(dec_a, dec_b, SM.jaccard)
        agg["dec_a"] += len(dec_a)
        agg["dec_b"] += len(dec_b)
        for i, j, s in pairs:
            if s < x.tau:
                continue
            agg["dec_lenient"] += 1
            t = SM.text_overlap(dec_a[i], dec_b[j])
            if t is not None:
                txt_scores.append(t)
                if t >= 0.5:
                    agg["dec_text_agree"] += 1

        # --- residues
        # Silent decisions carry `lines`, so they can be matched STRUCTURALLY
        # as well as lexically. Line matching is the better signal: it asks
        # "did both builds flag the same operation as unmentioned?" without
        # depending on the two builds phrasing it alike. Text matching is kept
        # as a floor for comparison.
        sa = ra["record"].get("silent_decisions", [])
        sb = rb["record"].get("silent_decisions", [])
        agg["sil_a"] += len(sa)
        agg["sil_b"] += len(sb)
        pairs, _, _ = SM.greedy_match(as_spans(sa), as_spans(sb), SM.jaccard)
        agg["sil_match_lines"] += sum(1 for _, _, s in pairs if s >= x.tau)
        cp, _, _ = SM.greedy_match(as_spans(sa), as_spans(sb), SM.containment)
        agg["sil_match_core"] += sum(1 for _, _, s in cp if s >= x.tau)
        n, _, _ = text_only_match(sa, sb)
        agg["sil_match"] += n

        ma = ra["record"].get("misalignments", [])
        mb = rb["record"].get("misalignments", [])
        n, na, nb = text_only_match(ma, mb)
        agg["mis_a"] += na
        agg["mis_b"] += nb
        agg["mis_match"] += n

    def f1(m, a, b):
        p = m / b if b else 0.0
        r = m / a if a else 0.0
        return round(2 * p * r / (p + r), 4) if (p + r) else 0.0

    txt_scores.sort()
    res = {
        "build_a": str(da), "build_b": str(db),
        "comparison_type": "replicate",
        "runs_compared": agg["runs"],
        "option_layer_input": {
            "decisions_matched_on_lines": agg["dec_lenient"],
            "of_those_text_agrees": agg["dec_text_agree"],
            "text_agreement_rate": (round(agg["dec_text_agree"]
                                          / agg["dec_lenient"], 4)
                                    if agg["dec_lenient"] else None),
            "median_text_overlap": (round(txt_scores[len(txt_scores) // 2], 4)
                                    if txt_scores else None),
            "note": ("lexical overlap of descriptions for decisions that DID "
                     "match on lines; a floor, not an estimate"),
        },
        "silent_decisions": {
            "n_a": agg["sil_a"], "n_b": agg["sil_b"],
            "matched_on_lines": agg["sil_match_lines"],
            "f1_lines": f1(agg["sil_match_lines"], agg["sil_a"], agg["sil_b"]),
            "matched_core": agg["sil_match_core"],
            "f1_core": f1(agg["sil_match_core"], agg["sil_a"], agg["sil_b"]),
            "matched_on_text": agg["sil_match"],
            "f1_text": f1(agg["sil_match"], agg["sil_a"], agg["sil_b"]),
        },
        "misalignments": {
            "n_a": agg["mis_a"], "n_b": agg["mis_b"],
            "matched_on_text": agg["mis_match"],
            "f1": f1(agg["mis_match"], agg["mis_a"], agg["mis_b"]),
        },
    }

    o, s, m = (res["option_layer_input"], res["silent_decisions"],
               res["misalignments"])
    print("Q1b  DOES JITTER REACH THE SEMANTIC LAYERS?\n")
    print(f"    runs compared  {res['runs_compared']}\n")
    print("    OPTION-LAYER INPUT  (what merging reads)")
    print(f"      decisions matched on lines        {o['decisions_matched_on_lines']}")
    print(f"      of those, descriptions agree      {o['of_those_text_agrees']}"
          f"  ({o['text_agreement_rate']})")
    print(f"      median text overlap               {o['median_text_overlap']}")
    print(f"      -> merging is semantic, but its INPUT is not invariant to")
    print(f"         where the boundary was drawn\n")
    print("    RESIDUES  (what is left over after aligning two channels)")
    print(f"      {'':<18}{'A':>6}{'B':>6}{'matched':>9}{'F1':>8}")
    print(f"      {'silent (lines)':<18}{s['n_a']:>6}{s['n_b']:>6}"
          f"{s['matched_on_lines']:>9}{s['f1_lines']:>8}")
    print(f"      {'silent (core)':<18}{s['n_a']:>6}{s['n_b']:>6}"
          f"{s['matched_core']:>9}{s['f1_core']:>8}")
    print(f"      {'silent (text)':<18}{s['n_a']:>6}{s['n_b']:>6}"
          f"{s['matched_on_text']:>9}{s['f1_text']:>8}")
    print(f"      {'misalignments':<18}{m['n_a']:>6}{m['n_b']:>6}"
          f"{m['matched_on_text']:>9}{m['f1']:>8}")
    print(f"      -> a residue inherits the instability of BOTH channels and")
    print(f"         of the alignment, and can move even when both are stable")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n    wrote {x.json}")


if __name__ == "__main__":
    main()
