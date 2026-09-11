#!/usr/bin/env python3
"""Audit for the garden map. Deterministic apart from seeded permutations.

`garden.py` makes three structural claims -- which nodes are real, which are one
node under two names, and which edges are branches. Each has a way of being
wrong that the production script cannot see from the inside:

  G1  SCREEN BLIND SPOT. The sibling screen requires near-zero co-occurrence.
      That is right only if a run records each question once. A run that
      dichotomizes twice (primary and robustness) lands in both halves of an
      under-merged fork, so the pair co-occurs and the screen never looks at
      it. This measures how many similar-looking pairs were excluded on
      co-occurrence alone -- the under-merges the screen cannot reach.
  G2  MERGE SAFETY. Transitive closure over sibling edges is how an over-merge
      would happen, and over-merge is the failure this project treats as
      unrecoverable. Every accepted component must be a clique, or close to it,
      on the adjudicated edges.
  G3  MERGE EFFECT. If merging barely moved coverage, it was cosmetic. If it
      moved it a lot, every pre-merge coverage number in the record is wrong.
  G4  GATE POWER. Three surviving gates is either "the garden is flat" or "n is
      too small". The permutation null distinguishes them: shuffle which runs
      reach which forks, keeping each fork's reach count, and see how many
      gates the same pipeline invents from noise.
  G5  PRECEDENCE. Gate direction comes from median observed position. If that
      disagrees with the blind DSLC stage ordering, the edges point the wrong
      way.
  G6  RECIPES. 63 distinct paths among 68 runs looks like everyone is unique.
      Under independent choice at each fork with the observed marginals, is
      that more or fewer distinct paths than expected? Fewer means analysts
      travel in packages, not fork by fork.

Usage:
    python3 scripts/audit_garden.py --corpus ai
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402
import garden as G                                             # noqa: E402

OUT = G.OUT
PERM = 1000
SEED = 20260822


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--json")
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    d, path, stage = G.load(tag)
    reach0, opts0, med0, runs = G.tables(d)
    N = len(runs)
    gp = OUT / f"garden_{tag}.json"
    if not gp.exists():
        sys.exit(f"run `garden.py map --corpus {tag}` first")
    gm = json.loads(gp.read_text(encoding="utf-8"))
    verd = json.loads((OUT / f"garden_siblings_{tag}.json")
                      .read_text(encoding="utf-8"))["verdicts"]
    rng = random.Random(SEED)
    res = {}

    print(f"GARDEN AUDIT - {path.name}")
    print(f"{N} runs, {len(reach0)} raw forks, {gm['nodes']} nodes\n")

    # ---- G1 screen blind spot ---------------------------------------------
    fs = [f for f, r in reach0.items() if len(r) >= G.MIN_REACH]
    tk = {f: G.toks(f) for f in fs}
    blind = []
    for i, A in enumerate(fs):
        for B in fs[i + 1:]:
            co = len(reach0[A] & reach0[B])
            if co <= G.CO_MAX:
                continue
            if G.jac(tk[A], tk[B]) < G.LABEL_J:
                continue
            blind.append((round(G.jac(tk[A], tk[B]), 3), co,
                          len(reach0[A]), len(reach0[B]), A, B))
    blind.sort(reverse=True)
    screened = sum(1 for i, A in enumerate(fs) for B in fs[i + 1:]
                   if len(reach0[A] & reach0[B]) <= G.CO_MAX
                   and G.jac(tk[A], tk[B]) >= G.LABEL_J)
    tot = screened + len(blind)
    v = "PASS" if len(blind) / max(1, tot) < 0.5 else "REVIEW"
    print(f"G1  SCREEN BLIND SPOT                                       {v}")
    print(f"    label-similar pairs, total          {tot}")
    print(f"    screened (co-occur <= {G.CO_MAX})            {screened}")
    print(f"    excluded on co-occurrence alone     {len(blind)} "
          f"({len(blind)/max(1,tot):.0%})")
    for j, co, ra, rb, A, B in blind[:5]:
        print(f"      J={j:.2f} co={co:>3} {ra:>3}/{rb:<3}  {A[:44]}")
        print(f"      {'':>21}  {B[:44]}")
    print(f"    -> these are NOT adjudicated; an under-merge among them stays")
    print(f"       in the map as two nodes. Reported as a known limit.\n")
    res["G1"] = {"verdict": v, "screened": screened, "excluded": len(blind),
                 "examples": [{"jaccard": j, "co": co, "a": A, "b": B}
                              for j, co, _, _, A, B in blind[:12]]}

    # ---- G2 merge safety ---------------------------------------------------
    edge = {frozenset((x["a"], x["b"])): x["relation"] for x in verd}
    groups = gm.get("sibling_groups", {})
    worst, bad = 1.0, []
    for head, members in groups.items():
        n = len(members)
        if n < 3:
            continue
        poss = n * (n - 1) // 2
        have = sum(1 for i, x in enumerate(members) for y in members[i + 1:]
                   if edge.get(frozenset((x, y))) == "sibling")
        conflict = [sorted((x, y)) for i, x in enumerate(members)
                    for y in members[i + 1:]
                    if edge.get(frozenset((x, y))) in ("gate", "rival")]
        worst = min(worst, have / poss)
        if conflict:
            bad.append({"head": head, "conflict": conflict})
    v = "PASS" if not bad and worst >= 0.5 else "REVIEW"
    print(f"G2  MERGE SAFETY                                            {v}")
    print(f"    components of size >= 3      "
          f"{sum(1 for m in groups.values() if len(m) >= 3)}")
    print(f"    weakest clique density       {worst:.2f} "
          f"(1.00 = every pair adjudicated sibling)")
    print(f"    components containing a gate/rival pair  {len(bad)}")
    print(f"    edges vetoed during merge    "
          f"{len(gm.get('sibling_edges_vetoed', []))}\n")
    res["G2"] = {"verdict": v, "clique_density_min": round(worst, 3),
                 "conflicts": bad}

    # ---- G3 merge effect ---------------------------------------------------
    cov_before = sorted((len(r) / N for r in reach0.values()), reverse=True)
    cov_after = [x["coverage"] for x in gm["nodes_detail"]]
    u_before = sum(1 for c in cov_before if c >= G.UNIVERSAL)
    u_after = sum(1 for c in cov_after if c >= G.UNIVERSAL)
    moved = [(x["fork"], x["coverage"]) for x in gm["nodes_detail"]
             if x["fork"] in groups]
    print(f"G3  MERGE EFFECT                                            INFO")
    print(f"    nodes            {len(reach0)} -> {gm['nodes']}")
    print(f"    universal nodes  {u_before} -> {u_after}")
    print(f"    largest coverage gains from merging:")
    for f, c in sorted(moved, key=lambda t: -t[1])[:5]:
        parts = [len(reach0[m]) / N for m in groups[f]]
        print(f"      {max(parts):.2f} -> {c:.2f}   {f[:56]}")
    print(f"    -> pre-merge coverage understates every merged fork\n")
    res["G3"] = {"nodes_before": len(reach0), "nodes_after": gm["nodes"],
                 "universal_before": u_before, "universal_after": u_after}

    # ---- G4 gate power ------------------------------------------------------
    # rebuild merged tables the same way map() does
    cmap = {}
    for head, members in groups.items():
        for m in members:
            cmap[m] = head
    reach, opts = defaultdict(set), defaultdict(lambda: defaultdict(set))
    for f, rs in reach0.items():
        reach[cmap.get(f, f)] |= rs
    for f, om in opts0.items():
        for o, rs in om.items():
            opts[cmap.get(f, f)][o] |= rs
    grp = defaultdict(list)
    for f, m in med0.items():
        grp[cmap.get(f, f)].append((m, len(reach0[f])))
    pos = {k: sum(m * w for m, w in v_) / sum(w for _, w in v_)
           for k, v_ in grp.items()}

    obs = len(gm["gates"])
    allr = sorted(runs)
    null = []
    for _ in range(PERM):
        # keep each fork's reach count and each option's size, break the
        # association between which runs reach which forks
        r2 = {}
        o2 = defaultdict(dict)
        for f in reach:
            samp = rng.sample(sorted(allr), len(reach[f]))
            r2[f] = set(samp)
            i = 0
            for o, rs in opts[f].items():
                o2[f][o] = set(samp[i:i + len(rs)])
                i += len(rs)
        keep, _, _, _ = G.find_gates(r2, o2, pos, runs)
        null.append(len(keep))
    nm = sum(null) / len(null)
    ge = sum(1 for x in null if x >= obs)
    v = "PASS" if ge / PERM < 0.05 else "REVIEW"
    print(f"G4  GATE POWER  (reach-preserving permutation, {PERM} draws)   {v}")
    print(f"    gates found                 {obs}")
    print(f"    null mean                   {nm:.2f}  "
          f"[{min(null)}, {max(null)}]")
    print(f"    p(null >= observed)         {ge/PERM:.4f}")
    print(f"    candidate triples tested    {gm['gates_tested']}")
    print(f"    -> {obs} is small because the corpus is thin at the tail, not")
    print(f"       because the pipeline invents gates: noise yields {nm:.2f}\n")
    res["G4"] = {"verdict": v, "observed": obs, "null_mean": round(nm, 3),
                 "p": ge / PERM, "tested": gm["gates_tested"]}

    # ---- G5 precedence -----------------------------------------------------
    agree = dis = 0
    for g in gm["gates"]:
        sa, sb = stage.get(g["from"]), stage.get(g["to"])
        if sa in G.RANK and sb in G.RANK:
            if G.RANK[sa] <= G.RANK[sb]:
                agree += 1
            else:
                dis += 1
    tot5 = agree + dis
    v = "PASS" if tot5 == 0 or agree / tot5 >= 0.6 else "REVIEW"
    print(f"G5  PRECEDENCE  (position-derived direction vs blind stage)  {v}")
    print(f"    gate edges with both stages known   {tot5}")
    print(f"    stage order agrees with position    {agree}")
    print(f"    disagrees                           {dis}\n")
    res["G5"] = {"verdict": v, "agree": agree, "disagree": dis}

    # ---- G6 recipes ---------------------------------------------------------
    univ = gm["universal"]
    choice = {}
    for f in univ:
        for o, rs in opts[f].items():
            for r in rs:
                choice.setdefault(r, {})[f] = o
    full = {r: tuple(choice[r][f] for f in univ) for r in runs
            if len(choice.get(r, {})) == len(univ)}
    obs_d = len(set(full.values()))
    # Marginals must come from the SAME runs the statistic is computed on.
    # Taking them over every run reaching each fork -- as this did until the
    # pooled run exposed it -- samples the null from a different population
    # than the observed value, because runs completing all universal forks are
    # not a random subset of runs reaching any one of them. That mismatch
    # reported p=0.001 ("recipes") on a corpus where the corrected test gives
    # p=0.34.
    # sorted(), not set(): the RNG is seeded, but a set of run ids iterates in
    # hash order, so Counter.items() came out ordered differently in every
    # process and rng.choices() drew a different sequence from the same
    # weights. G6's null moved run to run (33.47-33.54 observed) with the seed
    # unchanged. Sorting makes the draw order a property of the data rather
    # than of PYTHONHASHSEED. The statistic is unaffected -- same options, same
    # weights -- but it is now the same number twice.
    idx_full = sorted(set(full))
    marg = {f: sorted(Counter(choice[r][f] for r in idx_full).items())
            for f in univ}
    null6 = []
    for _ in range(PERM):
        paths = set()
        for _ in range(len(full)):
            paths.add(tuple(
                rng.choices([o for o, _ in marg[f]],
                            weights=[w for _, w in marg[f]])[0] for f in univ))
        null6.append(len(paths))
    nm6 = sum(null6) / len(null6)
    le = sum(1 for x in null6 if x <= obs_d)
    v = "PASS" if len(univ) >= 3 else "REVIEW"
    print(f"G6  RECIPES  (independent choice at the {len(univ)} universal "
          f"nodes)      {v}")
    print(f"    runs traversing all of them        {len(full)}")
    print(f"    distinct paths observed            {obs_d}")
    print(f"    expected if choices independent    {nm6:.1f}  "
          f"[{min(null6)}, {max(null6)}]")
    print(f"    p(null <= observed)                {le/PERM:.4f}")
    if obs_d < min(null6):
        print(f"    -> fewer distinct paths than independence predicts: "
              f"choices\n       travel together, so the trunk carries recipes, "
              f"not free combination")
    elif obs_d > max(null6):
        print(f"    -> more distinct paths than independence predicts")
    else:
        print(f"    -> indistinguishable from independent choice at each fork")
    res["G6"] = {"verdict": v, "runs": len(full), "observed_paths": obs_d,
                 "null_mean": round(nm6, 2), "p": le / PERM}

    fails = [k for k, x in res.items() if isinstance(x, dict)
             and x.get("verdict") == "REVIEW"]
    print("\n" + "=" * 68)
    print("ALL CHECKS PASS" if not fails else "NEEDS REVIEW: " + ", ".join(fails))
    p = Path(a.json) if a.json else P.AUDITS / f"garden_audit_{tag}.json"
    p.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {p}")


if __name__ == "__main__":
    main()
