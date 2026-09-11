# The agentic design — double accountability

This repository is two things: a decision map of 223 analyses, and the system
that produced it. The second is the part meant to generalise, and it is
governed by one principle.

## The principle

> **A consultation system is accountable in two directions at once: to the
> source material it represents, and to the person it is meant to support.**
>
> It must be rigorous about what the sources actually contain, and it must
> produce evidence the person can verify for themselves. Neither obligation
> discharges the other, and trust is earned by meeting both.

*Double accountability* is developed as a general model for AI consultation
architectures in a companion paper on method transfer, where the two directions
are an owner-authorized representation of a maintained method and an
adopter-governed research problem. What follows is what the principle requires
of a system whose source material is a corpus of analyses.

The two failure modes are distinct, and both are easy to reach.

**Accountable only to the source** produces a system that is rigorous and
useless. It reports correct things in a form nobody can act on: verdicts
without exhibits, statistics without the items behind them, a map whose
fidelity has to be taken on faith.

**Accountable only to the user** produces a system that is agreeable and
unmoored. It answers the question asked, smooths over what it could not
establish, and tells a person what their corpus probably contains rather than
what it does.

| direction | obligation | mechanisms here |
|---|---|---|
| **to the source** | the map is of the corpus, not of the model's priors | vocabulary induced, never matched to a schema · the chain from fork to source lines · provenance on every run · the instrument shared unchanged across studies · derived artifacts of the source refused as input |
| **to the user** | every claim ships what would falsify it | worst-first exhibits · a `REVIEW` that cannot be filed without showing what failed · handles that resolve · the review round as an asynchronous gate · retraction in place |

### The source here cannot correct us

One asymmetry is worth stating, because it makes this the harder case rather
than the easier one. In method transfer there is an owner who authorizes a
representation and can say *that is not my method*. Here the sources are 223
analyses whose authors are not in the room, did not consent to being distilled,
and cannot object.

There is no one to appeal to, so fidelity cannot be certified — it can only be
made **checkable**. That is why `trace.py` exists, why every exhibit carries a
handle, and why the raw corpora are referenced rather than paraphrased: a
reader who doubts the map can walk any claim back to the lines it came from and
judge for themselves. Traceability is what substitutes for an owner's
authorization.

### Human gates, and why they are asynchronous

The review round is a file, not a conversation, and that follows from the
second obligation rather than from convenience. A judgement given in chat is
applied once and lost; nobody can later say who decided that two forks were one
question, or why. Writing the questions down — each with its evidence and what
a given answer would change — lets the person answer on their own time, at
their own depth, and lets a third party see what was asked before seeing what
changed.

[`LIFECYCLE.md`](LIFECYCLE.md) places those gates: humans act in five of the
nine phases, and the AI does not proceed past a gate on its own reading of the
evidence.

## What the principle implies: frozen and live

The frozen/live split is a consequence rather than a separate idea.
Accountability to the source requires that a claim mean the same thing when
re-checked, so the judgements that *build* the vocabulary must be frozen.
Accountability to the user requires that a check be a real test rather than a
replay, so the judgements that *check* it must stay live.

> **Judgements that build the vocabulary are frozen. Judgements that check it
> stay live.**

Get that line wrong in either direction and the system fails, in opposite ways.
Freeze too much and you have a fixed codebook that cannot hold what it did not
anticipate. Freeze too little — let an agent decide afresh each run how options
cluster — and you get a defensible vocabulary that is **different every time**,
which is worse than a wrong one because nothing can falsify it.

| | frozen | live |
|---|---|---|
| **what** | `scripts/` + pinned `prompts/` + `cache/` | `.claude/agents/` |
| **calls** | 2,273, one per item | a handful per session |
| **must** | return the same answer on every re-run | reason fresh, or it is not a check |
| **e.g.** | is option A the same action as option B | is this reported finding supported |

The cache is what makes the frozen half frozen. The CLI exposes no temperature
and no seed, so determinism cannot come from decoding parameters; it comes from
`sha256(prompt + model + payload + schema)` on disk. Editing a prompt orphans
every answer the old wording produced — which is why `prompts/` is versioned
beside the cache and `prune_cache.py` reports what a re-run can still reach.

The phases those two halves alternate
through — who acts, what each leaves
behind, and what must hold before the next — are in
[`LIFECYCLE.md`](LIFECYCLE.md). Humans are in five of the nine.

## Three tiers, and the order is load-bearing

```
CHART   frozen        scripts + pinned prompts + cache      the garden
CHECK   adversarial   verdicts + falsification exhibits     grounds for belief
USE     live          human and agents explore and walk     what it is for
```

Tier 3 is only honest because tier 2 emits exhibits. Tier 2 means something
only because tier 1 is frozen — a check against a vocabulary that changes every
run tests nothing.

## Tier 0 — consult

