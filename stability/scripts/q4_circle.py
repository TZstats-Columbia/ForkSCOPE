#!/usr/bin/env python3
"""Q4 -- stability of the highways (strong fork-to-fork routes). No model calls.

A "highway" is a route between two forks walked by many runs -- the thick lines
in circle.html. The question is whether the same dyads carry the same traffic
across builds, and whether the persona enrichments on them reproduce.

THE MATCHING PROBLEM, AND WHY LABELS CANNOT SOLVE IT
----------------------------------------------------
Fork labels are re-induced on every build, so the same question comes back
worded differently -- "how are the two raters combined into a single skin-tone
exposure measure?" in one build and "how are the two independent raters'
skin-tone ratings reduced to a single value per player?" in another. Matching
on the label would score that as a miss.

But we do not have to match on labels. Both builds partition the SAME decision
instances (see partition.py), so a fork in A and a fork in B can be matched by
the instances they share. Each A-fork is mapped to the B-fork holding the most
of its instances, and the Jaccard overlap of that pairing is reported so a weak
match is visible rather than silently trusted. This is derived from the data,
costs nothing, and does not depend on any model agreeing about wording.

WHAT IS REPORTED
----------------
  dyad overlap    of the highways drawn in A, how many survive into B
  rank agreement  Spearman rho on traffic over the overlapping dyads -- the
                  question is whether the BUSY routes stay busy, not whether
                  the counts are identical
  enrichment      which (route, persona) enrichments reproduce

Persona enrichment should be read on the ai-only build: in a pooled build the
`human` label sits in the shuffle pool but no human run can carry a persona, so
every persona's expected share is diluted and enrichment is overstated.

Usage:
    python3 stability/scripts/q4_circle.py --circle-a A.json --circle-b B.json
        --vocab-a VA.json --vocab-b VB.json [--json out.json]
"""
import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import partition as P                                          # noqa: E402

SEED = 20260822
PERMS = 2000


def fork_members(path):
    """{fork_label: set(instance_key)} for one build."""
    lab, _ = P.labeling(path, "fork")
    out = defaultdict(set)
    for k, f in lab.items():
        out[f].add(k)
    return out


def match_forks(fa, fb):
    """A-fork -> (B-fork, jaccard, shared). Greedy best-overlap, not 1:1.

    Deliberately not a bijection. Forks legitimately split and merge between
    builds, and forcing a one-to-one assignment would hide exactly that. A
    many-to-one mapping is reported as such, and the Jaccard makes a weak or
    fragmented match visible.
    """
    m = {}
    for a, ka in fa.items():
        best, bj, bs = None, 0.0, 0
        for b, kb in fb.items():
            s = len(ka & kb)
            if not s:
                continue
            j = s / len(ka | kb)
            if s > bs or (s == bs and j > bj):
                best, bj, bs = b, j, s
        m[a] = (best, round(bj, 4), bs)
    return m


def edges(circle_path):
    """{(forkA, forkB): total_runs} plus enrichment records."""
    d = json.loads(Path(circle_path).read_text(encoding="utf-8"))
    e, enr = {}, []
    for rec in d.get("enrichment", ()):
        pair = tuple(rec["edge"])
        e[pair] = rec["edge_total"]
        if rec.get("enriched"):
            enr.append({"edge": pair, "persona": rec["persona"],
                        "n": rec["n"], "edge_total": rec["edge_total"],
                        "expected": rec.get("expected"), "p": rec.get("p")})
    return d, e, enr


