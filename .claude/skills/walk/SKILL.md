---
name: walk
description: >-
  Phase 4 — walk a human through the finalized garden so they can judge whether
  it looks like the corpus they know. Exploratory, no queue, no pending
  questions. Use when someone wants to look at the map rather than check a claim.
---

Show the person the garden and follow their curiosity. No argument, or a stage
or fork to start from.

This is not `/review`. Review works a ranked list of items a metric flagged. A
walk follows what a person who knows the field notices, and it finds a
different class of error — the fork that is obviously missing, the stage that
feels wrong, the option that reads oddly at a place no metric flagged.

**The rater-fork error was found on a walk**, by reading two option lists side
by side in the garden viewer, after a similarity statistic had reported that
2.7% of pairs were near-duplicates and everything was fine.

## Open with the shape, not the numbers

**Start in ForkSCOPE.** It is the viewer the guide sends people to, it is one
page, and it is the only one that puts the map and the outcomes side by side:

```bash
open figures/forkscope.html       # four tabs; start here
```

| tab | the question it answers |
|---|---|
| **The Garden** | every fork at once, on a ring by lifecycle stage, with the routes analysts actually travelled |
| **Pivotal Forks** | which decisions are worth arguing about, and whether they move the answer |
| **Lifecycle** | where the work sits, whether the process loops back, whether inventing helps |
| **Corpus Viewer** | one analysis at a time, its exon/intron map, how it compares |

If the owner has not read [`README.md`](../../../README.md) and
[`policy.json`](../../../policy.json) — the method and the dozen decisions that
are theirs — offer them before the walk rather than explaining the method as
you go. A walk spent explaining the pipeline is a walk not spent reading the
map.

Then, in a sentence each: how many analyses, how many forks, how many are
measurable, and where disagreement concentrates. Stop. Let them ask.

## Follow them, do not lecture

```bash
python3 scripts/trace.py fork "<whatever they name>" --limit 20
python3 scripts/trace.py run <run-id>
```

Useful moves when they stall:

- **The busiest forks** — is this what everyone actually had to decide?
- **The most contested** — rank by `eff_all`. On soccer that is the skin-tone
  exposure fork, 23 options over 211 analyses. Do those read as 23 real
  alternatives, or as one action described 23 ways?
- **The widest** — a different fork: the covariate adjustment set, 37 options
  over 127 analyses. Width and contest are not the same thing, and the gap
  between the two lists is itself worth showing them.
- **A stage they know well** — does its fork list look complete?
- **One whole run** — `trace.py run <id>` prints its path. Does that look like
  an analysis someone would write?
- **The silent decisions** — operations the code performs and the write-up never
  mentions. Are these really undisclosed in this field, or conventional and
  unremarked? Only they can tell you, and it is the one question the pipeline
  cannot even estimate.

Derive the counts rather than quoting the ones above; they are properties of one
vocabulary tag and they move when it does.

## What you are listening for

*"Where is X?"* — a missing fork. Possibly an extraction gap, possibly nobody
did it. Check before agreeing.

*"Those two are the same."* — an under-merge the metrics missed. This is the
highest-value thing a walk produces.

*"Nobody would do that."* — either a mis-extraction or a genuinely odd run.
Trace it to source before deciding which.

*"That's not a decision in our field."* — context the intake should have
captured. Record it either way.

## Close by opening a round

A walk that produced questions should end with them written down:

```bash
python3 scripts/review_round.py new --n 8
```

Add what they raised to the round rather than answering it here. **A walk that
generates a new round is a success, not a failure** — it means the map was read
by someone who could tell.

Do not defend the garden. If it looks wrong to someone who knows the corpus,
that is data.
