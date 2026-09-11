# Link executed operations to stated claims

You are given the **decisions** extracted from one run's code and the **claims**
extracted from the same run's write-up. Decide which describe the same thing,
and whether they agree.

You are **not** classifying anything. The presence categories — silent
decision, unbacked claim, and the rest — are computed downstream from the links
you return and the ones you leave out. Your only job is alignment and
agreement, and the residue on either side is the finding.

## What counts as a link

A decision and a claim link when they concern **the same operation on the same
data** — regardless of wording. *"average the two rater columns"* and *"an
average skin-tone rating was computed from the two coders"* are one link.

They do **not** link merely because they share a topic. *"dichotomize skin tone
at 0.5"* and *"skin tone was measured by two raters"* both concern skin tone and
are different operations. Topic overlap is not alignment.

A decision may link to several claims and a claim to several decisions. Say so
by emitting several links.

## Agreement

For each link set `agreement`:

- `aligned` — the claim describes what the code does
- `misaligned` — they describe the same operation and **disagree on a
  material particular**: a different threshold, a different variable set, a
  different direction, a different estimator, a different sample

Misalignment is not a wording difference. *"we controlled for exposure"* against
code adjusting for `games` is **aligned**. *"cards divided by games"* against
code computing `cards / (games + 1)` is **misaligned**, because the operation
differs in a way that changes the number.

When you mark `misaligned`, `note` must state the specific discrepancy in one
sentence. If you cannot name a specific discrepancy, it is not misaligned.

## Deliberate negatives

A claim with polarity `did_not` or `would_have` describes something the code
should **not** contain. Apply one test: **does the code do the thing the claim
denies?**

- **No — the code does not do it.** The claim is *correct*. Emit **no link**,
  whatever else is nearby. A decision that merely concerns the same topic is not
  a counterexample: a claim that standard errors were not clustered on referee
  is satisfied by code that clusters on *player*, or by code that clusters on
  nothing at all. Topic overlap with a negative claim is the single most common
  way to record a discrepancy that does not exist.
- **Yes — the code does it.** Emit the link with `agreement: "misaligned"`. The
  write-up says it did not cluster and the code clusters. This is the most
  consequential discrepancy there is; do not skip it because the polarity is
  negative.

Before marking a negative claim misaligned, name in `note` the specific line or
operation that performs the denied action. If you cannot name one, the claim is
consistent and there is no link.

## Never contradict yourself

`agreement: "misaligned"` and a `note` saying the two agree cannot both be
right. If your reasoning arrives at *consistent*, *aligned*, *matches*, *the
same*, or *no material difference*, the verdict is `aligned` — or there is no
link at all. A note that concedes agreement while the verdict claims
disagreement will be rejected.

## Do not force coverage

Leaving a decision or a claim unlinked is a legitimate and expected outcome. Do
not invent a weak link to reduce the residue. A forced link destroys the
measurement this whole step exists to produce.

## Output contract

Return only this JSON object. No prose, no code fences.

```
{
  "links": [
    {
      "decision_id": 3,
      "claim_id": 12,
      "agreement": "aligned",
      "confidence": "high",
      "note": ""
    },
    {
      "decision_id": 7,
      "claim_id": 20,
      "agreement": "misaligned",
      "confidence": "high",
      "note": "claim states cards divided by games; code divides by games + 1"
    }
  ]
}
```

`agreement` is `"aligned"` or `"misaligned"`. `confidence` is `"high"`,
`"medium"` or `"low"`. `note` is required when `misaligned`, optional otherwise.
