# Do these two lists record the same silent decisions?

Two independent extractions of the **same analysis script** are given. Each
lists the operations that extraction judged the script to perform without the
write-up ever mentioning them — its *silent decisions*.

Because both lists describe one script, an operation in list 1 either has a
counterpart in list 2 or it does not. Align them.

## The test

Two entries are the same silent decision when they name **the same operation on
the same data**, whatever words each extraction chose and whatever line range it
recorded.

- *"average rater1 and rater2 into a single skinTone score"* and *"combine the
  two raters into one continuous skin-tone value"* — **same**. One operation,
  two phrasings.
- *"drop dyads with missing skin tone"* and *"restrict to complete cases on the
  exposure"* — **same**. The second describes the first in the vocabulary of
  sampling rather than of deletion.
- *"drop dyads with missing skin tone"* and *"drop goalkeepers"* — **different**.
  Near-identical phrasing, same verb, different operation.
- *"choose which columns enter the analytic frame"* and *"load the raw dyad
  CSV"* — **different**. Both concern getting data in; one is selection, the
  other is reading.

## Boundaries are not evidence

The line ranges are reported because they are available, not because they
decide anything. Two extractions routinely draw slightly different boundaries
around one operation — a trailing print included or not — so a difference of a
few lines is expected and means nothing. Overlapping lines are weak evidence
*for* sameness; non-overlapping lines are **not** evidence against it, because
an operation implemented in two places can be recorded at either.

Read the operations. Use the lines only to break a tie between two otherwise
equally good candidates.

## What is NOT sameness

- Both being data cleaning, or both concerning the same variable. Most of this
  corpus is data cleaning and most of it concerns skin tone.
- One being a broader statement that would *include* the other. "Choose the
  analytic sample" is not the same decision as "drop goalkeepers", even though
  performing the second is one way of doing the first. Match specific to
  specific.
- Similar confidence labels. Confidence records how sure the extraction was,
  not what it found.

## Output contract

Return only this JSON.

```
{
  "pairs": [
    {"id_1": 6, "id_2": 22, "same": true,
     "why": "both average the two raters into one skin-tone score"}
  ],
  "unmatched_1": [9],
  "unmatched_2": [14, 31]
}
```

Every id from both lists must appear **exactly once**, either in a pair or in
the matching `unmatched` list. A pair asserts the two entries are the same
operation; do not emit a pair with `same` false — put both ids in `unmatched`
instead. Keep `why` under 20 words.

When genuinely unsure, leave both entries unmatched. A missed match understates
agreement and is visible in the result; a false match manufactures agreement
that was never there and cannot be detected downstream.
