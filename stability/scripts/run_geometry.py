#!/usr/bin/env python3
"""Does the corpus GEOMETRY reproduce? Distance correlation between builds.

No model calls.

WHY THIS IS BETTER THAN EVERY CLUSTER-MATCHING MEASURE HERE
-----------------------------------------------------------
Every other comparison in this folder needs a correspondence between two
builds' clusters, and building that correspondence is where all the difficulty
has been: one-to-one matching punishes splits, Jaccard punishes merges,
containment is permissive, and the threshold changes the answer. Four separate
measurements in this folder were understated by a matching choice before being
corrected.

This measure needs no correspondence whatever. The RUNS are shared between
builds -- same 223 identifiers, same analyses -- so instead of asking "is A's
fork the same object as B's fork", it asks

    do runs that look similar under A's vocabulary also look similar under B's?

Labels never meet. A build may rename every fork, split half of them and merge
the rest, and if the induced similarity between runs is preserved, the geometry
of the multiverse is the same and every analysis computed over it stands.

THE CONSTRUCTION
----------------
For a build and a level (option or fork), each run is the SET of clusters it
touches. Distance between two runs is Jaccard distance on those sets. That
gives one run x run matrix per (build, level), and the question becomes the
association between two distance matrices on the same objects.

Two statistics, because they answer slightly different questions:

  Mantel r   Pearson correlation over the off-diagonal entries. The classical
             choice, directly interpretable: do the same pairs of runs sit
             close together in both builds?

  dCor       distance correlation on doubly-centred matrices (Szekely). Picks
             up non-linear association a Pearson correlation misses, and is
             invariant to the monotone rescalings that differ between builds
             when one has systematically more clusters than the other -- which
             is exactly this corpus's situation (317 forks against 351).

Both against a permutation null that shuffles RUN LABELS in one matrix. That
holds each build's internal structure completely fixed and destroys only the
correspondence between them, which is the thing being tested.

A NOTE ON WHAT dCor DOES AND DOES NOT ESTABLISH
-----------------------------------------------
Szekely's theorem -- dCor = 0 iff independent -- is stated for random vectors
with sampled observations. Applied to two precomputed distance matrices, as
here, the quantity is well defined and the permutation test is valid, but the
iff theorem is not being invoked. It is used as a measure of association with
an empirical null, in the Mantel tradition, and nothing below depends on the
stronger claim.

Usage:
    python3 stability/scripts/run_geometry.py --builds A.json B.json [C.json]
        [--level option|fork|both] [--perms 2000] [--corpus ai] [--json out]
"""
import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

SEED = 20260822


def run_clusters(path, level, corpus=None, min_runs=1):
    """{run: frozenset(cluster labels touched)} for one build at one level.

    `min_runs` drops clusters touched by fewer than that many runs. A singleton
    cluster never appears in an intersection but does inflate every union it
    touches, so if one build splits more than the other, every similarity
    shrinks. Pearson absorbs a uniform shift, but not an uneven one -- so the
    result is reported with and without the tail rather than assumed robust.
    """
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    keep = None
    if corpus:
        keep = {r["run"] for r in dec if r.get("corpus", "") == corpus}
        if not keep:                       # corpus not recorded per decision
            keep = None
    per = defaultdict(set)
    for o in d["options"]:
        lab = o["option"] if level == "option" else o["fork"]
        for m in o.get("members", ()):
            if 0 <= m < len(dec):
                r = dec[m]["run"]
                if keep is None or r in keep:
                    per[r].add(lab)
    if min_runs > 1:
        touched = defaultdict(set)
        for r, labs in per.items():
            for lab in labs:
                touched[lab].add(r)
        keep_lab = {l for l, rs in touched.items() if len(rs) >= min_runs}
        per = {r: (v & keep_lab) for r, v in per.items()}
    return {r: frozenset(v) for r, v in per.items() if v}


