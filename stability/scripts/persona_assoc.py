#!/usr/bin/env python3
"""Do personas walk different routes at all? An omnibus test. No model calls.

`circle.py` tests each (route, persona) cell separately: is this edge walked by
more of this persona than its corpus share predicts? With ~1,350 cells, small
counts in most of them, and BH correction across all of them, that design has
little power per cell and a large multiplicity burden -- and its output did not
reproduce across two builds (1 of 10 enrichments survived).

That failure does not establish there is no persona signal. It establishes that
*which particular edge* carries the signal is not identifiable at this sample
size. Those are different claims, and only the second is supported.

So this asks the prior question, once, globally:

    do runs of the same persona walk more similar routes than runs of
    different personas?

WHY THIS IS THE RIGHT SHAPE
---------------------------
One test instead of 1,350 means no multiplicity correction and all of the
sample behind a single statistic. It is the multivariate-dispersion question
(PERMANOVA / Mantel family) rather than a per-feature scan, and it answers what
the persona manipulation was actually meant to probe: does the brief change the
analysis path?

STATISTIC
---------
Each run is the SET of fork-to-fork transitions it walks. Similarity between
two runs is Jaccard over those sets. The statistic is

    delta = mean(within-persona similarity) - mean(between-persona similarity)

Null: shuffle persona labels across runs, holding every route fixed. That
preserves route structure, run lengths and persona group sizes exactly, and
destroys only the association being tested -- the same logic as the label
shuffle `circle.py` uses per cell, applied once to the whole map.

Reported with a permutation p, a z against the null spread, and the two raw
means, because a delta of 0.01 on similarities of 0.30 means something quite
different from the same delta on similarities of 0.05.

The same statistic is computed on each build, so its REPRODUCIBILITY is
measurable too -- which is the point of running it here rather than in
`circle.py`.

Usage:
    python3 stability/scripts/persona_assoc.py --vocab V.json [--perms 2000]
"""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 20260822


def run_routes(path):
    """{run: (arm, frozenset of consecutive fork-pair transitions)}.

    A route is built the way circle.py builds it: order each run's decisions by
    source line, read off the fork each lands in, and take consecutive pairs.
    Pairs are unordered, so A->B and B->A are one edge -- the question is which
    forks a run travels between, not the direction of travel.
    """
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    fork_of = {}
    for o in d["options"]:
        for i in o.get("members", ()):
            if 0 <= i < len(dec):
                fork_of[i] = o["fork"]

    seq = defaultdict(list)
    arm = {}
    for i, rec in enumerate(dec):
        f = fork_of.get(i)
        if f is None:
            continue
        r = rec["run"]
        arm[r] = rec.get("arm") or rec.get("corpus") or "unknown"
        seq[r].append((rec.get("line", 0), f))

    out = {}
    for r, items in seq.items():
        items.sort()
        forks = [f for _, f in items]
        edges = set()
        for a, b in zip(forks, forks[1:]):
            if a != b:
                edges.add(tuple(sorted((a, b))))
        if edges:
            out[r] = (arm[r], frozenset(edges))
    return out


def jaccard(a, b):
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def delta(runs, labels, sim):
    """mean within-persona similarity minus mean between-persona similarity."""
    w = wn = b = bn = 0.0
    n = len(runs)
    for i in range(n):
        for j in range(i + 1, n):
            s = sim[i][j]
            if labels[i] == labels[j]:
                w += s
                wn += 1
            else:
                b += s
                bn += 1
    wm = w / wn if wn else 0.0
    bm = b / bn if bn else 0.0
    return wm - bm, wm, bm


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vocab", required=True)
    ap.add_argument("--perms", type=int, default=2000)
    ap.add_argument("--exclude", default="human",
                    help="comma-separated arms to drop; human runs carry no "
                         "persona and would be tested as if they did")
    ap.add_argument("--json")
    x = ap.parse_args()

    rr = run_routes(x.vocab)
    drop = {s.strip() for s in x.exclude.split(",") if s.strip()}
    runs = sorted(r for r, (a, _) in rr.items() if a not in drop)
    labels = [rr[r][0] for r in runs]
    sets = [rr[r][1] for r in runs]
    n = len(runs)
    if n < 10:
        raise SystemExit(f"only {n} runs after excluding {sorted(drop)}")

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = jaccard(sets[i], sets[j])
            sim[i][j] = sim[j][i] = s

    obs, wm, bm = delta(runs, labels, sim)

    rng = random.Random(SEED)
    perm = list(labels)
    null = []
    for _ in range(x.perms):
        rng.shuffle(perm)
        null.append(delta(runs, perm, sim)[0])
    null.sort()
    mean = sum(null) / len(null)
    var = sum((v - mean) ** 2 for v in null) / max(1, len(null) - 1)
    sd = var ** 0.5
    ge = sum(1 for v in null if v >= obs)
    p = (ge + 1) / (len(null) + 1)

    counts = defaultdict(int)
    for a in labels:
        counts[a] += 1

    res = {
        "vocab": x.vocab, "comparison_type": "single_build",
        "runs": n, "perms": x.perms,
        "arms": dict(sorted(counts.items())),
        "mean_within_persona_similarity": round(wm, 4),
        "mean_between_persona_similarity": round(bm, 4),
        "delta": round(obs, 5),
        "null_mean": round(mean, 5), "null_sd": round(sd, 5),
        "z": round((obs - mean) / sd, 2) if sd > 1e-12 else None,
        "p_permutation": round(p, 4),
        "relative_effect": round(obs / bm, 4) if bm else None,
    }

    print(f"PERSONA / ROUTE ASSOCIATION  (omnibus)\n")
    print(f"  vocabulary  {Path(x.vocab).name}")
    print(f"  runs        {n}   arms {dict(sorted(counts.items()))}\n")
    print(f"  mean similarity, same persona       {res['mean_within_persona_similarity']}")
    print(f"  mean similarity, different persona  {res['mean_between_persona_similarity']}")
    print(f"  delta                               {res['delta']}")
    print(f"  null                                {res['null_mean']} "
          f"+/- {res['null_sd']}")
    print(f"  z / p                               {res['z']} / "
          f"{res['p_permutation']}")
    print(f"  delta as share of between-mean      {res['relative_effect']}")
    print(f"\n  -> {'personas DO walk different routes' if p <= 0.05 else 'no detectable persona effect on routes'}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")


if __name__ == "__main__":
    main()
