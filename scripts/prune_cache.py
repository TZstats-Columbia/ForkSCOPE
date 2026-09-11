#!/usr/bin/env python3
"""Keep only the cached answers that produced the shipped data. No model calls.

WHY

The committed cache is the reproducibility mechanism: the CLI exposes no
temperature and no seed, so a re-run returns the previous answers because they
are on disk, not because the model is deterministic. That argument only holds
for entries a re-run can actually reach.

An entry is reachable when its prompt is still shipped AND its `prompt_hash`
matches the prompt text as committed -- the cache key includes that hash, so
editing a prompt orphans every answer produced by the old wording. Those
answers are not evidence about the shipped pipeline. They are a record of a
method we changed, and they belong outside the package.

Entries are MOVED, not deleted. Superseded work is still project history; it is
simply not part of an audit-ready package, and a reader who finds 1,657 cached
answers should be able to trust that all of them are load-bearing.

WHAT REACHABILITY DOES NOT PROVE

Only that the prompt text is current. An entry could match a shipped prompt and
still be unused, if the payload it answered no longer occurs anywhere. Testing
that would mean replaying every payload; this operates at prompt granularity
and claims nothing finer.

USAGE

    python3 scripts/prune_cache.py                    # dry run
    python3 scripts/prune_cache.py --apply
    python3 scripts/prune_cache.py --apply --archive ../.cache_superseded
"""
import argparse
import glob
import json
import os
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402
from llm import prompt_hash                                      # noqa: E402


def shipped():
    # README.md documents the prompts; it is not one of them
    return {os.path.basename(p)[:-3]: prompt_hash(os.path.basename(p)[:-3])
            for p in glob.glob(str(P.ROOT / "prompts" / "*.md"))
            if os.path.basename(p) != "README.md"}


def classify(cur):
    """Split the cache into reachable and superseded, with the reason."""
    keep, drop = [], []
    for f in glob.glob(str(P.CACHE / "*")):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            drop.append((f, "unreadable", None))
            continue
        n, h = d.get("prompt"), d.get("prompt_hash")
        if n not in cur:
            drop.append((f, "prompt not shipped", n))
        elif h != cur[n]:
            drop.append((f, "prompt text since edited", n))
        else:
            keep.append(f)
    return keep, drop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--archive", default="../.cache_superseded",
                    help="where to move superseded entries (outside the "
                         "package by default)")
    a = ap.parse_args()

    cur = shipped()
    keep, drop = classify(cur)
    tot = len(keep) + len(drop)
    by = Counter((r, n) for _, r, n in drop)

    print(f"CACHE PRUNE   {len(cur)} shipped prompts")
    print(f"  reachable by the shipped pipeline : {len(keep):>5} "
          f"({len(keep)/max(1,tot):.1%})")
    print(f"  superseded                        : {len(drop):>5}")
    for (reason, name), c in by.most_common():
        print(f"      {c:>4}  {name or '?':<22} {reason}")

    # the call log records what happened, including the superseded calls; the
    # same rule applies to it line by line
    log_keep, log_drop = {}, {}
    for f in glob.glob(str(P.CALL_LOG / "*.jsonl")):
        k, d = [], []
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except ValueError:
                d.append(line)
                continue
            n, h = r.get("prompt"), r.get("prompt_hash")
            (k if (n in cur and h == cur[n]) else d).append(line)
        log_keep[f], log_drop[f] = k, d
    nd = sum(len(v) for v in log_drop.values())
    nk = sum(len(v) for v in log_keep.values())
    print(f"\n  call log lines kept / moved       : {nk:>5} / {nd}")

    if not a.apply:
        print("\ndry run -- nothing moved. Re-run with --apply.")
        return 0

    arc = (P.ROOT / a.archive).resolve()
    try:
        arc.relative_to(P.ROOT)
        sys.exit(f"refusing: archive {arc} is inside the package; superseded "
                 f"entries must land outside it")
    except ValueError:
        pass
    (arc / "llm_cache").mkdir(parents=True, exist_ok=True)
    (arc / "llm_runs").mkdir(parents=True, exist_ok=True)

    for f, reason, _ in drop:
        shutil.move(f, arc / "llm_cache" / os.path.basename(f))
    for f, lines in log_drop.items():
        if lines:
            with open(arc / "llm_runs" / os.path.basename(f), "a",
                      encoding="utf-8") as fh:
                fh.writelines(lines)
            Path(f).write_text("".join(log_keep[f]), encoding="utf-8")
    (arc / "README.md").write_text(
        "# Superseded model answers\n\n"
        "Moved out of the package by `scripts/prune_cache.py`. These were "
        "produced by prompt versions that are no longer shipped, so the "
        "committed pipeline can never reach them and they are not evidence "
        "about it. Kept because superseded work is still project history.\n\n"
        f"- cache entries: {len(drop)}\n- call log lines: {nd}\n",
        encoding="utf-8")

    print(f"\nmoved {len(drop)} entries and {nd} log lines to {arc}")
    print(f"package cache is now {len(keep)} entries, all reachable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
