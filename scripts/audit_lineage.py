#!/usr/bin/env python3
"""End-to-end validation of decision -> option -> fork. Seeded and reproducible.

Every earlier check on the clustering compared *labels*. That cannot see the
error that matters most: whether the raw decisions grouped under one option
label really record one choice. `audit_granularity.py` asked whether two option
labels meant the same thing; this asks whether one option label is honest about
the twenty raw operations underneath it.

Two directions, because the two errors are not symmetric and are not found the
same way.

  L1  OVER-MERGE, traced downward. Sample forks, sample options within them,
      pull the RAW operation text of every decision assigned to each option, and
      ask whether they are one choice (prompt 20). This is the only check in the
      project that reads what the clustering actually consumed. Verdicts are
      `coherent`, `impure` (a few stragglers) or `split` (two choices of equal
      weight) -- distinguished because they imply different repairs.

  L3  UNDER-MERGE, tested sideways. Take neighbouring forks -- similar labels,
      or mutually exclusive across runs, or sharing option vocabulary -- and ask
      whether they are one question (prompt 21). Neighbours rather than random
      pairs: a random pair of forks is almost never the same question, so
      random sampling would spend the whole budget confirming the obvious.

  POST-MERGE RESIDUE. Re-measures within-fork option redundancy on whatever
      vocabulary is passed in. After `merge_options.py` this should be near
      1.00; if it is not, that pass under-performed and the number says so.

Reproducibility: sampling is seeded, model calls are cached on content, and
every verdict is written out with the fork, option and raw ids it was made
about, so any number here can be traced back to the text that produced it.

Usage:
    python3 scripts/audit_lineage.py --corpus ai+human.merged --forks 25 --pairs 30
"""
import argparse
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

from vocab import garden_path                                  # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
SEED = 20260823
WORKERS = 6
MAX_RAW = 14          # raw operations shown per option
MIN_RAW = 3           # below this there is nothing to test for purity
STOP = set("how is are the a an of to into for from in on at by with and or "
           "what which used use does do this that it its as be when where "
           "primary model analysis data".split())
PURITY_SCHEMA = {"type": "object", "required": ["verdict"]}
IDENT_SCHEMA = {"type": "object", "required": ["same"]}


def toks(s):
    return {w for w in re.findall(r"[a-z]+", (s or "").lower())
            if w not in STOP and len(w) > 2}


