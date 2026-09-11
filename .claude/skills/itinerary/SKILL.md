---
name: itinerary
description: >-
  Second consultation — walk a user through the key forks, help them choose an
  option at each, check the choices are compatible, compare the resulting path
  against what the corpus actually did, then build and run it and add it to the
  garden as a new run. Use when someone wants to specify their own analysis
  through the garden, ask what-if, or test a path.
---

The garden as a **specification** rather than a picture: pick a path, get the
analysis it implies, run it, and see where its answer lands among the runs that
took the same path.

Six phases. Do not skip 4 — a path that no run could have walked is not a
what-if, it is a bug.

## 1 · Which forks to offer

Not all of them — soccer has 317 and 17 are pivotal. Offer the ones a choice is
real at:

```bash
python3 scripts/trace.py fork "<label>" --limit 20
python3 -c "import json,sys;sys.path.insert(0,'scripts');import paths as P;\
d=json.load(open(P.ANALYSIS/f'stability_{P.FINAL_TAG}.json'));\
print(json.dumps(d['forks'][:12],indent=1))"
```

Rank by `eff_all`, which is what `policy.json:forks.pivotal` selects on — it
counts *did not reach* as a level, so one threshold carries both engagement and
disagreement. A fork everyone reached and agreed on is not a decision the user
gets to make; a fork many analyses reached and split over is.

On the soccer headline vocabulary the top of that ranking is **how the skin-tone
rating is entered as the exposure** — 23 options over 211 analyses, `eff_all`
5.07, modal share 0.42. The widest fork by raw option count is a different one,
**the covariate adjustment set**, at 37 options over 127 analyses. Read both:
the widest is not always the most contested.

Derive the ranking rather than repeating those numbers — they are properties of
one vocabulary tag and they move when it does.

## 2 · Explain the options honestly

For each fork, give the option list with run counts, and say what separates
them — the *action*, not the wording.

**Stable versus novel is the distinction users most need, and it is easy to
mislead on.**

| | means | does not mean |
|---|---|---|
| **stable** | most runs did this | it is correct |
| **novel** | one run did this | it is wrong, or bold |

Novelty is a fact about the corpus, not a verdict. In this study **novel options
do not move the outcome** — measured, not assumed. So "everyone else did X" is a
statement about convention and not evidence, and a user choosing a one-run
option is not thereby taking a risk with the answer.

Say when a fork is **not single-choice**: on the soccer headline vocabulary 43
of 317 have runs that took two options, and 199 of 223 analyses do it somewhere
— some because reporting both an odds ratio and a risk difference is one analyst
doing two legitimate things. `policy.json:forks.exclusivity_required` is `true`,
which does not make it true; it makes the violation the audited V2 exhibit. At
those forks, offer multi-select.

## 3 · Let them choose

Record fork handle, option handle, and their reason. The reason is the part
worth keeping — it is the rationale the corpus records for real analysts, and an
itinerary without one is not comparable to them.

Unset forks are fine. **Not reaching a fork is itself a choice** and the design
treats it as a level.

## 4 · Audit the path

Two checks, both cheap, both mandatory.

**Incompatibility.** Do any two chosen options never co-occur in any run? Use
the exclusivity signal — options at one fork almost never co-occur, and if two
choices at *different* forks never co-occur either, that is either a real
conflict or a combination nobody tried. Distinguish them: zero co-occurrence
with high individual counts is a conflict; zero with low counts is unexplored.

**Foreclosure.** Does one choice make another unreachable? Dichotomising the
exposure forecloses every option at forks that only continuous exposures reach.

Report both, and say which. "Nobody tried this" is the interesting case and
should not be reported as an error.

## 5 · Compare with the corpus

Before running anything:

- How many runs walked this exact path? Usually zero — say so plainly.
- The nearest real runs, by number of shared choices, and what they concluded.
- Which choices are modal and which are one-run.

If several real runs took this path and agreed, predict that. If none did, say
the itinerary is unprecedented and that its result is a single observation.

## 6 · Build, run, and file it

**Say this out loud before you start phase 6: there is no itinerary runner.**
Specifying a path and auditing it — phases 1 to 5 — is built and works. Turning
the path into an executable analysis is not built; there is no consolidation
step in this package that assembles N implementations of a fork's option into a
parameterized template, so the assembly is hand-written by you, from the source
lines the corpus contains, every time.

That has a consequence the user must know before they choose: the run you hand
back is **your** implementation of their choices, not the corpus's. Phase 7
(`/inspect`) exists to catch the gap, and the forks the itinerary did not fix
were decided by you rather than by them — list those explicitly.

This is one of the things Bayesian optimisation over pivotal forks would need
first. Do not describe it as available.

**Provenance is not optional.** The new run is tagged with one of:

| | |
|---|---|
| `corpus` | extracted from an analysis a real analyst wrote |
| `itinerary` | assembled entirely from options the corpus contains |
| `authored` | contains an operation no run in the corpus performed |

The run counts toward the statistics — it is a real analysis a person chose.
What the tag buys is that `stability.py` will report the headline with and
without non-corpus runs, so its influence is visible rather than silent.

Report the estimate beside the distribution of real runs. One run is one
observation; it does not update a finding on its own.

## Can a user propose an option nobody took?

Sometimes. Be precise about which case you are in, and say no when it is the
third.

**Yes — a new parameter on an existing action.** "Dichotomise at 0.4" where the
corpus has 0.25, 0.5 and 0.625. The action is attested and the template is
already parameterized; only the value is new. Tag `itinerary`, note the value is
outside the observed set.

**Usually — recombining attested actions.** An action seen at one fork applied
where no run applied it. Buildable if the operations compose, but check phase 4
first: it may be unattested because it is foreclosed. Tag `authored`, because
the *combination* is not in the corpus even though its parts are.

**No — a genuinely new operation.** A model family, an estimator, a
transformation nobody used. This is writable code and I can write it, but the
result is not charted: its provenance is me, not the corpus, and it belongs in a
different study rather than in this garden. Say so directly, offer to write it
as a standalone analysis outside the garden, and do not tag it as a run.

The line is whether the option's **action** is attested somewhere in the corpus.
Parameters are free, recombination needs an audit, invention leaves the garden.
