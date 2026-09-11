# Human benchmark packet

Three files per rater, to be completed **in order**. Roughly 90–120 minutes.

Three people rate the **same items**, independently. Do not discuss any item
with another rater until all three sheets are returned.

---

## Why this exists

Everything in `stability/` measures how much the pipeline agrees **with
itself** across two independent builds. A self-agreement rate has no meaning on
its own: 0.70 is poor if two humans agree at 0.95, and at ceiling if two humans
agree at 0.70. This packet supplies the missing comparison.

For that comparison to be valid you must answer the same questions the model
answered, on the same items, without seeing what it said. Hence the rules
below — they are not ceremony.

---

## Rules

1. **Order matters.** Complete `1_option_pairs.csv`, then `2_fork_pairs.csv`,
   then `3_fork_audit.csv`. Part 3 shows whole forks; seeing one first would
   tell you how the pipeline grouped things and contaminate parts 1 and 2 with
   context the model never had.
2. **Do not open `KEY-do-not-open.json`.** It holds the model's answers.
3. **Judge each pair on its own.** The pairs are shuffled and deliberately do
   not say which fork they came from.
4. **`unsure` is a real answer.** It means: *the description does not carry
   enough information for me to draw a conclusion.* It is a statement about the
   item, not a hedge about yourself — shown two covariate lists with no
   indication of which slot each came from, nobody can tell whether they are
   alternatives at one fork or the adjustment sets of two different models.
   A pair everyone marks unsure is a finding, not a gap.
5. **Fill in `confidence` every time** — **1–5, 1 low and 5 high**. It is doing
   as much work as the verdict. It is z-scored within rater before use, so use
   the range that feels natural to you rather than trying to match anyone else.
6. Add a `note` whenever the pair is interesting or the choices feel wrong.

---

## Part 1 — same **action**?

> Do these two lines describe the **same operation on data**, however
> differently worded?

Same: *"average rater1 and rater2 into a single score"* and *"compute the mean
of the two rater columns"* — one operation, two phrasings.

Different: *"drop dyads with missing skin tone"* and *"drop goalkeepers"* —
near-identical phrasing, different operation.

## Part 2 — same **decision point**?

> Are these two choices alternatives at the **same slot**?

**The test:** could one competent analyst, in one script, do **both**?

- yes → **different** decision points
- taking one rules out the other → **same** decision point

Same slot: *"drop rows with no rating"* and *"impute from the other rater"* —
no shared words, opposite operations, but you cannot do both to the same rows.

Different slots: *"drop rows with no rating"* and *"drop goalkeepers"* — you
can do both.

**Carve-out:** a robustness refit at another setting is *not* the same
decision. "Dichotomise at 0.25, then refit at 0.50" is one analyst reporting a
sensitivity analysis, not one analyst taking two options at one slot.

## Part 3 — how should this fork be re-merged?

**This part is not a test.** It is where you hand the pipeline an instruction
it can act on. One row per decision point, with its options and counts inline.

| verdict | meaning |
|---|---|
| `correct` | one question, and its options are alternatives at it |
| `split` | two or more questions have been fused — say along **which axis** |
| `absorb` | part of a question that also lives elsewhere — **name that fork** |
| `move` | some options belong elsewhere — name which, and where |
| `unsure` | the row does not carry enough to judge |

Then fill in **`remerge`** — the instruction itself, in your own words. That is
the column that gets acted on. A `split` or `move` with an empty `remerge` is
an incomplete row, not a filed one. For example:

> `split by axis: which variables enter | how each is transformed`
> `absorb into: how is the skin-tone rating entered as the exposure?`
> `move: the games-played options → their own fork`

**An axis you find yourself writing twice is worth saying once, loudly.** A
repeated re-merge instruction is a claim about the vocabulary, not about the
fork in front of you, and the scorer gathers those together rather than
counting them as separate complaints.

The first run of this packet proved the point. Eight scattered
`over-merged`/`under-merged` labels turned out to be one instruction — *the
model-specification forks tangle which variables enter with how each is
transformed* — and it was the free text that said so, not the labels. Which is
why `remerge` now exists.

---

## The hypothesis, registered before any rating

Recorded here so the reading cannot be chosen after the results are in.

> **If humans also split on the pairs the two builds disagree about**, then the
> pipeline's instability is tracking genuine ambiguity — it is uncertain
> exactly where the question is hard. That is the good outcome.
>
> **If humans agree confidently on those pairs**, the instability is model
> noise rather than ambiguity. That is the worse outcome, and it points at the
> prompt rather than at the task.

Both are publishable. Neither is the one we are hoping for.

---

## What happens next

```bash
python3 stability/scripts/score_review.py --packet reviews/human-benchmark
```

Reports human–human agreement per stratum, the model–model rate on the same
items, and whether the gold pairs were passed. Sheets failing the gold check
are reported separately rather than silently dropped.
