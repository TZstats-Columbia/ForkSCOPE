# Merge group labels that name the same choice

You are given labels produced independently from different batches of one
corpus. Because the batches did not see each other, the same choice will have
been labelled several times in slightly different words. Merge those.

## What to merge

Merge two labels when they name **the same choice** — substituting one for the
other would not change what the analysis did.

- *"average the two rater columns"* / *"mean of rater1 and rater2"* /
  *"combine both raters into one score"* — one option.
- *"drop dyads with no skin-tone rating"* / *"exclude unrated players"* — one
  option.

## What never to merge

Do **not** merge labels that differ in a number, a threshold, a direction, a
variable set, or an estimator, however similar the wording:

- *"dichotomize at 0.5"* and *"dichotomize at 0.25"* — **separate**.
- *"cluster SEs on player"* and *"cluster SEs on referee"* — **separate**.
- *"adjust for games and position"* and *"adjust for games, position and
  league"* — **separate**.

When in doubt, leave them separate. A wrongly split option is visible and
fixable downstream; a wrongly merged one is invisible and destroys the count.

## Do not compress

There is no target number. If 400 labels name 300 distinct choices, return 300
groups. Merging beyond what the data supports is the failure mode here, not
leaving too many.

## Output contract

Return only this JSON object. Every input label id must appear exactly once.

```
{
  "merged": [
    {
      "label": "the clearest phrasing among the members, or a better one",
      "question": "what fork this is an answer to",
      "members": [2, 19, 40]
    }
  ]
}
```
