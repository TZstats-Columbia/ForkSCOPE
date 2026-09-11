# Two forks that never co-occur — why?

Each pair below is two decision points ("forks") induced from a corpus of
independent analyses of the same dataset. In the data, **no run reaches both**.
Say why.

There are only four reasons this happens, and they mean completely different
things.

## `sibling` — the same question, split into two labels

The induction produced two paraphrases of one decision. Runs never appear in
both because each run's decision was filed under one label or the other, not
because analysts faced a branch.

Tells: the two labels ask the same thing in different words; the option lists
are interchangeable — you could move an option from A to B and nothing would
read as out of place.

> `how is the continuous skin-tone score turned into a binary exposure?`
> `how is the categorical skin-tone rating dichotomized into dark/light?`
> → sibling. One question, two names.

## `gate` — B exists only because of a choice at A

A genuine branch. Fork B is not a decision every analyst faces; it is created
by having chosen a particular option at A. An analyst who chose otherwise never
encounters B at all.

Tells: A is the more general question and B presupposes one of its answers;
B is unintelligible unless you already committed to something at A.

> `is the exposure modelled as continuous or dichotomized?`
> `at what cut-point is the exposure dichotomized?`
> → gate. The cut-point question only exists downstream of dichotomizing.

## `rival` — two incompatible ways of handling the same juncture

Both forks address the same point in the analysis, but they are alternative
framings that cannot both apply. Unlike siblings, the options are *not*
interchangeable — they belong to different approaches.

> `how are repeated observations per player handled by clustering?`
> `how are repeated observations per player handled by aggregation?`
> → rival. Same problem, two mutually exclusive strategies.

## `unrelated` — coincidence

The two never co-occur for no structural reason: both are uncommon, and no run
happened to do both. Vocabulary overlap is superficial.

## The distinction that matters most

`sibling` versus `gate` is the one to get right, and the test is whether an
analyst could have faced **both** decisions.

- Could a single competent analyst have made decision A *and then also*
  decision B, in one analysis? If yes it is a `gate` (or `unrelated`) — the
  reason no one did both is structural or accidental, not definitional.
- If the two questions are answered by the same act — deciding one *is*
  deciding the other — it is a `sibling`.

When genuinely torn between `sibling` and `gate`, answer `gate`. Wrongly
calling a real branch a sibling erases structure and cannot be recovered later;
wrongly calling a duplicate a gate leaves a visible, checkable edge.

## Output contract

Return only this JSON. Every input id exactly once. Keep `why` under 20 words.

```
{
  "verdicts": [
    {"id": 0, "relation": "sibling", "why": "same dichotomization question, two labels"},
    {"id": 1, "relation": "gate", "why": "cut-point presupposes the decision to dichotomize"}
  ]
}
```

`relation` is exactly one of `sibling`, `gate`, `rival`, `unrelated`.
