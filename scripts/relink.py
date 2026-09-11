#!/usr/bin/env python3
"""Rebuild links, and everything derived from them, under the shipped prompt.

WHY

The cache is what makes a re-run return the committed answers, and that only
holds while the prompt that produced an answer is the prompt still on disk --
the cache key includes a hash of the prompt text. `03_link` was revised during
development after most linking had already run, so 206 of its 225 committed
answers were produced by a prompt version that is no longer shipped. A rebuild
would silently re-adjudicate them.

Nothing in the vocabulary chain reads links, so the garden, options, forks,
Shapley, iteration and graph results were never affected. What is affected is
the residue of the alignment -- silent decisions and misalignments -- and every
number derived from it.

This script re-asks `03_link` for each run from the segmentations already on
disk, so it needs no raw corpus. Runs whose answer is already current are
served from cache and cost nothing; only the stale ones reach a model.

WHAT IT REWRITES, PER RUN

    links.json      the alignment
    record.json     presence grid, silent_decisions, misalignments
    summary.md      the human-readable view of both

It calls distill.link_and_record rather than reimplementing the derivation,
so there is one definition of the presence grid.

USAGE

    python3 scripts/relink.py                 # dry run: what would be re-asked
    python3 scripts/relink.py --apply         # do it
    python3 scripts/relink.py --apply --limit 5
"""
import argparse
import glob
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402
import distill                                                   # noqa: E402
from llm import prompt_hash                                      # noqa: E402


def cached_state():
    """Per run, whether its committed 03_link answer is still reachable.

    Reachability is by prompt hash: an entry written under an older prompt
    version can never be hit again, which is exactly why those runs need
    re-asking rather than trusting.
    """
    want = prompt_hash("03_link")
    live, seen, costs = set(), set(), []
    for f in glob.glob(str(P.CALL_LOG / "*.jsonl")):
        rid = os.path.basename(f)[:-6]
        # the call log also carries test fixtures, which have no distilled
        # record and are not runs; asking them to relink raises
        if not (P.DISTILLED / rid / "record.json").exists():
            continue
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("prompt") != "03_link":
                continue
            seen.add(rid)
            if r.get("prompt_hash") == want:
                live.add(rid)
            elif r.get("cost_usd"):
                costs.append(r["cost_usd"])
    # A run needs re-asking when it has NO answer at the current hash. After a
    # relink it has both -- the old lines stay in the log -- so subtracting the
    # other way round reports finished work as outstanding and invites paying
    # for it twice.
    return live, seen - live, costs


def run_one(rid):
    d = P.DISTILLED / rid
    rec = json.loads((d / "record.json").read_text(encoding="utf-8"))
    ps = json.loads((d / "prose_spans.json").read_text(encoding="utf-8"))
    cs = (json.loads((d / "code_spans.json").read_text(encoding="utf-8"))
          if (d / "code_spans.json").exists() else None)
    before = (rec["counts"].get("links"), rec["counts"].get("misaligned"),
              len(rec.get("silent_decisions") or []))
    new = distill.link_and_record(rid, rec["corpus"], rec.get("arm"),
                                  rec["artifacts"], ps, cs, d)
    after = (new["counts"].get("links"), new["counts"].get("misaligned"),
             len(new.get("silent_decisions") or []))
    return rid, before, after


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    live, stale, costs = cached_state()
    todo = sorted(stale)
    if a.limit:
        todo = todo[:a.limit]
    avg = sum(costs) / len(costs) if costs else 0.0

    print(f"03_link  current prompt hash {prompt_hash('03_link')}")
    print(f"  runs already current (cache hit) : {len(live)}")
    print(f"  runs to re-ask                   : {len(stale)}")
    print(f"  mean logged cost per call        : ${avg:.3f}")
    print(f"  estimated cost of the re-ask     : ${avg * len(stale):.2f}")
    if not a.apply:
        print(f"\ndry run -- nothing called. Re-run with --apply.")
        for r in todo[:8]:
            print(f"  would re-ask {r}")
        if len(todo) > 8:
            print(f"  ... and {len(todo) - 8} more")
        return 0

    print(f"\nre-asking {len(todo)} runs with {a.workers} workers\n")
    moved, done, fail = [], 0, []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_one, r): r for r in todo}
        for fu in as_completed(futs):
            try:
                rid, b, af = fu.result()
            except Exception as e:                              # noqa: BLE001
                fail.append((futs[fu], f"{type(e).__name__}: {e}"))
                continue
            done += 1
            if b != af:
                moved.append((rid, b, af))
            if done % 20 == 0:
                print(f"  {done}/{len(todo)}", flush=True)

    print(f"\n{done} rebuilt, {len(fail)} failed, {len(moved)} changed")
    if fail:
        print("\nfailures (left untouched):")
        for r, e in fail[:10]:
            print(f"  {r}  {e[:80]}")
    if moved:
        print(f"\n{'run':<34}{'links':>14}{'misaligned':>14}{'silent':>12}")
        for rid, b, af in sorted(moved)[:25]:
            print(f"  {rid:<32}{b[0]:>5} -> {af[0]:<5}{b[1]:>6} -> {af[1]:<6}"
                  f"{b[2]:>5} -> {af[2]:<5}")
        if len(moved) > 25:
            print(f"  ... and {len(moved) - 25} more")
        d = [sum(af[i] - b[i] for _, b, af in moved) for i in range(3)]
        print(f"\nnet change   links {d[0]:+d}   misaligned {d[1]:+d}   "
              f"silent {d[2]:+d}")
    print("\nNow regenerate what reads these:")
    print("  python3 scripts/distill.py index")
    print("  python3 scripts/cluster.py silent")
    print("  python3 scripts/cluster.py misaligned")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
