#!/usr/bin/env python3
"""Render every figure for one study root, from the vocabulary it finished with.

WHY THIS EXISTS SEPARATELY FROM build_all
-----------------------------------------
`build_all.py` renders the figures as stages 7a-7f at the end of a build, which
is right when you are building. But figures also need re-rendering on their own:
into a replicate root for side-by-side comparison, after a figure script
changes, or to check that the published SVGs still match the data they claim to
depict. Doing that by hand invites the failure this script exists to prevent.

THE TAG TRAP, WHICH IS WHY THE DEFAULT MATTERS
----------------------------------------------
Every figure script takes `--corpus`. Passing the obvious thing --

    --corpus ai,human

-- does NOT reproduce the headline figures. It resolves to the tag `ai+human`,
the UNREPAIRED base vocabulary: 463 decision points rather than the 317 the
repair loop converged to. The figures render without error and look entirely
plausible; the soccer study's circle draws 245 nodes and 264 routes instead of
148 and 225. Nothing warns you.

That happens because `build_all` promotes the tag to the repaired one only
inside its `--repair` branch, so the repaired tag exists nowhere a caller can
see it except `study.json`. So this script defaults `--tag` to `final_tag` from
`study.json` and REFUSES to run if the tag names a vocabulary that is not on
disk. Rendering the wrong vocabulary is now something you have to ask for.

WHAT IS DETERMINISTIC HERE, AND WHAT IS NOT
-------------------------------------------
Four of the five figures are pure computation over artifacts the build already
produced: no model calls, no cache reads, nothing spent. Re-rendering the soccer
study's build A reproduced `fork_atlas.svg`, `fork_graph.svg` and
`novelty_curve.svg` byte-for-byte, and 33 of its 35 analysis JSONs.

`circle.html` differs only in node coordinates. The placement optimiser is
unseeded, so it settles into a slightly different local optimum each run.
Every substantive number is identical.
If byte-identical figures ever matter, seed the optimiser; it is not seeded
today and this docstring is the honest statement of that.

`iteration.svg` is the exception and does not belong to that set. Stage 6d
shells out to the `claude` CLI, so it is an LLM stage sitting among the figure
stages, and re-running it costs money and adds a second source of variation. It
is SKIPPED by default and the existing file is left alone. `--with-llm` runs it.

WHAT THIS SCRIPT DOES NOT CLAIM
-------------------------------
Re-rendering holds the vocabulary fixed. That the drawing layer reproduces says
nothing about whether the pipeline reproduces -- that is measured in
`stability/`, and the two must not be quoted for each other.

Usage:
    python3 scripts/build_figures.py                       # this study, final_tag
    python3 scripts/build_figures.py --tag <explicit>      # override
    python3 scripts/build_figures.py --with-llm            # include iteration.svg
    python3 scripts/build_figures.py --list                # show plan, run nothing
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

# (stage, script, subcommand, takes --corpus, needs a model)
FIGURES = [
    ("6c", "novelty_curve.py", None,     True,  False),
    ("6d", "iteration.py",     "stages", True,  True),
    ("7c", "fork_atlas.py",    None,     True,  False),
    ("7d", "fork_graph.py",    None,     True,  False),
    ("7f", "circle.py",        None,     True,  False),
]


def study_tag():
    """`final_tag` from study.json -- the repaired vocabulary, not the base."""
    p = PATHS.ROOT / "study.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("final_tag")
    except Exception:
        return None


def check_tag(tag, final):
    """Refuse a tag with no vocabulary; warn loudly on one that is not headline.

    Existence is NOT the test. The base vocabulary is on disk too, and it is
    precisely the file that renders a plausible wrong picture -- which is why
    the interesting case here is a tag that resolves perfectly and is still the
    wrong one. Anything other than `final_tag` gets a banner naming the gap.
    """
    want = PATHS.VOCAB / f"bottom_up_{tag}.json"
    if not want.exists():
        have = sorted(p.name[len("bottom_up_"):-len(".json")]
                      for p in PATHS.VOCAB.glob("bottom_up_*.json"))
        sys.exit(f"no vocabulary for tag {tag!r}\n  looked for: {want}\n"
                 + "  on disk:\n" + "".join(f"    {t}\n" for t in have)
                 + "\n  the headline tag is study.json:final_tag.")

    if final and tag != final:
        n_here = forks_in(want)
        n_final = forks_in(PATHS.VOCAB / f"bottom_up_{final}.json")
        print("  " + "!" * 68)
        print(f"  NOT THE HEADLINE VOCABULARY. Rendering {tag!r}")
        print(f"    this tag   {n_here} decision points")
        print(f"    final_tag  {n_final} decision points   ({final})")
        print("  These figures will render cleanly and will not depict the")
        print("  study's result. Omit --tag unless you mean this.")
        print("  " + "!" * 68 + "\n")
    return want


def forks_in(path):
    """Decision-point count read from the options, never from the header.

    Six of ten vocabulary files in the soccer study carried a stale `n_forks`
    header, so the header is not a source of truth here.
    """
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        return len({o["fork"] for o in d["options"]})
    except Exception:
        return "?"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tag", default=None,
                    help="vocabulary tag; defaults to study.json:final_tag")
    ap.add_argument("--with-llm", action="store_true",
                    help="also run stage 6d (iteration.svg), which spends money")
    ap.add_argument("--only", default=None,
                    help="comma-separated stage ids, e.g. 7e,7f")
    ap.add_argument("--list", action="store_true",
                    help="print the plan and exit")
    a = ap.parse_args()

    tag = a.tag or study_tag()
    if not tag:
        sys.exit("no --tag and no final_tag in study.json")
    vocab = check_tag(tag, study_tag())

    want = set(a.only.split(",")) if a.only else None
    plan = [f for f in FIGURES
            if (want is None or f[0] in want)
            and (a.with_llm or not f[4])]

    print(f"study root   {PATHS.ROOT}")
    print(f"figures      {PATHS.FIGURES}")
    print(f"tag          {tag}")
    print(f"vocabulary   {vocab.name}\n")

    skipped = [f for f in FIGURES if f[4] and not a.with_llm
               and (want is None or f[0] in want)]
    if skipped:
        names = ", ".join(f"{s[0]} {s[1]}" for s in skipped)
        print(f"  skipping {names} -- LLM stage; --with-llm to include\n")

    if a.list:
        for st, script, sub, _, llm in plan:
            print(f"  {st}  {script}{' ' + sub if sub else ''}"
                  f"{'   (LLM)' if llm else ''}")
        return

    PATHS.FIGURES.mkdir(parents=True, exist_ok=True)
    failed = []
    for st, script, sub, corpus, _ in plan:
        argv = [sys.executable, "-u", str(S / script)]
        if sub:
            argv.append(sub)
        if corpus:
            argv += ["--corpus", tag]
        print(f"  {st} {script:<18} ", end="", flush=True)
        t0 = time.time()
        r = subprocess.run(argv, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"ok    {time.time() - t0:5.1f}s")
        else:
            print("FAILED")
            for ln in (r.stderr or r.stdout or "").strip().splitlines()[-6:]:
                print(f"        {ln}")
            failed.append(st)

    print()
    for p in sorted(PATHS.FIGURES.glob("*")):
        print(f"  {p.stat().st_size:>10,}  {p.name}")
    if failed:
        sys.exit(f"\n{len(failed)} stage(s) failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
