#!/usr/bin/env python3
"""Map the garden of forking paths: which forks branch from which.

v1 vectorized runs over forks and treated the forks as independent dimensions
(`soccer_vectorize.py`). That is a lattice, not a garden. A garden *branches*:
"at what cut-point?" is not a decision every analyst faces, it is a decision
created by having chosen to dichotomize. Mapping the garden means recovering
which forks are unavoidable and which exist only downstream of a prior choice.

TWO SCREENS, BECAUSE THEY HAVE OPPOSITE SIGNATURES
--------------------------------------------------
Both siblings and gates are invisible to the clustering and only appear once
runs are laid over the fork set, but they look nothing alike:

  SIBLING  one question split into two labels by L3. The two forks **never
           co-occur** -- each run was filed under one label or the other. The
           clustering deliberately prefers under-merge (over-merge is invisible
           and fatal, under-merge is visible and recoverable), so this is the
           expected residue, not a rare accident.

  GATE     B is reachable only after choosing option a at A. The two forks **do
           co-occur** -- every run that chose a reaches both. What marks a gate
           is that runs reaching A and *not* choosing a essentially never reach
           B.

So `siblings` screens for near-zero co-occurrence plus label similarity, and
adjudicates with the model (prompt 15). `map` screens for conditional
reachability with Fisher's exact test and BH-FDR, over pairs that co-occur.
Running only one of them gives a wrong map: unmerged siblings masquerade as
structure, and un-tested gates leave the garden flat.

Precedence comes from the median observed position of each fork, which is
independent of the DSLC stage labels (assigned blind to position, prompt 14)
and validated against them at rho = +0.657 in `audit_iteration.py`.

Subcommands:
    siblings   screen candidate under-merges, adjudicate with the model
    map        merge siblings, classify nodes, detect gates, measure coverage

Usage:
    python3 scripts/garden.py siblings --corpus ai
    python3 scripts/garden.py map      --corpus ai
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
OUT = P.ANALYSIS

STAGES = ["problem_formulation", "data_collection", "data_cleaning",
          "eda", "modeling", "communication"]
RANK = {s: i for i, s in enumerate(STAGES)}

MIN_REACH = 8        # a fork below this cannot support any structural claim
CO_MAX = 1           # "never co-occur" tolerates this many runs (extraction slips)
LABEL_J = 0.34       # fork-label token Jaccard to screen a sibling candidate
SIB_BATCH = 25

# gate detection
MIN_OPT = 5          # an option needs this many runs to gate anything
MIN_HIT = 5          # runs that both chose a and reached B
MAX_P0 = 0.06        # P(reach B | reached A, did NOT choose a) must be ~0
MIN_P1 = 0.25        # P(reach B | chose a) must be substantial
FDR = 0.05
UNIVERSAL = 0.60     # coverage at or above this = a decision nearly everyone faces

STOP = set("how is are the a an of to into for from in on at by with and or "
           "what which used use does do this that it its as be been was were "
           "if then than when where who whom whose there their they them".split())
SIB_SCHEMA = {"type": "object", "required": ["verdicts"]}


def load(tag):
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        cand = sorted(P.VOCAB.glob("bottom_up_*.json"))
        if not cand:
            sys.exit("no bottom_up_*.json; run cluster_up.py build first")
        p = cand[-1]
    d = json.loads(p.read_text(encoding="utf-8"))
    sp = OUT / f"fork_stage_{tag}.json"
    stage = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
    return d, p, stage


def tables(d):
    """fork -> runs, fork -> option -> runs, fork -> median relative position."""
    dec = d["decisions"]
    reach = defaultdict(set)
    opts = defaultdict(lambda: defaultdict(set))
    pos = defaultdict(list)
    span = {}
    for x in dec:
        span[x["run"]] = max(span.get(x["run"], 1), x["line"])
    for o in d["options"]:
        for i in o.get("members", []):
            if i >= len(dec):
                continue
            r = dec[i]["run"]
            reach[o["fork"]].add(r)
            opts[o["fork"]][o["option"]].add(r)
            pos[o["fork"]].append(dec[i]["line"] / max(1, span[r]))
    med = {f: sorted(v)[len(v) // 2] for f, v in pos.items()}
    return reach, opts, med, {x["run"] for x in dec}


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower())
            if w not in STOP and len(w) > 2}


def jac(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0


# --------------------------------------------------------------------------
# sibling screen
# --------------------------------------------------------------------------
def screen(reach, opts, med, stage):
    """Fork pairs that never co-occur and read like the same question.

    Mechanical and deliberately high-recall: a screen, not a verdict. String
    similarity is untrustworthy on option labels (95% are unique) but fork
    labels are a different population -- an under-merge splits one question
    into two paraphrases of itself, so token overlap has real signal. Every
    survivor is adjudicated by the model.
    """
    fs = [f for f, r in reach.items() if len(r) >= MIN_REACH]
    tk = {f: toks(f) for f in fs}
    cand = []
    for i, A in enumerate(fs):
        for B in fs[i + 1:]:
            co = len(reach[A] & reach[B])
            if co > CO_MAX:
                continue
            j = jac(tk[A], tk[B])
            if j < LABEL_J:
                continue
            cand.append({
                "a": A, "b": B, "co_runs": co,
                "reach_a": len(reach[A]), "reach_b": len(reach[B]),
                "label_jaccard": round(j, 3),
                "option_overlap": round(jac(set(opts[A]), set(opts[B])), 3),
                "same_stage": stage.get(A) == stage.get(B),
                "pos_a": round(med.get(A, 0), 2), "pos_b": round(med.get(B, 0), 2),
            })
    cand.sort(key=lambda c: -(c["label_jaccard"] + c["reach_a"] / 400))
    return cand


def siblings(tag):
    from llm import ask
    d, path, stage = load(tag)
    reach, opts, med, runs = tables(d)
    cand = screen(reach, opts, med, stage)
    elig = len([f for f, r in reach.items() if len(r) >= MIN_REACH])
    print(f"SIBLING SCREEN - {path.name}")
    print(f"{elig} forks with >= {MIN_REACH} runs; {len(cand)} candidate pairs "
          f"(co-occur <= {CO_MAX}, label Jaccard >= {LABEL_J})\n")
    for c in cand[:25]:
        print(f"  J={c['label_jaccard']:.2f} co={c['co_runs']} "
              f"{c['reach_a']:>3}/{c['reach_b']:<3}")
        print(f"    A  {c['a'][:88]}")
        print(f"    B  {c['b'][:88]}")
    if not cand:
        (OUT / f"garden_siblings_{tag}.json").write_text(
            json.dumps({"verdicts": []}, indent=1), encoding="utf-8")
        return

    print(f"\nadjudicating {len(cand)} pairs")
    verdicts = []
    for k in range(0, len(cand), SIB_BATCH):
        chunk = cand[k:k + SIB_BATCH]
        want = set(range(k, k + len(chunk)))

        def check(o, want=want):
            ids = [v.get("id") for v in o.get("verdicts", [])]
            miss = want - set(ids)
            if miss:
                raise ValueError(f"{len(miss)} ids unjudged: {sorted(miss)[:8]}")
            ok = {"sibling", "gate", "rival", "unrelated"}
            bad = sorted({str(v.get("relation")) for v in o["verdicts"]
                          if v.get("relation") not in ok})
            if bad:
                raise ValueError(f"relation must be one of {sorted(ok)}; got {bad}")

        out = ask("15_fork_relation",
                  {"pairs": [{"id": k + j, "fork_a": c["a"], "fork_b": c["b"],
                              "options_a": sorted(opts[c["a"]])[:12],
                              "options_b": sorted(opts[c["b"]])[:12]}
                             for j, c in enumerate(chunk)]},
                  schema=SIB_SCHEMA, model="opus", run_id="fork_relation",
                  check=check)
        for v in out["verdicts"]:
            i = v.get("id")
            if isinstance(i, int) and 0 <= i < len(cand):
                verdicts.append({**cand[i], "relation": v["relation"],
                                 "why": v.get("why", "")})
        print(f"  {min(k + SIB_BATCH, len(cand))}/{len(cand)}", flush=True)

    print(f"\nverdicts: {dict(Counter(v['relation'] for v in verdicts))}")
    p = OUT / f"garden_siblings_{tag}.json"
    p.write_text(json.dumps({"min_reach": MIN_REACH, "co_max": CO_MAX,
                             "label_jaccard": LABEL_J,
                             "n_candidates": len(cand), "verdicts": verdicts},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {p}")


# --------------------------------------------------------------------------
# merging siblings
# --------------------------------------------------------------------------
def merge_siblings(verdicts):
    """Connected components over `sibling` edges, refusing any component that
    would swallow a pair judged `gate` or `rival`.

    Transitive closure is the right default -- A~B and B~C really does mean one
    question under three labels, and three of the components here are closed
    triangles. But closure is also how an over-merge happens, and over-merge is
    the failure this project treats as unrecoverable. So every non-sibling
    verdict is a veto: if closure would place a gate's two endpoints in one
    node, the weakest sibling edge in that component is dropped and reported.
    """
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    sib = [v for v in verdicts if v["relation"] == "sibling"]
    veto = {frozenset((v["a"], v["b"])) for v in verdicts
            if v["relation"] in ("gate", "rival")}
    sib.sort(key=lambda v: -v["label_jaccard"])   # strongest edges first
    used, dropped = [], []
    for v in sib:
        ra, rb = find(v["a"]), find(v["b"])
        if ra == rb:
            used.append(v)
            continue
        ga = [x for x in parent if find(x) == ra] + [v["a"]]
        gb = [x for x in parent if find(x) == rb] + [v["b"]]
        clash = [frozenset((x, y)) for x in ga for y in gb
                 if frozenset((x, y)) in veto]
        if clash:
            dropped.append({**v, "blocked_by": [sorted(c) for c in clash[:2]]})
            continue
        union(v["a"], v["b"])
        used.append(v)
    comp = defaultdict(list)
    for x in parent:
        comp[find(x)].append(x)
    return {k: sorted(v) for k, v in comp.items()}, used, dropped


def canon_map(components):
    """Each component collapses to its longest-reaching member's label."""
    m = {}
    for members in components.values():
        head = max(members, key=lambda f: (len(f), f))
        for f in members:
            m[f] = head
    return m


