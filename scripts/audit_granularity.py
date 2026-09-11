#!/usr/bin/env python3
"""Did the clustering actually cluster? Audit of option and fork granularity.

Prompted by the study owner reading the garden and reporting that options within a fork
"all look like the same actions". That is a claim about the central product of
this pipeline, so it is measured rather than argued.

Three questions, three measures:

  REDUNDANCY   within a fork, how many of its options are the same action under
               different words? Reported as distinct actions / options. 1.00
               means every option is a genuinely different choice; 0.50 means
               half the option count is paraphrase.
  GRANULARITY  are options recording an *action*, or an action plus the
               variable it was applied to? A fork whose options are "test
               position for confounding", "test league", "test club" has one
               action recorded three times, which inflates the option count and
               deflates every concentration statistic computed from it.
  MISFILING    options that do not answer the question their fork poses.

A token-overlap screen was tried first and is not adequate: it found only 2.7%
of within-fork option pairs above Jaccard 0.60, while missing that all four
top options of the rater-combination fork are the same averaging step. Lexical
similarity cannot see that "compute the mean of the two rater columns" and
"average the two raters' scores" are one action, which is the whole difficulty.
So adjudication is semantic, by the model, over a stratified sample.

Sampling is stratified by run count because the failure differs by size: small
forks are nearly all-singleton by construction, while the large forks carry
every statistic the project reports.

Usage:
    python3 scripts/audit_granularity.py --corpus ai --sample 40
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

from vocab import garden_path                                  # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
SEED = 20260822
WORKERS = 6
STRATA = [(2, 4, 0.25), (5, 9, 0.25), (10, 29, 0.25), (30, 10 ** 9, 0.25)]
SCHEMA = {"type": "object", "required": ["groups"]}


def tables(tag):
    _gp = garden_path(tag)
    gm = json.loads(_gp.read_text(encoding="utf-8"))
    d = json.loads((P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    dec = d["decisions"]
    cmap = {}
    for h, ms in gm.get("sibling_groups", {}).items():
        for m in ms:
            cmap[m] = h
    opts = defaultdict(lambda: defaultdict(set))
    for o in d["options"]:
        n = cmap.get(o["fork"], o["fork"])
        for i in o.get("members", []):
            if i < len(dec):
                opts[n][o["option"]].add(dec[i]["run"])
    return opts, d, gm


def judge(fork, om):
    from llm import ask
    items = sorted(om.items(), key=lambda kv: -len(kv[1]))
    ids = list(range(len(items)))

    def check(o):
        seen = [i for g in o.get("groups", []) for i in g.get("ids", [])]
        seen += o.get("misfiled", [])
        miss = set(ids) - set(seen)
        if miss:
            raise ValueError(f"option ids unplaced: {sorted(miss)[:8]}")
        dup = [i for i, c in Counter(seen).items() if c > 1]
        if dup:
            raise ValueError(f"option ids in more than one group: {dup[:6]}")

    out = ask("19_option_granularity",
              {"decision_point": fork,
               "options": [{"id": i, "option": o, "runs": len(rs)}
                           for i, (o, rs) in enumerate(items)]},
              schema=SCHEMA, model="opus", run_id="granularity", check=check)
    groups = out.get("groups", [])
    return {"fork": fork, "n_options": len(items),
            "n_runs": len(set().union(*om.values())),
            "n_actions": len(groups),
            "param_only": sum(1 for g in groups if g.get("parameter_only")),
            "misfiled": len(out.get("misfiled", [])),
            "note": out.get("note", ""),
            "groups": [{"action": g.get("action", ""),
                        "options": [items[i][0] for i in g.get("ids", [])
                                    if i < len(items)],
                        "runs": sum(len(items[i][1]) for i in g.get("ids", [])
                                    if i < len(items)),
                        "parameter_only": bool(g.get("parameter_only"))}
                       for g in groups]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    ap.add_argument("--sample", type=int, default=40)
    a = ap.parse_args()
    tag = "+".join(c.strip() for c in a.corpus.split(","))
    opts, d, gm = tables(tag)
    rng = random.Random(SEED)

    pool = {}
    for lo, hi, share in STRATA:
        cand = sorted(f for f, om in opts.items()
                      if len(om) >= 2 and lo <= len(set().union(*om.values())) <= hi)
        k = min(len(cand), max(1, round(a.sample * share)))
        for f in rng.sample(cand, k):
            pool[f] = (lo, hi)
    forks = sorted(pool)
    print(f"OPTION GRANULARITY AUDIT - {tag}")
    print(f"{len(opts)} forks total; adjudicating {len(forks)} sampled, "
          f"stratified by run count\n")

    res = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(judge, f, opts[f]): f for f in forks}
        for n, fu in enumerate(futs, 1):
            f = futs[fu]
            try:
                res.append(fu.result())
            except Exception as e:                              # noqa: BLE001
                print(f"  FAIL {f[:50]}: {type(e).__name__}", flush=True)
            if n % 8 == 0:
                print(f"  {n}/{len(forks)}", flush=True)

    if not res:
        sys.exit("no forks adjudicated")
    tot_o = sum(r["n_options"] for r in res)
    tot_a = sum(r["n_actions"] for r in res)
    print(f"\nREDUNDANCY  (distinct actions / options; 1.00 = no paraphrase)")
    print(f"  overall            {tot_a}/{tot_o} = {tot_a/tot_o:.3f}")
    print(f"  {'runs':<10}{'forks':>6}{'options':>9}{'actions':>9}{'ratio':>8}")
    for lo, hi, _ in STRATA:
        sub = [r for r in res if lo <= r["n_runs"] <= hi]
        if not sub:
            continue
        o = sum(x["n_options"] for x in sub)
        ac = sum(x["n_actions"] for x in sub)
        lab = f"{lo}-{hi}" if hi < 10 ** 9 else f"{lo}+"
        print(f"  {lab:<10}{len(sub):>6}{o:>9}{ac:>9}{ac/o:>8.3f}")

    par = [r for r in res if r["param_only"]]
    mis = [r for r in res if r["misfiled"]]
    print(f"\nGRANULARITY  forks with a parameter-only group: "
          f"{len(par)}/{len(res)}")
    print(f"MISFILING    forks with a misfiled option:       "
          f"{len(mis)}/{len(res)} "
          f"({sum(r['misfiled'] for r in mis)} options)")

    print(f"\nWORST COLLAPSES  (most option labels for one action)")
    flat = [(g["runs"], len(g["options"]), g["action"], r["fork"])
            for r in res for g in r["groups"] if len(g["options"]) >= 3]
    for runs, n, act, f in sorted(flat, reverse=True)[:10]:
        print(f"  {n:>2} labels, {runs:>3} runs   {act[:44]:<44} in {f[:38]}")

    payload = {"corpus": tag, "sampled": len(res),
               "options": tot_o, "actions": tot_a,
               "redundancy": round(tot_a / tot_o, 4),
               "param_only_forks": len(par), "misfiled_forks": len(mis),
               "forks": res}
    p = P.AUDITS / f"granularity_audit_{tag}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"\n-> {p}")


if __name__ == "__main__":
    main()