def spearman(x, y):
    """Rank correlation, average ranks for ties. numpy-free."""
    def rank(v):
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
    if len(x) < 3:
        return float("nan")
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx and dy else float("nan")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--circle-a", required=True)
    ap.add_argument("--circle-b", required=True)
    ap.add_argument("--vocab-a", required=True)
    ap.add_argument("--vocab-b", required=True)
    ap.add_argument("--min-jaccard", type=float, default=0.5,
                    help="fork matches weaker than this are not trusted")
    ap.add_argument("--json")
    x = ap.parse_args()

    fa, fb = fork_members(x.vocab_a), fork_members(x.vocab_b)
    fmap = match_forks(fa, fb)
    strong = {a: v for a, v in fmap.items() if v[0] and v[1] >= x.min_jaccard}

    da, ea, enr_a = edges(x.circle_a)
    db, eb, enr_b = edges(x.circle_b)

    # Translate A's edges into B's fork space, then look them up in B.
    hit, miss, unmatched = {}, [], 0
    for (u, v), tot_a in ea.items():
        mu, mv = strong.get(u), strong.get(v)
        if not mu or not mv:
            unmatched += 1
            continue
        key = (mu[0], mv[0])
        tot_b = eb.get(key, eb.get((key[1], key[0])))
        if tot_b is None:
            miss.append({"edge_a": [u, v], "edge_b": list(key),
                         "total_a": tot_a})
        else:
            hit[(u, v)] = (tot_a, tot_b)

    ta = [a for a, _ in hit.values()]
    tb = [b for _, b in hit.values()]
    rho = spearman(ta, tb)

    # A rank correlation reported alone is not evidence. Traffic counts are
    # heavy-tailed -- a handful of highways carry an order of magnitude more
    # runs than the rest -- so even a poor correspondence can score high simply
    # by putting the big ones near the top. The null shuffles B's traffic
    # across the SAME matched dyads, which preserves both marginal
    # distributions exactly and destroys only the pairing being tested.
    rng = random.Random(SEED)
    shuffled, null_rho = list(tb), []
    for _ in range(PERMS):
        rng.shuffle(shuffled)
        null_rho.append(spearman(ta, shuffled))
    null_rho.sort()
    nm = sum(null_rho) / len(null_rho)
    nsd = (sum((v - nm) ** 2 for v in null_rho)
           / max(1, len(null_rho) - 1)) ** 0.5
    ge = sum(1 for v in null_rho if v >= rho)
    rho_p = (ge + 1) / (len(null_rho) + 1)
    rho_z = (rho - nm) / nsd if nsd > 1e-12 else None

    # Enrichment reproducibility, in B's fork space.
    def to_b(rec):
        mu, mv = strong.get(rec["edge"][0]), strong.get(rec["edge"][1])
        if not mu or not mv:
            return None
        return (tuple(sorted((mu[0], mv[0]))), rec["persona"])
    set_b = {(tuple(sorted(r["edge"])), r["persona"]) for r in enr_b}
    enr_rows = []
    for r in enr_a:
        k = to_b(r)
        enr_rows.append({**{kk: r[kk] for kk in ("persona", "n", "edge_total")},
                         "edge_a": list(r["edge"]),
                         "reproduced": bool(k and k in set_b),
                         "matchable": k is not None})

    res = {
        "circle_a": x.circle_a, "circle_b": x.circle_b,
        "corpus_a": da.get("corpus"), "corpus_b": db.get("corpus"),
        "runs_a": da.get("runs"), "runs_b": db.get("runs"),
        "nodes_a": da.get("nodes"), "nodes_b": db.get("nodes"),
        "routes_a": da.get("routes_drawn"), "routes_b": db.get("routes_drawn"),
        "forks_a": len(fa), "forks_b": len(fb),
        "forks_matched_strongly": len(strong),
        "fork_match_rate": round(len(strong) / len(fa), 4) if fa else 0,
        "median_jaccard": sorted(v[1] for v in fmap.values())[len(fmap) // 2]
                          if fmap else 0,
        "edges_a": len(ea), "edges_b": len(eb),
        "edges_unmatchable": unmatched,
        "edges_overlapping": len(hit),
        "edges_lost": len(miss),
        "dyad_overlap_rate": round(len(hit) / len(ea), 4) if ea else 0,
        "traffic_spearman": round(rho, 4),
        "traffic_spearman_null_mean": round(nm, 4),
        "traffic_spearman_null_sd": round(nsd, 4),
        "traffic_spearman_z": round(rho_z, 2) if rho_z else None,
        "traffic_spearman_p": round(rho_p, 4),
        "enriched_a": len(enr_a), "enriched_b": len(enr_b),
        "enriched_reproduced": sum(1 for r in enr_rows if r["reproduced"]),
        "enrichment_detail": enr_rows,
    }

    print("Q4  HIGHWAY STABILITY")
    print(f"    {res['corpus_a']}\n    {res['corpus_b']}\n")
    for k in ("runs_a", "runs_b", "nodes_a", "nodes_b", "routes_a", "routes_b",
              "forks_matched_strongly", "fork_match_rate", "median_jaccard",
              "edges_overlapping", "edges_lost", "edges_unmatchable",
              "dyad_overlap_rate", "traffic_spearman",
              "traffic_spearman_null_mean", "traffic_spearman_z",
              "traffic_spearman_p",
              "enriched_a", "enriched_b", "enriched_reproduced"):
        print(f"    {k:<24} {res[k]}")
    print("\n    persona enrichments in A:")
    for r in enr_rows:
        mark = "reproduced" if r["reproduced"] else (
            "LOST" if r["matchable"] else "unmatchable")
        print(f"      {r['persona']:<30} {r['n']:>3}/{r['edge_total']:<4} {mark}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n    wrote {x.json}")


if __name__ == "__main__":
    main()
