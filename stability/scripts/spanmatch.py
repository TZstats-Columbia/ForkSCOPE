#!/usr/bin/env python3
"""Match extracted spans across two builds at several strictness levels.

THE MEASUREMENT PROBLEM
-----------------------
Ask a model to segment the same script twice and it will find substantially the
same operations while drawing slightly different boundaries around them: a
decision spanning lines 44-51 in one build spans 44-52 in the other, because the
blank line or the trailing `print` was judged part of the operation or not.

Every strict partition metric -- ARI, Variation of Information, exact line
agreement -- charges that one-line difference at close to the same rate as it
would charge finding a completely different decision. So a strict score answers
"did the two builds draw identical boundaries?" when the question that actually
matters downstream is "did the two builds find the same decisions?"

Those are different questions and they have different answers. Reporting only
the first understates stability; reporting only the second hides real
segmentation drift. This module reports BOTH, and the gap between them is
itself the finding: it quantifies how much of the apparent instability is
boundary jitter rather than disagreement about what the analysis did.

FOUR LEVELS, EACH ANSWERING A DIFFERENT QUESTION
------------------------------------------------
  verbatim   identical line sets. "Would the two builds produce byte-identical
             artifacts?" The strictest, and the only one that guarantees
             downstream files match.
  lenient    Jaccard of line sets >= TAU (default 0.5). "Did both builds find
             this decision, allowing the boundary to move?" This is the level
             downstream work actually depends on.
  core       overlap >= TAU of the SMALLER span. Deliberately asymmetric: it
             still matches when one build splits a decision the other kept
             whole, or absorbs an adjacent line. Catches containment that
             Jaccard penalises for the size difference alone.
  text       token overlap of the span descriptions, for pairs already matched
             on lines. A weak proxy for "and they describe the same operation",
             reported as a check rather than a claim -- it is lexical, so it is
             evidence against a match, not proof of one.

Matching is greedy on descending overlap: repeatedly take the best remaining
pair and remove both. This is deterministic and close to optimal for the sparse,
near-diagonal overlap structure two segmentations of one script produce; a full
maximum-weight bipartite matching would differ only in rare ties and is not
worth the dependency.

WHAT IS NOT CLAIMED
-------------------
None of this is semantic adjudication. Line overlap is a structural proxy, and
token overlap is lexical. Two spans can overlap heavily and mean different
things. The honest use is to reduce the number of pairs a model (or a person)
has to judge -- the same pattern the ablation gate uses -- not to replace that
judgement.
"""
import argparse
import json
import re
from pathlib import Path

TAU = 0.5
_WORD = re.compile(r"[a-z0-9_]+")
# Tokens carried by nearly every description, so their overlap is not evidence
# that two spans describe the same operation.
_STOP = frozenset("""a an the and or of to in on for with from by as is are be
was were this that these those it its at into over under then than so if when
which what how use used using apply applied set sets compute computed
calculate calculated data value values column columns row rows""".split())


# ---------- primitives -------------------------------------------------------
def line_set(span):
    """The set of source lines a span covers."""
    out = set()
    lines = span.get("lines")
    if isinstance(lines, list):
        for x in lines:
            if isinstance(x, (list, tuple)) and len(x) == 2:
                out.update(range(int(x[0]), int(x[1]) + 1))
            elif isinstance(x, int):
                out.add(x)
    elif "line_start" in span:
        out.update(range(int(span["line_start"]),
                         int(span.get("line_end", span["line_start"])) + 1))
    return out


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0


def containment(a, b):
    """Overlap as a fraction of the smaller set.

    Asymmetric where Jaccard is not: a 3-line span wholly inside a 30-line one
    scores 1.0 here and 0.1 by Jaccard. That is the right behaviour when one
    build split a decision the other kept whole -- the smaller span was still
    found, not missed.
    """
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def tokens(text):
    return {t for t in _WORD.findall((text or "").lower())
            if t not in _STOP and len(t) > 2}


def text_overlap(sa, sb):
    ta = tokens(sa.get("note") or sa.get("operation") or "")
    tb = tokens(sb.get("note") or sb.get("operation") or "")
    if not ta or not tb:
        return None
    return len(ta & tb) / len(ta | tb)


