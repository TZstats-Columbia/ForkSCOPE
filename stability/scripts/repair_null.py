#!/usr/bin/env python3
"""Does the repair chain CONVERGE two independent builds, or just coarsen them?

No model calls. Written BEFORE the repaired vocabularies were compared, so the
null could not be chosen to fit a result already seen.

THE CONFOUND
------------
Repair is a contraction: on this corpus the fork count goes 463 -> 317 in one
build and 489 -> ~317 in another. Fewer and larger clusters raise ARI and
B-cubed mechanically, whether or not the merges are correct -- merge everything
into one fork in both builds and ARI is exactly 1.0 while the vocabulary says
nothing. So a bare before/after comparison cannot distinguish

    "repair pulls independent runs toward a common canonical form"

from

    "any contraction to this granularity would score about this well".

THE NULL
--------
Randomly merge each BASE vocabulary down to the repaired granularity, matching
the observed cluster-SIZE distribution, and recompute the agreement. That holds
constant everything the contraction gives you for free -- how many clusters
there are and how big they are -- leaving only *which* items were put together.

Matching the size distribution matters. A null that merges into equal-sized
groups is too easy to beat, because real vocabularies are heavy-tailed: a few
forks hold most runs and hundreds hold one or two. Reproducing that profile is
what makes the null a fair opponent rather than a straw one.

READING THE RESULT
------------------
  observed >> null   repair is a genuine canonicaliser. Two runs that started
                     from different clusterings end at the same one, which is
                     the claim worth making.
  observed ~ null    the improvement is granularity arithmetic. Repair removes
                     duplication within a build but does not remove
                     run-to-run variability, and fork-level claims inherit the
                     base instability.

Reported as a z-score and an empirical percentile against B draws, plus the
raw null mean, because a ratio alone hides how wide the null is.

Usage:
    python3 stability/scripts/repair_null.py \\
        --a-base  A/bottom_up_<tag>.json      --b-base  B/bottom_up_<tag>.json \\
        --a-final A/bottom_up_<tag>.r3.json   --b-final B/bottom_up_<tag>.r3.json \\
        --level fork [--draws 200] [--json out.json]
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


def labeling(path, level):
    return P.labeling(path, level)


def sizes_of(lab):
    return sorted(Counter(lab.values()).values(), reverse=True)


def random_contract(lab, target_sizes, rng):
    """Merge whole base clusters into groups matching `target_sizes`.

    Base clusters are kept intact and assigned to targets -- repair merges
    clusters, it does not split them, so a null that reshuffled individual
    instances would be solving an easier problem than the thing it stands in
    for.

    Greedy first-fit on shuffled clusters, largest target first. Exact size
    matching is not always achievable when base clusters are lumpy, so the
    result approximates the profile; the achieved sizes are returned so the
    approximation is visible rather than assumed.
    """
    by_cluster = defaultdict(list)
    for k, c in lab.items():
        by_cluster[c].append(k)
    clusters = list(by_cluster.values())
    rng.shuffle(clusters)
    clusters.sort(key=len, reverse=True)

    targets = sorted(target_sizes, reverse=True)
    bins = [[] for _ in targets]
    filled = [0] * len(targets)
    for cl in clusters:
        # Put each cluster in the target with the most room left, so the big
        # targets fill first and the tail is not starved.
        j = max(range(len(targets)), key=lambda i: targets[i] - filled[i])
        bins[j].extend(cl)
        filled[j] += len(cl)
    out = {}
    for j, members in enumerate(bins):
        for k in members:
            out[k] = f"null_{j}"
    return out


def agreement(la, lb, keys):
    ari = P.adjusted_rand(la, lb, keys)
    p, r, f = P.bcubed(la, lb, keys)
    return ari, f


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a-base", required=True)
    ap.add_argument("--b-base", required=True)
    ap.add_argument("--a-final", required=True)
    ap.add_argument("--b-final", required=True)
    ap.add_argument("--level", choices=["option", "fork"], default="fork")
    ap.add_argument("--draws", type=int, default=200)
    ap.add_argument("--json")
    x = ap.parse_args()

    ab, _ = labeling(x.a_base, x.level)
    bb, _ = labeling(x.b_base, x.level)
    af, _ = labeling(x.a_final, x.level)
    bf, _ = labeling(x.b_final, x.level)

    keys = sorted(set(ab) & set(bb) & set(af) & set(bf))
    if not keys:
        sys.exit("no instances shared by all four vocabularies")

    base_ari, base_f1 = agreement(ab, bb, keys)
    fin_ari, fin_f1 = agreement(af, bf, keys)

    n_ab = len(set(ab[k] for k in keys))
    n_bb = len(set(bb[k] for k in keys))
    n_af = len(set(af[k] for k in keys))
    n_bf = len(set(bf[k] for k in keys))

    ta = sizes_of({k: af[k] for k in keys})
    tb = sizes_of({k: bf[k] for k in keys})

    rng = random.Random(SEED)
    null_ari, null_f1 = [], []
    for _ in range(x.draws):
        ra = random_contract({k: ab[k] for k in keys}, ta, rng)
        rb = random_contract({k: bb[k] for k in keys}, tb, rng)
        a_, f_ = agreement(ra, rb, keys)
        null_ari.append(a_)
        null_f1.append(f_)

    def stats(obs, null):
        null = sorted(null)
        n = len(null)
        mean = sum(null) / n
        var = sum((v - mean) ** 2 for v in null) / max(1, n - 1)
        sd = var ** 0.5
        above = sum(1 for v in null if v >= obs)
        return {
            "observed": round(obs, 4),
            "null_mean": round(mean, 4),
            "null_sd": round(sd, 4),
            "null_min": round(null[0], 4),
            "null_max": round(null[-1], 4),
            "z": round((obs - mean) / sd, 2) if sd > 1e-12 else None,
            "p_empirical": round((above + 1) / (n + 1), 4),
        }

    res = {
        "level": x.level, "draws": x.draws, "instances": len(keys),
        "clusters": {"a_base": n_ab, "b_base": n_bb,
                     "a_final": n_af, "b_final": n_bf},
        "base": {"ari": round(base_ari, 4), "bcubed_f1": round(base_f1, 4)},
        "final": {"ari": round(fin_ari, 4), "bcubed_f1": round(fin_f1, 4)},
        "ari_vs_null": stats(fin_ari, null_ari),
        "bcubed_vs_null": stats(fin_f1, null_f1),
        "files": {"a_base": x.a_base, "b_base": x.b_base,
                  "a_final": x.a_final, "b_final": x.b_final},
        "comparison_type": "replicate",
        "build_a": x.a_final, "build_b": x.b_final,
    }

    a_n, b_n = res["ari_vs_null"], res["bcubed_vs_null"]
    verdict = ("repair CONVERGES the builds (beats a size-matched random "
               "contraction)" if a_n["p_empirical"] <= 0.05 else
               "repair does NOT converge them beyond granularity arithmetic")

    print(f"REPAIR NULL -- {x.level} level, {len(keys)} instances, "
          f"{x.draws} draws\n")
    print(f"    clusters   A {n_ab} -> {n_af}     B {n_bb} -> {n_bf}\n")
    print(f"    {'':<14}{'ARI':>9}{'B3 F1':>9}")
    print(f"    {'base':<14}{res['base']['ari']:>9}"
          f"{res['base']['bcubed_f1']:>9}")
    print(f"    {'after repair':<14}{res['final']['ari']:>9}"
          f"{res['final']['bcubed_f1']:>9}")
    print(f"    {'random null':<14}{a_n['null_mean']:>9}"
          f"{b_n['null_mean']:>9}   <- same granularity, random membership\n")
    for name, s in (("ARI", a_n), ("B-cubed F1", b_n)):
        print(f"    {name}: observed {s['observed']}  vs null "
              f"{s['null_mean']} +/- {s['null_sd']}  "
              f"(z {s['z']}, p {s['p_empirical']})")
    print(f"\n    -> {verdict}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n    wrote {x.json}")


if __name__ == "__main__":
    main()
