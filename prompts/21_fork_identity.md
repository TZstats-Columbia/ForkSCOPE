# Are these two decision points the same question?

Two decision points are given, each with the options recorded under it. They
were induced separately from a corpus of independent analyses. Decide whether
they are one decision point that the induction split in two.

## The test

They are the same decision point when a single analyst, writing a single
script, would answer **both at once with one act**. If answering one leaves the
other still open, they are different.

- *"what dataset/file is loaded?"* and *"what is the source/scope of the
  dataset?"* — same. Loading the file IS choosing the scope; nobody does one and
  then separately does the other.
- *"how is the exposure dichotomized?"* and *"at what cutpoint?"* — same. The
  cutpoint is not a second decision, it is the content of the first.
- *"which covariates enter the model?"* and *"how is games-played
  transformed?"* — different. Choosing the adjustment set leaves the functional
  form of each member still to decide.

## The strongest evidence is the options

If the two option lists contain the same operations in different words, they are
one question. If each list contains operations the other could not, they are
two.

Read the options before the labels. Question wording is the least reliable
signal here — the induction produced the wording, so two labels for one question
is exactly the error being looked for, and their difference is the artifact, not
the evidence.

## What is NOT sameness

- Both concerning the same variable. Dropping rows with missing skin tone and
  averaging the two skin-tone raters are both about skin tone and are two
  decisions.
- One being a special case of the other. A robustness refit at a different
  cutpoint is a different decision from the primary cutpoint, even though both
  are cutpoint choices.
- Belonging to the same DSLC stage. Most of this corpus is data cleaning.

## Output contract

Return only this JSON.

```
{
  "same": true,
  "confidence": "high",
  "why": "both record loading the raw dyad CSV unfiltered; option lists overlap",
  "merged_question": "what dataset is loaded as the analysis population?"
}
```

`confidence` is `high`, `medium` or `low`. `merged_question` only when
`same` is true; omit it otherwise. Keep `why` under 20 words.

When genuinely unsure, answer `false`. Splitting one question in two is visible
downstream and recoverable; merging two questions destroys a distinction the
corpus drew and cannot be undone.
