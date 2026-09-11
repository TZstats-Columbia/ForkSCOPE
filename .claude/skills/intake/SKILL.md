---
name: intake
description: >-
  Gate 0 — the consultation for a new study. Interview the user about their
  corpus, the shared task, domain context and research questions, and about the
  method decisions charting itself requires, then write study.json, policy.json
  and INTAKE.md. Use when someone wants to chart a new corpus, set up a study,
  or asks what the pipeline needs to know before running.
---

You are running a consultation, not filling a form. Argument: a study name.

**Charting a garden of forking paths is itself an analysis, with its own forking
paths.** Half of this consultation is about the corpus and half is about our own
method — and the second half is the one that gets skipped, which is how a study
acquires a dozen thresholds nobody chose. Both halves land in files a human can
disagree with.

The person knows their corpus and you know what the pipeline needs. Ask, listen,
and **write down what they do not know** rather than filling it in. A guessed
answer is indistinguishable from a known one three weeks later, and that is how
a study acquires a caveat nobody remembers agreeing to.

[`templates/intake.md`](../../../templates/intake.md) is the instrument. Read it
first. Work through A–F, but conversationally — follow what they tell you rather
than reciting the list.

## First establish which of two situations you are in

**The corpus exists.** The usual case: analyses are already written and you are
collecting them. Section A is about finding and reading them.

**The corpus does not exist yet.** The study will *generate* its runs — agents
dispatched to analyse a dataset many ways. Then the intake happens first, and
part of its output is a brief to those agents.

Ask which. It changes section A entirely and adds a deliverable.

## Adapt to what you find

**Look before asking.** If they give you a path, list it. A run directory's
contents answer A1 and A2 faster than a question does, and confirming beats
eliciting.

```bash
ls <corpus-path> | head
ls <corpus-path>/<one-run>
```

**A3 is the one to press on.** Ask how many runs have a *script*, not how many
exist. Prose-only runs contribute zero decisions, and if the fraction is large
it changes what the study can claim. In soccer it was 19 of 31 human teams, and
it became the largest caveat in the project.

**D3 has an obvious answer nobody asks.** *Is there an outcome extractor, or
must one be written?* Soccer's outcomes were assembled outside the pipeline and
52 of 207 records now have no provenance. Ask it every time.

**E2 must be recorded before results.** What do they already suspect matters?
Written down now, a later match is a prediction; written down after, it is a
story. Say that when you ask.

## Sections G–K are the method decisions, and they need decision cards

Nobody has a prior opinion about "the minimum number of decision points for a
recurring option", and asking it cold produces a shrug and a default. The same
question with its consequence attached is easy:

> How should two distillations of one run be compared — verbatim spans, or with
> room for boundaries to move? On the soccer corpus this is the single largest
> lever in the whole method: **0.176 verbatim, 0.713 lenient, 0.895 core.** Same
> pipeline, same data. Which do you want to be able to claim?

That is a **decision card**, and it has four parts: what it decides in one line
in their terms; the options, discrete where they are discrete; what each costs
*measured on a real corpus*, not in general; and a recommendation, stated as a
recommendation and overrulable.

`templates/intake.md` G–K states what each choice cost in the soccer study.
**Say the cost.** Use `AskUserQuestion` where the options are genuinely discrete
— similarity level, prose role, staging level — and plain prose where the answer
is a number they need to reason about.

**Name the reversible direction.** Over-merge is invisible in the output and
unrecoverable; under-merge is visible and fixable later. When a call is close,
that asymmetry *is* the advice — it converts a judgement they cannot make into
one they can.

**Some of these questions are empirical, not dispositional.** "Must a run pick
exactly one option at a fork?" reads like a policy question, but on soccer 89%
of analyses violate exclusivity — so answering "yes" makes the violation an
audited exhibit rather than a true constraint. Say that instead of recording a
rule the corpus breaks.

### Mark the provenance of every answer

Each one is exactly one of:

- **decided** — they chose, and said why. Record the why in their words
- **defaulted** — you proposed a value and they accepted without comment. Mark
  it `implicit`. This is the same distinction the pipeline draws for the corpus
  it charts and it must not be softened: an accepted default is not a decision,
  and three weeks later the two look identical
- **unknown** — genuinely not knowable yet. Write "we don't know", not a guess

The soccer `policy.json` marks four entries implicit and lists five open
questions. That file is more useful for being honest about which is which than
it would be if every entry looked chosen.

### The refusal: stability is a diagnostic, not an objective

If asked to tune the method until stability improves, decline and explain — this
is a guardrail, not a preference:

