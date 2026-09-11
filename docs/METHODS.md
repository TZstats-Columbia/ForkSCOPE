# Methods — how a script becomes a decision map

Four questions decide whether any of the downstream numbers mean anything:
what counts as a decision, how decisions become options, how options become
decision points, and how decision points get a lifecycle stage. Each is
answered by a named script and a versioned prompt.

---

## 1. What counts as a decision

**A decision is an operation on data that could have gone otherwise.** Not a
step in the code — a fork where a competent analyst could have chosen
differently.

The useful analogy is genetic: a decision is a **gene** whose **exons** are the
lines implementing it, which need not be contiguous — a variable created on
line 30 and used on line 140 is one decision. Everything else is an **intron**
and must still be *typed*: configuration, glue, printing, a comment. Typed, not
discarded, because "this line does nothing analytically interesting" is a claim
that should be inspectable.

`prompts/01_segment_code.md` partitions a script **exhaustively and
exclusively**: every line lands somewhere, no line lands twice.
`prompts/02_segment_prose.md` partitions the write-up into claims and typed
non-claims — exhaustive but **not** exclusive, because one sentence can assert
two things and code cannot.

Coverage is enforced as a **retryable invariant**: a response that fails to
partition is rejected with a specific complaint and re-asked. It is the basis of
every downstream claim, so it is a precondition rather than a diagnostic.

## 2. Linking, and the residue that is the finding

`prompts/03_link.md` aligns code decisions to prose claims within a run. What
fails to align is the point:

- **silent decision** — an operation the code performs that no claim mentions
- **misalignment** — a code decision and a claim that describe the same
  operation differently

Both are recovered from the residue of an alignment rather than searched for
directly, which is why they can be counted rather than illustrated.

## 3. Decisions → options: same action, different words

An **option** is one concrete choice. Two decisions belong to the same option
when substituting one description for the other would not change what a reader
thinks the analysis did.

Bottom-up, in three layers (`cluster_up.py`): local grouping, then label
merging, then question merging. **No embeddings and no cap.** 95% of option
labels in this corpus are unique, so no vector or string metric separates them;
an earlier top-down attempt that sampled a fraction of items and capped
categories was discarded as the fixed-schema move this project exists to avoid.

Two refinements, each added after an audit found it necessary:

- **`prompts/19_option_granularity.md`** (`merge_options.py`) collapses
  paraphrase *within* a decision point. Given one decision point and the twenty
  options recorded under it, "which of these are the same action?" is a far
  better-posed question than comparing items across the whole corpus, and it
  finds what the corpus-wide passes cannot.
- **Numeric and set normalisation** (`repair_clusters.py`): `>0` and `>=1` are
  the same rule on integers; `{0.25}` and `{0.25, 0.75}` are one two-sided rule,
  not three. Splitting on these fabricates singletons.

Repair passes **split only, never merge**. The two errors are not symmetric:
over-merge is invisible in the output and unrecoverable, under-merge is visible
and fixable later.

## 4. Options → decision points: same purpose, not same action

A **decision point** is a slot where an analyst must pick one alternative and,
having picked it, cannot take the others. What makes options rivals is the
**job they do**, not what they look like — and this cuts against surface
similarity in *both* directions:

| | |
|---|---|
| *drop rows with no rating* / *impute from the other rater* | **one** decision point — no shared words, opposite operations, same slot |
| *drop rows with no rating* / *drop goalkeepers* | **two** — near-identical phrasing, same operation, different slots |

Any lexical or embedding method gets both backwards. The second is the damaging
one: it manufactures a decision point nobody faced.

`prompts/22_induce_forks.md` (`induce_forks.py`) groups by purpose, with
**foreclosure** as the operational test:

> Could one competent analyst, in one script, do **both**?
> Yes → different decision points. Taking one rules out the other → same.

with an explicit carve-out for robustness refits, since "dichotomise at 0.25
then refit at 0.50" is not one analyst taking two options at one slot.

### The structural veto

Options at one decision point are alternatives, so they should rarely appear
together in one run. Measured on this corpus: same-decision-point option pairs
almost never co-occur; different-decision-point pairs frequently do.

That is a **cannot-link constraint**, and it is used three ways: to score which
decision-point pairs are worth adjudicating, as evidence given to the
adjudicator, and as a test of the result: options that co-occur in ≥2 runs
are split apart by graph colouring — no model calls.

It is nearly necessary and far from sufficient, so semantics proposes and
co-occurrence vetoes, never the reverse.

### Transitivity is earned

`merge_forks.py` grows merge groups edge by edge with two brakes: an explicit
veto where a pair was adjudicated *different*, and a **density floor** requiring
a decision point to be judged the same as 60% of a group before joining it.

The veto alone is insufficient. Only a small fraction of all pairs are ever
adjudicated, so most pairs inside a growing component were never looked at and
no veto can fire — pure transitive closure then chains through pairs nobody
judged.

## 5. Decision points → DSLC stage

`prompts/14_fork_stage.md` assigns one of six stages — problem formulation,
data collection, data cleaning, EDA, modelling, communication — by **the job the
question does, not where it appears**.

The prompt is given the decision-point label and **nothing else**: no line
number, no position, no neighbours. That is deliberate, because the iteration
analysis compares stage against position, and a stage inferred *from* position
would make it circular.

The blind assignment reproduces the pipeline order anyway (Spearman ≈ +0.59
against observed position), which is what licenses reading a deviation as a
deviation rather than as labelling error.

## 6. Reproducibility

The model is reached through the `claude` CLI, which exposes **no temperature
and no seed**. Determinism therefore cannot come from decoding parameters, and
comes instead from a content-addressed cache keyed on
`sha256(prompt + model + payload + schema)`.

`llm.py` is the only module that talks to a model. It separates two failure
kinds that need opposite responses: **transport** failures (rate limits — retry
with backoff, prompt unchanged) and **content** failures (retry with the
specific complaint appended, so the retry is informed rather than a coin flip).
Conflating them once cost 154 of 204 runs in a single burst.

Semantic invariants that a JSON schema cannot express — "these line ranges must
partition 1..n" — are enforced in the same retry path rather than checked
afterwards.

Sampling and bootstraps are seeded. Permutation tests escalate their draw count
for anything surviving a screen, because a permutation *p* cannot fall below
1/(B+1) and a multiplicity-corrected threshold often sits below the floor of a
cheap screen.

## 7. What is never used as input

Both source corpora ship with the original authors' own derived analyses.
Neither is read. `decisions_mapped.json` is the AWS team's extraction against a
fixed 21-slot schema; using it would import the taxonomy this project exists to
avoid. It is worth reading as a comparison — 33% of what it found landed in
`unmapped_decisions`, which is a ready-made inventory of what a fixed schema
cannot hold.
