# Do these raw operations belong under one option?

You are given a decision point, one option recorded under it, and the **raw
operation text of every decision assigned to that option**. Those raw texts were
written independently while reading different analyses, and were grouped
together by an earlier clustering step.

Judge whether the grouping is right: does every raw operation record the same
choice?

## The standard

Two raw operations belong under one option when substituting one for the other
would not change what a reader thinks the analysis did.

- *"skin_avg = (rater1 + rater2)/2"* and *"take the mean of the two rater
  columns"* belong together. Different wording, one operation.
- *"drop rows where rater1 is missing"* and *"drop rows where either rater is
  missing"* do **not**: they select different rows, so they produce different
  analytic samples.
- *"dichotomize at 0.25"* and *"dichotomize at the median"* do **not**, even
  when the median happens to be near 0.25, because the rule differs.

## What to return

For each raw operation, either accept it into the option or reject it.

**reject** an operation that records a different choice from the option's
majority. Say which choice it actually records.

If the option is a coherent single choice, return an empty `rejects` list. That
is the expected outcome for a healthy grouping and you should not manufacture
rejections to appear thorough.

If the operations split into two or more roughly equal groups with no majority,
set `verdict` to `split` and describe each group. That is a different failure
from a few stragglers and is worth distinguishing.

## Output contract

Return only this JSON.

```
{
  "verdict": "coherent",
  "rejects": [],
  "groups": [],
  "note": "under 20 words"
}
```

or

```
{
  "verdict": "impure",
  "rejects": [{"id": 4, "records": "drops only rows missing BOTH raters"}],
  "groups": [],
  "note": "one straggler, rest are the same averaging step"
}
```

or

```
{
  "verdict": "split",
  "rejects": [],
  "groups": [{"choice": "average the two raters", "ids": [0,1,2]},
             {"choice": "use rater1 only", "ids": [3,4]}],
  "note": "two distinct choices of equal weight"
}
```

`verdict` is exactly one of `coherent`, `impure`, `split`.
