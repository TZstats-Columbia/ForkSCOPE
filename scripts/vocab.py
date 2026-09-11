#!/usr/bin/env python3
"""Where a vocabulary's garden file lives. Shared by every script that reads one.

A vocabulary tag is either a corpus (`ai`, `ai+human`) or a corpus plus the
repair passes applied to it (`ai+human.merged.forkmerged.merged.induced`).
Derived tags carry their own `bottom_up_` file but not necessarily their own
`garden_`, and two different scripts guessing differently is how the pipeline
ends up reading one vocabulary's options against another's fork map.

The rule, in one place:

    prefer garden_<full tag>.json when it exists -- a derived vocabulary that
    has been through `finalize_vocab.py` has its own node table, stages and
    coverage, and that is the correct map for it;

    otherwise fall back to garden_<base corpus>.json, which is right for a
    vocabulary that only relabelled options, since the sibling map and stage
    assignment still describe the same forks.

Getting this wrong is silent: the analysis runs and produces numbers against a
mismatched map.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                              # noqa: E402

# Resolve through paths.py rather than deriving a location here. This module
# hardcoded the working tree's layout, and because nothing in the package
# exercised it, two audits shipped pointing at a directory that does not exist.
OUT = P.ANALYSIS


def base_of(tag):
    """`ai+human.merged.forkmerged` -> `ai+human`."""
    return tag.split(".")[0]


def sync_counts(d):
    """Recompute the header counts from the options array, in place.

    `n_options` and `n_forks` are written once by `cluster_up.py` at build
    time. Every repair pass afterwards rewrites `options` -- relabelling forks,
    merging option records -- and each computes the new totals for its own
    console output, but the header was never updated from them. So a repaired
    vocabulary reported its BASE fork count forever: 463 in a file whose
    options actually spanned 317 decision points.

    That is a silent wrong number in a published artifact, and it is the kind
    that survives review because it looks like a field someone maintained. The
    counts are derivable from `options` at any time, so the header should never
    be the authority -- it should be a cache of the derivation, refreshed on
    every write.

    Returns the dict for chaining.
    """
    opts = d.get("options") or []
    d["n_options"] = len(opts)
    d["n_forks"] = len({o["fork"] for o in opts if "fork" in o})
    return d


def garden_path(tag):
    p = OUT / f"garden_{tag}.json"
    return p if p.exists() else OUT / f"garden_{base_of(tag)}.json"


def load_garden(tag):
    return json.loads(garden_path(tag).read_text(encoding="utf-8"))


def sibling_map(tag):
    """fork label -> merged node label. Empty once forks have been re-induced."""
    gm = load_garden(tag)
    out = {}
    for head, members in gm.get("sibling_groups", {}).items():
        for m in members:
            out[m] = head
    return out


# ---------------------------------------------------------------------------
# Provenance: how a run's analysis came to exist.
#
# Every run counts. An itinerary run is a human's deliberate choice, executed,
# which is exactly what a corpus run is -- excluding it would treat a person's
# choice as less real than an analyst's, and would mean the garden can never
# grow. So provenance STRATIFIES, the way `arm` does. It never filters.
#
# What it buys is the ability to tell. If a headline number moves when the
# non-corpus runs are set aside, that must be visible rather than prevented,
# because the alternative -- a statistic that silently drifts as paths are
# walked -- is the actual hazard.
PROVENANCE = ("corpus", "itinerary", "authored")
DEFAULT_PROVENANCE = "corpus"


def provenance_of(runs=None):
    """{run_id: provenance}. Read from each run's record; defaults to corpus.

    Runs distilled before provenance existed have none recorded, and they are
    corpus runs by construction -- the tag was introduced with the first
    assembled run.
    """
    import json as _json
    import paths as _P
    out = {}
    for d in sorted(_P.DISTILLED.glob("*")):
        if runs is not None and d.name not in runs:
            continue
        f = d / "record.json"
        if not f.exists():
            continue
        try:
            rec = _json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        p = rec.get("provenance", DEFAULT_PROVENANCE)
        out[d.name] = p if p in PROVENANCE else DEFAULT_PROVENANCE
    if runs:
        for r in runs:
            out.setdefault(r, DEFAULT_PROVENANCE)
    return out


def split_by_provenance(runs):
    """(corpus_runs, other_runs) -- for reporting a statistic both ways."""
    prov = provenance_of(set(runs))
    corpus = {r for r in runs if prov.get(r, DEFAULT_PROVENANCE) == "corpus"}
    return corpus, set(runs) - corpus


# ---------------------------------------------------------------------------
# Effective options, defined once.
#
# THE UNIT IS AN ANALYSIS, NOT A DECISION RECORD.
#
# Two implementations of this existed and both over-counted, differently.
# `forkscope.py` counted decision INSTANCES, so an analysis that recorded the
# same fork twice voted twice. `fork_atlas.py` counted run sets per option and
# summed their sizes, so an analysis holding two options at one fork voted in
# both. Neither is a rounding error: 86% of analyses hold two options at some
# fork, and the skin-tone exposure fork alone does it in 158 of 223. Instance
# counting reported 10.06 effective options there against 4.61 per analysis.
#
# So each analysis contributes exactly one vote per fork -- its MODAL option
# there. That is the same rule `aws_compare.py` already used, for the same
# reason: the alternative is dropping the analysis, which silently narrows
# every statistic to the forks that behave.
#
# TWO POPULATIONS, AND THE DENOMINATOR IS THE WHOLE DIFFERENCE
#
#   eff_reached   over analyses that REACHED the fork -- among those who acted,
#                 how many ways did they act?
#   eff_all       over ALL analyses, with "did not reach" as a level -- of
#                 everyone who could have acted, how divided were they?
#
# `eff_reached` badly overrates rare forks: one reached by six analyses that
# each did something different scores 6.0, as contested as a genuine three-way
# split across two hundred. `eff_all` scores it 1.06, because the choice almost
# everyone made was not to go there -- which is a choice, and is carried
# everywhere else in this project as a silent decision.
#
# `eff_all` therefore needs BOTH engagement and disagreement to be high, which
# is why it replaces the two-condition pivotal test. It is a good scalar for
# ranking and a poor one for interpretation: a niche contested fork and a
# widely-skipped but agreed one score alike, and only the pair separates them.


def fork_stats(d, n_runs=None):
    """{fork: {reach, coverage, eff_reached, eff_all, options, modal_share}}.

    `d` is a loaded bottom_up vocabulary. `n_runs` defaults to the number of
    distinct analyses appearing in it.
    """
    from collections import Counter, defaultdict

    dec = d["decisions"]
    per = defaultdict(lambda: defaultdict(Counter))
    for o in d["options"]:
        for m in o.get("members", ()):
            if 0 <= m < len(dec):
                per[o["fork"]][dec[m]["run"]][o["option"]] += 1
    N = n_runs or len({x["run"] for x in dec})

    def inv_hhi(counts):
        t = sum(counts)
        return round(1.0 / sum((c / t) ** 2 for c in counts), 3) if t else 0.0

    out = {}
    for f, runs in per.items():
        modal = Counter(c.most_common(1)[0][0] for c in runs.values())
        reach = len(runs)
        absent = N - reach
        vals = list(modal.values())
        out[f] = {
            "reach": reach,
            "coverage": round(reach / N, 4) if N else 0.0,
            "eff_reached": inv_hhi(vals),
            "eff_all": inv_hhi(vals + ([absent] if absent else [])),
            "options": len(modal),
            "modal_share": round(max(vals) / reach, 4) if reach else 0.0,
            # The distribution the two numbers are computed from, in ANALYSES.
            # Returned so a caller can draw the spectrum without recounting it
            # a third way -- `absent` is the level that separates eff_all from
            # eff_reached, and any picture of one has to be able to show it.
            "dist": dict(modal.most_common()),
            "absent": absent,
        }
    return out


def is_pivotal(st, min_eff_all=1.5):
    """A fork is pivotal when enough analyses engaged AND they disagreed.

    One criterion, because `eff_all` already carries both: low coverage lets
    the absent level dominate, and agreement lets the modal option dominate.
    Nothing scores high without both.
    """
    return st["eff_all"] > min_eff_all
