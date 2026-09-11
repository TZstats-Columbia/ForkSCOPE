---
name: replicate
description: >-
  Measure how much a layer agrees with itself — build isolated replicates of
  distillation, vocabulary, or fork formation and report the variance. Spends
  real money. Use when a stability number is needed, before /settle.
---

You are measuring a layer against itself. Argument: a stage (`distill`,
`vocab`, `forks`).

A replicate re-runs one stage with everything upstream held byte-identical, so
any difference downstream is that stage's own variability and nothing else.

## Isolation is filesystem-level, and it must stay that way

Every replicate gets its own study root with an empty cache.

**Never reach for `nocache=True`.** It skips the cache read and still WRITES to
the same key, so running it in place overwrites the entries the baseline is made
of — destroying the build being measured, irreversibly, with no error.

```bash
python3 stability/scripts/replicate.py init --root replicates/B --stage vocab
python3 stability/scripts/replicate.py run  --root replicates/B --stage vocab \
        --corpus ai,human
```

Run it in the **LLM container**. `distill-dev` has no `claude` CLI and dies at
the manifest step.

## Choosing the stage

| stage | freezes | costs | answers |
|---|---|---|---|
| `distill` | nothing | ~$60 / 30 runs | does extraction reproduce |
| `vocab` | distillation | ~$250 | does the whole vocabulary reproduce |
| `forks` | distillation and options | ~$21 | does fork formation reproduce |

`forks` is the one that separates a layer's own noise from noise it inherited.
It needs `--from-vocab` (the frozen options) and, for any parent that is not
this repo, `--parent-root`.

**`--parent-root` is load-bearing.** `merge_forks` reads `garden_<tag>.json` and
falls back to `garden_<base>.json`, where `base` truncates at the first dot — so
a replicate of build B given no parent root silently reads build A's garden, and
the resulting agreement is an artifact of the shared input. Both sides complete.
Nothing warns.

## Batches

```bash
python3 stability/scripts/fork_replicate_batch.py \
  --parent A=../../replicates/A-parent/bottom_up_<tag>.json \
  --parent B=../../replicates/B-root/data/vocabulary/bottom_up_<tag>.json:../../replicates/B-root \
  --n 5
```

**Fix `n` before the first build and say so.** At *k* replicates a parent gives
*k−1* degrees of freedom; an sd on 2 df is compatible with almost anything.
Running a few, looking at the spread, and extending is optional stopping on a
variance estimate — it biases the exact quantity being reported.

`policy.json:stability.replicates` is where that commitment lives:
`n_per_parent` with `pre_committed: true`. On soccer it is 5, decided before the
first build for exactly this reason. Read `n` from there rather than choosing it
now; if there is no policy file, fix the number in writing before you spend
anything.

Resumable: a replicate whose manifest records a `final_tag` is skipped, and a
failed build keeps its cache so the retry is nearly free.

## Report it

```bash
python3 stability/scripts/fork_variance.py --root <root you just built> \
        --json replicates/results/fork_variance.json
```

**`--root replicates` will not work in the shipped package.** `fork_variance`
skips any replicate whose `manifest.json` has no `final_tag`, and every
committed manifest lacks one — the built replicates themselves are not shipped,
only `replicates/results/fork_variance.json`. Point `--root` at the root your
own run produced. To quote the existing figure instead, read that result file
and say it is the committed one.

Then turn the disagreement into work, which is the point of having run it:

```bash
python3 stability/scripts/arbitrate.py --help
```

`arbitrate.py` applies the rule the audits have only ever *reported*: two
decisions stay merged **only if every build kept them together** — the meet of
the partitions, which is "default to unmerged". Not a majority vote: with three
builds, majority keeps a merge one build rejected, at exactly the moment there
is clearest evidence the merge is disputed. Majority is right when errors are
symmetric and here they are not. It writes
`stability/data/arbitration_queue_option.csv`, which is the ranked queue a human
should read, and `/review` is where they read it.

The cost is real and must be stated rather than hidden: the meet is finer than
any input, so the arbitrated vocabulary has **more** clusters than any single
build. That is the intended direction — a split is recoverable and an over-merge
is not.

**Compare each layer against perfect agreement, not against each other.** The
tempting reading — "the within/between gap is large, so the disagreement is
inherited" — compares the wrong pair. Decomposed as shortfall from 1.0, soccer's
fork induction contributes 0.384 and the differing options 0.282: induction is
the *larger* share, and the gap invited the opposite conclusion.

**Say what was frozen.** A fork replicate drops `merge_options`, so it is a
modified pipeline measuring fork-formation variance under frozen options — not
end-to-end variance. Parents built by the full loop are not exchangeable with
it and are excluded from the statistics.

## Rules

**Stability is a diagnostic, not an objective.** Do not tune the method to
improve it. Induction can be pushed toward 1.0 by merging almost nothing, which
raises the number and destroys what it measures. `policy.json:stability.role`
must say `objective`, with a pre-registered candidate set, a held-out split and
an external criterion, before any tuning — and if it does not, decline and say
why.

**Turn the number into a queue, not a grade.** Per-option assignment entropy
across replicates ranks what a human should adjudicate — an option landing in
one fork 10/10 times is settled; one scattered over six forks is the pipeline
saying it cannot decide, which is a question for a person phrased exactly as
`/review` phrases them. That is what stability is *for*.

**Report a ceiling, or say there isn't one.** An agreement figure read against
1.0 is a grade, and two people doing this task will not agree at 1.0 either.
Without an external criterion — on soccer, the human benchmark in
`reviews/human-benchmark/` — every stability number is a bare figure rather
than a ratio against what is achievable. Say so every time you
report one; it is the first thing a reader will ask.

**Report cost.** Every replicate is real money; the manifest records spend on
success and on failure, so it never looks free.