def cluster_weights(clusters, scheme):
    """Per-cluster weight for the Jaccard numerator and denominator.

    `binary` weights every cluster equally. `idf` uses log(N / df), on the
    information-retrieval argument that two runs both touching a fork 95%% of
    runs touch tells you almost nothing, while sharing a rare one is highly
    informative.

    That argument is sound and, on this corpus, it LOWERS cross-build
    agreement monotonically -- fork 0.727 binary, 0.612 smoothed idf, 0.500
    idf, 0.352 at 1/df. The reason is not a flaw in the weighting: rare
    clusters are exactly where the pipeline does not reproduce (by-option ARI
    0.31 at >=1 instance against 0.69 at >=5), so upweighting them upweights
    the noise. The gap between schemes measures how much the geometry result
    depends on the well-populated core, and is worth reporting rather than
    choosing between.

    Singletons must be dropped BEFORE weighting (see min_runs): a cluster held
    by one run can never enter an intersection, so it is pure denominator, and
    under idf it receives the largest weight of all while contributing nothing.
    """
    import math
    df = defaultdict(int)
    for labs in clusters.values():
        for l in labs:
            df[l] += 1
    n = len(clusters)
    if scheme == "binary":
        return {l: 1.0 for l in df}
    if scheme == "idf":
        return {l: math.log(n / c) for l, c in df.items()}
    if scheme == "idf_smooth":
        return {l: math.log(1 + n / c) for l, c in df.items()}
    if scheme == "inv":
        return {l: 1.0 / c for l, c in df.items()}
    raise ValueError(scheme)


def distance_matrix(clusters, runs, weighted=False, w=None):
    """Jaccard DISTANCE between runs, as a dense symmetric matrix.

    Binary by default: a run is the SET of clusters it touches, so three
    decisions landing in one fork record it once. `weighted` uses Ruzicka
    (sum(min)/sum(max) over decision counts) instead, which keeps multiplicity.

    Measured on this corpus: 90%% of runs touch some fork more than once, yet
    the two geometries correlate at 0.968 and the cross-build agreement moves
    by +0.025. Binary is the default because it is the simpler and more
    conservative claim, not because multiplicity was assumed irrelevant.
    """
    n = len(runs)
    D = np.zeros((n, n), dtype=float)
    sets = [clusters[r] for r in runs]
    for i in range(n):
        si = sets[i]
        for j in range(i + 1, n):
            sj = sets[j]
            if w is None:
                u = len(si | sj)
                d = 1.0 - (len(si & sj) / u if u else 0.0)
            else:
                num = sum(w.get(l, 0.0) for l in (si & sj))
                den = sum(w.get(l, 0.0) for l in (si | sj))
                d = 1.0 - (num / den if den > 0 else 0.0)
            D[i, j] = D[j, i] = d
    return D


def mantel_r(A, B):
    """Pearson correlation over the strict upper triangle."""
    iu = np.triu_indices_from(A, k=1)
    a, b = A[iu], B[iu]
    if a.std() < 1e-12 or b.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def _double_center(D):
    m = D.mean(axis=0, keepdims=True)
    n = D.mean(axis=1, keepdims=True)
    return D - m - n + D.mean()


def dcor(A, B):
    """Distance correlation between two precomputed distance matrices."""
    Ac, Bc = _double_center(A), _double_center(B)
    dcov2 = (Ac * Bc).mean()
    dvarA = (Ac * Ac).mean()
    dvarB = (Bc * Bc).mean()
    den = np.sqrt(np.sqrt(dvarA * dvarB))
    if den < 1e-15:
        return float("nan")
    return float(np.sqrt(max(dcov2, 0.0)) / den)


def permute(D, idx):
    return D[np.ix_(idx, idx)]


