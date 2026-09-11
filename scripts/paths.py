#!/usr/bin/env python3
"""Every path the pipeline uses, defined once — and the code/study seam.

Each script derives its locations from here rather than from its own copy of
`Path(__file__).parents[1] / ...`. That is not tidiness: several scripts read a
vocabulary written by another, and when two of them disagree about where a file
lives the analysis does not crash — it reads the wrong vocabulary and reports
numbers that look fine.

THE SEAM: SHARED INSTRUMENT, SEPARATE DATA

Two roots, and the distinction is the whole point of running more than one
case study.

    CODE_ROOT    scripts/ and prompts/ — the instrument
    STUDY_ROOT   data/, figures/, cache/ — one study's material

`scripts/` and `prompts/` are never per-study. If a second corpus got its own
copy of the pipeline you would have run two instruments and could compare
nothing; the claim a second study supports is precisely that the instrument was
unchanged. So the code root is fixed to this file's grandparent and cannot be
overridden.

`STUDY_ROOT` defaults to the same directory, which is where the soccer study
lives today, so nothing moves until there is a reason to move it. A second
study is either a directory under `studies/` or an absolute path:

    FORKSCOPE_STUDY=ads-repos      -> <code root>/studies/ads-repos
    FORKSCOPE_STUDY=/data/ads      -> /data/ads

WHAT MAKES A STUDY

`study.json` at the study root. It carries what is genuinely corpus-specific
and used to be hard-coded here: the headline vocabulary tag, and for each
corpus where its raw material lives, how to glob it, and which files in a run
directory are code and which are prose. Everything soccer-shaped lives there
rather than in the pipeline.

Missing or unreadable, the soccer defaults below apply, so an old checkout
still runs.

LAYOUT, relative to STUDY_ROOT unless noted

    data/raw/          pointers to the source corpora, which are NOT vendored;
                       see data/raw/MANIFEST.md
    data/distilled/    per-run segmentation and linking, one directory per run
    data/corpus/       indexed decision tables built from those records
    data/vocabulary/   bottom_up_*.json — decisions grouped into options and
                       options into decision points, one file per repair stage;
                       the filename carries the lineage
    data/analysis/     every analysis output
    data/audits/       every audit output, kept apart because the audits are
                       what license the analyses
    data/ablation/     validation gate 5.4 working files
    data/outcomes/     reported effect sizes and verdicts per run
    figures/           SVG and self-contained HTML
    cache/llm_cache/   responses, keyed sha256(prompt+model+payload+schema)
    cache/llm_runs/    per-call log: timing, tokens, cost, retries
    prompts/           (CODE_ROOT) versioned prompt text
    scripts/           (CODE_ROOT) the pipeline

OVERRIDES

    FORKSCOPE_STUDY     study name under studies/, or an absolute path
    FORKSCOPE_ROOT      legacy alias for FORKSCOPE_STUDY
    FORKSCOPE_RAW_AI    where the AI corpus was unpacked
    FORKSCOPE_RAW_HUMAN where the human corpus was unpacked
"""
import json
import os
from pathlib import Path

# ---- the two roots ---------------------------------------------------------
CODE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = CODE_ROOT / "scripts"
PROMPTS = CODE_ROOT / "prompts"
STUDIES = CODE_ROOT / "studies"


def _study_root():
    s = os.environ.get("FORKSCOPE_STUDY") or os.environ.get("FORKSCOPE_ROOT")
    if not s:
        return CODE_ROOT
    p = Path(s)
    return p if p.is_absolute() else STUDIES / s


STUDY_ROOT = _study_root()
# Legacy name. It meant "the package root" when there was only one study; every
# use of it wants the study's data, so it aliases STUDY_ROOT rather than
# CODE_ROOT. Prefer the explicit name in new code.
ROOT = STUDY_ROOT

DOCS = CODE_ROOT / "docs"
FIGURES = STUDY_ROOT / "figures"

DATA = STUDY_ROOT / "data"
RAW = DATA / "raw"
DISTILLED = DATA / "distilled"
CORPUS = DATA / "corpus"
VOCAB = DATA / "vocabulary"
ANALYSIS = DATA / "analysis"
AUDITS = DATA / "audits"
ABLATION = DATA / "ablation"
OUTCOMES = DATA / "outcomes" / "outcomes.json"

CACHE = STUDY_ROOT / "cache" / "llm_cache"
CALL_LOG = STUDY_ROOT / "cache" / "llm_runs"

# ---- study material that is not `data/` ------------------------------------
# These three were the seam's blind spot. `data/`, `figures/` and `cache/` were
# declared study-scoped from the start; reviews, replicates and the written
# report were not, so they sat at the PACKAGE root and a second study would
# have written its review rounds and its paper on top of the soccer study's.
#
# `stability/scripts/` stays under CODE_ROOT and is deliberately not here: the
# replicate machinery is instrument, the replicates it produces are material.
# Keeping them in one directory conflated the two, which is why the soccer
# replicates were first written to `stability/replicates/`.
REVIEWS = STUDY_ROOT / "reviews"
REPLICATES = STUDY_ROOT / "replicates"
REPORT = STUDY_ROOT / "report"

