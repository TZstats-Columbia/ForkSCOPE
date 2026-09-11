# Consolidate rationale tags into families

Below is the full list of tags produced while characterising decision points,
with how many decisions each was applied to. They were written freely, one
decision at a time, so the same consideration appears under several wordings.

Group them into **families**, where a family is one consideration under all the
names it was given.

## What belongs together

`measurement error`, `measurement reliability`, `rater disagreement` and
`construct validity` are one family: all concern whether the variable measures
what it claims to.

`arbitrary threshold`, `cutpoint choice` and `discretisation` are one family:
all concern imposing a boundary on a continuum.

## What does not

Do **not** merge on shared words. `sample size` (statistical power) and
`sample restriction` (who is in the population) share a word and are different
considerations — one is about precision, the other about the estimand.

Do **not** merge two considerations because they often co-occur. Confounding
control and functional form appear together constantly and are distinct: one is
about which variables enter, the other about how they enter.

When two tags are close but not the same, keep them apart. These families
become the coordinates decisions are clustered on, so an over-merge collapses a
distinction the corpus actually drew, and cannot be recovered downstream. An
under-merge leaves two similar coordinates, which is visible and harmless.

## Naming

Name each family with the clearest of its member tags, or a better phrase if
none is clear. 1–4 words, lower case.

## Output contract

Return only this JSON. Every input tag appears in exactly one family.

```
{
  "families": [
    {"name": "measurement error",
     "members": ["measurement error", "rater disagreement", "construct validity"]},
    {"name": "arbitrary threshold",
     "members": ["arbitrary threshold", "cutpoint choice"]}
  ]
}
```

A tag that belongs with nothing else is a family of one. That is expected and
correct — do not pad families to make them look substantial.
