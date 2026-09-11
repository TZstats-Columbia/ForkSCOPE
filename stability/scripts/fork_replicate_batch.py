#!/usr/bin/env python3
"""Run N fork replicates per parent build, resumably. Spends real money.

WHAT THIS MEASURES, AND WHY IT NEEDS MORE THAN A COUPLE OF RUNS
--------------------------------------------------------------
Build A and build B disagree about forks far more than they disagree about
options (by-option ARI 0.31 against 0.85). Two readings fit that equally well:

    fork induction is itself unstable    -- it would disagree with ITSELF given
                                            byte-identical options
    fork induction inherits the noise    -- it is a near-deterministic function
                                            of an options layer that differed

A and B cannot separate those, because their options differ. Replicates that
FREEZE the options and re-run only fork formation can: the spread WITHIN one
parent is fork induction's own contribution, and the gap between the two
parents' spreads is what upstream contributes.

That is a variance decomposition, and variance is what needs replicates. With
3 builds per parent there are 2 degrees of freedom and the confidence interval
on a standard deviation runs from about half the estimate to three times it --
too wide to support any claim. With 6 per parent it is roughly 0.7x to 1.8x.
This is one of the few places where more runs buy the result rather than a
tighter version of it.

PRE-COMMIT TO N, AND DO NOT PEEK
--------------------------------
Running a few, looking at the spread, and extending if it seems large is
optional stopping on a variance estimate -- it biases the exact quantity being
reported. `--n` is chosen once, before the first build. If a later session
wants more, that is a new pre-registered batch reported separately, not an
extension of this one.

RESUMABLE, BECAUSE IT RUNS OVERNIGHT
------------------------------------
Each replicate is skipped if its manifest records a `final_tag`, so a crash
loses at most the build in flight, and re-running the batch resumes rather than
restarts. A failed build keeps its cache: `replicate.py` writes the manifest on
failure too, so the retry is nearly free and the money already spent stays
visible instead of looking like it was never spent.

Usage (inside the LLM container, which has the `claude` CLI):
    python3 stability/scripts/fork_replicate_batch.py \\
        --parent A=../../replicates/A-parent/bottom_up_<tag>.json \\
        --parent B=../../replicates/B-root/data/vocabulary/bottom_up_<tag>.json:../../replicates/B-root \\
        --n 5 --out replicates

A parent is `NAME=vocab_path` or `NAME=vocab_path:parent_root`, where
parent_root is the build whose distilled/analysis are copied in. It defaults to
this repo, which is correct for A and WRONG for B -- B's `merge_forks` must read
B's garden, not A's.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def done(root):
    m = root / "manifest.json"
    if not m.exists():
        return False
    try:
        d = json.loads(m.read_text(encoding="utf-8"))
        return bool(d.get("final_tag"))
    except Exception:
        return False


def spend_of(root):
    m = root / "manifest.json"
    if not m.exists():
        return 0.0
    try:
        return float(json.loads(m.read_text(encoding="utf-8"))
                     .get("spend_usd") or 0)
    except Exception:
        return 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--parent", action="append", required=True,
                    help="NAME=vocab_path[:parent_root]")
    ap.add_argument("--n", type=int, default=5,
                    help="replicates per parent; pre-committed, not tuned")
    ap.add_argument("--out", default="replicates")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    parents = {}
    for spec in a.parent:
        name, _, rest = spec.partition("=")
        vocab, _, proot = rest.partition(":")
        parents[name] = (vocab, proot or None)

    out = Path(a.out)
    plan = [(f"{name}{i}", name, v, pr)
            for name, (v, pr) in parents.items()
            for i in range(1, a.n + 1)]

    todo = [p for p in plan if not done(out / p[0])]
    print(f"  {len(plan)} replicates planned, {len(plan) - len(todo)} already "
          f"complete, {len(todo)} to run")
    # Measured on the first completed replicate, not projected from build B's
    # log. B's $35.64 was the fork stages of a FULL build, where merge_forks
    # ran against a fork layer the option passes kept disturbing; with options
    # frozen it converges in two rounds and costs less.
    print(f"  ~${21.23 * len(todo):.0f} estimated, "
          f"~{0.6 * len(todo):.1f} h  (measured: A1 = $21.23, 35 min)\n")
    for tag, name, v, pr in plan:
        print(f"    {tag:<6} {'done' if (out / tag) and done(out / tag) else 'TO RUN':<7}"
              f" parent {name}  root {pr or REPO.name}")
    if a.dry_run:
        return

    P = [sys.executable, "-u", str(HERE / "replicate.py")]
    started = time.time()
    failed = []
    for k, (tag, name, vocab, proot) in enumerate(todo, 1):
        root = out / tag
        print(f"\n{'=' * 70}\n  [{k}/{len(todo)}]  {tag}   "
              f"({time.time() - started:.0f}s elapsed)\n{'=' * 70}")
        if not (root / "manifest.json").exists():
            argv = P + ["init", "--root", str(root), "--stage", "forks",
                        "--from-vocab", vocab]
            if proot:
                argv += ["--parent-root", proot]
            if subprocess.run(argv, cwd=str(REPO)).returncode:
                failed.append((tag, "init"))
                continue
        argv = P + ["run", "--root", str(root), "--stage", "forks",
                    "--workers", str(a.workers)]
        if subprocess.run(argv, cwd=str(REPO)).returncode:
            failed.append((tag, "run"))
            print(f"  {tag} FAILED; cache kept, batch continues")

    print(f"\n{'=' * 70}\n  BATCH COMPLETE  ({(time.time() - started)/3600:.2f} h)")
    total = 0.0
    for tag, _, _, _ in plan:
        r = out / tag
        s = spend_of(r)
        total += s
        ft = "-"
        if (r / "manifest.json").exists():
            ft = json.loads((r / "manifest.json").read_text(encoding="utf-8")
                            ).get("final_tag") or "-"
        print(f"    {tag:<6} ${s:>7.2f}  {'ok' if done(r) else 'INCOMPLETE':<10} "
              f"{ft[-28:]}")
    print(f"    {'TOTAL':<6} ${total:>7.2f}")
    if failed:
        print("\n  failed: " + ", ".join(f"{t} ({w})" for t, w in failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
