# What does this decision rest on?

For each decision point below, say what an analyst is really trading off when
they answer it, and what they must be assuming for any answer to be defensible.

You are given the question only. Do not invent the specific options — describe
the *kind* of judgement the question demands.

## What to produce

**assumption** — the belief that has to hold for the choice to be defensible,
stated as a claim about the world or the data, not about the analyst. Good:
*"the two raters measure the same underlying construct"*. Bad: *"the analyst
assumes the raters agree"* — that restates the question with the word
"assumes" in front of it.

**tradeoff** — what is gained and what is given up. Good: *"gains contrast
between groups, loses external validity and sample"*. If a decision is purely
conventional and gives up nothing, say so.

**tags** — two to five short phrases naming the *kind* of consideration in
play. These are the units that will be clustered, so they matter most.

## Tags: describe the reasoning, not the subject matter

This is the whole point of the exercise and the easiest thing to get wrong.
Tags must name what makes the decision hard, not what the decision is about.

- Wrong: `skin tone`, `red cards`, `referees`, `covariates`. Those are the
  study's nouns. Every fork in this corpus concerns them, so tagging with them
  produces one cluster containing everything.
- Right: `measurement error`, `information loss from discretisation`,
  `confounding control`, `multiple comparisons`, `dependence between
  observations`, `post-hoc selection`, `external validity`, `statistical
  power`, `arbitrary threshold`, `convention over justification`.

Two decisions about completely different variables should share tags when they
are hard for the same reason. Dropping rows with missing exposure and dropping
rows with missing outcome are both `selection on availability` and both risk
`non-random missingness` — the variable involved is irrelevant.

Invent whatever tags the decision needs. Do not work from a fixed list, and do
not force a decision into a tag that nearly fits. Reuse the same wording when
the same consideration recurs, so the vocabulary stays comparable.

## Output contract

Return only this JSON. Every input id exactly once.

```
{
  "forks": [
    {"id": 0,
     "assumption": "the discarded middle category carries no information about the outcome",
     "tradeoff": "sharper group contrast, at the cost of sample size and generalisability",
     "tags": ["information loss from discretisation", "arbitrary threshold",
              "selection on availability"]}
  ]
}
```

Keep `assumption` and `tradeoff` under 20 words each. Tags are 1–4 words,
lower case.
