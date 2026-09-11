# Assign each fork to a DSLC stage

You are given decision points ("forks") induced from a corpus of independent
analyses. Assign each to the stage of the data-science lifecycle whose *job* it
belongs to.

## Stages

- `problem_formulation` — what is being estimated, on what population, framed
  how; the estimand, the posture, the causal claim being attempted
- `data_collection` — what data enters at all: sources, files, joins, scope
- `data_cleaning` — constructing and conditioning the variables and the rows:
  recoding, deriving, transforming, excluding, imputing
- `eda` — looking at the data before or beside the model: descriptives,
  distributions, reliability checks, balance, exploratory search
- `modeling` — fitting and estimating: model family, adjustment set, dependence
  structure, uncertainty quantification, sensitivity refits
- `communication` — what leaves the analysis: effect measures, verdict rules,
  figures, disclosure, reproducibility

## Assign by job, not by location

A fork's stage is the *kind of question it answers*, not where in a script it
happens to appear. Deciding the estimand is `problem_formulation` even when the
code that reveals it sits in the middle of the modelling section — this corpus
routinely writes framing decisions late. Do not use position; you are not given
it, deliberately.

## Borderline rules

- Constructing the exposure variable is `data_cleaning`. Choosing *whether the
  effect is linear in it* is `modeling`.
- Dropping rows for missingness is `data_cleaning`. Restricting the population
  to change what is being estimated is `problem_formulation`.
- Computing an unadjusted rate to look at it is `eda`. Reporting it as the
  answer is `communication`.
- A sensitivity refit is `modeling`. Deciding which refits to *show* is
  `communication`.

## Output contract

Return only this JSON. Every input id exactly once.

```
{
  "assignments": [
    {"id": 0, "stage": "data_cleaning", "confidence": "high"},
    {"id": 1, "stage": "modeling", "confidence": "medium"}
  ]
}
```

`confidence` is `high`, `medium` or `low`.
