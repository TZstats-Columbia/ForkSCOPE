# Segment an analysis script into decisions and non-decisions

You are partitioning a script. You are **not** summarising it, and you are not
hunting for interesting parts. Every line gets assigned to exactly one span.

## The model

A **decision** is a fork where a competent analyst could have chosen otherwise:
a threshold, an exclusion, a transformation, a model family, an adjustment set,
a reporting choice. It is not a step-by-step narration of the code.

A decision behaves like a gene. Its functional segments are **exons**, and they
need not be contiguous — a threshold set at line 40 and applied at line 210 is
**one** decision with two exons. Everything that is not part of some decision is
**intron**, and intron must still be labelled with a type. Intron is a claim
about the code, not an absence of one.

## Hard requirements

1. **Exhaustive.** The union of all `lines` ranges across all spans must be
   exactly `1..n_lines`, with no gaps. Blank lines count and must be assigned —
   attach them to the adjacent span they belong with, or to an intron span.
2. **Exclusive.** No line may appear in two spans. If a single line genuinely
   serves two decisions, assign it to the more specific one and add the other
   decision's id to `shares_lines_with`.
3. **Describe only what is there.** Do not infer intent the code does not show.
   Do not quote code back — the span *is* the reference.

## When you are unsure

Prefer marking something a **decision with `confidence: "low"`** over marking it
intron. The errors are not symmetric: a decision you miss becomes silence that
nobody can audit, while a decision you assert wrongly is a claim a reader can
inspect and reject. Bias toward the disputable error.

## Vocabulary

Describe each decision's `operation` in **your own words**, as a short verb
phrase saying what it does to the data. Do **not** map it onto a fixed taxonomy
and do not try to use consistent phrasing across decisions — later stages
cluster these, and imposing a vocabulary now would destroy the signal they need.

`targets` lists the data entities the decision acts on, using the names as they
appear in the script (column names, variable names).

## Intron types

`import` · `config` (seeds, warning filters, display options, constants) ·
`glue` (control flow, function definitions with no analytic content, file
paths) · `print` (console output of results) · `plot` (figure construction) ·
`comment` (standalone comment or docstring blocks) · `dead` (commented-out or
unreachable code) · `other` (use `note` to say what it is)

Writing a *result* out to disk is `glue`. Reading the *input data* is a
decision, not intron — data source and scope is a fork.

## Output contract

Return only this JSON object. No prose, no code fences.

```
{
  "n_lines": <int, echo the input's n_lines>,
  "spans": [
    {
      "id": 1,
      "kind": "decision",
      "lines": [[38,38],[210,214]],
      "operation": "average the two rater columns into one skin-tone score",
      "targets": ["rater1","rater2"],
      "confidence": "high",
      "shares_lines_with": []
    },
    {
      "id": 2,
      "kind": "intron",
      "subtype": "import",
      "lines": [[1,12]],
      "note": ""
    }
  ]
}
```

`kind` is `"decision"` or `"intron"`. `confidence` is `"high"`, `"medium"` or
`"low"` and is required on decisions only. `subtype` is required on introns
only. `lines` is a list of `[start, end]` inclusive ranges, 1-indexed, sorted.