Before a corpus can be charted, someone has to say what it is. `/intake` runs
that as a consultation and writes two files: `study.json`, the machine-readable
manifest, and `INTAKE.md`, the record of what was asked — including **what was
not known at the time** and what the user predicted would matter.

The prediction matters more than it looks. Recorded before results, a later
match is a prediction; recorded after, it is a story.

**Domain context is data, not instruction.** A study supplies a glossary, its
field's conventions, and what looks like a decision there and is not. All of it
is appended to a fixed prompt as JSON — `llm.py` renders template + payload and
never rewrites the template. So two studies can claim the same instrument, and
the claim is checkable: `prompt_hash` is identical across them or it is false.

What a study may **not** do is change what counts as a decision. That
definition is fixed. A corpus that needs it changed is a finding about the
instrument, to be reported rather than configured away.

## Tier 1 — chart

`/chart` runs the pipeline. It orchestrates scripts; it does not adjudicate.

The instrument is shared across studies and must not be modified per corpus.
`scripts/paths.py` splits `CODE_ROOT` from `STUDY_ROOT` for exactly this
reason: a second case study is worth running only if the instrument was
unchanged, and a per-study copy of the pipeline would forfeit that. If a corpus
seems to need a new prompt, that is a finding about the instrument, not a
configuration step.

## Tier 2 — check

`/audit` runs the check sets. The `auditor` agent verifies one finding
adversarially, and several can run in parallel on the same claim.

**The evidence contract.** Every check emits four things, not one: a verdict,
the measurement and the null it faced, the **exhibits** — the actual items —
and handles that walk each item back to source. Two rules are enforced in
`exhibit.py` rather than left to discipline:

- `exhibit()` requires a `worst` key function and sorts by it, so a
  representative sample cannot be attached.
- A `REVIEW` with no exhibits raises.

This exists because a statistic once reported that 2.7% of within-fork option
pairs were near-duplicates, offered as reassurance. It failed **both**
accountabilities at once, which is what makes it the useful example.

*Unaccountable to the source:* token overlap cannot see that *"compute the mean
of the two rater columns"* and *"average the two raters' scores"* are one
action. The measure was structurally blind to the failure it was being used to
rule out, so it was never evidence about the corpus.

*Unaccountable to the user:* it shipped a number and not the items. A reader
had no way to check it without redoing the work, and the one thing that would
have exposed it — the two option lists side by side — was exactly what the
summary replaced.

A person reading those lists found it in minutes. **The summary hid the error;
the artifact showing raw items revealed it.**

So: a weak signal is a legitimate sort key for human attention and never
evidence of absence.

**The contract does not cover every way a check fails.** Worst-first exhibits
catch a *blind* measure; they do nothing about an *entangled* one, where the
items are real, the ordering honest, and the check is still partly restating a
decision the pipeline already made. That failure cost a wrong reading of the
repair chain before it was named. Two further refusals now exist — no `PASS`
without a declared blind spot, no `PASS` while entangled — and the eight
questions behind them are in [`AUDITING.md`](AUDITING.md).

**Independence, kept from the earlier pilot.** Verifiers get byte-identical
prompts, may not read each other's output, and do not write their own verdict
files. Agreement that was coordinated measures nothing. The `auditor` agent
defaults to `refuted: true` when it cannot establish a claim — a finding that
survives a skeptical reading is worth reporting; one that survives a charitable
reading is worth nothing.

## Tier 3 — use

| | |
|---|---|
| `/distill` | stage S — segment the artifacts into typed spans, align prose to code |
| `/replicate` | build isolated replicates of one layer and report its variance |
| `/settle` | close a checkpoint — evidence, a human decision, and a lock |
| `/report` | re-derive every number in `report/REPORT.md` and rewrite the prose over it |
| `/review` | put the open questions to a human, record the answers |
| `/refine` | apply those answers, re-run what they touched |
| `/walk` | exploratory examination of the finished map |
| `/investigate` | walk one claim to its source lines |
| `/inspect` | examine a new run before it is filed |
| `/challenge` | escalate a test, enlarge a sample, re-adjudicate |
| `/itinerary` | specify a path, check it, run it, add it to the garden |
| `interpreter` | verdicts and numbers into prose that states what failed |

`/challenge` matters more than it looks. Its levers are real — permutation
draw counts, `--sample`, and `nocache=True`. That last one measures whether an
adjudication pass agrees with itself, which **has never been run** and which
is the largest outstanding methodological gap. A
challenge that exercises it closes that gap as a side effect.

### The review round-trip

`/review` and `/refine` are separate on purpose, and the artifact between them
is the point. `scripts/review_round.py` writes `reviews/round-NN.md`: the
questions the pipeline cannot settle, each with its evidence and each stating
**what a given answer would change**. The human answers in the file; `read`
parses the answers back.

