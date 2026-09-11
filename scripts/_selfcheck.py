#!/usr/bin/env python3
"""Is this package complete and internally consistent? No model calls.

An audit-ready collection has to be checkable as a collection, not only as a
set of analyses. This asserts the things a reader would otherwise have to take
on trust:

  every script named in docs/WORKFLOW.md exists, and every script present is named
  every prompt referenced exists, and every prompt present is actually called
  every relative link in the documentation resolves
  every analysis output has the script that produced it
  the headline vocabulary is present and self-consistent
  the cache covers the prompts as committed

Run from the repository root:  python3 scripts/_selfcheck.py
"""
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402

DOCS = ["README.md", "docs/WORKFLOW.md", "docs/METHODS.md",
        "docs/DESIGN.md", "docs/LIFECYCLE.md", "AGENTS.md", "docs/AUDITING.md", "NOT-INCLUDED.md",
        "templates/corpus_brief.md",
        "templates/README.md",
        "data/raw/MANIFEST.md", "INTAKE.md", "templates/intake.md"] + sorted(glob.glob("data/**/README.md", recursive=True))        + ["scripts/README.md", "prompts/README.md"]
fails = []


def check(label, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
    if not ok:
        fails.append(label)


def _c(pattern):
    """Glob the INSTRUMENT, which does not live under the study root.

    main() chdirs to P.ROOT so data paths stay short. scripts/, prompts/,
    docs/, templates/ and .claude/ live under P.CODE_ROOT instead, and reading
    them relative to the study root worked only while the two were the same
    directory -- which they were for every study before soccer-C. The first
    study with its own root died on FileNotFoundError: 'docs/WORKFLOW.md',
    which is the /chart gate to phase 2, so nothing downstream could pass.
    """
    return sorted(str(q) for q in P.CODE_ROOT.glob(pattern))


def _cf(rel):
    """One instrument file, as a Path under CODE_ROOT."""
    return P.CODE_ROOT / rel


def _docpath(d):
    """Resolve a DOCS entry against the study root, then the instrument.

    DOCS mixes per-study files (INTAKE.md, data/**/README.md) with instrument
    documentation (docs/, templates/, scripts/README.md). Before soccer-C the
    two roots were the same directory and a bare relative path found both.
    Returns None when neither has it, because a new study legitimately lacks
    some of these and the link check should skip rather than crash.
    """
    for base in (Path("."), P.CODE_ROOT):
        q = base / d
        if q.exists():
            return q
    return None


def main():
    os.chdir(P.ROOT)
    print(f"SELF-CHECK — {P.ROOT}\n")

    wf = _cf("docs/WORKFLOW.md").read_text(encoding="utf-8")
    # DOCS mixes instrument documentation with per-study files. Resolve each
    # against the study root first, then the instrument, and skip what neither
    # has rather than crashing -- a new study legitimately lacks some of these.
    alldoc = "".join(q.read_text(encoding="utf-8")
                     for q in (_docpath(d) for d in DOCS) if q)

    named = set(re.findall(r"`([a-z_0-9]+\.py)", wf))
    have = {os.path.basename(p) for p in _c("scripts/*.py")}
    internal = {"_selfcheck.py", "_importcheck.py", "check_outcomes.py"}
    check("every script in WORKFLOW exists", not (named - have),
          str(sorted(named - have)) if named - have else "")
    check("every script is documented", not (have - named - internal),
          str(sorted(have - named - internal)) if have - named - internal else "")

    # README.md documents the prompts; it is not one of them
    ph = {os.path.basename(p) for p in _c("prompts/*.md")
          if os.path.basename(p) != "README.md"}
    # stability/scripts/ counts as a caller. It is part of the package and
    # calls the model: q1c_adjudicate.py drives 30_silent_identity, which this
    # check reported as an orphan for as long as it scanned scripts/ alone.
    src = "".join(Path(p).read_text(encoding="utf-8")
                  for p in _c("scripts/*.py")
                  + _c("stability/scripts/*.py"))
    orphan = [p for p in sorted(ph) if p[:-3] not in src]
    check("every prompt is called by a script", not orphan,
          str(orphan) if orphan else f"{len(ph)} prompts")

    bad = []
    for f in DOCS:
        q = _docpath(f)
        if q is None:
            continue
        for l in re.findall(r"\]\(([^)#][^)]*)\)",
                            q.read_text(encoding="utf-8")):
            if l.startswith("http"):
                continue
            # a trailing #anchor is legitimate markdown; check the file part.
            # Relative to the file's OWN directory, which is now wherever it
            # resolved to -- not to the study root it used to be read from.
            t = os.path.normpath(os.path.join(os.path.dirname(str(q)),
                                              l.split("#")[0]))
            if not os.path.exists(t):
                bad.append(f"{f} -> {l}")
    check("documentation links resolve", not bad, str(bad[:4]) if bad else "")

    tag = P.FINAL_TAG
    vf = P.vocab_file(tag)
    check("headline vocabulary present", vf.exists(), vf.name)
    if vf.exists():
        d = json.loads(vf.read_text(encoding="utf-8"))
        runs = {x["run"] for x in d["decisions"]}
        forks = {o["fork"] for o in d["options"]}
        opts = {(o["fork"], o["option"]) for o in d["options"]}
        idx = {i for o in d["options"] for i in o.get("members", [])}
        check("every option member indexes a real decision",
              max(idx) < len(d["decisions"]),
              f"{len(d['decisions'])} decisions, {len(opts)} options, "
              f"{len(forks)} decision points, {len(runs)} runs")
        orphans = len(set(range(len(d["decisions"]))) - idx)
        check("decisions not assigned to any option", orphans == 0
              or orphans < 0.02 * len(d["decisions"]),
              f"{orphans} unassigned")
        gf = P.garden_file(tag)
        check("node table present for it", gf.exists(), gf.name)
        if gf.exists():
            g = json.loads(gf.read_text(encoding="utf-8"))
            gn = {n["fork"] for n in g["nodes_detail"]}
            check("node table covers the vocabulary", gn == forks,
                  f"{len(gn ^ forks)} mismatched")

    # A failed patch script was committed into the package root and shipped.
    # The documentation check only globs scripts/*.py, so scratch anywhere else
    # was invisible to it.
    scratch = sorted(glob.glob("**/.tmp_*", recursive=True)
                     + glob.glob("**/*.bak", recursive=True))
    check("no scratch files in the package", not scratch,
          str(scratch[:3]) if scratch else "")

    sk = sorted(_c(".claude/skills/*/SKILL.md"))
    ag = sorted(_c(".claude/agents/*.md"))
    check("skills and agents present", len(sk) >= 5 and len(ag) >= 2,
          f"{len(sk)} skills, {len(ag)} agents")
    named = (_cf("docs/DESIGN.md").read_text(encoding="utf-8")
             + _cf("docs/LIFECYCLE.md").read_text(encoding="utf-8"))
    miss = [os.path.basename(os.path.dirname(x)) for x in sk
            if f"/{os.path.basename(os.path.dirname(x))}`" not in named]
    check("every skill appears in docs/DESIGN.md", not miss, str(miss))

    # Every script must import, and every module-level path it defines must
    # live inside the package. Two audits shipped documented, present, and
    # pointing at the working tree's layout -- a directory that does not exist
    # here -- because nothing had ever executed them against the package.
    r = subprocess.run([sys.executable, str(P.SCRIPTS / "_importcheck.py")],
                       capture_output=True, text=True, cwd=str(P.CODE_ROOT))
    stray = [x for x in r.stdout.strip().splitlines() if x]
    check("every script imports and resolves inside the package", not stray,
          "; ".join(stray[:3]) if stray else
          f"{len(glob.glob('scripts/*.py'))} scripts")

    n_cache = len(glob.glob(str(P.CACHE / "*")))
    check("response cache present", n_cache > 0, f"{n_cache} entries")
    prompts_in_cache = set()
    for f in glob.glob(str(P.CACHE / "*"))[:4000]:
        try:
            prompts_in_cache.add(json.loads(
                Path(f).read_text(encoding="utf-8")).get("prompt"))
        except Exception:                                       # noqa: BLE001
            pass
    missing = {p[:-3] for p in ph} - prompts_in_cache
    check("cache covers the committed prompts", not missing,
          f"uncached: {sorted(missing)}" if missing else
          f"{len(prompts_in_cache)} prompts represented")

    # Reachability, not just presence. An entry written under an older prompt
    # version can never be hit again, so the claim "the cache makes a re-run
    # return the committed answers" is false for it. That drift is silent and
    # went unnoticed until someone asked what was in the cache.
    from llm import prompt_hash                                 # noqa: E402
    cur = {p[:-3]: prompt_hash(p[:-3]) for p in ph}
    live = dead = 0
    for f in glob.glob(str(P.CACHE / "*")):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        n = d.get("prompt")
        if n in cur and d.get("prompt_hash") == cur[n]:
            live += 1
        else:
            dead += 1
    check("every cached answer is reachable by the shipped prompts",
          dead == 0,
          f"{live} reachable, {dead} superseded — run scripts/prune_cache.py"
          if dead else f"all {live} entries")

    undocumented = [d for d in sorted(glob.glob("data/*/"))
                    if not (os.path.exists(d + "README.md")
                            or os.path.exists(d + "MANIFEST.md"))]
    check("every data directory has a README", not undocumented,
          str(undocumented) if undocumented else
          f"{len(glob.glob('data/*/'))} directories")

    for d, lo in (("data/distilled", 200), ("data/analysis", 20),
                  ("data/audits", 5), ("figures", 4)):
        n = len(glob.glob(f"{d}/*"))
        check(f"{d} populated", n >= lo, f"{n} entries")

    print(f"\n{'ALL CHECKS PASS' if not fails else 'FAILED: ' + ', '.join(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