# --------------------------------------------------------------------------
# gate detection
# --------------------------------------------------------------------------
def fisher_greater(a, b, c, d):
    """One-sided Fisher exact p for the 2x2 [[a,b],[c,d]], tail = more extreme.

    Used rather than chi-square because the interesting cells are small by
    construction: a gate is defined by one cell being near zero.
    """
    n = a + b + c + d
    r1, c1 = a + b, a + c
    lo = max(0, c1 - (n - r1))
    hi = min(r1, c1)
    tot = comb(n, c1)
    return sum(comb(r1, k) * comb(n - r1, c1 - k) for k in range(a, hi + 1)) / tot \
        if tot else 1.0


def bh(ps, q):
    """Benjamini-Hochberg threshold. 92 forks squared is a lot of tests, and
    without this the gate list is mostly the multiple-comparison tail."""
    if not ps:
        return 0.0
    s = sorted(ps)
    thr = 0.0
    for i, p in enumerate(s, 1):
        if p <= q * i / len(s):
            thr = p
    return thr


def find_gates(reach, opts, med, runs):
    """(A, option a) -> B where reaching B is conditional on having chosen a.

    Restricted to runs that reached A, so the comparison is between analysts who
    faced the same decision and answered it differently -- not between analysts
    who faced it and analysts who never got there.
    """
    fs = [f for f in reach if len(reach[f]) >= MIN_REACH]
    cand = []
    # The funnel is reported because "3 gates" invites the reading "the garden
    # has 3 branches", when what it means is "3 branches are detectable at
    # n=204". Most triples die on MIN_HIT: a gate needs enough runs to have
    # walked through it, and 289 of 344 nodes are reached by under 5% of runs.
    fun = Counter()
    for A in fs:
        RA = reach[A]
        for a, ra in opts[A].items():
            if len(ra) < MIN_OPT:
                fun["option too rare"] += 1
                continue
            rest = RA - ra
            if len(rest) < MIN_OPT:
                fun["no comparison group"] += 1
                continue
            for B in fs:
                if B == A:
                    continue
                if med.get(B, 0) <= med.get(A, 0):
                    fun["B not downstream of A"] += 1
                    continue
                hit = len(ra & reach[B])
                if hit < MIN_HIT:
                    fun["too few runs took the path"] += 1
                    continue
                miss = len(rest & reach[B])
                p1 = hit / len(ra)
                p0 = miss / len(rest)
                if p0 > MAX_P0:
                    fun["non-choosers reach B too"] += 1
                    continue
                if p1 < MIN_P1:
                    fun["choosers mostly don't reach B"] += 1
                    continue
                p = fisher_greater(hit, len(ra) - hit, miss, len(rest) - miss)
                cand.append({"from": A, "option": a, "to": B,
                             "n_option": len(ra), "hit": hit, "miss": miss,
                             "p1": round(p1, 3), "p0": round(p0, 3),
                             "lift": round(p1 / p0, 1) if p0 else None,
                             "p": p})
    thr = bh([c["p"] for c in cand], FDR)
    keep = [c for c in cand if c["p"] <= thr]
    keep.sort(key=lambda c: (c["p"], -c["hit"]))
    return keep, len(cand), thr, fun