# ---- the study manifest ----------------------------------------------------
_DEFAULT = {
    "study": "soccer",
    "final_tag": "ai+human.merged.forkmerged.merged.induced",
    "corpora": {
        "ai": {"env": "FORKSCOPE_RAW_AI", "default": "data/raw/afp",
               "glob": "experiment_data/workspaces/*/bedrock_us.anthropic."
                       "claude-sonnet-4-5-20250929-v1_0/sample_soccer/*"},
        "human": {"env": "FORKSCOPE_RAW_HUMAN",
                  "default": "data/raw/human_corpus", "glob": "team-*"},
    },
}


def _load_study():
    f = STUDY_ROOT / "study.json"
    if not f.exists():
        # The defaults describe soccer. Applying them to a study that merely
        # forgot its manifest would compute against another study's vocabulary
        # tag and report numbers that look fine, which is the exact failure
        # this module exists to prevent. Only the in-place default is allowed
        # to fall back, and only so older checkouts keep running.
        if STUDY_ROOT != CODE_ROOT:
            raise SystemExit(
                f"no study.json at {STUDY_ROOT}. A study must declare its own "
                f"corpora and headline vocabulary tag — inheriting another "
                f"study's would silently answer the wrong question. Copy "
                f"{CODE_ROOT / 'templates' / 'study.json'} and edit it.")
        return dict(_DEFAULT)
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:                                     # noqa: BLE001
        raise SystemExit(f"{f} is not valid JSON: {e}")
    for k in ("study", "final_tag", "corpora"):
        if k not in d:
            raise SystemExit(f"{f} is missing required key {k!r}")
    return d


STUDY = _load_study()
STUDY_NAME = STUDY["study"]

# The vocabulary every headline number is computed on. Earlier stages stay in
# data/vocabulary so any figure traces to the vocabulary that produced it.
FINAL_TAG = STUDY["final_tag"]


def corpus_root(name):
    """Where a corpus's raw material lives. Fetched, not vendored."""
    c = STUDY["corpora"].get(name)
    if c is None:
        raise KeyError(f"{name!r} is not a corpus of study {STUDY_NAME!r}; "
                       f"have {sorted(STUDY['corpora'])}")
    env = c.get("env")
    p = os.environ.get(env) if env else None
    return Path(p) if p else STUDY_ROOT / c.get("default", f"data/raw/{name}")


def corpus_glob(name):
    """Glob matching one run directory (or file) of a corpus."""
    c = STUDY["corpora"][name]
    return str(corpus_root(name) / c["glob"]) if c.get("glob") \
        else str(corpus_root(name))


def corpora():
    return sorted(STUDY["corpora"])


# Kept as module constants because scripts import them by name. They now come
# from the manifest, so a second study changes them without touching code.
RAW_AI = corpus_root("ai") if "ai" in STUDY["corpora"] else RAW / "afp"
RAW_AI_GLOB = corpus_glob("ai") if "ai" in STUDY["corpora"] else ""
RAW_HUMAN = (corpus_root("human") if "human" in STUDY["corpora"]
             else RAW / "human_corpus")


def vocab_file(tag):
    return VOCAB / f"bottom_up_{tag}.json"


def garden_file(tag):
    """Node table for a vocabulary: coverage, script position, DSLC stage.

    Derived vocabularies get their own from `finalize_vocab.py`; a plain corpus
    tag falls back to the base garden, which still describes its forks.
    """
    p = ANALYSIS / f"garden_{tag}.json"
    return p if p.exists() else ANALYSIS / f"garden_{tag.split('.')[0]}.json"


def ensure_dirs():
    for d in (DISTILLED, CORPUS, VOCAB, ANALYSIS, AUDITS, ABLATION,
              FIGURES, CACHE, CALL_LOG, OUTCOMES.parent,
              REVIEWS, REPLICATES, REPORT):
        d.mkdir(parents=True, exist_ok=True)


# CALLED AT IMPORT, because nothing else called it.
#
# ensure_dirs has existed since the beginning and had no callers on the build
# path. It never mattered while every study root WAS the repo root, where the
# output tree is committed and therefore always present. soccer-C is the first
# study with its own root, and `build_all --repair` spent 20 minutes and real
# money computing 1082 options and 385 forks before dying on
# FileNotFoundError writing bottom_up_ai.json into a data/vocabulary/ that did
# not exist. The work was cached, so the retry was cheap -- but a crash at the
# final write of a 20-minute stage is the expensive shape of this bug.
#
# Every script in the pipeline imports paths, so creating the tree here means
# no stage can reach its own output write and find nowhere to put it.
ensure_dirs()


def describe():
    """One-line summary, for scripts that report where they are working."""
    same = STUDY_ROOT == CODE_ROOT
    return (f"study {STUDY_NAME!r} · corpora {'+'.join(corpora())} · "
            f"tag {FINAL_TAG}"
            + ("" if same else f" · data at {STUDY_ROOT}"))
