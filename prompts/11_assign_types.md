# Assign items to an induced typology

You are given a typology and a batch of items. Put each item in exactly one
category.

## Rules

1. **Use the definitions, not the names.** A category name is a handle; the
   `definition` and `criterion` decide membership.

2. **`NEW` is available and you should use it when it is right.** If an item
   genuinely does not fit any category, assign `NEW` and write a one-line
   `proposed` category for it. The typology was induced from a sample and is
   expected to be incomplete. Forcing a bad fit destroys the measurement; a
   `NEW` is cheap and gets consolidated later.

3. **Do not use `NEW` to avoid a judgement call.** If an item sits between two
   categories, apply the `criterion`, pick one, and set `confidence` to `low`.
   `NEW` means *no category describes this*, not *two do*.

4. **One item, one category.** No multi-labelling.

5. **Judge the item, not its wording.** Two items describing the same thing in
   different words belong in the same category.

## Output contract

Return only this JSON object, with one entry per input item and no others. No
prose, no code fences.

```
{
  "assignments": [
    {"id": 7, "category": "silent_inference_machinery", "confidence": "high"},
    {"id": 8, "category": "NEW", "confidence": "high",
     "proposed": "undisclosed reweighting of the analysis sample"}
  ]
}
```

`confidence` is `high`, `medium` or `low`. `proposed` is required when and only
when `category` is `NEW`.