# ---------- matching ---------------------------------------------------------
def greedy_match(spans_a, spans_b, score=jaccard, floor=0.0):
    """[(i, j, score)] plus unmatched indices, greedy on descending score.

    Deterministic: ties broken by index order, so the same inputs always give
    the same matching regardless of dict iteration order.
    """
    la = [line_set(s) for s in spans_a]
    lb = [line_set(s) for s in spans_b]
    cand = []
    for i, A in enumerate(la):
        for j, B in enumerate(lb):
            if A & B:                       # no overlap, no candidate
                s = score(A, B)
                if s > floor:
                    cand.append((-s, i, j))
    cand.sort()
    used_a, used_b, pairs = set(), set(), []
    for neg, i, j in cand:
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        pairs.append((i, j, -neg))
    return (pairs,
            [i for i in range(len(spans_a)) if i not in used_a],
            [j for j in range(len(spans_b)) if j not in used_b])


def prf(n_match, n_a, n_b):
    p = n_match / n_b if n_b else 0.0       # of B's spans, how many are real
    r = n_match / n_a if n_a else 0.0       # of A's spans, how many B found
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return round(p, 4), round(r, 4), round(f, 4)


def compare_spans(spans_a, spans_b, tau=TAU):
    """All four levels for one pair of span lists."""
    la = [line_set(s) for s in spans_a]
    lb = [line_set(s) for s in spans_b]
    n_a, n_b = len(spans_a), len(spans_b)

    pairs, un_a, un_b = greedy_match(spans_a, spans_b, jaccard)
    verbatim = [(i, j, s) for i, j, s in pairs if s >= 0.999]
    lenient = [(i, j, s) for i, j, s in pairs if s >= tau]

    cpairs, cun_a, cun_b = greedy_match(spans_a, spans_b, containment)
    core = [(i, j, s) for i, j, s in cpairs if s >= tau]

    # Boundary jitter, measured only on pairs that DID match leniently. This is
    # the quantity that separates "found the same decision, drew it slightly
    # differently" from "found a different decision".
    jit = sorted(len(la[i] ^ lb[j]) for i, j, _ in lenient)
    jac = sorted(s for _, _, s in lenient)
    txt = [t for t in (text_overlap(spans_a[i], spans_b[j])
                       for i, j, _ in lenient) if t is not None]

    def med(v):
        return round(v[len(v) // 2], 4) if v else None

    vp, vr, vf = prf(len(verbatim), n_a, n_b)
    lp, lr, lf = prf(len(lenient), n_a, n_b)
    cp, cr, cf = prf(len(core), n_a, n_b)
    return {
        "n_a": n_a, "n_b": n_b, "tau": tau,
        "verbatim_matched": len(verbatim),
        "verbatim_precision": vp, "verbatim_recall": vr, "verbatim_f1": vf,
        "lenient_matched": len(lenient),
        "lenient_precision": lp, "lenient_recall": lr, "lenient_f1": lf,
        "core_matched": len(core),
        "core_precision": cp, "core_recall": cr, "core_f1": cf,
        "unmatched_a": n_a - len(lenient), "unmatched_b": n_b - len(lenient),
        "median_jaccard_matched": med(jac),
        "median_boundary_jitter_lines": med(jit),
        "mean_boundary_jitter_lines": (round(sum(jit) / len(jit), 2)
                                       if jit else None),
        "median_text_overlap_matched": med(sorted(txt)),
        # The headline of this module: how much apparent instability is jitter.
        "jitter_share": (round((len(lenient) - len(verbatim)) / len(lenient), 4)
                         if lenient else None),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True, help="build A *_spans.json")
    ap.add_argument("--b", required=True, help="build B *_spans.json")
    ap.add_argument("--kind", default="decision",
                    help="span kind to compare, or 'all'")
    ap.add_argument("--tau", type=float, default=TAU)
    x = ap.parse_args()

    def load(p):
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        sp = d["spans"] if isinstance(d, dict) else d
        return sp if x.kind == "all" else [s for s in sp
                                           if s.get("kind") == x.kind]

    res = compare_spans(load(x.a), load(x.b), x.tau)
    w = max(len(k) for k in res)
    for k, v in res.items():
        print(f"  {k:<{w}}  {v}")


if __name__ == "__main__":
    main()
