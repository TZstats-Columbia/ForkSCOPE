#!/usr/bin/env python3
"""Merge decision points that the induction split in two. Seeded, reproducible.

`audit_lineage.py` settled which of the two clustering errors is actually
present, and it is not the one that was feared:

  decision -> option  is sound. 32 of 33 sampled options traced down to their
                      raw operations came back coherent, 0 split, and 1 of 237
                      raw operations rejected. The option layer does not
                      over-merge, and `merge_options.py` did not damage it.
  option -> fork      is not. 23 of the 30 most similar fork pairs are one
                      question judged by prompt 21 -- including the pair the study owner
                      found by eye, which co-occurs in 0 runs against 47.4
                      expected.

So this pass merges forks and leaves options alone.

CANDIDATES, NOT ALL PAIRS
-------------------------
441 forks is 97,020 pairs and almost none of them are the same question, so
adjudicating all of them would spend the entire budget confirming the obvious.
Candidates are scored on three independent signals -- label wording, shared
option vocabulary, and mutual exclusivity across runs (co-occurrence far below
what each fork's reach predicts). Mutual exclusivity is the strongest of the
three and the only one that is a property of the runs rather than of the
induction's own phrasing, which is why it carries weight even when the labels
look unalike.

Everything above SCORE_MIN is adjudicated -- 118 pairs on this corpus -- rather
than a fixed top-N, so the cut is a stated threshold rather than a budget.

TRANSITIVITY IS EARNED, NOT ASSUMED
-----------------------------------
A~B and B~C does not give A~C. Two brakes, and the second is the one that
matters: an explicit veto where a pair was judged DIFFERENT, and a density
floor requiring a fork to be adjudicated the same as most of a group before it
joins. The veto alone is not enough -- only 118 of 97,020 pairs were judged, so
most pairs inside a growing component were never looked at and no veto can
fire. Without the floor this chained seven forks at density 0.38, bundling
threshold-sensitivity analyses with primary exposure construction, which is
exactly the case prompt 21 tells the judge to keep apart.

Usage:
    python3 scripts/merge_forks.py run   --corpus ai+human.merged
    python3 scripts/merge_forks.py apply --corpus ai+human.merged
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402
from audit_lineage import identity, jac, load, neighbours, toks   # noqa: E402

from vocab import garden_path, sync_counts                     # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
WORKERS = 6
SCORE_MIN = 0.55      # matches neighbours(); stated, not a budget


def do_run(tag):
    forks, _ = load(tag)
    cand = neighbours(forks, 10 ** 6)
    print(f"MERGE FORKS - {tag}")
    print(f"{len(forks)} forks; {len(cand)} candidate pairs above "
          f"score {SCORE_MIN}\n")
    res, fails = [], []

    def work(c):
        try:
            return {**identity(c[1], c[2], forks), "score": round(c[0], 3),
                    "label_jaccard": c[3], "option_jaccard": c[4],
                    "co_runs": c[5], "expected_co": c[6]}
        except Exception as e:                                  # noqa: BLE001
            return {"a": c[1], "b": c[2], "error": f"{type(e).__name__}"}

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for n, r in enumerate(ex.map(work, cand), 1):
            (fails if "error" in r else res).append(r)
            if n % 20 == 0:
                print(f"  {n}/{len(cand)}", flush=True)

    same = [r for r in res if r["same"]]
    print(f"\n  adjudicated   {len(res)} ({len(fails)} failed)")
    print(f"  ONE question  {len(same)} ({len(same)/max(1,len(res)):.0%})")
    print(f"\n  hit rate by candidate score (does the ranking work?)")
    for lo, hi in ((1.4, 99), (1.0, 1.4), (0.8, 1.0), (SCORE_MIN, 0.8)):
        sub = [r for r in res if lo <= r["score"] < hi]
        if sub:
            k = sum(1 for r in sub if r["same"])
            print(f"    {lo:>4}-{hi:<4} {k:>3}/{len(sub):<3} = "
                  f"{k/len(sub):.0%}")
    p = OUT / f"fork_merge_{tag}.json"
    p.write_text(json.dumps({"corpus": tag, "score_min": SCORE_MIN,
                             "failures": fails, "pairs": res},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {p}")


def components(pairs, density_min=0.60):
    """Grow merge groups from `same` edges, with two brakes on transitivity.

    An explicit VETO: no edge may unite two forks an adjudication called
    different.

    And a DENSITY floor, which the veto alone does not provide. Only 118 of
    97,020 possible pairs were adjudicated, so most pairs inside a growing
    component were never judged at all and there is no veto to fire. Pure
    transitive closure then chains A~B~C~D through pairs nobody looked at: the
    first run of this produced a seven-fork group at density 0.38 that bundled
    threshold-sensitivity analyses with primary exposure construction --
    exactly the "a robustness refit is a different decision" case prompt 21
    tells the judge to keep apart.

    So a fork joins a group only if it was adjudicated the SAME as at least
    `density_min` of the members already in it. Over-merge is the error this
    project treats as unrecoverable; requiring positive evidence against most
    of a group, rather than absence of contrary evidence, is the conservative
    reading and it costs only under-merge, which is visible.
    """
    same = {frozenset((r["a"], r["b"])) for r in pairs if r["same"]}
    diff = {frozenset((r["a"], r["b"])) for r in pairs if not r["same"]}
    groups, used, vetoed = [], [], []
    for r in sorted([r for r in pairs if r["same"]], key=lambda r: -r["score"]):
        a, b = r["a"], r["b"]
        ga = next((g for g in groups if a in g), None)
        gb = next((g for g in groups if b in g), None)
        if ga is not None and ga is gb:
            used.append(r)
            continue

        def ok(node, grp):
            if any(frozenset((node, m)) in diff for m in grp):
                return False, "explicitly judged different"
            hits = sum(1 for m in grp if frozenset((node, m)) in same)
            if hits < math.ceil(density_min * len(grp)):
                return False, (f"same as {hits}/{len(grp)} of the group, "
                               f"below {density_min:.0%}")
            return True, ""

        if ga is None and gb is None:
            groups.append({a, b})
            used.append(r)
        elif ga is not None and gb is None:
            good, why = ok(b, ga)
            (used.append(r) or ga.add(b)) if good else \
                vetoed.append({**r, "reason": why})
        elif gb is not None and ga is None:
            good, why = ok(a, gb)
            (used.append(r) or gb.add(a)) if good else \
                vetoed.append({**r, "reason": why})
        else:
            cross = sum(1 for x in ga for y in gb if frozenset((x, y)) in same)
            need = math.ceil(density_min * len(ga) * len(gb))
            bad = any(frozenset((x, y)) in diff for x in ga for y in gb)
            if bad or cross < need:
                vetoed.append({**r, "reason": (
                    "explicitly judged different" if bad else
                    f"only {cross}/{len(ga)*len(gb)} cross edges adjudicated "
                    f"same, below {density_min:.0%}")})
            else:
                ga |= gb
                groups.remove(gb)
                used.append(r)
    return ({i: sorted(g) for i, g in enumerate(groups)}, used, vetoed)


def do_apply(tag, out_tag=None):
    mp = OUT / f"fork_merge_{tag}.json"
    if not mp.exists():
        sys.exit(f"run `merge_forks.py run --corpus {tag}` first")
    pairs = json.loads(mp.read_text(encoding="utf-8"))["pairs"]
    forks, _ = load(tag)
    comp, used, vetoed = components(pairs)

    reach = {f: len({r for o in forks[f] for _, _, r in forks[f][o]})
             for f in forks}
    name, groups = {}, {}
    for members in comp.values():
        if len(members) < 2:
            continue
        # the merged question is the model's phrasing where the pair agreed on
        # one, else the label of the fork more runs reached: an induced name is
        # better than an arbitrary pick, but a real corpus label beats both
        prop = [r.get("merged_question") for r in used
                if r["a"] in members and r["b"] in members
                and r.get("merged_question")]
        head = max(members, key=lambda f: reach.get(f, 0))
        label = prop[0] if prop else head
        for m in members:
            name[m] = label
        groups[label] = members

    d = json.loads((P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    _gp = garden_path(tag)
    gm = json.loads(_gp.read_text(encoding="utf-8"))
    cmap = {}
    for h, ms in gm.get("sibling_groups", {}).items():
        for m in ms:
            cmap[m] = h
    moved = 0
    # count the input BEFORE relabelling: `fork_raw` may already hold a label
    # from an earlier pass, and reading it afterwards reports that pass's
    # baseline instead of this one's -- 411 where the input had 375.
    before = len({o["fork"] for o in d["options"]})
    for o in d["options"]:
        node = cmap.get(o["fork"], o["fork"])
        if node in name and name[node] != o["fork"]:
            o["fork_raw"] = o["fork"]
            o["fork"] = name[node]
            moved += 1
    after = len({o["fork"] for o in d["options"]})
    d["fork_merge"] = {"groups": groups, "relabelled": moved,
                       "forks_before": before, "forks_after": after,
                       "edges_used": len(used), "edges_vetoed": len(vetoed)}
    p = P.VOCAB / f"bottom_up_{out_tag or tag + '.forkmerged'}.json"
    p.write_text(json.dumps(sync_counts(d), ensure_ascii=False, indent=1),
                 encoding="utf-8")

    print(f"APPLY - {tag}")
    print(f"  merge groups        {len(groups)}")
    print(f"  option records      {moved} relabelled")
    print(f"  decision points     {before} -> {after}")
    print(f"  edges used/vetoed   {len(used)}/{len(vetoed)}")
    print(f"\n  largest merges")
    for lab, mem in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:8]:
        print(f"    {len(mem)}x -> {lab[:66]}")
        for m in mem:
            print(f"         {m[:70]}")
    for v in vetoed[:4]:
        print(f"  VETOED {v['a'][:38]} ~ {v['b'][:38]}")
    print(f"\n-> {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "apply"])
    ap.add_argument("--corpus", default="ai+human.merged")
    # The repair chain loops to a fixpoint. Appending one suffix per
    # pass grew the tag to 77 characters that did not say which round
    # was which; build_all names the rounds `.rN` through this.
    ap.add_argument("--out-tag", dest="out_tag",
                    help="name the output; default <corpus>.forkmerged")
    a = ap.parse_args()
    if a.cmd == "run":
        do_run(a.corpus)
    else:
        do_apply(a.corpus, a.out_tag)