def jac(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def load(tag):
    """Fork -> option -> [(decision index, raw text, run)], via garden merges."""
    _gp = garden_path(tag)
    d = json.loads((P.VOCAB / f"bottom_up_{tag}.json").read_text(encoding="utf-8"))
    gm = json.loads(_gp.read_text(encoding="utf-8"))
    dec = d["decisions"]
    cmap = {}
    for h, ms in gm.get("sibling_groups", {}).items():
        for m in ms:
            cmap[m] = h
    forks = defaultdict(lambda: defaultdict(list))
    for o in d["options"]:
        node = cmap.get(o["fork"], o["fork"])
        for i in o.get("members", []):
            if i < len(dec):
                forks[node][o["option"]].append(
                    (i, (dec[i].get("text") or "").strip(), dec[i]["run"]))
    return forks, dec


# --------------------------------------------------------------------------
def purity(fork, option, rows, rng):
    from llm import ask
    show = rows if len(rows) <= MAX_RAW else rng.sample(rows, MAX_RAW)
    ids = list(range(len(show)))

    def check(o):
        v = o.get("verdict")
        if v not in ("coherent", "impure", "split"):
            raise ValueError("verdict must be coherent, impure or split")
        bad = [r.get("id") for r in o.get("rejects", [])
               if r.get("id") not in ids]
        if bad:
            raise ValueError(f"reject ids not in the list: {bad[:5]}")
        if v == "impure" and not o.get("rejects"):
            raise ValueError("verdict 'impure' needs at least one reject")
        if v == "coherent" and o.get("rejects"):
            raise ValueError("verdict 'coherent' cannot carry rejects")

    out = ask("20_option_purity",
              {"decision_point": fork, "option": option,
               "raw_operations": [{"id": i, "operation": t}
                                  for i, (_, t, _) in enumerate(show)]},
              schema=PURITY_SCHEMA, model="opus", run_id="lineage_purity",
              check=check)
    return {"fork": fork, "option": option, "n_members": len(rows),
            "n_shown": len(show), "verdict": out["verdict"],
            "rejects": out.get("rejects", []),
            "groups": out.get("groups", []), "note": out.get("note", ""),
            "shown_ids": [i for i, _, _ in show]}


def identity(fa, fb, forks):
    from llm import ask
    def opts(f):
        return sorted(forks[f], key=lambda o: -len(forks[f][o]))[:12]
    out = ask("21_fork_identity",
              {"fork_a": {"question": fa, "options": opts(fa)},
               "fork_b": {"question": fb, "options": opts(fb)}},
              schema=IDENT_SCHEMA, model="opus", run_id="lineage_identity")
    return {"a": fa, "b": fb, "same": bool(out.get("same")),
            "confidence": out.get("confidence", ""),
            "why": out.get("why", ""),
            "merged_question": out.get("merged_question", "")}


def neighbours(forks, k):
    """Fork pairs worth testing: similar wording, mutually exclusive, or
    sharing option vocabulary. Random pairs would waste the budget."""
    fs = sorted(forks)
    runs = {f: {r for o in forks[f] for _, _, r in forks[f][o]} for f in fs}
    tk = {f: toks(f) for f in fs}
    ov = {f: set().union(*[toks(o) for o in forks[f]]) if forks[f] else set()
          for f in fs}
    cand = []
    for i, a in enumerate(fs):
        for b in fs[i + 1:]:
            if len(runs[a]) < 4 or len(runs[b]) < 4:
                continue
            lab = jac(tk[a], tk[b])
            opv = jac(ov[a], ov[b])
            co = len(runs[a] & runs[b])
            exp = len(runs[a]) * len(runs[b]) / max(1, len(set().union(*runs.values())))
            excl = 1.0 if (co == 0 and exp >= 4) else 0.0
            score = 1.6 * lab + 1.0 * opv + 0.9 * excl
            if score > 0.55:
                cand.append((score, a, b, round(lab, 2), round(opv, 2),
                             co, round(exp, 1)))
    cand.sort(reverse=True)
    return cand[:k]


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="ai+human.merged")
    ap.add_argument("--forks", type=int, default=25)
    ap.add_argument("--pairs", type=int, default=30)
    a = ap.parse_args()
    tag = a.corpus
    forks, dec = load(tag)
    rng = random.Random(SEED)

    print(f"LINEAGE AUDIT - {tag}")
    print(f"{len(forks)} forks, {sum(len(v) for v in forks.values())} options, "
          f"{len(dec)} decisions")
    print(f"seed {SEED}; every verdict traceable to the raw ids it was made "
          f"about\n")

    # ---- L1 over-merge, traced downward ---------------------------------
    pool = [(f, o) for f in forks for o in forks[f]
            if len(forks[f][o]) >= MIN_RAW]
    pool.sort()
    fset = sorted({f for f, _ in pool})
    pick_f = rng.sample(fset, min(a.forks, len(fset)))
    jobs = []
    for f in pick_f:
        os_ = sorted([o for o in forks[f] if len(forks[f][o]) >= MIN_RAW],
                     key=lambda o: -len(forks[f][o]))
        jobs += [(f, o) for o in os_[:3]]
    print(f"L1 OVER-MERGE  tracing {len(jobs)} options in {len(pick_f)} forks "
          f"down to raw operations")

    res = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(purity, f, o, forks[f][o],
                          random.Random(hash((f, o)) & 0xffffffff))
                for f, o in jobs]
        for n, fu in enumerate(futs, 1):
            try:
                res.append(fu.result())
            except Exception as e:                              # noqa: BLE001
                print(f"  FAIL: {type(e).__name__}: {e}"[:110], flush=True)
            if n % 10 == 0:
                print(f"  {n}/{len(jobs)}", flush=True)

    v = Counter(r["verdict"] for r in res)
    shown = sum(r["n_shown"] for r in res)
    rej = sum(len(r["rejects"]) for r in res)
    print(f"\n  options traced        {len(res)}")
    print(f"  raw operations read   {shown}")
    print(f"  coherent              {v['coherent']:>4}  "
          f"{v['coherent']/max(1,len(res)):.0%}")
    print(f"  impure (stragglers)   {v['impure']:>4}  "
          f"{v['impure']/max(1,len(res)):.0%}")
    print(f"  split (two choices)   {v['split']:>4}  "
          f"{v['split']/max(1,len(res)):.0%}")
    print(f"  raw ops rejected      {rej} of {shown} ({rej/max(1,shown):.1%})")
    for r in [x for x in res if x["verdict"] == "split"][:5]:
        print(f"    SPLIT  {r['option'][:56]}")
        for g in r["groups"][:3]:
            print(f"           {len(g.get('ids', []))}x {g.get('choice','')[:52]}")
    for r in [x for x in res if x["verdict"] == "impure"][:5]:
        print(f"    IMPURE {r['option'][:52]}")
        for x in r["rejects"][:2]:
            print(f"           -> {str(x.get('records',''))[:60]}")

    # ---- L3 under-merge, tested sideways --------------------------------
    cand = neighbours(forks, a.pairs)
    print(f"\nL3 UNDER-MERGE  {len(cand)} neighbouring fork pairs "
          f"(label / option-vocabulary / mutual-exclusion)")
    pairs = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(identity, x[1], x[2], forks) for x in cand]
        for n, fu in enumerate(futs, 1):
            try:
                pairs.append(fu.result())
            except Exception as e:                              # noqa: BLE001
                print(f"  FAIL: {type(e).__name__}"[:80], flush=True)
            if n % 10 == 0:
                print(f"  {n}/{len(cand)}", flush=True)
    same = [p for p in pairs if p["same"]]
    print(f"\n  pairs tested          {len(pairs)}")
    print(f"  judged ONE question   {len(same)} "
          f"({len(same)/max(1,len(pairs)):.0%} of candidates)")
    for p in same[:10]:
        print(f"    [{p['confidence']}] {p['why'][:62]}")
        print(f"       {p['a'][:66]}")
        print(f"       {p['b'][:66]}")

    # ---- post-merge residue ----------------------------------------------
    dup = tot = 0
    for f in forks:
        os_ = list(forks[f])
        for i, x in enumerate(os_):
            for y in os_[i + 1:]:
                tot += 1
                if jac(toks(x), toks(y)) >= 0.6:
                    dup += 1
    print(f"\nPOST-MERGE RESIDUE  (lexical, a floor not a measure)")
    print(f"  within-fork option pairs at Jaccard >= 0.60: "
          f"{dup} of {tot} ({dup/max(1,tot):.2%})")

    payload = {"corpus": tag, "seed": SEED,
               "purity": {"traced": len(res), "raw_read": shown,
                          "verdicts": dict(v), "rejected_raw": rej,
                          "results": res},
               "identity": {"tested": len(pairs), "same": len(same),
                            "candidates": [{"score": round(c[0], 3), "a": c[1],
                                            "b": c[2], "label_jaccard": c[3],
                                            "option_jaccard": c[4],
                                            "co_runs": c[5], "expected": c[6]}
                                           for c in cand],
                            "results": pairs},
               "residue": {"dup_pairs": dup, "pairs": tot}}
    p = P.AUDITS / f"lineage_audit_{tag}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"\n-> {p}")


if __name__ == "__main__":
    main()
