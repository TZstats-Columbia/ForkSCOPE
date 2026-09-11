#!/usr/bin/env python3
"""Promote the same-run option split into the study, and rebuild what depends on it.

WHY A PROMOTION STEP EXISTS AT ALL
----------------------------------
`stability/scripts/repair_option_splits.py` was written as an experiment: does
splitting options that merged a run's distant decisions change what the build
says? It does, and the split is the sanctioned direction (over-merge is
unrecoverable, under-merge is visible), so the repair earned a place in the
study rather than beside it.

Left as an experiment it created a provenance split that was actively
misleading. The repaired vocabularies sat outside the repo in
`replicates/repaired/`, `study.json:final_tag` still named the unrepaired
vocabulary, and `data/audits/vocab_exhibits.json` -- committed -- described
`...r3.osplit`, a file the repo did not contain. The audit and the figures
described two different objects and nothing said so.

WHAT THIS SCRIPT DOES
---------------------
  1  runs the repair on the current `final_tag` vocabulary, writing the result
     into `data/vocabulary/` under `<final_tag>.osplit`
  2  rebuilds every analysis and audit keyed to a tag, for the new tag
  3  re-renders the figures
  4  rewrites `study.json:final_tag` -- LAST, so a failure anywhere above
     leaves the study pointing at a vocabulary whose analyses all exist

Step 4 is the reason the order matters. `final_tag` is the one pointer that
decides what every downstream caller reads, and a study whose headline tag names
a half-built vocabulary is worse than one that is merely out of date.

IT MIRRORS build_all --repair, DELIBERATELY
-------------------------------------------
Stages 6d, 6g and 6h are skipped here for the same reason `build_all` skips them
after a repair: `finalize_vocab` has already written `fork_stage_` and `garden_`
for the repaired vocabulary, and re-running them would overwrite that map with
one built on a sibling merge already folded into the labels -- applying the same
merge twice. This is not an independent judgement about those stages; it is the
tested path, copied.

WHAT CHANGES, AND WHAT A READER MUST BE TOLD
--------------------------------------------
The repair splits options; it does not touch forks. On the soccer study, build A
goes from 729 options to 777 and stays at 317 decision points. So any figure or
number quoting an OPTION count changes and must be re-quoted, while fork-level
headlines do not move.

The warning in `repair_option_splits.py` carries over and is not softened by
promotion: applying one deterministic transformation to two builds can raise
their agreement for a trivial reason. Agreement measured after this repair must
be reported against the pre-repair number, never on its own.

Usage:
    python3 scripts/promote_repair.py                 # do it
    python3 scripts/promote_repair.py --dry-run       # show the plan
    python3 scripts/promote_repair.py --span 5        # repair threshold
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as PATHS                                              # noqa: E402

S = Path(__file__).resolve().parent
# The CODE root, not PATHS.ROOT. `paths` fixes the code root to this file's
# grandparent precisely because the study root moves -- and the two coincide
# for the soccer study, so deriving this from PATHS.ROOT works there and fails
# the moment a second study root is promoted. It failed exactly that way on the
# first attempt at build B's root.
STAB = S.parent / "stability" / "scripts"


def sh(label, argv, dry):
    if dry:
        print(f"  {label:<34} {' '.join(str(x) for x in argv[2:])[:80]}")
        return True
    print(f"  {label:<34} ", end="", flush=True)
    t0 = time.time()
    r = subprocess.run(argv, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"ok    {time.time() - t0:6.1f}s")
        return True
    print("FAILED")
    for ln in (r.stderr or r.stdout or "").strip().splitlines()[-10:]:
        print(f"      {ln}")
    return False


def counts(tag):
    p = PATHS.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    return len(d["options"]), len({o["fork"] for o in d["options"]})


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--span", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-figures", action="store_true")
    a = ap.parse_args()

    sj = PATHS.ROOT / "study.json"
    study = json.loads(sj.read_text(encoding="utf-8"))
    old = study["final_tag"]
    new = f"{old}.osplit"

    src = PATHS.VOCAB / f"bottom_up_{old}.json"
    dst = PATHS.VOCAB / f"bottom_up_{new}.json"
    if not src.exists():
        sys.exit(f"final_tag vocabulary missing: {src}")

    print(f"study root  {PATHS.ROOT}")
    print(f"from        {old}   {counts(old)[0]} options, {counts(old)[1]} forks")
    print(f"to          {new}\n")

    P = [sys.executable, "-u"]
    OUTC = PATHS.ANALYSIS

    if not sh("repair: split same-run merges",
              P + [str(STAB / "repair_option_splits.py"), "--vocab", str(src),
                   "--out", str(dst), "--span", str(a.span),
                   "--report", str(PATHS.AUDITS / f"option_splits_{new}.csv")],
              a.dry_run):
        sys.exit("repair failed; study.json untouched")

    if not a.dry_run:
        c = counts(new)
        if not c:
            sys.exit("repair wrote nothing")
        print(f"\n  repaired: {c[0]} options, {c[1]} forks "
              f"(+{c[0] - counts(old)[0]} options)\n")

    # finalize first: it writes fork_stage_ and garden_ for the new tag, which
    # is exactly why 6d/6g/6h are skipped below.
    stages = [
        ("6-6 finalize vocabulary", [str(S / "finalize_vocab.py"),
                                     "--corpus", new]),
        ("6a stability", [str(S / "stability.py"), "--corpus", new,
                          "--json", str(OUTC / f"stability_{new}.json")]),
        ("6b novelty", [str(S / "novelty.py"), "--corpus", new,
                        "--json", str(OUTC / f"novelty_{new}.json")]),
        ("6c novelty dose-response", [str(S / "novelty_curve.py"),
                                      "--corpus", new, "--json",
                                      str(OUTC / f"novelty_curve_{new}.json")]),
        ("6e stage iteration", [str(S / "iteration.py"), "run",
                                "--corpus", new]),
        ("6f audit iteration", [str(S / "audit_iteration.py"),
                                "--corpus", new]),
        ("6j shapley", [str(S / "shapley_v2.py"), "--corpus", new]),
        ("6k audit shapley", [str(S / "audit_shapley.py"), "--corpus", new]),
        ("V1-V7 audit vocabulary", [str(S / "audit_vocab.py"),
                                    "--corpus", new]),
    ]
    print("  rebuilding analyses and audits for the new tag")
    print("  (6d, 6g, 6h skipped -- finalize_vocab already wrote them, as in "
          "build_all --repair)\n")
    for label, argv in stages:
        if not sh(label, P + argv, a.dry_run):
            sys.exit(f"\n{label} failed. study.json still points at {old}; "
                     f"fix and re-run.")

    if not a.skip_figures:
        print()
        if not sh("figures", P + [str(S / "build_figures.py"), "--tag", new],
                  a.dry_run):
            sys.exit(f"\nfigures failed. study.json still points at {old}.")

    if a.dry_run:
        print(f"\n  would set study.json final_tag -> {new}")
        return

    study["final_tag"] = new
    sj.write_text(json.dumps(study, indent=2, ensure_ascii=False) + "\n",
                  encoding="utf-8")
    print(f"\n  study.json final_tag -> {new}")
    print("  NOTE: option counts changed; fork counts did not. Re-quote any "
          "option-level number.")


if __name__ == "__main__":
    main()
