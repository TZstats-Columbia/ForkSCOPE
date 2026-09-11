---
name: intake
description: Run the charting consultation with a human — elicit the study and method decisions, then write INTAKE.md, study.json and policy.json for their review.
---

# The charting consultation

Charting a garden of forking paths is itself an analysis, with its own forking
paths. Every question below is a point where a competent analyst could choose
otherwise, and the pipeline cannot choose for them. This skill runs that
consultation and produces three artifacts for a human to review and correct.

**You are eliciting decisions, not administering a form.** Most people have no
prior opinion about "the minimum number of decision points for a recurring
option" — and should not be asked to invent one cold. They acquire an opinion
when shown what the choice costs. Lead with the consequence.

## What you produce

| file | holds | when knowable |
|---|---|---|
| `INTAKE.md` | the consultation record, in the human's own words | during the session |
| `study.json` | corpus facts and domain context | during the session |
| `policy.json` | the method decisions of `templates/policy.json` | during the session |

`final_tag` in `study.json` stays `CHANGE-ME`. The lineage is not knowable
before the repair chain runs, and writing a plausible one is worse than leaving
it obviously unset.

**Never write policy into prompt text.** Policy reaches the model as data
appended to a fixed prompt, exactly as `study.json:context` already does. If
intake answers edited prompts, `prompt_hash` would differ between studies and
the shared-instrument claim would be false rather than merely unchecked.

## How to run it

Work from `templates/intake.md`, in order. It is the instrument;
this file is how to hold it.

**1 · Read the corpus first, then ask.**
Before section A, look at the actual directories. Count the runs. Open one and
find the code and the prose. Check how many deposited a script — in the soccer
study 12 of 31 human teams had none, which became the largest caveat in the
work and was not known up front. Arriving with "I see 204 runs under five
workspace names, and 19 of 31 teams have a script — is that right?" is worth
more than four questions.

**2 · Ask one section at a time, and carry the consequence.**
For every method question in G–K the template states what the choice cost in
the soccer study. Say it. The useful form is:

> How should two distillations of one run be compared — verbatim spans, or with
> room for boundaries to move? In the soccer corpus this is the single largest
> lever in the whole method: 0.176 verbatim, 0.713 lenient, 0.895 core. Same
> pipeline, same data. Which do you want to be able to claim?

Use `AskUserQuestion` where the options are genuinely discrete — similarity
level, prose role, staging level. Use plain prose where the answer is a number
they need to reason about.

**3 · Record provenance on every answer.** Each one is exactly one of:

- **decided** — the human chose, and said why
- **defaulted** — you proposed the soccer value and they accepted without
  comment. Mark it `implicit: true`. This is the same distinction the pipeline
  draws for the corpus it charts, and it must not be softened: an accepted
  default is not a decision, and three weeks later it looks identical to one.
- **unknown** — genuinely not knowable yet. Write "we don't know", not a guess.

**4 · Say when a question is already answered by evidence.**
Some intake questions are empirical, not dispositional, and the human should
not be asked to have a preference. "Must a run pick exactly one option at a
fork?" is a policy question — but 86% of soccer runs violate exclusivity, so
answering "yes" makes the violation an audited finding rather than a true
constraint. Say that plainly rather than recording a rule the corpus breaks.

**5 · Refuse to make stability an objective, unless J2 is fully satisfied.**
When asked to tune the method until stability improves, decline and explain —
this is a guardrail, not a preference:

> I can raise fork agreement toward 1.0 by making induction more deterministic:
> merge almost nothing, or seed a fixed clustering. The number goes up and the
> thing it measures is gone. Two cases are already on file — core-first fork
> formation was principled and made agreement worse, and the option-split
> repair raises agreement partly because one deterministic transform is applied
> to both builds.

Stability may select among *a priori equally defensible* options only with all
three of a pre-registered candidate set, a held-out split, and an external
criterion. If the human wants tuning, help them construct those three; then it
is authorised and `policy.json:stability.role` becomes `objective`. Otherwise
report stability and leave it alone.

**6 · Hand back a draft, not a decision.**
Write the three files, then show the human what you recorded — especially every
`defaulted` and `unknown`. The purpose of the artifact is that they can
disagree with it.

## After the session

```bash
python3 scripts/paths.py                 # confirm the study resolves
python3 scripts/build_all.py --corpus <c> --repair
python3 scripts/audit_vocab.py --corpus <tag>
python3 scripts/build_figures.py
```

Then return to the intake. `final_tag`, the exclusivity rate, the stability
figures and the pivotal-fork count are all empirical, and the intake is where
they are written back — with the date, beside the answer that was guessed.

## What you may not configure away

The definition of a decision is fixed: **an operation on data that could have
gone otherwise.** A study that needs it changed is a finding about the
instrument, to be reported, not a parameter to set.

Likewise `scripts/` and `prompts/` are the instrument and are never per-study.
The claim a second study supports is precisely that the instrument was
unchanged; a per-study copy forfeits it.
