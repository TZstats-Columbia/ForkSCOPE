# Study intake — the consultation

Questions to answer before charting a corpus. `/intake` walks a person through
these and writes `study.json`; this file is the underlying instrument, useful
on its own if you would rather fill it in by hand.

Answer what you know. **"I don't know yet" is a real answer** for several of
these and the pipeline can start without them — but say so, rather than
guessing, because a guessed answer looks identical to a known one three weeks
later.

---

## A · The corpus

**A1. Where are the analyses, and what is one run?**
A path, and the pattern matching a single analysis. One directory per analyst
is the usual shape.

**A2. Inside a run, which file is the code and which is the write-up?**
Extraction is code-anchored: a decision is an operation on data, recovered from
a script. Prose is read to find what was *claimed*, which is how silent
decisions are detected — but a claim is not itself a decision record.

**A3. How many runs deposited a script?**
Not how many runs exist. Runs with prose only contribute zero decisions. In the
soccer study 12 of 31 human teams had no script, and every pooled statistic
rests on the other 19 — the single largest caveat in that study.

**A4. Are there arms or conditions, and how are they encoded?**
A directory name, a manifest, a filename. If runs were randomised to anything,
that is the only assigned variable you will have; everything else is
observational.

**A5. May the corpus be redistributed?**
If no, it is referenced and fetched, never vendored. Participant materials
usually cannot be.

---

## B · The shared task

**B1. What dataset did every analyst work from — the same one?**

**B2. What question were they all asked?**
Write the question as the analysts received it. This is the load-bearing
answer: forks are comparable *because* every run answered the same question,
and it is what makes two studies two gardens rather than one.

**B3. Were they genuinely asked the same thing?**
If some got a different brief, that is either an arm (A4) or two studies. Say
which.

---

## C · Domain context

This is what an extraction model cannot infer and would otherwise get wrong. It
travels to the model as **data appended to a fixed prompt** — never as an edit
to the prompt. That distinction is what lets two studies claim the same
instrument, and it is checkable: `prompt_hash` is identical across studies or
the claim is false.

**C1. What are the key variables and what do they mean?**
Short glossary. "A dyad is one player–referee pair, and rows are dyads, not
matches" prevents a whole class of misreading.

**C2. What vocabulary would an outsider misread?**
Field-specific terms, and anything whose everyday meaning differs.

**C3. What looks like an analytic decision here but is not?**
Boilerplate that is conventional in this field — a fixed random seed, a
standard library import, a house plotting theme. These are recorded as typed
non-decisions, so naming them improves the partition rather than hiding them.

**C4. What is easy to miss as a decision?**
The reverse. In the soccer corpus, turning two raters' scores into one exposure
looked like data cleaning and was the most contested choice in the study.

> **What you may not do here.** You cannot change what counts as a decision.
> The definition is fixed — *an operation on data that could have gone
> otherwise* — and a study that needs it changed is a finding about the
> instrument, to be reported, not configured away.

---

## D · The outcome side

**D1. Did each run report a comparable estimate, and where?**
An effect size, an interval, a verdict. Without this, the garden describes what
analysts did and cannot link it to what they concluded.

**D2. Do the runs report it on a common scale?**
Odds ratio, risk difference, standardised. If several, one must be convertible
to another or the payout is not comparable.

**D3. Is there an extractor, or must one be written?**
Write it as a pipeline stage. Soccer's outcomes were assembled per run outside
the pipeline, and 52 of 207 records now have no provenance at all — an avoidable
gap that cannot be closed after the fact.

---

## E · What you want to learn

The answers here decide which analyses are worth running. All of them are
optional and none should be invented to fill the space.

**E1. Once the garden is mapped, what do you most want to know?**

**E2. Which decisions do you already suspect matter?**
Recorded now, before the results, so a later match is a prediction rather than
a story. If you are wrong, that is worth as much.

**E3. What result would surprise you?**

**E4. What claim would you like to be able to defend?**
This sets the evidential bar. "Analysts disagree" needs far less than "this
choice drives the conclusion."

**E5. Is anyone being compared — arms, corpora, tools?**
Say what would make the comparison unfair. Soccer's is stark: outcomes exist
for the AI arm and not for the human teams, so no Shapley result there is an
AI-versus-human comparison.

---

## F · Constraints

**F1. Budget.** Adjudication dominates. The soccer study spent $804 over
2,273 calls; a re-run against a warm cache costs nothing.

**F2. Anything that must not be published?**
Participant materials, unreleased data, identifying content in prose.

**F3. Is there a deadline that should cap scope?**

---

## G · What counts as one decision, inside the artifact

Sections A–F describe the corpus and what you want from it. **G through J are
different in kind: they are forks in the charting method itself**, where a
competent analyst could choose otherwise. They become `policy.json`, and the
pipeline records them the way it records any decision — what was chosen, why,
and whether it was chosen or merely defaulted into.

Each carries what the choice cost in the soccer study. That is not a
recommendation; it is what you are trading.

**G1. Which artifacts may a decision be recovered from?**
Code only, or code and prose? Prose reproduces far worse than code — spans
agree at ARI 0.48 against 0.90 — so anything resting on prose inherits the
weaker number. Soccer uses code only, with prose read *solely* to surface
choices the code makes silently.

