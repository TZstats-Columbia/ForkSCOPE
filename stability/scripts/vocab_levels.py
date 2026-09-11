#!/usr/bin/env python3
"""Vocabulary agreement at several strictness levels. No model calls.

`partition.py` reports ARI, VI and B-cubed. Those are *graded* -- a cluster that
differs by one instance loses a little, not everything -- but they are summary
statistics, and none of them answers the question a reader actually asks:

    how many of the 317 decision points came back the same?

That question has a different answer at every strictness level, exactly as it
did for distillation (`spanmatch.py`), and quoting one level without the others
is how a reproducibility number becomes misleading in either direction.

WHAT PARAPHRASE DOES AND DOES NOT AFFECT HERE
----------------------------------------------
Nothing in this module reads a cluster's LABEL. Clusters are compared by the
decision instances they contain, and the instances are identical across builds
by construction. So a fork re-worded from "how are the two raters combined?" to
"how are the two ratings reduced to one value?" is not penalised at all --
label paraphrase is invisible to every number below.

That is worth stating plainly because it is the opposite of the distillation
case, where boundary jitter was the dominant effect. Here the vocabulary can
rename everything and score 1.0; what it cannot do is move members between
clusters.

THE LEVELS
----------
  verbatim    identical member sets. "Would the two builds produce the same
              fork?" The strictest reading, and the one `stable_clusters`
              already reports.
  strict      Jaccard >= 0.9 -- the same fork, give or take an instance
  lenient     Jaccard >= 0.5 -- recognisably the same fork
  core        containment >= 0.5 of the smaller -- still matched when one build
              split a fork the other kept whole

Matching is greedy on descending overlap, one-to-one, deterministic.

Usage:
    python3 stability/scripts/vocab_levels.py --a A.json --b B.json
                                              --level fork [--json out]
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import partition as P                                          # noqa: E402

LEVELS = [("verbatim", "jaccard", 1.0),
          ("strict", "jaccard", 0.9),
          ("lenient", "jaccard", 0.5),
          ("core", "containment", 0.5)]


def clusters(path, level):
    lab, _ = P.labeling(path, level)
    out = defaultdict(set)
    for k, c in lab.items():
        out[c].add(k)
    return out


def match(ca, cb, kind, tau):
    """Greedy one-to-one matching of clusters at one strictness level."""
    cand = []
    for a, A in ca.items():
        for b, B in cb.items():
            inter = len(A & B)
            if not inter:
                continue
            s = (inter / len(A | B) if kind == "jaccard"
                 else inter / min(len(A), len(B)))
            if s >= tau:
                cand.append((-s, a, b))
    cand.sort(key=lambda t: (t[0], str(t[1]), str(t[2])))
    ua, ub, n = set(), set(), 0
    for _, a, b in cand:
        if a in ua or b in ub:
            continue
        ua.add(a)
        ub.add(b)
        n += 1
    return n


def dispersion(ca, cb, cover=0.9):
    """How many B clusters does each A cluster's membership land in?

    The matched/unmatched framing above is one-to-one, and that is too harsh
    for this pipeline in a specific and asymmetric way. If build B SPLITS a
    fork that build A kept whole, one-to-one matching pairs A's fork with one
    half, leaves the other half unmatched, and may fail the Jaccard threshold
    on the pair it did make -- three penalties for one event.

    But a split is not the failure the project cares about. Its whole design
    rests on over-merge being invisible and unrecoverable while under-merge is
    visible and fixable. A fork that came back as two forks is intact
    information at a finer grain; a fork whose members SCATTERED across many
    unrelated forks is genuine disagreement about what the question is.

    So: for each A cluster, count the minimum number of B clusters needed to
    hold `cover` of its members.

        1        intact -- same question, possibly absorbed into a larger one
        2-3      split  -- recoverable, and the direction the pipeline prefers
        4+       scattered -- the members no longer travel together at all

    Reported both directions, because A-split-by-B and B-split-by-A are
    different events and averaging them hides which build was finer.
    """
    def one_way(src, dst):
        hist = Counter()
        for members in src.values():
            if not members:
                continue
            overlaps = Counter()
            for name, other in dst.items():
                k = len(members & other)
                if k:
                    overlaps[name] = k
            need, acc, target = 0, 0, cover * len(members)
            for _, k in overlaps.most_common():
                acc += k
                need += 1
                if acc >= target:
                    break
            hist[min(need, 4) if need else 0] += 1
        return hist

    out = {}
    for tag, (s, d) in (("a_in_b", (ca, cb)), ("b_in_a", (cb, ca))):
        h = one_way(s, d)
        n = sum(h.values())
        out[tag] = {
            "intact_1": h[1], "split_2_3": h[2] + h[3],
            "scattered_4plus": h[4], "unplaced": h[0], "n": n,
            "intact_or_split_rate": round((h[1] + h[2] + h[3]) / n, 4)
            if n else None,
        }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--level", choices=["option", "fork"], default="fork")
    ap.add_argument("--json")
    x = ap.parse_args()

    ca, cb = clusters(x.a, x.level), clusters(x.b, x.level)
    # Restrict to instances present in both, so the comparison is over one
    # item set rather than two overlapping ones.
    shared = set().union(*ca.values()) & set().union(*cb.values())
    ca = {k: (v & shared) for k, v in ca.items() if v & shared}
    cb = {k: (v & shared) for k, v in cb.items() if v & shared}

    rows = []
    for name, kind, tau in LEVELS:
        m = match(ca, cb, kind, tau)
        p = m / len(cb) if cb else 0.0
        r = m / len(ca) if ca else 0.0
        f = 2 * p * r / (p + r) if (p + r) else 0.0
        rows.append({"level": name, "rule": f"{kind} >= {tau}", "matched": m,
                     "precision": round(p, 4), "recall": round(r, 4),
                     "f1": round(f, 4)})

    disp = dispersion(ca, cb)
    res = {"build_a": x.a, "build_b": x.b, "comparison_type": "replicate",
           "level": x.level, "instances": len(shared),
           "clusters_a": len(ca), "clusters_b": len(cb),
           "label_paraphrase_penalised": False,
           "levels": rows, "dispersion": disp}

    print(f"{x.level.upper()} agreement by strictness  "
          f"({len(ca)} in A, {len(cb)} in B, {len(shared)} instances)\n")
    print(f"  {'level':<10}{'rule':<20}{'matched':>9}{'prec':>8}"
          f"{'recall':>8}{'F1':>8}")
    for r in rows:
        print(f"  {r['level']:<10}{r['rule']:<20}{r['matched']:>9}"
              f"{r['precision']:>8}{r['recall']:>8}{r['f1']:>8}")
    print(f"\n  DISPERSION -- clusters of the other build holding 90% of each")
    print(f"  {'direction':<12}{'intact':>8}{'split 2-3':>11}"
          f"{'scattered':>11}{'intact+split':>14}")
    for tag, dd in disp.items():
        print(f"  {tag:<12}{dd['intact_1']:>8}{dd['split_2_3']:>11}"
              f"{dd['scattered_4plus']:>11}"
              f"{dd['intact_or_split_rate']:>14}")
    print(f"\n  a split is not the failure this pipeline cares about: "
          f"under-merge is\n  visible and fixable, over-merge is not. "
          f"'scattered' is the real signal.")
    print(f"\n  label paraphrase is NOT penalised: clusters are compared by "
          f"membership,\n  never by name.")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")


if __name__ == "__main__":
    main()
