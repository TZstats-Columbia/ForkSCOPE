# Induce a typology from a sample of items

You are given a sample of items of one kind. Propose the **categories that are
actually present**, from the items themselves.

## Rules

1. **Read the sample before naming anything.** Do not start from a taxonomy you
   already know. If the sample contains three kinds of thing, propose three
   categories, not the eight a textbook would list.

2. **Name what distinguishes, not what is common.** Every item here shares the
   property that got it into the sample. A category earns its place by
   separating items that behave differently, not by restating the sample.

3. **Between 4 and 12 categories.** Fewer means you have merged distinct things;
   more means you are describing items rather than grouping them. If the honest
   answer is outside that range, say so in `note` and give your best grouping.

4. **Categories must be mutually exclusive.** An item belongs to exactly one. If
   two categories overlap, either merge them or sharpen the boundary and say in
   `criterion` what decides a borderline case.

5. **No residual category.** Do not propose "other" or "miscellaneous". If items
   do not fit, that means the typology is wrong; propose one that fits them.

6. **Consequence, not surface form.** Group by what the item *does* to the
   analysis — what a reader would need to know to judge it — rather than by
   which function or variable it mentions.

## Output contract

Return only this JSON object. No prose, no code fences.

```
{
  "categories": [
    {
      "id": "short_snake_case_id",
      "name": "a short human-readable name",
      "definition": "one sentence: what belongs here",
      "criterion": "what decides a borderline case, in one clause",
      "examples": [3, 17, 42]
    }
  ],
  "note": ""
}
```

`examples` are the integer `id` values of two or three sample items that are
clear members. `note` is for anything the contract above forced you to leave
out; leave it empty otherwise.