**G2. May one decision own lines that are not adjacent?**
Artifacts contain lines belonging to no decision at all — imports, theming,
seeds. Call them **introns**; the lines that do belong are **exons**. May a
decision's exons be split by introns? Soccer: yes.

**G3. May one decision's exons be split by *another decision's* exons?**
Interleaving. Soccer: no. Allowing it makes span matching much harder to
falsify, because almost any grouping becomes defensible.

**G4. How far apart are two operations before they are two decisions?**
A run that dichotomises at 0.25 on line 27 and refits at 0.50 on line 236 did
two things, not one thing twice. Soccer sets five lines. **Measured: 76 of 96
same-run merge groups spanned more than five lines and were over-merges** —
this is audit V6, and the repair that acts on it.

**G5. How is one distillation compared to another?**
Verbatim span equality, or with room for boundaries to move?

> **This is the most consequential answer in the intake.** Soccer scores
> **0.176 verbatim, 0.713 lenient, 0.895 core.** The same pipeline is
> irreproducible or excellent depending only on which you quote. Choose before
> measuring, and report the level beside every number.

---

## H · Options — grouping decisions that recur

**H1. How many decision points make an option *recurring*?**

**H2. Are single-decision options allowed, and what are they called?**
Soccer allows them and calls them **novel options** — the rare-variant
analogue. They are not noise: **64% of soccer options are singletons**, and
excluding them moves by-option fork agreement from 0.31 to 0.69. That is a
change in the question being asked, not an improvement in the answer.

**H3. May one run hold the same option twice? Across stages? At different
positions in the artifact?**
Soccer permits position, forbids repetition. The repetition rule is what G4
enforces.

**H4. When two charting runs are compared, are novel options included?**
Excluding singletons flatters the statistic. Report both or neither.

---

## I · Forks — grouping options into decision points

**I1. How many options make a fork? Are single-option forks allowed?**

**I2. Must a run pick exactly one option at a fork?**
This is *exclusivity*, and it is where soccer's honest answer is uncomfortable:
**86% of runs violate it**, dominated by a single fork at 158 of 223 runs.
Answering "yes" does not make it true — it makes the violation an audited
finding (V2) rather than a silent assumption.

**I3. Which forks are worth reporting — the *pivotal* ones?**
Coverage is the share of runs reaching the fork; effective options is 1/HHI.
Soccer uses 25% and 1.5. **Measured: 18 forks clear that bar and all 18 are
recovered by both builds** — against 317 vs 351 raw. The filter that makes the
analysis tractable is the same filter that selects the reproducible population,
and that is a finding, not a convenience.

**I4. Should fork similarity be measured over all forks or only pivotal ones?**
Restricting raises agreement substantially and answers a narrower question. Say
which, or report both.

**I5. When is the DSLC stage assigned — at decision, option, or fork? Is it
revised after repair?**

---

## J · Reproducibility — and what it is allowed to do

**J1. What does "the same result twice" mean at each layer?**
G5 answers it for decisions; H4 and I4 for options and forks. State all three.

**J2. May the agent adjust the method to improve stability?**

> **The default is no, and the refusal is encoded rather than advised.**
>
> Stability is trivially gameable in the wrong direction. Fork induction can be
> pushed toward ARI 1.0 by making it more deterministic — merge almost nothing,
> or seed a fixed clustering — which raises the number and destroys what it
> measures. Two worked cases are on file: core-first fork formation was
> principled and made agreement *worse*; the option-split repair raises
> agreement partly *because* one deterministic transform is applied to both
> builds.
>
> There is also a reflexive hazard. Tuning until stability looks good and then
> reporting that stability is a garden of forking paths, run on the instrument
> built to measure gardens of forking paths.
>
> Stability may select among *a priori equally defensible* options only with
> all three of: a **pre-registered candidate set**, a **held-out split**, and an
> **external criterion** (human benchmark, rediscovery of an independent
> schema, or outcome prediction). Without them the agent reports stability and
> declines to optimise it — and says so.

**J3. How many replicates, decided now?**
At *k* replicates a parent contributes *k−1* degrees of freedom; an sd on 2 df
is compatible with almost anything. Soccer uses 5 per parent. Fix it before the
first build: extending because the spread looks interesting is optional
stopping on the quantity being reported.

**J4. Which audit exhibits block a build, and which only rank for attention?**
Soccer blocks none, deliberately — most checks carry no null, so treating them
as gates would convert a weak signal into a hard decision. But a review queue
of 561 pairs is not a queue; say how many a human will actually read.

---

## K · What the charted garden is used for

Optional. None of these should be invented to fill the space.

**K1.** Do the arms (personas, tools, conditions) change what analysts *do*, or
only what they *report*?
**K2.** What do pivotal forks predict — out of sample?
**K3.** Where do novel options sit, and do they matter?
**K4.** How is multiplicity handled?
**K5.** What summary statistics describe the garden itself?
**K6.** Which results must be shown to be stable before they are believed?

---

## What happens next

`/intake` writes `study.json`, then `/chart` runs the pipeline. `final_tag`
stays `CHANGE-ME` until the repair chain has run — the lineage is not knowable
in advance.

Keep the filled-in intake beside `study.json` as `INTAKE.md`. It records the
questions that were asked, what was not known at the time, and the predictions
in E2 — none of which survives in the manifest.
