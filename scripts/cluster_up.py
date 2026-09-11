#!/usr/bin/env python3
"""Bottom-up clustering: decisions -> options -> forks, with no imposed cap.

This replaces the top-down path in cluster.py, which sampled 2.5% of the corpus,
had a model propose 4-12 categories from that sample, and force-fitted the rest.
That is the fixed-schema move this project exists to avoid -- derived from a
sample rather than a design meeting, but a cap either way, and it produced 10
forks for 3,665 decisions with ~350 items each.

Here the counts emerge:

  L1 group   sort decisions so related ones are adjacent, then group each batch
             with no target number. A group of one is a valid answer -- that is
             how a rare choice survives to be counted.
  L2 merge   the same choice was labelled independently in different batches;
             merge those labels. Still no target number.
  L3 fork    every option already carries the question it answers; merge the
             questions the same way. Forks are what is left.

Ordering is the only place a prior enters, and it is a weak one: decisions are
sorted by their most distinctive data target and then by pipeline position, so
a batch is likely to contain related decisions. The model is free to ignore the
adjacency, and a wrong sort costs recall at L1 which L2 then recovers.

Usage:
    python3 scripts/cluster_up.py l1    --corpus ai       # phase 1, per corpus
    python3 scripts/cluster_up.py l1    --corpus human
    python3 scripts/cluster_up.py build --corpus ai,human # L2+L3 over both
    python3 scripts/cluster_up.py report --corpus ai,human

Cluster POOLED for any AI-vs-human comparison. Clustering the corpora separately
produces two incomparable vocabularies -- the mistake v1 made and the reason its
human side ended up ten times finer-grained per record than its AI side.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402
from llm import ask                                            # noqa: E402
import cluster as C                                            # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS

BATCH = 55           # decisions per L1 call
MERGE_BATCH = 70     # labels per L2/L3 call
MERGE_ROUNDS = 3     # repeat merging until it stops changing, or this many
L1_WORKERS = 8       # L1 batches are independent; the real cap is llm.py's semaphore

GROUP_SCHEMA = {"type": "object", "required": ["groups"]}
MERGE_SCHEMA = {"type": "object", "required": ["merged"]}


def norm_target(t):
    """Collapse the surface variants of one data entity.

    Runs name the same column differently -- dark_skin, darkskin, skinTone,
    skin_tone_avg. This is not a semantic judgement, just spelling: lowercase,
    drop separators, strip the affixes runs habitually add.
    """
    s = re.sub(r"[^a-z0-9]", "", str(t).lower())
    for a in ("df", "data", "the"):
        if s.startswith(a) and len(s) > len(a) + 2:
            s = s[len(a):]
    for z in ("avg", "mean", "cat", "bin", "std", "log", "col", "var", "idx"):
        if s.endswith(z) and len(s) > len(z) + 2:
            s = s[: -len(z)]
    return s or "unknown"


def sort_key(items):
    """Order decisions so related ones land in the same batch.

    Primary key is the decision's rarest target -- the rarest one is the most
    identifying, since `df` or `games` appears everywhere and tells us little.
    Secondary key is pipeline position, so that within one entity the cleaning
    decisions precede the modelling ones.
    """
    freq = Counter()
    for it in items:
        for t in it["meta"]["targets"]:
            freq[norm_target(t)] += 1

    def key(i):
        ts = [norm_target(t) for t in items[i]["meta"]["targets"]] or ["unknown"]
        rarest = min(ts, key=lambda t: (freq[t], t))
        return (rarest, items[i]["meta"]["line"], i)
    return sorted(range(len(items)), key=key)


def _l1_batch(bi, chunk, items):
    out = ask("12_group_batch",
              {"batch_index": bi,
               "decisions": [{"id": i, "decision": items[i]["text"],
                              "targets": items[i]["meta"]["targets"]}
                             for i in chunk]},
              schema=GROUP_SCHEMA, run_id="cluster_up_l1")
    got, seen = [], set()
    cset = set(chunk)
    for g in out["groups"]:
        ids = [i for i in g.get("ids", []) if i in cset]
        if not ids:
            continue
        seen.update(ids)
        got.append({"label": g.get("label", "?"),
                    "question": g.get("question", "?"), "ids": ids})
    # a decision the model dropped becomes its own group rather than vanishing:
    # losing an item silently is worse than an ugly singleton
    for i in chunk:
        if i not in seen:
            got.append({"label": items[i]["text"][:90], "question": "?",
                        "ids": [i]})
    return bi, got


def l1_group(items):
    """Batch the sorted decisions and group each batch. No cap on group count.

    Batches are independent, so they run concurrently; the ceiling is the
    semaphore in llm.py, not this loop. Results are reassembled in batch order
    so the output does not depend on completion order -- otherwise the same
    inputs would produce a differently-ordered file on every run and the
    downstream merge would not be reproducible.
    """
    order = sort_key(items)
    batches = [(k // BATCH, order[k:k + BATCH])
               for k in range(0, len(order), BATCH)]
    done, out = 0, {}
    with ThreadPoolExecutor(max_workers=L1_WORKERS) as ex:
        futs = [ex.submit(_l1_batch, bi, ch, items) for bi, ch in batches]
        for f in as_completed(futs):
            bi, got = f.result()
            out[bi] = got
            done += 1
            print(f"  L1 {done}/{len(batches)} batches "
                  f"-> {sum(len(v) for v in out.values())} groups", flush=True)
    return [g for bi in sorted(out) for g in out[bi]]


def _merge_batch(bi, base, chunk, prompt, run_id):
    """Merge one batch of labels. Returns (batch_index, merged_units)."""
    out = ask(prompt,
              {"labels": [{"id": base + j,
                           "label": u["label"], "question": u["question"]}
                          for j, u in enumerate(chunk)]},
              schema=MERGE_SCHEMA, run_id=run_id)
    merged, taken = [], set()
    for m in out["merged"]:
        mem = [x - base for x in m.get("members", [])
               if base <= x < base + len(chunk)]
        if not mem:
            continue
        taken.update(mem)
        merged.append({
            "label": m.get("label", chunk[mem[0]]["label"]),
            "question": m.get("question", chunk[mem[0]]["question"]),
            "members": [i for j in mem for i in chunk[j]["members"]],
        })
    # a label the model failed to place survives unmerged rather than vanishing
    for j, u in enumerate(chunk):
        if j not in taken:
            merged.append(dict(u))
    return bi, merged


def merge_labels(units, prompt, run_id):
    """One merging round over `units`, batches in parallel, order preserved."""
    batches, base = [], 0
    for k in range(0, len(units), MERGE_BATCH):
        batches.append((k // MERGE_BATCH, base, units[k:k + MERGE_BATCH]))
        base += len(units[k:k + MERGE_BATCH])
    done, out = 0, {}
    with ThreadPoolExecutor(max_workers=L1_WORKERS) as ex:
        futs = [ex.submit(_merge_batch, bi, b, ch, prompt, run_id)
                for bi, b, ch in batches]
        for f in as_completed(futs):
            bi, got = f.result()
            out[bi] = got
            done += 1
            print(f"  merge {done}/{len(batches)} batches "
                  f"-> {sum(len(v) for v in out.values())}", flush=True)
    return [u for bi in sorted(out) for u in out[bi]]


def decisions_for(corpus):
    """Decisions from one corpus, tagged so the pooled merge can tell them apart.

    Split by corpus because L1 batching depends on sorting the whole item set:
    adding the 31 human teams to a pooled sort reshuffles every batch and
    invalidates all 67 cached AI calls. Running L1 per corpus keeps each one
    stable and cached, and L2 merges across them afterwards -- which is the
    right shape anyway, since L1 is local grouping and L2 is global.
    """
    runs = [r for r in C.load_runs()
            if corpus == "pooled" or r.get("corpus", _default_corpus()) == corpus]
    items = C.items_decisions(runs)
    for it in items:
        it["corpus"] = next((r.get("corpus", _default_corpus())
                             for r in runs if r["run_id"] == it["run"]),
                            _default_corpus())
    return items


def l1(corpus):
    """Phase 1 for one corpus. Cached and re-runnable; safe to call again."""
    OUT.mkdir(parents=True, exist_ok=True)
    items = decisions_for(corpus)
    if not items:
        sys.exit(f"no decisions found for corpus={corpus}")
    print(f"L1 [{corpus}]: {len(items)} decisions "
          f"over {len({i['run'] for i in items})} runs")
    groups = l1_group(items)
    p = OUT / f"l1_{corpus}.json"
    p.write_text(json.dumps(
        {"corpus": corpus, "n_decisions": len(items),
         "items": [{"run": i["run"], "arm": i["arm"], "corpus": i["corpus"],
                    "text": i["text"], "line": i["meta"]["line"],
                    "targets": i["meta"]["targets"]} for i in items],
         "groups": groups}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"L1 [{corpus}] done: {len(groups)} raw groups -> {p}")
    return p


def _default_corpus():
    """Fallback when a record predates the `corpus` field. Records written by
    the current distill.py always carry it, so this is defensive only."""
    cs = P.corpora()
    return cs[0] if cs else "corpus"


def build(corpora=None):
    """L2 + L3 over the union of whichever L1 phases exist."""
    corpora = tuple(corpora or P.corpora())
    OUT.mkdir(parents=True, exist_ok=True)
    items, units, offset = [], [], 0
    for c in corpora:
        p = OUT / f"l1_{c}.json"
        if not p.exists():
            print(f"  no l1_{c}.json; running L1 for {c} first")
            l1(c)
        d = json.loads(p.read_text(encoding="utf-8"))
        for g in d["groups"]:
            units.append({"label": g["label"], "question": g["question"],
                          "members": [i + offset for i in g["ids"]]})
        items.extend({"run": x["run"], "arm": x["arm"],
                      "corpus": x.get("corpus", c), "text": x["text"],
                      "meta": {"line": x.get("line", 0),
                               "targets": x.get("targets", [])}}
                     for x in d["items"])
        offset += len(d["items"])
        print(f"  loaded l1_{c}: {d['n_decisions']} decisions, "
              f"{len(d['groups'])} groups")
    tag = "+".join(corpora)
    print(f"\n{len(items)} decisions, {len(units)} raw groups [{tag}]\n")

    print("L2: merging labels across batches")
    prev = len(units) + 1
    for rnd in range(MERGE_ROUNDS):
        if len(units) >= prev:
            print(f"  round {rnd+1}: no further merging, stopping")
            break
        prev = len(units)
        # interleave so a merge round sees pairs the previous batching split
        units = [units[i] for i in
                 sorted(range(len(units)), key=lambda i: (i % MERGE_BATCH, i))]
        units = merge_labels(units, "13_merge_groups", "cluster_up_l2")
        print(f"  round {rnd+1}: {prev} -> {len(units)} options")
        if len(units) > 0.95 * prev:
            break
    options = units
    print(f"L2 done: {len(options)} options\n")

    print("L3: merging questions into forks")
    qs = {}
    for o in options:
        qs.setdefault(o["question"], []).append(o)
    qunits = [{"label": q, "question": q, "members": [i]}
              for i, q in enumerate(sorted(qs))]
    print(f"  {len(qunits)} distinct questions")
    qmerged = merge_labels(qunits, "13_merge_groups", "cluster_up_l3")
    qlist = sorted(qs)
    fork_of = {}
    for f in qmerged:
        for m in f["members"]:
            fork_of[qlist[m]] = f["label"]
    print(f"L3 done: {len(qmerged)} forks\n")

    payload = {
        "corpora": list(corpora), "n_decisions": len(items),
        "n_runs": len({i["run"] for i in items}),
        "n_options": len(options), "n_forks": len(qmerged),
        "forks": [{"fork": f["label"],
                   "questions": [qlist[m] for m in f["members"]]}
                  for f in qmerged],
        "options": [{"option": o["label"],
                     "fork": fork_of.get(o["question"], o["question"]),
                     "question": o["question"],
                     "n": len(o["members"]),
                     "runs": sorted({items[i]["run"] for i in o["members"]}),
                     "arms": dict(Counter(items[i]["arm"] for i in o["members"])),
                     "corpora": dict(Counter(items[i].get("corpus", _default_corpus())
                                             for i in o["members"])),
                     "members": o["members"]}
                    for o in options],
        "decisions": [{"run": it["run"], "arm": it["arm"], "text": it["text"],
                       "line": it["meta"]["line"]} for it in items],
    }
    tag = tag or P.FINAL_TAG
    p = P.VOCAB / f"bottom_up_{tag}.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"-> {p}")
    report(tag)


def report(tag=None):
    tag = tag or P.FINAL_TAG
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        cand = sorted(P.VOCAB.glob("bottom_up_*.json"))
        if not cand:
            sys.exit("run `cluster_up.py build` first")
        p = cand[-1]
    d = json.loads(p.read_text(encoding="utf-8"))
    print(f"\n{d['n_decisions']} decisions -> {d['n_options']} options "
          f"-> {d['n_forks']} forks\n")
    byfork = defaultdict(list)
    for o in d["options"]:
        byfork[o["fork"]].append(o)
    print(f"  {'fork':<52}{'opts':>6}{'runs':>6}{'top option share':>18}")
    for f, os_ in sorted(byfork.items(), key=lambda kv: -sum(o["n"] for o in kv[1])):
        n = sum(o["n"] for o in os_)
        runs = len({r for o in os_ for r in o["runs"]})
        top = max(o["n"] for o in os_) / n
        print(f"  {f[:52]:<52}{len(os_):>6}{runs:>6}{top:>17.0%}")
    sing = sum(1 for o in d["options"] if o["n"] == 1)
    print(f"\n  singleton options (chosen by exactly one decision): "
          f"{sing}/{d['n_options']} ({sing/d['n_options']:.0%})")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["l1", "build", "report"])
    ap.add_argument("--corpus", default=P.FINAL_TAG,
                    help="comma-separated: ai, human, or both for the pooled "
                         "vocabulary (default ai)")
    a = ap.parse_args()
    cs = [c.strip() for c in a.corpus.split(",") if c.strip()]
    if a.cmd == "l1":
        for c in cs:
            l1(c)
    elif a.cmd == "build":
        build(tuple(cs))
    else:
        report("+".join(cs))
