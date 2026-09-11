#!/usr/bin/env python3
"""Partition-agreement metrics over a fixed item set. No model calls.

The whole point of this module is that two vocabulary builds, however
differently they label things, are both *partitions of the same decision
instances*. The distilled records are byte-identical across builds, so the
instance set is fixed and the comparison needs no semantic matching at all --
it is exact arithmetic on two labelings of one item set.

That matters because the obvious alternative (match option labels by string or
embedding similarity, then count matches) imports exactly the failure this
project rejects for clustering: 95% of option labels are unique, so a lexical
match rate measures phrasing, not agreement.

Three metrics, because they fail differently:

  ARI    Adjusted Rand Index. Chance-corrected agreement on whether each PAIR
         of instances is co-clustered. Robust, symmetric, 0 at chance, 1 at
         identity. Insensitive to how the disagreement is shaped.
  VI     Variation of Information. H(A|B) + H(B|A), in bits. A true metric on
         the space of partitions, so it obeys the triangle inequality -- which
         ARI does not, and which matters once there are three builds to compare.
         Lower is better; 0 is identity.
  B3     B-cubed precision/recall/F1. Per-instance, so it decomposes: precision
         below recall means build B split things build A had together;
         recall below precision means B merged them. This is the one that says
         WHICH DIRECTION the vocabulary moved, which is what the audit hook and
         the split-never-merge rule care about.

Usage:
    python3 stability/scripts/partition.py --a <vocabA.json> --b <vocabB.json>
                                           --level option|fork [--json out.json]
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from math import log2
from pathlib import Path


# ---------- loading ---------------------------------------------------------
def instance_keys(vocab):
    """Stable per-decision identity: (run, line, text-prefix).

    `members` in the options array are integer indices into `decisions`, and
    those indices are only meaningful WITHIN one file. Two builds order their
    decisions array the same way today, but relying on that would make the
    comparison silently wrong the day it changes. The key is derived from
    content instead: run id and source line pin an instance, and a short text
    prefix breaks the rare tie of two decisions extracted from one line.
    """
    keys = []
    for d in vocab["decisions"]:
        keys.append((d["run"], d.get("line", -1), (d.get("text") or "")[:60]))
    return keys


def labeling(path, level):
    """{instance_key: cluster_label} for one build at one level.

    An instance not claimed by any option is left out rather than given a
    singleton label. A singleton would be a claim -- "this decision stands
    alone" -- and the absence of an assignment is not that claim; it is the
    build declining to place it. Coverage is reported separately so the
    exclusion is visible rather than absorbed into the metric.
    """
    vocab = json.loads(Path(path).read_text(encoding="utf-8"))
    keys = instance_keys(vocab)
    lab = {}
    for opt in vocab["options"]:
        label = opt["option"] if level == "option" else opt["fork"]
        for m in opt.get("members", ()):
            if 0 <= m < len(keys):
                lab[keys[m]] = label
    return lab, len(keys)


# ---------- metrics ---------------------------------------------------------
def contingency(a, b, keys):
    n = defaultdict(Counter)
    for k in keys:
        n[a[k]][b[k]] += 1
    return n


def adjusted_rand(a, b, keys):
    """Chance-corrected pair agreement.

    ARI = (RI - E[RI]) / (max RI - E[RI]), computed from the contingency table
    in the standard comb-of-2 form. Returns 1.0 for identical partitions and
    ~0 for independent ones (it can go slightly negative -- worse than chance).
    """
    def c2(x):
        return x * (x - 1) / 2

    n = len(keys)
    if n < 2:
        return float("nan")
    tab = contingency(a, b, keys)
    sum_ij = sum(c2(v) for row in tab.values() for v in row.values())
    ra = Counter()
    rb = Counter()
    for k in keys:
        ra[a[k]] += 1
        rb[b[k]] += 1
    sum_a = sum(c2(v) for v in ra.values())
    sum_b = sum(c2(v) for v in rb.values())
    exp = sum_a * sum_b / c2(n)
    mx = (sum_a + sum_b) / 2
    return (sum_ij - exp) / (mx - exp) if mx != exp else 1.0


def variation_of_information(a, b, keys):
    """H(A|B) + H(B|A) in bits. A metric: obeys the triangle inequality.

    Also returned normalised by log2(n), which bounds it to [0,1] and makes it
    comparable across item sets of different size -- necessary here because the
    pooled and ai-only instance sets differ.
    """
    n = len(keys)
    if n == 0:
        return float("nan"), float("nan")
    ra, rb = Counter(), Counter()
    joint = Counter()
    for k in keys:
        ra[a[k]] += 1
        rb[b[k]] += 1
        joint[(a[k], b[k])] += 1
    hab = 0.0
    for (x, y), v in joint.items():
        p = v / n
        hab -= p * log2(p)
    ha = -sum((v / n) * log2(v / n) for v in ra.values())
    hb = -sum((v / n) * log2(v / n) for v in rb.values())
    vi = 2 * hab - ha - hb          # = H(A|B) + H(B|A)
    return vi, (vi / log2(n) if n > 1 else 0.0)


def bcubed(a, b, keys):
    """Per-instance precision/recall/F1, treating A as reference.

    precision_i = |A(i) & B(i)| / |B(i)|   -- how pure B's cluster is
    recall_i    = |A(i) & B(i)| / |A(i)|   -- how much of A's cluster B kept

    Precision > recall  =>  B SPLIT what A held together. B's clusters are
        small and pure (high precision) but no longer contain everything A put
        with them (low recall).
    Recall > precision  =>  B MERGED what A held apart. B's clusters keep all
        of A's members (high recall) but drag in foreign ones (low precision).

    Cross-check the verdict against the cluster counts: a genuine split raises
    the cluster count. If the two disagree, the metric is being read backwards.
    """
    ca, cb = defaultdict(set), defaultdict(set)
    for k in keys:
        ca[a[k]].add(k)
        cb[b[k]].add(k)
    p = r = 0.0
    for k in keys:
        inter = len(ca[a[k]] & cb[b[k]])
        p += inter / len(cb[b[k]])
        r += inter / len(ca[a[k]])
    n = len(keys)
    p, r = p / n, r / n
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


def merge_split_events(a, b, keys):
    """Count clusters that fragmented or fused, and the instances involved.

    A cluster of A that lands in >1 cluster of B is a SPLIT; several clusters of
    A landing in one cluster of B is a MERGE. Reported as counts of clusters and
    of instances, because one huge split and twenty tiny ones are different
    events and a cluster count alone conflates them.
    """
    tab = contingency(a, b, keys)
    rev = defaultdict(Counter)
    for x, row in tab.items():
        for y, v in row.items():
            rev[y][x] += v
    split = {x: dict(row) for x, row in tab.items() if len(row) > 1}
    merge = {y: dict(row) for y, row in rev.items() if len(row) > 1}
    return {
        "clusters_a": len(tab),
        "clusters_b": len(rev),
        "split_clusters": len(split),
        "split_instances": sum(sum(r.values()) - max(r.values())
                               for r in split.values()),
        "merge_clusters": len(merge),
        "merge_instances": sum(sum(r.values()) - max(r.values())
                               for r in merge.values()),
        "stable_clusters": sum(1 for x, row in tab.items() if len(row) == 1
                               and len(rev[next(iter(row))]) == 1),
    }


def direction(p, r, n_a, n_b, tol=0.02):
    """Which way the vocabulary moved, from two independent signals.

    B-cubed asymmetry says it (precision above recall => B finer); so does the
    raw cluster count. They are derived differently, so when they disagree the
    honest answer is that neither is trustworthy -- typically because |p - r|
    is inside the noise. Asserting a direction from a 0.01 gap is how a
    rounding artifact becomes a reported finding, so the disagreement is
    surfaced instead of resolved.
    """
    if p > r + tol:
        by_b3 = "finer"
    elif r > p + tol:
        by_b3 = "coarser"
    else:
        by_b3 = "balanced"
    by_count = ("finer" if n_b > n_a else
                "coarser" if n_b < n_a else "balanced")
    agree = by_b3 == by_count
    if by_b3 == "balanced":
        verdict = f"balanced (|p-r| <= {tol}); cluster count says {by_count}"
    elif agree:
        verdict = f"B {by_b3} than A (both signals agree)"
    else:
        verdict = (f"AMBIGUOUS: b-cubed says {by_b3}, cluster count says "
                   f"{by_count} -- do not report a direction")
    return {"direction": verdict,
            "direction_by_bcubed": by_b3,
            "direction_by_count": by_count,
            "direction_signals_agree": agree}


# ---------- driver ----------------------------------------------------------
def compare(path_a, path_b, level):
    la, na = labeling(path_a, level)
    lb, nb = labeling(path_b, level)
    keys = sorted(set(la) & set(lb))
    if not keys:
        sys.exit(f"no shared instances between {path_a} and {path_b}")
    ari = adjusted_rand(la, lb, keys)
    vi, vin = variation_of_information(la, lb, keys)
    p, r, f = bcubed(la, lb, keys)
    ev = merge_split_events(la, lb, keys)
    return {
        "level": level,
        "build_a": str(path_a), "build_b": str(path_b),
        "instances_a": na, "instances_b": nb,
        "assigned_a": len(la), "assigned_b": len(lb),
        "shared": len(keys),
        "coverage_a": round(len(la) / na, 4) if na else 0,
        "coverage_b": round(len(lb) / nb, 4) if nb else 0,
        "ari": round(ari, 4),
        "vi_bits": round(vi, 4),
        "vi_normalised": round(vin, 4),
        "bcubed_precision": round(p, 4),
        "bcubed_recall": round(r, 4),
        "bcubed_f1": round(f, 4),
        **direction(p, r, ev["clusters_a"], ev["clusters_b"]),
        **ev,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True, help="build A vocabulary json")
    ap.add_argument("--b", required=True, help="build B vocabulary json")
    ap.add_argument("--level", choices=["option", "fork"], default="option")
    ap.add_argument("--json", help="write result here")
    x = ap.parse_args()
    res = compare(x.a, x.b, x.level)
    w = max(len(k) for k in res)
    for k, v in res.items():
        print(f"  {k:<{w}}  {v}")
    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\nwrote {x.json}")


if __name__ == "__main__":
    main()
