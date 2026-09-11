#!/usr/bin/env python3
"""Induce a vocabulary from a corpus of items, then assign every item to it.

One algorithm, three uses: typing the silent decisions, typing the
misalignments, and grouping the 3,665 decisions into forks. All three are the
same problem -- what categories are actually present in this data -- and none
of them may start from a taxonomy chosen in advance. That is the difference
from the upstream approach, whose fixed 21-slot schema dropped 33% of what its
own extractor found into `unmapped_decisions`.

Why not embeddings + a distance threshold: 94% of the decision strings are
unique (3,459 distinct of 3,665), so there is almost nothing for a lexical
metric to work with, and a dense embedding cannot be trusted to separate
"dichotomize at 0.25" from "dichotomize at 0.5" -- measured at cosine 1.00
under TF-IDF earlier in this project. The model does the semantic judgement;
this script does the sampling, batching, bookkeeping and convergence.

The loop:

  induce      show a stratified sample, get a candidate typology
  assign      batch every item against it, `NEW` allowed and encouraged
  consolidate fold recurring NEW proposals into the typology
  re-assign   only the items that came back NEW, against the grown typology

Convergence is measured, not assumed: the NEW rate after re-assignment is
reported, and a high residual means the typology is wrong rather than the items
being odd.

Usage:
    python3 scripts/cluster.py silent      # type the silent decisions
    python3 scripts/cluster.py misaligned  # type the misalignments
    python3 scripts/cluster.py forks       # group decisions into forks
    python3 scripts/cluster.py options     # options within each fork
    python3 scripts/cluster.py report      # tables from whatever exists
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import ask                                            # noqa: E402

import paths as P                                             # noqa: E402

OUT = P.ANALYSIS

SAMPLE_N = 90        # items shown to the induction pass
BATCH = 60           # items per assignment call
NEW_MIN = 3          # a NEW proposal needs this many hits to become a category

INDUCE_SCHEMA = {"type": "object", "required": ["categories"]}
ASSIGN_SCHEMA = {"type": "object", "required": ["assignments"]}


# ---------- item sources ----------------------------------------------------
def load_runs():
    """Records written before `arm` existed have none. The arm is a property of
    where the run lives in the corpus, so recover it from the layout rather than
    re-running anything -- same recovery distill.index() does."""
    out = []
    for d in sorted(P.DISTILLED.glob("*")):
        p = d / "record.json"
        if p.exists():
            out.append(json.loads(p.read_text(encoding="utf-8")))
    missing = [r for r in out if not r.get("arm") or r["arm"] == r.get("corpus")]
    if missing:
        try:
            import distill
            known = {rid: a for rid, _c, _arts, a in distill.discover()}
            for r in missing:
                r["arm"] = known.get(r["run_id"], r.get("arm") or "unknown")
        except Exception:
            for r in missing:
                r.setdefault("arm", "unknown")
    return out


def items_silent(runs):
    out = []
    for r in runs:
        for s in r["silent_decisions"]:
            out.append({"run": r["run_id"], "arm": r["arm"],
                        "text": s["operation"],
                        "meta": {"confidence": s.get("confidence")}})
    return out


def items_misaligned(runs):
    out = []
    for r in runs:
        for m in r["misalignments"]:
            out.append({"run": r["run_id"], "arm": r["arm"],
                        "text": f"CODE: {m['decision']}\nREPORT: {m['claim']}\n"
                                f"DISCREPANCY: {m['note']}",
                        "meta": {}})
    return out


def items_decisions(runs):
    """Every decision, for fork induction. Read from the span files, since the
    record only carries the silent ones."""
    out = []
    for r in runs:
        p = P.DISTILLED / r["run_id"] / "code_spans.json"
        if not p.exists():
            continue
        for s in json.loads(p.read_text(encoding="utf-8"))["spans"]:
            if s["kind"] != "decision":
                continue
            out.append({"run": r["run_id"], "arm": r["arm"],
                        "text": s["operation"],
                        "meta": {"targets": s.get("targets", []),
                                 "span_id": s["id"],
                                 "line": s["lines"][0][0] if s["lines"] else 0}})
    return out


KINDS = {
    "silent": (items_silent, "silent decision: an operation the code performs "
               "that the run's own report never mentions"),
    "misaligned": (items_misaligned, "misalignment: the code and the report "
                   "describe the same operation and disagree on a material "
                   "particular"),
    "forks": (items_decisions, "analytic decision: one choice a run made about "
              "how to handle the data. Group by the QUESTION each answers -- "
              "two runs answering the same question differently belong in one "
              "category, and the category is that question"),
}


# ---------- the loop --------------------------------------------------------
def stratified(items, n):
    """Spread the induction sample over arms and over the corpus, so the
    typology is not induced from whichever arm happens to sort first."""
    by = defaultdict(list)
    for i, it in enumerate(items):
        by[it["arm"]].append(i)
    arms, picked, k = sorted(by), [], 0
    while len(picked) < min(n, len(items)):
        a = arms[k % len(arms)]
        if by[a]:
            step = max(1, len(by[a]) // (n // max(1, len(arms)) + 1))
            picked.append(by[a].pop(len(by[a]) // 2 if step == 1 else 0))
        elif all(not by[x] for x in arms):
            break
        k += 1
    return picked


def induce(kind, items):
    idx = stratified(items, SAMPLE_N)
    sample = [{"id": i, "item": items[i]["text"]} for i in idx]
    out = ask("10_induce_types",
              {"item_kind": KINDS[kind][1], "n_total": len(items),
               "sample": sample},
              schema=INDUCE_SCHEMA, model="opus", run_id=f"cluster_{kind}")
    return out["categories"], out.get("note", "")


def assign(kind, items, cats, only=None):
    """Assign items to `cats`; returns {index: (category, confidence, proposed)}."""
    todo = list(range(len(items))) if only is None else list(only)
    brief = [{"id": c["id"], "name": c["name"], "definition": c["definition"],
              "criterion": c.get("criterion", "")} for c in cats]
    res = {}
    for k in range(0, len(todo), BATCH):
        chunk = todo[k:k + BATCH]
        out = ask("11_assign_types",
                  {"item_kind": KINDS[kind][1], "typology": brief,
                   "items": [{"id": i, "item": items[i]["text"]} for i in chunk]},
                  schema=ASSIGN_SCHEMA, run_id=f"cluster_{kind}")
        got = {a["id"]: a for a in out["assignments"]}
        for i in chunk:
            a = got.get(i)
            res[i] = ((a or {}).get("category", "NEW"),
                      (a or {}).get("confidence", "low"),
                      (a or {}).get("proposed", "") if a else "unassigned")
        print(f"    assigned {min(k+BATCH, len(todo))}/{len(todo)}", flush=True)
    return res


def consolidate(kind, res, items):
    """Fold recurring NEW proposals into real categories."""
    props = [(i, r[2]) for i, r in res.items() if r[0] == "NEW" and r[2]]
    if len(props) < NEW_MIN:
        return []
    out = ask("10_induce_types",
              {"item_kind": KINDS[kind][1] + " -- these did not fit the first "
                            "typology; propose categories that cover them",
               "n_total": len(props),
               "sample": [{"id": i, "item": items[i]["text"]} for i, _ in props]},
              schema=INDUCE_SCHEMA, model="opus", run_id=f"cluster_{kind}")
    return out["categories"]


def run(kind):
    OUT.mkdir(parents=True, exist_ok=True)
    runs = load_runs()
    items = KINDS[kind][0](runs)
    print(f"{kind}: {len(items)} items over {len(runs)} runs")

    print("  inducing typology...", flush=True)
    cats, note = induce(kind, items)
    print(f"  {len(cats)} categories: " + ", ".join(c["id"] for c in cats))
    if note:
        print(f"  note: {note}")

    print("  assigning...", flush=True)
    res = assign(kind, items, cats)
    n_new = sum(1 for r in res.values() if r[0] == "NEW")
    print(f"  NEW after first pass: {n_new}/{len(items)} ({n_new/len(items):.0%})")

    if n_new >= NEW_MIN:
        print("  consolidating...", flush=True)
        extra = consolidate(kind, res, items)
        if extra:
            print(f"  +{len(extra)} categories: " + ", ".join(c["id"] for c in extra))
            cats = cats + extra
            res.update(assign(kind, items, cats,
                              only=[i for i, r in res.items() if r[0] == "NEW"]))
            n_new = sum(1 for r in res.values() if r[0] == "NEW")
            print(f"  NEW after consolidation: {n_new}/{len(items)} "
                  f"({n_new/len(items):.0%})")

    payload = {
        "kind": kind, "n_items": len(items), "n_runs": len(runs),
        "residual_new": n_new, "categories": cats,
        "items": [{"run": items[i]["run"], "arm": items[i]["arm"],
                   "text": items[i]["text"], "meta": items[i]["meta"],
                   "category": res[i][0], "confidence": res[i][1],
                   "proposed": res[i][2]}
                  for i in range(len(items))],
    }
    p = OUT / f"{kind}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {p}")
    report_one(payload)


# ---------- reporting -------------------------------------------------------
def report_one(d):
    kind = d["kind"]
    cats = {c["id"]: c for c in d["categories"]}
    by = Counter(it["category"] for it in d["items"])
    arms = sorted({it["arm"] for it in d["items"]})
    print(f"\n{kind.upper()} — {d['n_items']} items, {len(cats)} categories, "
          f"{d['residual_new']} unassigned\n")
    w = max(len(c) for c in by) + 2
    print(f"  {'category':<{w}}{'n':>5}  " + "".join(f"{a[:11]:>13}" for a in arms))
    for c, n in by.most_common():
        cells = ""
        for a in arms:
            k = sum(1 for it in d["items"]
                    if it["category"] == c and it["arm"] == a)
            cells += f"{k:>13}"
        print(f"  {c:<{w}}{n:>5}  {cells}")
    print()
    for c, n in by.most_common():
        if c in cats:
            print(f"  {c}: {cats[c]['definition']}")


def report():
    for kind in ("silent", "misaligned", "forks"):
        p = OUT / f"{kind}.json"
        if p.exists():
            report_one(json.loads(p.read_text(encoding="utf-8")))
            print("\n" + "=" * 78 + "\n")


# ---------- level 2: options within a fork ----------------------------------
OPTION_MIN = 12      # below this a fork has too few decisions to cluster


def options():
    """Induce the distinct answers *within* each fork.

    A fork is the question; an option is an answer. Running induction inside a
    fork rather than over the whole corpus is what makes the categories
    comparable -- 'dichotomize at 0.5' and 'dichotomize at 0.25' are only
    distinguishable as answers to one question, and across the whole corpus they
    would be swamped by the difference between cleaning and modelling.

    This is the level stability and novelty are computed on: a stable option is
    one many runs chose, a novel option is one a single run chose, and the shape
    of that distribution per fork is the multiverse result.
    """
    src = OUT / "forks.json"
    if not src.exists():
        sys.exit("run `cluster.py forks` first")
    fk = json.loads(src.read_text(encoding="utf-8"))
    by = defaultdict(list)
    for it in fk["items"]:
        by[it["category"]].append(it)

    out = {"forks": {}, "n_items": len(fk["items"])}
    for fork in sorted(by, key=lambda f: -len(by[f])):
        items = by[fork]
        if len(items) < OPTION_MIN:
            out["forks"][fork] = {"n": len(items), "skipped": "too few decisions"}
            continue
        print(f"\n{fork}: {len(items)} decisions", flush=True)
        kind_desc = (f"answer to the analytic question '{fork}'. Group by WHICH "
                     f"ANSWER was given -- two runs that did the same thing in "
                     f"different words are one option; two runs that used "
                     f"different thresholds, variables or estimators are "
                     f"different options even if the wording is near-identical")
        KINDS["_opt"] = (None, kind_desc)
        idx = stratified(items, SAMPLE_N)
        cats = ask("10_induce_types",
                   {"item_kind": kind_desc, "n_total": len(items),
                    "sample": [{"id": i, "item": items[i]["text"]} for i in idx]},
                   schema=INDUCE_SCHEMA, model="opus",
                   run_id=f"opt_{fork}")["categories"]
        print(f"  {len(cats)} options: " + ", ".join(c["id"] for c in cats),
              flush=True)
        res = assign("_opt", items, cats)
        n_new = sum(1 for r in res.values() if r[0] == "NEW")
        print(f"  NEW: {n_new}/{len(items)} ({n_new/len(items):.0%})", flush=True)
        out["forks"][fork] = {
            "n": len(items), "residual_new": n_new, "options": cats,
            "items": [{"run": items[i]["run"], "arm": items[i]["arm"],
                       "text": items[i]["text"], "option": res[i][0],
                       "confidence": res[i][1]} for i in range(len(items))],
        }
        (OUT / "options.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {OUT / 'options.json'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd == "report":
        report()
    elif cmd == "options":
        options()
    elif cmd in KINDS:
        run(cmd)
    else:
        sys.exit(__doc__)
