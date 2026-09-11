# Are these genuinely different choices?

Below is one decision point and every option recorded under it. Each option was
written independently while reading a different analysis, so the same choice may
appear several times in different words.

Partition the options into **distinct actions**.

## What makes two options the same action

Two options are the same action when substituting one for the other would not
change what a reader thinks the analysis did.

- *"average the two raters into one continuous score"* and *"average the two
  raters' scores into a single continuous skin-tone measure"* are one action.
  The wording differs; the operation does not.
- *"drop rows with missing skin tone"* and *"exclude dyads lacking a rating"*
  are one action.

## What makes them different

- A different **operation**: averaging versus taking the minimum. Dropping rows
  versus imputing them.
- A different **value that changes the result**: a 0.25 cutpoint versus 0.5.
  `log(games)` versus `log(games + 1)` differ in how zeros are handled, which
  changes the fitted model, so they are different actions.

A difference that is real but inconsequential — naming the variable `skin_avg`
versus `avg_rating` — is **not** a different action.

## Also flag two other things

**parameter_only**: the group differs only in *which variable* the same
operation was applied to — testing position for confounding, then testing
league, then club. One action applied to several targets, recorded as several
options. Say so; do not merge them, just mark the group.

**misfiled**: an option that does not answer the question posed by this
decision point at all. It belongs to some other decision.

## Output contract

Return only this JSON. Every option id appears in exactly one group.

```
{
  "groups": [
    {"action": "average the two raters", "ids": [0, 3, 7],
     "parameter_only": false},
    {"action": "take the minimum of the two raters", "ids": [5],
     "parameter_only": false}
  ],
  "misfiled": [9],
  "note": "under 20 words on anything odd about this decision point"
}
```

Be strict about sameness and permissive about difference: if two options might
change what the analysis did, they are different actions. Wrongly calling two
distinct choices identical hides real variation, which is the error that
matters here.
