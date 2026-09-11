# Segment an analysis write-up into claims and non-claims

You are partitioning a document. You are **not** summarising it. Every line
gets assigned to exactly one span.

## What counts as a claim

A **claim unit** asserts something about what the analysis *did* or *found*: an
operation performed on the data, a choice made, an alternative rejected, a
threshold used, a model fitted, a number obtained, a conclusion drawn.

Everything else is **non-claim**, and non-claim must still be typed. A non-claim
span is a statement about the document, not an absence of one.

## Hard requirements

1. **Exhaustive.** The union of all `lines` ranges must be exactly `1..n_lines`,
   no gaps. Blank lines and headings count and must be assigned.
2. **Exclusive.** No line in two spans.
3. **One assertion per claim.** A sentence making two separable assertions —
   *"we averaged the two raters and dropped unrated players"* — is two claims
   over the same line range; put the shared range in both and note the overlap
   in `shares_lines_with`. This is the one permitted exception to rule 2, and it
   exists because prose bundles decisions in a way code does not.
4. **Describe only what is asserted.** Do not resolve, correct or complete a
   claim using your own knowledge of how such analyses usually go.

## Claim polarity

Set `polarity` on every claim:

- `did` — asserts the analysis performed this
- `did_not` — asserts it deliberately did **not**, or rejected an alternative
  (*"we decided against a Poisson model"*, *"no cases were excluded"*)
- `would_have` — asserts a preference or intention not carried out
  (*"we would have preferred a mixed model but lacked the computing power"*)
- `found` — asserts a result or number rather than an action

`did_not` and `would_have` matter as much as `did`. A rejected alternative is a
resolved fork, and a stated preference that was not executed is a gap between
intent and delivery. Both are easy to read past; do not.

## When you are unsure

Prefer marking something a **claim with `confidence: "low"`** over marking it a
non-claim. A missed claim becomes silence nobody can audit; an over-eager claim
is a proposition a reader can inspect and reject.

## Vocabulary

Write each `assertion` in **your own words** as a short statement of what is
being claimed. Do not map onto a fixed taxonomy and do not try to phrase
similar claims consistently — later stages cluster these, and imposing a
vocabulary now destroys the signal they need.

`targets` lists the data entities the claim concerns, using the document's own
terms.

## Non-claim types

`heading` · `framing` (research question, motivation, restatement of the brief)
· `background` (prior literature, dataset provenance not tied to a choice) ·
`hedging` (caveats and limitations that assert no specific action) ·
`citation` · `boilerplate` (author lines, section scaffolding, tables of
contents) · `other` (use `note`)

A limitation that names a specific choice — *"we did not cluster standard
errors"* — is a **claim** with polarity `did_not`, not hedging.

## Output contract

Return only this JSON object. No prose, no code fences.

```
{
  "n_lines": <int, echo the input's n_lines>,
  "spans": [
    {
      "id": 1,
      "kind": "claim",
      "lines": [[42,43]],
      "assertion": "the two rater columns were averaged into one skin-tone score",
      "polarity": "did",
      "targets": ["rater1","rater2"],
      "confidence": "high",
      "shares_lines_with": []
    },
    {
      "id": 2,
      "kind": "nonclaim",
      "subtype": "heading",
      "lines": [[1,3]],
      "note": ""
    }
  ]
}
```

`kind` is `"claim"` or `"nonclaim"`. `polarity` and `confidence` are required on
claims only; `subtype` on non-claims only. `lines` is a list of `[start, end]`
inclusive ranges, 1-indexed, sorted.