An answer given in conversation is applied once and lost. Nobody can later say
who decided that two forks were one question, or why — so it is asked again,
and may be answered differently. A round makes the judgement citable, and
separating asking from applying lets a reader see what was decided before
seeing what changed.

### Provenance — a stratifier, not a filter

`/itinerary` adds runs. Every run therefore carries one of three tags:

| | |
|---|---|
| `corpus` | extracted from an analysis a real analyst wrote |
| `itinerary` | assembled entirely from options the corpus contains |
| `authored` | contains an operation no run in the corpus performed |

**Every run counts, and provenance stratifies rather than filters** — the way
`arm` does. An itinerary run is a human's deliberate choice, executed, which is
exactly what a corpus run is; excluding it would treat a person's choice as
less real than an analyst's and would stop the garden growing.

What the tag buys is the ability to tell. `stability.py` reports its
concentration statistics with and without non-corpus runs as soon as one
exists, so a headline that moves is visible. The hazard was never that
assembled runs count — it is a statistic that drifts silently as paths are
walked.

`authored` is the tag to watch, not to exclude: it marks a run containing an
operation no analyst performed, so a reader can ask whether a result depends on
it.

The same three-way split answers *can a user propose an option nobody took?*
A new **parameter** on an attested action is free — the template is already
parameterized. **Recombining** attested actions is buildable but needs the
compatibility audit first, since it may be unattested precisely because it is
foreclosed. A genuinely **new operation** is writable code, but its provenance
is the model rather than the corpus, so it leaves the garden rather than
entering it. The line is whether the option's *action* is attested somewhere.

## What is deliberately not here

**A per-repo review chain.** An earlier pilot ran `/stage → /reviewer →
/synthesize → /insight` over ten repositories, asking *"is this analysis
defensible?"* This project asks *"what decisions did it make?"* Both are worth
asking; carrying the first would blur what the second claims. Where reviewers
split on identical input is a genuinely interesting signal and a separate
study.

Two things were kept from that pilot and are visible above: the independence
contract now used for `auditor`, and refusing to synthesize a partial panel —
a synthesis over fewer reviews than were dispatched silently biases the
majority.

**An ontology layer.** Dropped on evidence: `fork_graph.py` found **11 of
1,081** co-reach pairs and **0 of 189** co-choice pairs significant against a
margin-preserving null. Asserting structure the corpus does not contain would
be decoration.

## The principle under test

Four occasions when a reported result failed one direction or both. They are
recorded because the design is largely a response to them, and because the
pattern across them is the honest finding.

**A blind measure offered as reassurance.** The 2.7% claim, above. Failed both
directions. → the evidence contract: `exhibit()` requires a `worst` key, and a
`REVIEW` with no exhibits raises.

**A claim tested in one direction and reported as tested in both.** Asked how
we knew the option clustering had not *under*-merged, the honest answer was
that it had been checked only *within* a fork — while two forks were still
duplicates, their option lists could not see each other. Accountable to the
user in form, not in substance: the reader was told a check had passed that had
not been run. → a second option pass, which collapsed 146 more.

**A test that could not return the answer it was reporting.** A permutation *p*
cannot fall below 1/(B+1), and with BH correction the threshold sat under the
floor of the screen — so "nothing significant" was produced *by construction*.
Four separate occurrences, one of them reported before it was caught. → every
permutation test escalates its draw count for screen survivors.

**A reproducibility claim that was false for one stage.** The README said the
committed cache makes a re-run return the committed answers. Asked what was in
the cache, it turned out 86% of it was reachable and `03_link` had been revised
after most linking ran — 206 of 225 answers came from a prompt no longer
shipped. → `prune_cache.py`, `relink.py`, and a check that fails on drift.

### What the pattern says

**A human caught all four.** Not the audits, not an agent — a person asking a
question the system had not thought to ask itself. Two of them arrived as
one-line challenges (*"the options from the two first forks look identical"*,
*"are they going to show our development decisions?"*) that overturned a
published claim and a reproducibility guarantee respectively.

That is not a failure of the design; it is the design's premise. **The system's
job is not to be right — it is to make being wrong discoverable.** Every
mechanism above exists to shorten the distance between a person's suspicion and
the evidence that settles it: the exhibit that shows items rather than
summaries, the handle that resolves to source lines, the round that records
what was asked before what changed.

Measured that way, the useful question about a consultation system is not how
often it is correct, but how quickly a skeptical user can find out that it is
not.

## Adding to this

A new **script** is frozen: deterministic, cached if it calls a model,
documented in `WORKFLOW.md`, and it must not adjudicate anything a later run
would need to re-decide.

A new **agent** is live: it may judge, and it may not write into `data/`.

A new **check** writes through `exhibit.py`. If you cannot say what exhibit
would falsify your claim, the check is not ready.
