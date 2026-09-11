# Group a batch of decisions into whatever groups are actually there

You are given decisions from a corpus of independent analyses of one dataset.
They have been sorted so that related ones are adjacent, but the sort is crude
and you should ignore it where it is wrong.

Put each decision into a group with the others that made **the same choice**.

## There is no target number of groups

Do not aim for a tidy count. If these 60 decisions contain 40 distinct choices,
return 40 groups. If they contain 4, return 4. A group of one is a correct
answer when a decision is genuinely unlike the others — singletons are how a
rare choice survives to be counted later, and forcing one into a neighbouring
group destroys exactly the signal this corpus exists to measure.

## Same choice, not same topic

Two decisions are the same choice when substituting one for the other would not
change what the analysis did in any way a reader would care about.

- *"average the two rater columns"* and *"compute the mean of rater1 and
  rater2"* — **same group**, different words for one operation.
- *"dichotomize skin tone at >= 0.5"* and *"dichotomize skin tone at >= 0.25"* —
  **different groups**. Same operation, different threshold, different players
  in each arm.
- *"drop rows with no skin-tone rating"* and *"drop rows missing any covariate"*
  — **different groups**. Both are exclusions; they remove different rows.
- *"fit logistic regression of any_red on dark_skin"* and *"fit logistic
  regression adjusting for games and position"* — **different groups**, the
  adjustment set differs.

Numbers, thresholds, directions, variable sets and estimator names are
load-bearing. Wording is not.

## Label each group by what it does

`label` states the choice in one short phrase, in your own words, at the level
of specificity that distinguishes it from a near neighbour: *"dichotomize skin
tone at 0.5"*, not *"handle skin tone"*, and not *"line 55 dichotomization"*.

`question` states what the group is an answer *to* — the fork it sits on:
*"how is the continuous skin-tone score turned into an exposure?"*. Several
groups in this batch will share a question; that is expected and is how the
next stage builds forks.

## Output contract

Return only this JSON object. Every input id must appear in exactly one group.

```
{
  "groups": [
    {
      "label": "dichotomize skin tone at 0.5",
      "question": "how is the continuous skin-tone score turned into an exposure?",
      "ids": [3, 17, 42]
    }
  ]
}
```