def compare(A, B, perms, rng):
    obs_m, obs_d = mantel_r(A, B), dcor(A, B)
    n = A.shape[0]
    nm, nd = [], []
    for _ in range(perms):
        p = rng.permutation(n)
        Bp = permute(B, p)
        nm.append(mantel_r(A, Bp))
        nd.append(dcor(A, Bp))
    nm, nd = np.array(nm), np.array(nd)

    def stat(obs, null):
        sd = null.std(ddof=1)
        return {"observed": round(float(obs), 4),
                "null_mean": round(float(null.mean()), 4),
                "null_sd": round(float(sd), 4),
                "z": round(float((obs - null.mean()) / sd), 2)
                if sd > 1e-12 else None,
                "p": round(float((np.sum(null >= obs) + 1) / (len(null) + 1)),
                           4)}
    return {"mantel": stat(obs_m, nm), "dcor": stat(obs_d, nd)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--builds", nargs="+", required=True)
    ap.add_argument("--names", nargs="*")
    ap.add_argument("--level", choices=["option", "fork", "both"],
                    default="both")
    ap.add_argument("--perms", type=int, default=2000)
    ap.add_argument("--corpus", help="restrict to one corpus, e.g. ai")
    ap.add_argument("--min-cluster-runs", type=int, default=2,
                    help="drop clusters touched by fewer than N runs; 2 is "
                         "the floor for a pairwise measure -- a singleton "
                         "cannot enter an intersection")
    ap.add_argument("--weighting", default="binary",
                    choices=["binary", "idf", "idf_smooth", "inv"],
                    help="per-cluster weight; idf upweights rare clusters")
    ap.add_argument("--json")
    x = ap.parse_args()

    names = x.names or [f"build{i+1}" for i in range(len(x.builds))]
    levels = ["option", "fork"] if x.level == "both" else [x.level]
    rng = np.random.default_rng(SEED)
    res = {"builds": dict(zip(names, x.builds)), "perms": x.perms,
           "corpus": x.corpus, "comparison_type": "replicate", "levels": {}}

    for level in levels:
        cl = [run_clusters(p, level, x.corpus, x.min_cluster_runs)
              for p in x.builds]
        # Shared runs only -- a run missing from one build has no geometry to
        # compare, and silently keeping it would compare different populations.
        runs = sorted(set.intersection(*[set(c) for c in cl]))
        mats = [distance_matrix(c, runs, w=cluster_weights(c, x.weighting)
                                if x.weighting != "binary" else None)
                for c in cl]

        out = {"runs": len(runs), "pairs": len(runs) * (len(runs) - 1) // 2,
               "clusters": {names[i]: len(set().union(*cl[i].values()))
                            for i in range(len(cl))},
               "pairwise": {}}
        for i, j in itertools.combinations(range(len(mats)), 2):
            out["pairwise"][f"{names[i]} vs {names[j]}"] = compare(
                mats[i], mats[j], x.perms, rng)
        res["levels"][level] = out

    print(f"RUN GEOMETRY  ({', '.join(names)}"
          f"{'; corpus ' + x.corpus if x.corpus else ''})\n")
    for level, out in res["levels"].items():
        print(f"  {level.upper()} level -- {out['runs']} runs, "
              f"{out['pairs']} run pairs")
        print(f"    clusters  {out['clusters']}")
        for k, v in out["pairwise"].items():
            m, dc = v["mantel"], v["dcor"]
            print(f"    {k}")
            print(f"      Mantel r  {m['observed']:>7}   null "
                  f"{m['null_mean']:>7} +/- {m['null_sd']:<7} "
                  f"z {str(m['z']):>7}  p {m['p']}")
            print(f"      dCor      {dc['observed']:>7}   null "
                  f"{dc['null_mean']:>7} +/- {dc['null_sd']:<7} "
                  f"z {str(dc['z']):>7}  p {dc['p']}")
        print()
    print("  labels never meet: this asks whether runs that look similar")
    print("  under one vocabulary look similar under the other.")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")


if __name__ == "__main__":
    main()
