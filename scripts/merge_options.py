#!/usr/bin/env python3
"""Collapse paraphrase options into distinct actions, corpus-wide.

The study owner read the garden, said the options within a fork all looked like the same
action, and was right. `audit_granularity.py` measured it on a stratified
sample of 40 forks: distinct actions / options = 0.611 overall, and **0.541 on
the forks reached by 30+ runs** -- the ones every reported statistic rests on.
Six labels for "average the two raters" over 211 runs; eleven for "drop dyads
missing the skin-tone rating" over 141.

WHY L1/L2 DID NOT CATCH THIS
----------------------------
L1 groups decisions locally and L2 merges group *labels*, both working over the
whole corpus at once, where near-duplicates are separated by thousands of
unrelated items and never compared directly. This pass asks a much easier
question: given one decision point and the twenty-odd options recorded under
it, which are the same action? Same model, far smaller and better-posed
comparison -- which is why it finds what the earlier passes missed.

The token-overlap screen tried first is not a substitute. It flagged 2.7% of
within-fork option pairs and missed the rater fork entirely, because lexical
similarity cannot see that "compute the mean of the two rater columns" and
"average the two raters' scores" are one action.

WHAT THIS CHANGES, AND WHAT IT DOES NOT
---------------------------------------
Merging paraphrase options RAISES modal share and LOWERS effective options, so
every concentration statistic moves toward "more settled" -- contested/settled
rankings, the atlas quadrants, the "no conventions" reading. Coverage, run
counts and singleton *runs* are untouched: an option split in two still covers
the same runs.

Output is written alongside the original rather than over it. Nothing that has
already been reported is silently restated.

Usage:
    python3 scripts/merge_options.py run   --corpus ai,human   # LLM, cached
    python3 scripts/merge_options.py apply --corpus ai,human   # rewrite
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402
from audit_granularity import judge, tables                     # noqa: E402

from vocab import garden_path, sync_counts                     # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
WORKERS = 8


def do_run(tag):
    opts, _, _ = tables(tag)
    todo = sorted(f for f, om in opts.items() if len(om) >= 2)
    print(f"MERGE OPTIONS - {tag}")
    print(f"{len(opts)} forks, {len(todo)} with >= 2 options to adjudicate\n")
    res, fails = {}, []

    def work(f):
        try:
            return f, judge(f, opts[f])
        except Exception as e:                                  # noqa: BLE001
            return f, {"error": f"{type(e).__name__}: {e}"[:180]}

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for n, (f, r) in enumerate(ex.map(work, todo), 1):
            if "error" in r:
                fails.append({"fork": f, **r})
                print(f"  FAIL {f[:56]}: {r['error'][:70]}", flush=True)
            else:
                res[f] = r
            if n % 20 == 0:
                print(f"  {n}/{len(todo)}", flush=True)

    o = sum(r["n_options"] for r in res.values())
    a = sum(r["n_actions"] for r in res.values())
    print(f"\n{len(res)} forks adjudicated, {len(fails)} failed")
    print(f"options {o} -> actions {a}  (redundancy {a/o:.3f})")
    p = OUT / f"option_merge_{tag}.json"
    p.write_text(json.dumps({"corpus": tag, "failures": fails, "forks": res},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {p}")


def do_apply(tag, out_tag=None):
    mp = OUT / f"option_merge_{tag}.json"
    if not mp.exists():
        sys.exit(f"run `merge_options.py run --corpus {tag}` first")
    merge = json.loads(mp.read_text(encoding="utf-8"))["forks"]
    src = P.VOCAB / f"bottom_up_{tag}.json"
    d = json.loads(src.read_text(encoding="utf-8"))
    _gp = garden_path(tag)
    gm = json.loads(_gp.read_text(encoding="utf-8"))
    cmap = {}
    for h, ms in gm.get("sibling_groups", {}).items():
        for m in ms:
            cmap[m] = h

    # (node, original option) -> merged action label
    lut, misfiled = {}, set()
    for f, r in merge.items():
        for g in r["groups"]:
            # name the action by its most-used original label, not by the
            # model's paraphrase: the corpus's own wording stays traceable
            best = max(g["options"], key=lambda o: len(o)) if g["options"] else ""
            name = g.get("action") or best
            for o in g["options"]:
                lut[(f, o)] = name
        for o in r.get("misfiled_options", []):
            misfiled.add((f, o))

    moved = 0
    for o in d["options"]:
        node = cmap.get(o["fork"], o["fork"])
        new = lut.get((node, o["option"]))
        if new and new != o["option"]:
            # a list, always. Writing a bare string here made the field
            # dual-typed, and the first consumer to read it back reported a
            # 27-label merge for an option nobody merged.
            o["option_raw"] = [o["option"]]
            o["option"] = new
            moved += 1

    # options that now share (fork, option) are the same thing: fold members
    fold = defaultdict(list)
    for o in d["options"]:
        fold[(o["fork"], o["option"])].append(o)
    merged = []
    for (fk, op), group in fold.items():
        if len(group) == 1:
            merged.append(group[0])
            continue
        head = dict(group[0])
        head["members"] = sorted({i for g in group for i in g.get("members", [])})
        # option_raw is already a list when this pass runs a second time over
        # an earlier merge, so flatten rather than nest: the point of the field
        # is that every original corpus label stays recoverable
        raw = set()
        for g in group:
            v = g.get("option_raw", g["option"])
            raw.update(v if isinstance(v, list) else [v])
        head["option_raw"] = sorted(raw)
        head["n"] = len(head["members"])
        head["runs"] = sorted({r for g in group for r in (g.get("runs") or [])})
        merged.append(head)

    before, after = len(d["options"]), len(merged)
    d["options"] = merged
    d["n_options"] = after
    d["option_merge"] = {"source": src.name, "relabelled": moved,
                         "options_before": before, "options_after": after}
    p = P.VOCAB / f"bottom_up_{out_tag or tag + '.merged'}.json"
    p.write_text(json.dumps(sync_counts(d), ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"APPLY - {tag}")
    print(f"  option records relabelled  {moved}")
    print(f"  option records             {before} -> {after}")
    print(f"  misfiled flagged           {len(misfiled)} (left in place)")
    print(f"-> {p}")
    print(f"\nnothing overwritten; point analyses at the .merged file to "
          f"compare")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "apply"])
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    # see the note in merge_forks.py
    ap.add_argument("--out-tag", dest="out_tag",
                    help="name the output; default <corpus>.merged")
    a = ap.parse_args()
    t = "+".join(c.strip() for c in a.corpus.split(","))
    if a.cmd == "run":
        do_run(t)
    else:
        do_apply(t, a.out_tag)
