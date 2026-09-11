# Align two accounts of the same analysis

Below are two lists of decisions, both describing **the same single analysis**,
derived from two different sources. You are not told which source is which, and
the order is randomised. Do not assume either list is more authoritative.

Your job: say which items in list 1 and list 2 describe **the same decision**,
and for each aligned pair, whether they record the **same choice**.

## What "the same decision" means

Two items describe the same decision when they answer the same question about
what to do with the data — dichotomising the exposure, choosing the adjustment
set, deciding which rows to drop. The wording will differ. One list is written
as operations on data, the other as statements in a write-up, so
*"skin_tone_avg = (rater1 + rater2)/2"* and *"we averaged the two raters'
ratings"* are the same decision.

## Verdicts for an aligned pair

- `same_option` — the same choice. Substituting one description for the other
  would not change what a reader thinks the analysis did.
- `same_fork_different_option` — the same question, but a **different answer**.
  One says the cutoff was 0.25, the other says the median. One says rows were
  dropped, the other says they were imputed. This is disagreement between the
  two accounts and is the most important category to get right.
- `vaguer` — the same choice, but one side is too underspecified to pin down
  which option it is. *"We controlled for player characteristics"* against a
  named list of six covariates. Not a disagreement; a loss of resolution.

## Unmatched items

List every item with no counterpart, on either side, under `unmatched_1` and
`unmatched_2`. Do not force a match. An item with no counterpart is a real and
expected outcome — the two sources genuinely differ in what they record — and
inventing a weak pairing destroys the measurement this feeds.

## Be strict

Two decisions that merely concern the same variable are **not** the same
decision. *"Dropped rows missing skin tone"* and *"averaged the two skin-tone
raters"* both concern skin tone and are different decisions. Match on the
question being answered, not on shared nouns.

If you are unsure whether two items are the same decision, leave them unmatched.
An unmatched pair costs a recall point; a wrong match corrupts the agreement
rate, which is the number this exists to produce.

## Output contract

Return only this JSON.

```
{
  "pairs": [
    {"id_1": "3", "id_2": "11", "verdict": "same_option",
     "why": "both average the two rater columns"},
    {"id_1": "7", "id_2": "4", "verdict": "same_fork_different_option",
     "why": "one dichotomises at 0.25, the other at the median"}
  ],
  "unmatched_1": ["1", "5"],
  "unmatched_2": ["2", "9", "12"]
}
```

Every id from both lists must appear exactly once — either in one pair or in the
matching `unmatched` list. `why` stays under 15 words.
