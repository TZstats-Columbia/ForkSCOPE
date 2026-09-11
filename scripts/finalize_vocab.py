#!/usr/bin/env python3
"""Give a derived vocabulary its own garden file, so downstream runs unchanged.

Ten analysis and viewer scripts read `garden_<tag>.json` for the node table --
coverage, median script position, DSLC stage, the universal set. A corpus tag
gets that from `garden.py map`. A derived vocabulary (`....induced`) does not,
and without it every downstream script either crashes or, worse, silently falls
back to the base corpus map and reports one vocabulary's options against
another vocabulary's forks.

This builds the missing file:

  coverage / position   recomputed from the derived options, not inherited.
                        Both change when forks merge: a decision split across
                        two labels was two forks each reaching half the corpus.
  stage                 re-assigned by prompt 14 for fork labels that are new.
                        Labels carried over unchanged keep their existing stage
                        from the base garden, so this costs a model call only
                        for what actually changed.
  sibling_groups        emptied. Sibling merging is already folded into the
                        derived labels; leaving the base map in place would
                        apply it twice.

After this, `stability.py --corpus <tag>`, `grounds.py`, `circle.py` and the rest
work with no changes, because they only ever needed the two files this
guarantees exist.

Usage:
    python3 scripts/finalize_vocab.py --corpus ai+human.merged.forkmerged.merged.induced
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402
from vocab import OUT, base_of                                  # noqa: E402

BATCH = 70
UNIVERSAL = 0.60
STAGES = ["problem_formulation", "data_collection", "data_cleaning",
          "eda", "modeling", "communication"]
STAGE_SCHEMA = {"type": "object", "required": ["assignments"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    a = ap.parse_args()
    tag = a.corpus
    src = P.VOCAB / f"bottom_up_{tag}.json"
    if not src.exists():
        sys.exit(f"no {src.name}")
    d = json.loads(src.read_text(encoding="utf-8"))
    dec = d["decisions"]

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
            opts[o["fork"]][o["option"]].add(r)
            pos[o["fork"]].append(dec[i]["line"] / max(1, span[r]))
    runs = {x["run"] for x in dec}
    N = len(runs)

    # carry stages forward where the label is unchanged; only pay for new ones
    old = {}
    bp = OUT / f"fork_stage_{base_of(tag)}.json"
    if bp.exists():
        old = json.loads(bp.read_text(encoding="utf-8"))
    forks = sorted(opts)
    need = [f for f in forks if f not in old]
    print(f"FINALIZE - {tag}")
    print(f"{len(forks)} decision points, {sum(len(v) for v in opts.values())} "
          f"options, {N} runs")
    print(f"stages: {len(forks)-len(need)} carried over, {len(need)} to assign")

    stage = {f: old[f] for f in forks if f in old}
    if need:
        from llm import ask
        for k in range(0, len(need), BATCH):
            chunk = need[k:k + BATCH]
            want = set(range(k, k + len(chunk)))

            def check(o, want=want):
                ids = [x.get("id") for x in o.get("assignments", [])]
                miss = want - set(ids)
                if miss:
                    raise ValueError(f"{len(miss)} ids unassigned: "
                                     f"{sorted(miss)[:8]}")
                bad = sorted({str(x.get("stage")) for x in o["assignments"]
                              if x.get("stage") not in STAGES})
                if bad:
                    raise ValueError(f"stage must be one of {STAGES}; "
                                     f"got {bad[:4]}")

            out = ask("14_fork_stage",
                      {"forks": [{"id": k + j, "fork": f}
                                 for j, f in enumerate(chunk)]},
                      schema=STAGE_SCHEMA, model="opus",
                      run_id="fork_stage", check=check)
            for x in out["assignments"]:
                i = x.get("id")
                if isinstance(i, int) and 0 <= i < len(need):
                    stage[need[i]] = x.get("stage") if x.get("stage") in STAGES \
                        else "modeling"
            print(f"  {min(k + BATCH, len(need))}/{len(need)}", flush=True)
    for f in forks:
        stage.setdefault(f, "modeling")

    nodes = []
    for f in forks:
        rs = set().union(*opts[f].values())
        p = sorted(pos[f])
        nodes.append({"fork": f, "runs": len(rs),
                      "coverage": round(len(rs) / N, 3),
                      "options": len(opts[f]),
                      "position": round(p[len(p) // 2], 3) if p else 0.0,
                      "stage": stage[f]})
    nodes.sort(key=lambda x: -x["coverage"])
    gm = {"source": src.name, "derived": True, "runs": N,
          "raw_forks": len(forks), "nodes": len(forks),
          "sibling_groups": {},          # already folded into the labels
          "nodes_detail": nodes,
          "universal": [x["fork"] for x in nodes
                        if x["coverage"] >= UNIVERSAL],
          "gates": [], "gates_tested": 0, "gate_p_threshold": 0.0}
    gp = OUT / f"garden_{tag}.json"
    gp.write_text(json.dumps(gm, ensure_ascii=False, indent=1),
                  encoding="utf-8")
    sp = OUT / f"fork_stage_{tag}.json"
    sp.write_text(json.dumps(stage, ensure_ascii=False, indent=1),
                  encoding="utf-8")
    print(f"\nstage mix: {dict(Counter(stage[f] for f in forks))}")
    print(f"universal (>= {UNIVERSAL:.0%} of runs): {len(gm['universal'])}")
    print(f"-> {gp}\n-> {sp}")


if __name__ == "__main__":
    main()
