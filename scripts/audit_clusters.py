#!/usr/bin/env python3
"""Quality audit of the bottom-up clustering. Deterministic; no model calls.

Every measure here is computable from the artifacts alone. That is deliberate:
an audit that needed a model would itself need auditing, and the point is to
have one layer in this pipeline whose output nobody has to take on trust.

Clustering can fail in exactly two directions, and they are not symmetric:

  OVER-MERGE   two genuinely different choices collapsed into one option.
               Invisible downstream -- the count looks clean and is wrong.
               This is the failure that destroys a multiverse analysis.
  UNDER-MERGE  one choice split across several options. Visible as suspicious
               near-duplicates, and recoverable by another merge round.

So the audit weights them differently: over-merge evidence is reported as a
defect list to be read, under-merge as a rate to be tolerated.

MEASURES
--------

L1 (decisions -> local groups)

  partition_integrity   Every decision must appear in exactly one L1 group.
                        Anything else means items were lost or duplicated by
                        the batching. Target: exact. A miss is a bug, not a
                        quality gradient.
  backfill_rate         Share of decisions the model failed to place, which the
                        pipeline then rescued as singletons. High values mean
                        the batch is too large or the prompt is failing, and
                        the resulting singletons are artifacts rather than
                        genuinely rare choices. Target: < 2%.
  compression           groups / decisions. 1.0 means no grouping happened;
                        very low means the batches are being flattened. There
                        is no correct value -- it is corpus-dependent -- but it
                        anchors the two rates below.

L2 (local groups -> options)

  numeric_conflict      THE over-merge test. An option whose members carry
                        different numbers (0.25 vs 0.5, 500 vs 2000 draws) has
                        merged choices that are not interchangeable. Numbers
                        are the discriminant a language model most reliably
                        ignores -- measured at cosine 1.00 for "dichotomize at
                        0.5" vs "at 0.25" under TF-IDF earlier in this project.
                        Target: 0 conflicts. Each one is listed.
  negation_conflict     Same idea for polarity: an option mixing members that
                        do and do not negate ("cluster SEs" with "do not
                        cluster SEs"). Target: 0.
  near_duplicate_pairs  The under-merge rate. Distinct options whose labels are
                        lexically near-identical after normalisation, and which
                        carry no conflicting number -- so they plausibly should
                        have merged. Reported as a rate; some are legitimate.
  singleton_options     Share of options chosen by exactly one decision. This
                        is NOT a defect: a rare choice is the signal a
                        multiverse study exists to find. It is reported because
                        a sudden change in it between runs indicates the
                        merging behaviour drifted.

L3 (questions -> forks)

  exclusivity           THE fork test, and the one structural check available.
                        If a fork is a set of alternatives, a single run should
                        pick one option from it. Options within a fork that
                        co-occur in the same run mean the fork is a *category*
                        -- a bag of compatible features -- not a fork. Measured
                        on v1 at 98% exclusive within-fork against 13% between,
                        so the signal is strong. Target: > 90% of forks clean.
  fork_run_coverage     Runs reaching each fork. A fork only one or two runs
                        reach cannot support any cross-arm comparison, and
                        should be reported as coverage rather than disagreement.
  orphan_questions      Questions that survived L3 as their own fork with a
                        single option. Usually under-merge at L3.

Usage:
    python3 scripts/audit_clusters.py [--corpus ai] [--json out.json]
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS

STOP = set("the a an of to in on for with and or as at by from is are was were "
           "be this that it its into per than then so such which each every all "
           "run runs analysis model data set".split())

# A number only discriminates when it sits in a comparison, and only in the same
# slot as the number it is compared against. A first cut that flagged any two
# differing numbers reported 54 conflicts of which most were an option
# mentioning both a z-multiplier and a confidence level, or two runs quoting
# their own sample sizes -- neither is a merge error. Slotting removes those
# without weakening the real test.
THRESH = re.compile(
    r"(>=|<=|>|<|=|at|above|below|cutoff|cut-off|threshold|thresholded)"
    r"\s*(\d+(?:\.\d+)?)", re.I)
# Contexts where a number is descriptive, not a choice between alternatives.
DESCRIPTIVE = re.compile(
    r"\b(?:95|99|90)\s*%|\b1\.96\b|\bp\s*<\s*0?\.0\d\b|\balpha\b|"
    r"\bn\s*=\s*\d|\bsample size\b|\bcount(?:s)? of\b", re.I)

# Negating the ACTION needs an auxiliary, "never", or "without <gerund>".
# A bare "no" almost always modifies a noun -- "drop dyads with no rating",
# "load the CSV with no filtering" -- where the absence is in the data, not in
# what the run did. Matching bare "no"/"not" flagged 10 options, all of them
# exclusion or load operations, and none of them a genuine polarity conflict.
NEG = re.compile(
    r"\b(?:do|does|did|is|are|was|were|has|have|had|can|could|would|should)"
    r"\s+not\b"
    r"|\bnot\s+(?:be|been|being|applied|used|performed|adjusted|clustered)\b"
    r"|\bnever\b|\bwithout\s+\w+ing\b|n't\b", re.I)


def toks(s):
    return frozenset(w for w in re.findall(r"[a-z]+", s.lower())
                     if w not in STOP and len(w) > 2)


def slot_nums(s):
    """Numbers that sit in a comparison slot, ignoring descriptive contexts.

    Returns a set of floats. `dichotomize at >= 0.5` yields {0.5}; `95% CI using
    1.96` yields nothing, because neither number is a choice between
    alternatives that a different run could have made otherwise.
    """
    out = set()
    for m in THRESH.finditer(s):
        window = s[max(0, m.start() - 24):m.end() + 8]
        if DESCRIPTIVE.search(window):
            continue
        try:
            op, v = m.group(1).lower(), float(m.group(2))
        except ValueError:
            continue
        # On an integer count, `> 0` and `>= 1` are the same threshold. Left
        # unnormalised they read as two different choices and the repair splits
        # a 62-member option into 61 + 1, manufacturing a singleton out of a
        # phrasing difference.
        if v.is_integer():
            if op == ">":
                v += 1
            elif op == "<":
                v -= 1
        out.add(v)
    return out


def negates(s):
    """True when the text negates its own action, not merely mentions removal.

    `exclude dyads with missing ratings` is not a negation -- excluding IS the
    action. `do not cluster standard errors` is. Bare 'exclude'/'drop' were
    firing on 136 options, essentially all of them exclusion options.
    """
    return bool(NEG.search(s))


def load(tag):
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        cand = sorted(P.VOCAB.glob("bottom_up_*.json"))
        if not cand:
            sys.exit("no bottom_up_*.json; run cluster_up.py build first")
        p = cand[-1]
    return json.loads(p.read_text(encoding="utf-8")), p


def load_l1(corpora):
    out = []
    for c in corpora:
        p = OUT / f"l1_{c}.json"
        if p.exists():
            out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


def audit_l1(l1s):
    rows = {}
    for d in l1s:
        c = d["corpus"]
        n = d["n_decisions"]
        seen = Counter()
        for g in d["groups"]:
            for i in g["ids"]:
                seen[i] += 1
        missing = [i for i in range(n) if i not in seen]
        dup = [i for i, k in seen.items() if k > 1]
        # a backfilled singleton is one whose label is the raw decision text
        texts = {i: x["text"] for i, x in enumerate(d["items"])}
        backfill = sum(1 for g in d["groups"]
                       if len(g["ids"]) == 1 and g.get("question") == "?"
                       and texts.get(g["ids"][0], "")[:90] == g["label"])
        rows[c] = {
            "decisions": n, "groups": len(d["groups"]),
            "compression": round(len(d["groups"]) / n, 3),
            "missing": len(missing), "duplicated": len(dup),
            "partition_ok": not missing and not dup,
            "backfilled": backfill,
            "backfill_rate": round(backfill / n, 4),
            "singleton_groups": sum(1 for g in d["groups"] if len(g["ids"]) == 1),
        }
    return rows


def audit_l2(d):
    opts = d["options"]
    dec = d["decisions"]
    conflicts, negs = [], []
    for o in opts:
        mem = o.get("members", [])
        if len(mem) < 2:
            continue
        texts = [dec[i]["text"] for i in mem if i < len(dec)]
        # OVER-MERGE, numeric: two members put different values in a comparison
        # slot. Members carrying no threshold at all are not evidence either way.
        sets = [slot_nums(t) for t in texts]
        vals = sorted(set().union(*sets)) if sets else []
        if len(vals) > 1:
            conflicts.append({"option": o["option"], "n": o["n"],
                              "numbers": vals,
                              "example": [t[:110] for t, s in zip(texts, sets)
                                          if s][:2]})
        # OVER-MERGE, polarity: members that are lexically near-identical but
        # disagree on negation. Requiring near-identity is what separates
        # "cluster SEs" vs "do not cluster SEs" from two unrelated members that
        # happen to differ in phrasing.
        for x in range(len(texts)):
            for y in range(x + 1, len(texts)):
                if negates(texts[x]) == negates(texts[y]):
                    continue
                tx, ty = toks(texts[x]), toks(texts[y])
                if tx and ty and len(tx & ty) / len(tx | ty) >= 0.6:
                    negs.append({"option": o["option"], "n": o["n"],
                                 "example": [texts[x][:110], texts[y][:110]]})
                    break
            else:
                continue
            break

    # under-merge: near-identical labels in different options, no number clash
    by = defaultdict(list)
    for i, o in enumerate(opts):
        by[o["fork"]].append(i)
    near = []
    for fork, idxs in by.items():
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                x, y = opts[idxs[a]], opts[idxs[b]]
                tx, ty = toks(x["option"]), toks(y["option"])
                if not tx or not ty:
                    continue
                j = len(tx & ty) / len(tx | ty)
                if j >= 0.8 and slot_nums(x["option"]) == slot_nums(y["option"]):
                    near.append({"fork": fork, "a": x["option"],
                                 "b": y["option"], "jaccard": round(j, 2)})
    return {
        "options": len(opts),
        "numeric_conflicts": len(conflicts),
        "negation_conflicts": len(negs),
        "near_duplicate_pairs": len(near),
        "near_duplicate_rate": round(len(near) / max(1, len(opts)), 4),
        "singleton_options": sum(1 for o in opts if o["n"] == 1),
        "singleton_rate": round(sum(1 for o in opts if o["n"] == 1)
                                / max(1, len(opts)), 3),
        "_conflicts": conflicts, "_negs": negs, "_near": near,
    }


def audit_l3(d):
    opts = d["options"]
    byfork = defaultdict(list)
    for o in opts:
        byfork[o["fork"]].append(o)
    bad, cover = [], {}
    for fork, os_ in byfork.items():
        runs = [set(o["runs"]) for o in os_]
        allruns = set().union(*runs) if runs else set()
        cover[fork] = len(allruns)
        # co-occurrence: a run holding two options of one fork
        clash = 0
        for a in range(len(os_)):
            for b in range(a + 1, len(os_)):
                if runs[a] & runs[b]:
                    clash += 1
        pairs = len(os_) * (len(os_) - 1) // 2
        if pairs and clash / pairs > 0.25:
            bad.append({"fork": fork, "options": len(os_),
                        "clashing_pairs": clash, "pairs": pairs,
                        "clash_rate": round(clash / pairs, 2),
                        "runs": len(allruns)})
    orphans = [f for f, os_ in byfork.items() if len(os_) == 1]
    return {
        "forks": len(byfork),
        "forks_failing_exclusivity": len(bad),
        "exclusivity_pass_rate": round(1 - len(bad) / max(1, len(byfork)), 3),
        "orphan_forks": len(orphans),
        "median_runs_per_fork": sorted(cover.values())[len(cover) // 2] if cover else 0,
        "forks_under_5_runs": sum(1 for v in cover.values() if v < 5),
        "_bad": bad, "_orphans": orphans[:20],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--json", nargs="?", const="",
                    help="write the report; defaults to "
                         "data/audits/audit_<tag>.json")
    a = ap.parse_args()
    corpora = [c.strip() for c in a.corpus.split(",") if c.strip()]
    tag = "+".join(corpora)
    d, path = load(tag)
    l1s = load_l1(corpora)

    print(f"CLUSTER QUALITY AUDIT — {path.name}")
    print(f"{d['n_decisions']} decisions -> {d['n_options']} options "
          f"-> {d['n_forks']} forks\n")

    r1 = audit_l1(l1s)
    print("L1 — decisions into local groups")
    for c, v in r1.items():
        ok = "PASS" if v["partition_ok"] else "FAIL"
        print(f"  [{c}] partition integrity      {ok}  "
              f"(missing {v['missing']}, duplicated {v['duplicated']})")
        print(f"       groups / decisions        {v['groups']}/{v['decisions']} "
              f"= {v['compression']}")
        bf = "PASS" if v["backfill_rate"] < 0.02 else "WARN"
        print(f"       backfill rate             {v['backfill_rate']:.2%}  {bf}"
              f"   (model failed to place; rescued as singletons)")
        print(f"       singleton groups          {v['singleton_groups']}")

    r2 = audit_l2(d)
    print("\nL2 — local groups into options")
    nc = "PASS" if r2["numeric_conflicts"] == 0 else "FAIL"
    print(f"  numeric conflicts (OVER-MERGE) {r2['numeric_conflicts']}  {nc}")
    ng = "PASS" if r2["negation_conflicts"] == 0 else "FAIL"
    print(f"  negation conflicts (OVER-MERGE) {r2['negation_conflicts']}  {ng}")
    print(f"  near-duplicate pairs (UNDER-MERGE) {r2['near_duplicate_pairs']} "
          f"= {r2['near_duplicate_rate']:.1%} of options")
    print(f"  singleton options              {r2['singleton_options']} "
          f"= {r2['singleton_rate']:.0%}   (signal, not defect)")
    for c in r2["_conflicts"][:6]:
        print(f"     conflict: {c['option'][:60]!r} mixes {c['numbers']}")
    for c in r2["_negs"][:4]:
        print(f"     negation: {c['option'][:60]!r} (n={c['n']})")

    r3 = audit_l3(d)
    print("\nL3 — questions into forks")
    ex = "PASS" if r3["exclusivity_pass_rate"] >= 0.90 else "FAIL"
    print(f"  exclusivity pass rate          {r3['exclusivity_pass_rate']:.0%}  "
          f"{ex}   ({r3['forks_failing_exclusivity']} of {r3['forks']} forks "
          f"look like categories, not forks)")
    print(f"  median runs per fork           {r3['median_runs_per_fork']}")
    print(f"  forks reached by < 5 runs      {r3['forks_under_5_runs']} "
          f"(coverage, not disagreement)")
    print(f"  orphan forks (one option)      {r3['orphan_forks']}")
    for b in sorted(r3["_bad"], key=lambda x: -x["clash_rate"])[:6]:
        print(f"     {b['fork'][:54]!r}: {b['clash_rate']:.0%} of option pairs "
              f"co-occur in a run")

    if a.json:
        Path(a.json).write_text(json.dumps(
            {"source": path.name, "l1": r1, "l2": r2, "l3": r3},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n-> {a.json}")


if __name__ == "__main__":
    main()
