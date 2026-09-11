---
name: chart
description: >-
  Chart the garden of forking paths for a study — run the full pipeline from
  raw analysis repositories to a decision map, its audits, and its figures.
  Use when the user wants to run the pipeline on a corpus, start a new case
  study, or rebuild a study end to end.
---

Run the pipeline for one study. Argument: a study name (default: the study
`FORKSCOPE_STUDY` selects, or `soccer`).

The instrument is shared and must not be modified per study. If a corpus
appears to need a new prompt or a new script, **stop and say so** — that is a
finding about the instrument, not a configuration step, and silently forking
the pipeline forfeits the only thing a second case study proves.

**Charting a garden is itself an analysis with its own forking paths**, and they
are written down: `policy.json` holds the dozen method decisions this pipeline
rests on, each recording what was chosen, why, and whether it was *decided* or
*defaulted into*. Read it before you build, and quote from it when you report —
a number produced under a policy nobody has seen is not reproducible in the
sense this project means.

Two entries govern this skill in particular: `forks.pivotal` (the criterion that
selects what is worth arguing about — `eff_all > 1.5` on soccer, giving 17
forks) and `stability.role`, which is `diagnostic` and carries the refusal in
the rules below.

## 1. Establish where you are

```bash
python3 -c "import sys;sys.path.insert(0,'scripts');import paths as P;print(P.describe())"
```

Confirm the study name, corpora and headline tag are the ones intended. A
study with no `study.json` errors rather than falling back — do not work around
that by setting `FORKSCOPE_STUDY` to a study that does have one.

For a new study, follow [`templates/README.md`](../../../templates/README.md)
first. Leave `final_tag` as `CHANGE-ME`; it is not knowable until the repair
chain has run.

## 2. Check the raw material is reachable

```bash
python3 scripts/distill.py all --limit 2
```

Two runs, not the corpus. If the glob matches nothing, or the artifacts named
in `study.json` are not in a run directory, that surfaces here for the price of
two model calls instead of two hundred.

Extraction has its own skill and its own gate. If this is a first build, or if
the smoke test looks wrong, go to `/distill` and come back — charting a
vocabulary over an extraction nobody has read means any disagreement you find
later could be either layer, and you will not be able to tell which.

## 3. Build

```bash
python3 scripts/build_all.py --corpus <corpora> --repair --gate
```

`--repair` runs the vocabulary repair chain, whose **order is load-bearing**:
options, forks, options *again*, induce. The second option pass is not
redundant — while two forks were duplicates their option lists could not see
each other.

This is the expensive step. Cached calls are free; new ones are not. Report the
cost from `cache/llm_runs/` rather than guessing.

## 4. Settle the tag

```bash
python3 scripts/compare_vocab.py
```

Read the stage-by-stage counts, decide which vocabulary is the headline, and
write it into `study.json` as `final_tag`. For a new study this is the moment
the tag becomes knowable.

## 5. Audit before analysing

Invoke `/audit`. Do not report analysis numbers from a build whose audits you
have not run — the audits have overturned reported results four times, and a
number quoted before its check is a number you will have to retract.

## 6. Analyse and draw

`build_all.py` runs these; re-run individually when iterating. Every figure
regenerates from `data/`, so never edit one by hand.

The one to open is `figures/forkscope.html` — the five-tab viewer over the
garden, the pivotal forks, the lifecycle and the corpus. It computes no
statistic of its own; a viewer that recomputed would be a second implementation
to keep in agreement with the first.

```bash
python3 scripts/build_figures.py          # every figure, from data/ only
python3 scripts/forkscope.py              # -> figures/forkscope.html
node scripts/forkscope_check.js figures/forkscope.html
```

`build_figures.py` skips the model-calling stage unless given `--with-llm`, so
the whole figure set redraws for free against the committed cache — about 70
seconds. It prints a banner naming any gap between the tag you asked for and
`final_tag`: read it, because a figure rendered from the wrong vocabulary exits
0 and looks entirely normal.

**Pass the path.** `forkscope_check.js` defaults to an absolute container path
and dies with `ENOENT` anywhere else; the argument is the fix, not a broken
check.

`forkscope_check.js` runs the generated viewer against a
DOM stub and calls every entry point — `node --check` proves it parses, this
proves it runs. It exists because a `ReferenceError` once shipped: the page
loaded, the tabs switched, and the ring numbering and every click handler were
dead. Needs node, which the analysis container does not have.

## 7. Report

State: study, corpora, analysis count, decisions, options, forks, how many are
pivotal under `policy.json:forks.pivotal`, how many are measurable (≥10
analyses), which audits returned REVIEW, and what remains unread.
`data/audits/vocab_exhibits.md` is the review queue; **say how much of it is
unread rather than implying it is clean.**

Then say what this build is **not** yet: results v1 is a draft, and numbers from
it are not quotable until `/review` and `/refine` have run and the owner has
closed the charting gate at `/settle chart`. `/report` writes them up once they
are.