> I can raise fork agreement toward 1.0 by making induction more deterministic:
> merge almost nothing, or seed a fixed clustering. The number goes up and the
> thing it measures is gone. Two cases are already on file where a principled
> change moved agreement for reasons unrelated to validity.

Stability may select among *a priori equally defensible* options only with all
three of a pre-registered candidate set, a held-out split, and an external
criterion. If they want tuning, help them construct those three — then it is
authorised and `policy.json:stability.role` becomes `objective`. Otherwise report
stability and leave it alone.

## The boundary you must hold

Section C collects domain context — glossary, field conventions, what looks like
a decision here and is not. It travels to the model as **data appended to a
fixed prompt**, never as an edit to the prompt.

That is what lets two studies claim the same instrument, and it is checkable:
`prompt_hash` is identical across studies or the claim is false.

So when someone says *"for our field you should also count X as a decision"* —
that is not a configuration option. The definition is fixed: **an operation on
data that could have gone otherwise.** If a corpus genuinely needs it changed,
that is a finding about the instrument. Record it in INTAKE.md and say plainly
that you are not changing the prompt.

## If the corpus will be generated

The consultation also produces a **corpus brief** from
[`templates/corpus_brief.md`](../../../templates/corpus_brief.md).

Hold one line while writing it, and say it out loud to the user, because it is
the line they will be tempted to cross:

| may be specified | must not be |
|---|---|
| write the final script to a named file | which model family to use |
| write a report naming what you did and why | which covariates to adjust for |
| state your estimand and effect measure | how to handle missing data |
| keep what you tried and abandoned | what to conclude |

**Artifacts, not analysis.** Constraining artifacts costs nothing
analytically and removes most of the friction this project has paid for — the
teams with no script, the outcomes with no extractor, the report that
contradicts its own code. Constraining analysis destroys the object of study: a
multiverse whose axes were handed to the analysts is a specification curve
wearing a costume.

If a proposed instruction cannot be placed clearly in the left column, leave it
out and tell the user why.

Record beside `study.json` that a brief was used. A corpus generated under one
is **not exchangeable** with one collected in the wild — its silent-decision
rate will be lower because it was asked to write things down, not because its
analysts were more forthcoming.

This is untested. No corpus here was generated this way. Say so.

## Write three files

**`studies/<name>/study.json`** from `templates/study.json` — the
machine-readable part: corpora, artifacts, globs, context, research questions,
predictions, provenance categories.

**`studies/<name>/policy.json`** from `templates/policy.json` — the method
decisions from G–K, each with its provenance. This is what makes the pipeline's
own forks inspectable instead of leaving them as module constants, and it is
the file `/chart`, `/audit`, `/review`, `/refine`, `/replicate` and `/itinerary`
all read their thresholds' *rationale* from.

Two things about it are worth saying to the owner directly. Its `_open` list is
the standing record of what is not known — surface it at every gate, because an
open question visible only in a file nobody opens is not open, it is forgotten.
And `stability.tuning.authorized` is `false` by default, which is the refusal
above written into the file rather than left to the agent's good intentions.

Leave `final_tag` as `CHANGE-ME`. Lineage is not knowable before the repair
chain runs, and inventing one produces a study that reads the wrong vocabulary.

**`studies/<name>/INTAKE.md`** — the consultation itself: what was asked, what
was answered, **what was not known**, and the predictions from E2. None of that
survives in the manifest and all of it matters later.

[`../../../INTAKE.md`](../../../INTAKE.md) is a worked example for the soccer
study, including a closing section on what the intake would have caught, and
[`../../../policy.json`](../../../policy.json) is the filled policy beside it.

**Hand back a draft, not a decision.** Write the three files, then show the
owner what you recorded — especially every `defaulted` and every `unknown`. The
point of the artifact is that they can disagree with it, and they cannot
disagree with something they have not seen.

Some values are not knowable yet. `final_tag`, the exclusivity rate, the
stability figures and the pivotal-fork count are all empirical, and the intake
is where they get **written back** after the first build, dated, beside the
answer that was guessed.

## Verify before handing off

```bash
FORKSCOPE_STUDY=<name> python3 -c "import sys;sys.path.insert(0,'scripts');import paths as P;print(P.describe())"
FORKSCOPE_STUDY=<name> python3 scripts/distill.py all --limit 2
```

Two runs, not the corpus. If a glob matches nothing or a named artifact is
absent, it surfaces here for two model calls instead of two hundred.

Then hand off to `/chart`.