# --------------------------------------------------------------------------
# map
# --------------------------------------------------------------------------
def build_map(tag):
    d, path, stage = load(tag)
    reach0, opts0, med0, runs = tables(d)
    N = len(runs)

    sp = OUT / f"garden_siblings_{tag}.json"
    if not sp.exists():
        sys.exit(f"run `garden.py siblings --corpus {tag}` first")
    verd = json.loads(sp.read_text(encoding="utf-8"))["verdicts"]
    comps, used, dropped = merge_siblings(verd)
    cmap = canon_map(comps)

    # rebuild tables on merged nodes
    reach, opts, pos = defaultdict(set), defaultdict(lambda: defaultdict(set)), {}
    for f, rs in reach0.items():
        reach[cmap.get(f, f)] |= rs
    for f, om in opts0.items():
        for o, rs in om.items():
            opts[cmap.get(f, f)][o] |= rs
    grp = defaultdict(list)
    for f, m in med0.items():
        grp[cmap.get(f, f)].append((m, len(reach0[f])))
    for k, v in grp.items():
        pos[k] = sum(m * w for m, w in v) / sum(w for _, w in v)

    merged = {k: v for k, v in comps.items() if len(v) > 1}
    print(f"GARDEN - {path.name}")
    print(f"{N} runs, {len(reach0)} raw forks -> {len(reach)} nodes after "
          f"merging {len(merged)} sibling groups\n")

    print(f"SIBLING MERGES  ({len(used)} edges accepted, "
          f"{len(dropped)} vetoed by a gate/rival)")
    for members in sorted(merged.values(), key=lambda m: -len(reach[cmap[m[0]]])):
        head = cmap[members[0]]
        before = ", ".join(str(len(reach0[m])) for m in members)
        print(f"  {len(reach[head]):>3} runs ({before})  {head[:62]}")
        for m in members:
            if m != head:
                print(f"      + {m[:74]}")
    for v in dropped:
        print(f"  VETOED  {v['a'][:44]} ~ {v['b'][:44]}")

    # ---- node classes ----------------------------------------------------
    rows = sorted(((len(reach[f]) / N, f) for f in reach), reverse=True)
    univ = [f for c, f in rows if c >= UNIVERSAL]
    print(f"\nNODE CLASSES  (coverage = share of {N} runs reaching the fork)")
    for lab, lo, hi in (("universal", UNIVERSAL, 1.01), ("common", 0.25, UNIVERSAL),
                        ("occasional", 0.05, 0.25), ("rare", 0.0, 0.05)):
        n = sum(1 for c, _ in rows if lo <= c < hi)
        print(f"  {lab:<12}{n:>4} nodes   coverage {lo:.2f}-{hi if hi<=1 else 1:.2f}")
    print(f"\nTHE TRUNK  (coverage >= {UNIVERSAL:.0%}: decisions almost every "
          f"run faced)")
    print(f"  {'cov':>5}{'runs':>6}{'opts':>6}  {'pos':>5}  fork")
    for c, f in rows[:12]:
        mark = "*" if c >= UNIVERSAL else " "
        print(f" {mark}{c:>5.2f}{len(reach[f]):>6}{len(opts[f]):>6}"
              f"  {pos.get(f,0):>5.2f}  {f[:58]}")

    # ---- gates ------------------------------------------------------------
    gates, tested, thr, fun = find_gates(reach, opts, pos, runs)
    print(f"\nGATE SCREEN FUNNEL  (why (A, option, B) triples were dropped)")
    for k, v in fun.most_common():
        print(f"  {k:<32}{v:>10,}")
    print(f"  {'reached the test':<32}{tested:>10,}")
    print(f"\nCANDIDATE GATES  ({tested} edges tested, BH-FDR {FDR} -> "
          f"p <= {thr:.2g}, {len(gates)} kept)")
    print(f"  a gate is: among runs that reached A, choosing this option "
          f"predicts reaching B,\n  and NOT choosing it essentially rules B out")
    print(f"  CANDIDATE, not finding. BH-FDR controls the tail of the tests "
          f"that ran; it\n  cannot see the {sum(fun.values()):,} triples the "
          f"funnel dropped first. Whether this\n  count beats a "
          f"reach-preserving permutation null is check G4 in\n"
          f"  audit_garden.py, and at n={N} it does not.")
    for g in gates[:14]:
        print(f"\n  {g['from'][:70]}")
        print(f"    choose: {g['option'][:66]}")
        print(f"    opens:  {g['to'][:66]}")
        print(f"    {g['hit']}/{g['n_option']} who chose it reach B (p1={g['p1']}), "
              f"vs {g['miss']} of the rest (p0={g['p0']}), p={g['p']:.1e}")

    # ---- path coverage on the trunk ---------------------------------------
    print(f"\nPATH SPACE  (over the {len(univ)} universal nodes)")
    if univ:
        choice = {}
        for f in univ:
            for o, rs in opts[f].items():
                for r in rs:
                    choice.setdefault(r, {})[f] = o
        full = [tuple(choice[r].get(f) for f in univ) for r in runs
                if len(choice.get(r, {})) == len(univ)]
        prod = 1
        for f in univ:
            prod *= len(opts[f])
        print(f"  runs traversing every universal node   {len(full)} of {N}")
        print(f"  distinct full paths among them         {len(set(full))}")
        print(f"  product space                          {prod:,}")
        print(f"  fraction of the product space visited  "
              f"{len(set(full))/prod:.2e}")
        seen2, poss2 = 0, 0
        for i, A in enumerate(univ):
            for B in univ[i + 1:]:
                pairs = {(choice[r].get(A), choice[r].get(B)) for r in runs
                         if r in choice and A in choice[r] and B in choice[r]}
                seen2 += len(pairs)
                poss2 += len(opts[A]) * len(opts[B])
        if poss2:
            print(f"  pairwise (t=2) coverage                "
                  f"{seen2}/{poss2} = {seen2/poss2:.1%}")

    payload = {
        "source": path.name, "runs": N,
        "raw_forks": len(reach0), "nodes": len(reach),
        "sibling_groups": {cmap[m[0]]: m for m in merged.values()},
        "sibling_edges_used": len(used),
        "sibling_edges_vetoed": dropped,
        "nodes_detail": [{"fork": f, "runs": len(reach[f]),
                          "coverage": round(len(reach[f]) / N, 3),
                          "options": len(opts[f]), "position": round(pos.get(f, 0), 3),
                          "stage": stage.get(f)}
                         for _, f in rows],
        "universal": univ,
        "gates": gates, "gates_tested": tested, "gate_p_threshold": thr,
    }
    p = OUT / f"garden_{tag}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"\n-> {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["siblings", "map"])
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    (siblings if a.cmd == "siblings" else build_map)(tag)
