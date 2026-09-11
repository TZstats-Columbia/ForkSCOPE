#!/usr/bin/env python3
"""Group options into decision points by purpose. The missing clustering step.

The study owner's diagnosis: options belong to one fork when they serve the same
*purpose*, not when they look like similar actions. Checking the pipeline
against that showed the step does not exist. Prompt 13 merges option LABELS and
emits a `question` per group as free text, written in isolation, never compared
to any other group's question. So decision points were a by-product of option
merging rather than a clustering of options -- which is exactly why
`merge_forks.py` found 63 duplicate fork pairs to clean up afterwards.

This does the step properly, with purpose as the criterion and a structural
check on the result.

WHY PURPOSE CUTS AGAINST SURFACE SIMILARITY
-------------------------------------------
    drop dyads with no rating  /  impute the rating from the other rater
        no shared words, opposite operations -- ONE decision point
    drop dyads with no rating  /  drop goalkeepers
        near-identical phrasing, same operation -- TWO decision points

Any lexical or embedding method gets both of these backwards, which is why the
grouping is adjudicated (prompt 22) and the operational test is foreclosure:
could one analyst do both in one script? If yes they are different slots; if
taking one rules out the other they are rivals at one slot.

THE STRUCTURAL VETO, FINALLY WIRED IN
-------------------------------------
The v2 plan specified a cannot-link constraint from mutual exclusivity -- 98% of
same-fork option pairs never co-occur, against 13% of different-fork pairs --
and it was never implemented; it only ever appeared as a diagnostic. Here it is
used twice: co-occurrence counts are given to the adjudicator as evidence, and
afterwards every induced group is scored for how often its supposedly rival
options actually co-occur. A group whose options routinely appear together in
one run is reported as a violation rather than quietly kept.

Batching is by cluster of related options, not arbitrary slices, because the
question "are these rivals?" is unanswerable when the rival is in another
batch.

Usage:
    python3 scripts/induce_forks.py run   --corpus ai+human.merged.forkmerged
    python3 scripts/induce_forks.py apply --corpus ai+human.merged.forkmerged
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
from audit_lineage import jac, load, toks                        # noqa: E402
from vocab import sync_counts                                   # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
WORKERS = 6
BATCH = 45            # options per adjudication
CO_WARN = 0.25        # a group is flagged when this share of its pairs conflict
CO_MIN = 2            # ...and a pair conflicts only at this many shared runs.
# One shared run is not evidence that two options are non-rivals: it is one
# analyst who fitted three moderation specs, or recorded the same slot twice.
# Counting a single co-occurrence turned that into a 100% violation rate and
# made the check disagree with `enforce_exclusivity.py`, which uses 2. They
# agree now, and on this corpus no group has any pair sharing more than 2 runs.
SCHEMA = {"type": "object", "required": ["decision_points"]}


def batches(opts, runs_of, size=BATCH):
    """Seed batches on the busiest option, then pull in its nearest relatives.

    Arbitrary slices would separate rivals, and the adjudicator cannot see that
    two options are alternatives when one of them is in another batch. Nearness
    here is lexical, which is a weak proxy for purpose -- but it only decides
    what gets COMPARED, not what gets merged, so a weak proxy is acceptable
    where it would not be for the decision itself.
    """
    tk = {o: toks(o) for o in opts}
    left = sorted(opts, key=lambda o: (-len(runs_of[o]), o))
    out = []
    while left:
        seed = left.pop(0)
        grp = [seed]
        left.sort(key=lambda o: -jac(tk[seed], tk[o]))
        take = min(size - 1, len(left))
        grp += left[:take]
        left = left[take:]
        out.append(grp)
    return out


def co_matrix(grp, runs_of):
    co = {}
    for i, a in enumerate(grp):
        for b in grp[i + 1:]:
            n = len(runs_of[a] & runs_of[b])
            if n:
                co[(a, b)] = n
    return co


def adjudicate(grp, runs_of):
    from llm import ask
    idx = {o: i for i, o in enumerate(grp)}
    co = co_matrix(grp, runs_of)
    ids = set(idx.values())

    def check(o):
        seen = [i for dp in o.get("decision_points", []) for i in dp.get("ids", [])]
        miss = ids - set(seen)
        if miss:
            raise ValueError(f"{len(miss)} option ids unplaced: "
                             f"{sorted(miss)[:8]}")
        dup = [i for i, c in Counter(seen).items() if c > 1]
        if dup:
            raise ValueError(f"option ids in more than one group: {dup[:6]}")
        bad = [dp.get("question", "") for dp in o["decision_points"]
               if not (dp.get("question") or "").strip().endswith("?")]
        if bad:
            raise ValueError("every question must be phrased as a question "
                             f"ending in '?'; got {bad[:3]}")

    out = ask("22_induce_forks",
              {"options": [{"id": idx[o], "option": o,
                            "runs": len(runs_of[o])} for o in grp],
               "co_occurring_pairs": [{"a": idx[a], "b": idx[b], "co_runs": n}
                                      for (a, b), n in
                                      sorted(co.items(), key=lambda kv: -kv[1])[:60]]},
              schema=SCHEMA, model="opus", run_id="induce_forks", check=check)
    return [{"question": dp["question"].strip(),
             "options": [grp[i] for i in dp["ids"] if i < len(grp)],
             "why_rival": dp.get("why_rival", "")}
            for dp in out["decision_points"]]


def do_run(tag):
    forks, _ = load(tag)
    runs_of = defaultdict(set)
    for f in forks:
        for o, rows in forks[f].items():
            runs_of[o] |= {r for _, _, r in rows}
    opts = sorted(runs_of)
    bs = batches(opts, runs_of)
    print(f"INDUCE FORKS - {tag}")
    print(f"{len(opts)} options -> {len(bs)} batches of <= {BATCH}, "
          f"seeded on the busiest option and filled with its nearest\n")

    groups, fails = [], []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(adjudicate, g, runs_of) for g in bs]
        for n, fu in enumerate(futs, 1):
            try:
                groups += fu.result()
            except Exception as e:                              # noqa: BLE001
                fails.append(f"{type(e).__name__}: {e}"[:160])
                print(f"  FAIL batch {n}: {fails[-1][:80]}", flush=True)
            print(f"  {n}/{len(bs)}", flush=True)

    # structural check: rivals should not co-occur
    viol = []
    for g in groups:
        os_ = g["options"]
        if len(os_) < 2:
            continue
        tot = len(os_) * (len(os_) - 1) // 2
        hit = sum(1 for i, a in enumerate(os_) for b in os_[i + 1:]
                  if len(runs_of[a] & runs_of[b]) >= CO_MIN)
        g["co_pair_share"] = round(hit / tot, 3)
        if hit / tot > CO_WARN:
            viol.append(g)
    print(f"\n  decision points induced   {len(groups)}")
    print(f"  singletons                "
          f"{sum(1 for g in groups if len(g['options']) == 1)}")
    print(f"  batches failed            {len(fails)}")
    print(f"\n  STRUCTURAL CHECK  (options at one decision point are rivals, "
          f"so they\n  should rarely co-occur in the same run)")
    print(f"  groups above {CO_WARN:.0%} co-occurring pairs: "
          f"{len(viol)} of {sum(1 for g in groups if len(g['options'])>1)}")
    for g in sorted(viol, key=lambda g: -g["co_pair_share"])[:6]:
        print(f"    {g['co_pair_share']:.0%}  {g['question'][:62]}")
        for o in g["options"][:3]:
            print(f"          {o[:66]}")
    p = OUT / f"induced_forks_{tag}.json"
    p.write_text(json.dumps({"corpus": tag, "batch": BATCH,
                             "failures": fails, "violations": len(viol),
                             "decision_points": groups},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {p}")


def do_apply(tag):
    ip = OUT / f"induced_forks_{tag}.json"
    if not ip.exists():
        sys.exit(f"run `induce_forks.py run --corpus {tag}` first")
    dps = json.loads(ip.read_text(encoding="utf-8"))["decision_points"]
    lut = {}
    for dp in dps:
        for o in dp["options"]:
            lut.setdefault(o, dp["question"])
    d = json.loads((P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    moved = 0
    for o in d["options"]:
        q = lut.get(o["option"])
        if q and q != o["fork"]:
            o.setdefault("fork_raw", o["fork"])
            o["fork"] = q
            moved += 1
    before = len({o.get("fork_raw", o["fork"]) for o in d["options"]})
    after = len({o["fork"] for o in d["options"]})
    d["fork_induction"] = {"relabelled": moved, "forks_before": before,
                           "forks_after": after}
    p = P.VOCAB / f"bottom_up_{tag}.induced.json"
    p.write_text(json.dumps(sync_counts(d), ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"APPLY - {tag}")
    print(f"  option records relabelled  {moved}")
    print(f"  decision points            {before} -> {after}")
    print(f"-> {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "apply"])
    ap.add_argument("--corpus", default="ai+human.merged.forkmerged")
    a = ap.parse_args()
    (do_run if a.cmd == "run" else do_apply)(a.corpus)
