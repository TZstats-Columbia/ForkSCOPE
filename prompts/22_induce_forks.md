# Group options into decision points

Below are options — concrete choices recorded from analyses of one dataset.
Group them into **decision points**: the slots in an analysis where an analyst
must pick one alternative and, having picked it, cannot also take the others.

## The criterion is purpose, not action

Two options belong to the same decision point when they are **rival answers to
one question the analysis has to settle**. What makes them rivals is the job
they do, not what they look like.

This cuts against surface similarity in both directions, and both directions
matter:

**Different actions, same decision point.** *"drop dyads with no skin-tone
rating"* and *"impute the missing skin-tone rating from the other rater"* share
almost no words and do opposite things to the data. They are the same decision
point: both settle *what happens to records with no exposure measurement*, and
an analyst does one or the other.

**Same action, different decision points.** *"drop dyads with no skin-tone
rating"* and *"drop goalkeepers"* are both row removal, phrased almost
identically. They are different decision points: one settles missing-data
handling, the other settles who the study is about. An analyst does **both**,
in the same script, without any conflict.

Grouping by what the action looks like will put the second pair together and
split the first. Both are errors, and the second is the one that quietly
destroys the analysis, because it manufactures a decision point nobody faced.

## The test that decides it

> Could one competent analyst, in one script, do **both** of these?

- **Yes** → different decision points. Doing one leaves the other still open.
- **No — taking one means not taking the other** → same decision point.

Apply the test to the *primary* analysis. An analyst who dichotomises at 0.25
and then refits at 0.50 as a robustness check has not taken both options at one
decision point; the refit is its own decision about what to check.

## Sanity signal

Options at one decision point are alternatives, so they should rarely appear
together in the same run. You are given `runs` for each option and `co_runs`
for pairs that do co-occur. Heavy co-occurrence is evidence that two options
are **not** rivals and belong to different decision points — treat it as
contradicting a grouping you were otherwise inclined to make.

It is only a signal. Two genuinely rival options can co-occur when a run
records the same slot twice, and two unrelated options can fail to co-occur
because both are rare.

## Naming

Name each decision point as the **question it settles**, phrased so it would
make sense to an analyst who had never seen this dataset:

- good: *"how are records with a missing exposure measurement handled?"*
- bad: *"skin tone missingness"* — a topic, not a question
- bad: *"drop or impute"* — names two of the answers, not the question

## Output contract

Return only this JSON. Every option id appears in exactly one decision point.

```
{
  "decision_points": [
    {"question": "how are records with a missing exposure measurement handled?",
     "ids": [3, 8, 12],
     "why_rival": "each disposes of the same unmeasured records a different way"}
  ]
}
```

A decision point with one option is expected and fine — plenty of choices were
made by a single analyst. Do not pad groups to make them look substantial, and
do not merge two questions because each has few answers.
