---
name: review
description: >-
  Phase 2 — put the questions the pipeline cannot settle to a human, with their
  evidence, and record the answers. Two-way: the human answers, comments, and
  asks back. Use after a build and its audits, before any number is quoted.
---

You are asking, not presenting. Argument: an optional round number.

The pipeline has produced results v1 and a set of judgements it cannot make. A
handful of those genuinely require a person — whether two forks are one
question, whether a fork is multi-select or mis-clustered, whether an option
bundles two decisions. The shape is identical in each case and only reading
settles it.

## This is the charting layer only

`review_round.py` reads `data/audits/vocab_exhibits.json` and exits if it is
absent. There is **no `--layer` flag**, so there is no such thing as a
distillation round: the whole machinery is bound to the vocabulary.

That is a real gap, not a design choice, and it matters because distillation has
its own gate. If the question is about extraction — whether spans reproduce,
whether the jitter reaches the option layer, whether an unmatched silent decision
is a limit or a matching artifact — the evidence is the `q1_*` scripts and the
conversation belongs to `/settle distill`. Say so rather than opening a chart
round and asking extraction questions inside it.

## Open a round

```bash
python3 scripts/audit_vocab.py            # refresh the exhibits first
python3 scripts/review_round.py new --n 12
```

Questions come from the audit exhibits, already ordered worst-first, so a round
is the top of a ranked queue rather than a sample.

`policy.json:audit.review_queue_max` caps how deep the queue goes — 60 on
soccer, and it is marked **implicit**: a guess about attention that has never
been checked against what a person actually read. The cap is an admission that
attention is finite, so if the owner reads to the bottom and wants more, that is
evidence about the cap and worth recording.

## The second queue: what replication could not decide

`review_round.py` draws only from the audit exhibits. There is a second source
of questions, and it is the better one where it exists — **the places two builds
of the same pipeline disagreed**:

```bash
python3 -m json.tool stability/data/arbitrated_option.json | head -30
head -20 stability/data/arbitration_queue_option.csv
```

An option that lands in one fork in every replicate is settled. One scattered
across six is the pipeline saying it cannot decide, and that is a question for a
person phrased exactly the way this skill phrases the others. Rank by that
disagreement, cut at `review_queue_max`, and work it the same way.

These rows are not in `reviews/round-NN.md` and `review_round.py` will not put
them there. Bring them into the round by hand, and say that you did — a
question's provenance matters when someone later asks why it was asked.

## Then work it with the person, in the file

Do not paste twelve questions into chat. Take them a few at a time, and for
each one:

**Show the items, not a summary.** Print both option lists side by side. That
is the view that caught the rater fork after a similarity statistic said
everything was fine.

```bash
python3 scripts/trace.py resolve fork:8d07b365
python3 scripts/trace.py fork "<label>" --limit 20
```

**Say what each answer changes.** The question is only worth their attention if
the answers diverge. If both lead to the same action, drop it and say why.

**Say which error they are risking.** Over-merge is invisible and
unrecoverable; under-merge is visible and fixable later. When a call is close,
that asymmetry is the advice.

**Answer their questions.** This goes both ways. When they ask something you
cannot settle from the evidence, say so and offer `/challenge` rather than
reasoning toward a plausible answer.

**`need more evidence` is a real answer.** Route it to `/challenge`, do not
push for a decision.

## Read the answers back

```bash
python3 scripts/review_round.py read
```

Their prose is kept verbatim — do not paraphrase it into the JSON. A comment
that disagrees with your framing is the most useful thing in the round and must
survive intact.

## Rules

**Never report a queue as clean.** V1, V3 and V4 rank by weak signals that
cannot see two descriptions of one action sharing no words. Report depth read
against depth queued — *"N queued, 12 read"* — and get N from the exhibit rather
than from the number of rows it chose to display.

**Do not answer your own questions.** If you already know, it was not a
question. If you have a view, state it as a view and let them overrule it.

**Do not apply anything here.** Applying is `/refine`, and separating the two
is what lets someone see what was decided before seeing what was changed.

Close by reporting: answered, deferred, and what the deferred ones block.
