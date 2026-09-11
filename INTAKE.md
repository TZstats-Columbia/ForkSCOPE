# Study intake — soccer

Filled against [`templates/intake.md`](templates/intake.md).

**Reconstructed after the fact.** This study was charted before the intake
existed, so the answers below are what the consultation *would* have elicited,
recovered from what the pipeline was actually built to do. Where the honest
answer at the time would have been "we didn't know", it says so — those are the
places the study later paid for, and they are the reason the intake exists.

---

## A · The corpus

**A1. Where, and what is one run?**
Two corpora, neither vendored.

| | |
|---|---|
| `ai` | `amazon-science/agentic-forking-path`, one directory per run under `experiment_data/workspaces/<arm>/<model>/sample_soccer/<run>/` |
| `human` | Silberzahn et al. 2018 via OSF, one directory per team, `team-NN` |

**A2. Code and prose per run**

| | code | prose |
|---|---|---|
| `ai` | `final_analysis.py` | `mirrored_report.txt` |
| `human` | `script.txt` | larger of `survey.txt` / `report.txt` |

The human corpus has two prose channels at two time points; the larger is
primary and the other is carried for a second pass.

**A3. How many deposited a script?**
204 of 204 AI runs. **19 of 31 human teams.** The other twelve contribute 1,123
prose spans and zero decisions.

*This is the answer that most shaped the study, and it was not known up front.*
Every pooled statistic rests on 19 human teams against 204 AI runs, and it is
the largest threat to any AI-versus-human claim here.

**A4. Arms**
The AI corpus is randomised to five persona briefs, encoded as the workspace
directory name: `standard`, `positive`, `negative`, `confirmation_seeking`,
`strong_confirmation_seeking`. Human teams have no arm.

**This is the only assigned variable in the study.** Everything else is
observational.

**A5. Redistribution**
AI corpus: yes, but large — fetched. Human corpus: **no.** Participant
materials from a human-subjects study; that decision belongs to the original
authors.

---

## B · The shared task

**B1. Dataset** — one player–referee dyad table, 2012–13 European leagues.

**B2. The question, as asked**

> Are soccer players with darker skin tone more likely to be given a red card
> by referees?

**B3. Genuinely the same?**
Yes for the question. **No for the framing** — the five AI arms received
different briefs about what to expect, which is A4 and is the manipulation.
Human teams received the original Silberzahn brief, which is not identical to
any AI arm. Recorded as a limitation rather than assumed away.

---

## C · Domain context

**C1. Glossary**

| term | |
|---|---|
| dyad | one player–referee pair. **Rows are dyads, not matches or players** |
| rater1, rater2 | two independent skin-tone ratings, 5-point scale, 0–1 normalised |
| redCards | count over all games in that dyad |
| games | appearances in the dyad — the natural exposure offset |
| position | playing position; goalkeepers are often excluded |
| IAT, Exp | implicit and explicit bias scores for the referee's country |

**C2. Easily misread**
"Dyad" reads as a match to an outsider. A skin-tone *rating* is not the
*exposure* — turning one into the other is a modelling choice, and the most
contested one here.

**C3. Looks like a decision but is not**
Loading the CSV from a fixed path; a set random seed; `library()` walls; plot
theming. All recorded as typed non-decisions rather than dropped.

**C4. Easy to miss as a decision**
Combining the two raters. It reads as data cleaning and is the study's most
contested fork: **22 runs, 22 distinct options, no two the same.**

Also: the reference date age is computed from; which columns survive into the
modelling frame; whether dyads with zero games are dropped. All three are
frequently **silent** — made in code, mentioned nowhere.

---

## D · The outcome side

**D1. Where** — reported in each run's write-up: effect size, interval,
verdict.

**D2. Scale** — mixed. Odds ratios, risk differences, IRRs. Converted to a
common odds-ratio scale where possible; `or_scale_estimate` holds the result.

**D3. Extractor**
**None. This is the study's avoidable mistake.** Outcomes were assembled per
run outside the pipeline, so `outcomes.json` has five readers and no writer.
155 of 207 records have per-run fragments behind them; **52 have no provenance
at all** and cannot be verified. `scripts/check_outcomes.py` reports the gap it
cannot close.

Human teams have no extracted outcome, so every Shapley result uses the pooled
*vocabulary* with AI-only *outcomes*.

---

## E · What we wanted to learn

**E1.** Whether the garden of forking paths is a real, mappable object — and if
so, what shape.

**E2. Suspected in advance**
The dichotomisation cutpoint; the adjustment set; whether the model accounts
for repeated referees.

*Scored honestly:* all three are contested, and the pivotal forks **do predict
the reported conclusion out of sample** (cross-validated R² 0.262 for the
verdict and 0.246 for *z*), though not the effect size (0.032 for log(OR)).

**E3. What would surprise us** — that choices predict the answer. It would have
made the multiverse tractable. It does, for the conclusion and not for the
effect size: see E2. An earlier reading that nothing predicted out of sample
was an artifact of a cross-validation bug, corrected 2026-08-30 and recorded in
`study.json`.

**E4. The claim to defend** — that variance across analysts is large *and*
transmission to the conclusion is weak. Both halves needed defending, and the
second needed a cross-validated estimate and a permutation null, not an
in-sample fit.

**E5. Comparisons** — persona arms against each other (fair, randomised); AI
against human (**not fair**: no human outcomes, 19 of 31 teams, different
brief).

---

## F · Constraints

**F1. Budget** — $804 over 2,273 model calls. A re-run against the
committed cache is free.

**F2. Must not publish** — the human corpus itself.

**F3. Deadline** — none that capped scope.

---

## G · What counts as one decision, inside the artifact

Sections A–F describe the corpus. G–K are the **forks in the charting method
itself**, and they became [`policy.json`](policy.json). Each answer below is
marked *decided* or *implicit* — an implicit one is a default nobody argued
with, and those are the entries most worth revisiting.

**G1. Which artifacts may a decision be recovered from?** — **decided: code
only.** Prose is read solely to surface choices the code makes silently.
Confirmed afterwards by measurement: prose spans reproduce at ARI 0.480 against
code at 0.895 core, so anything resting on prose inherits the weaker number.

**G2/G3. Disjoint spans, interleaving** — **implicit: gaps yes, interleaving
no.** The extraction prompt permits one and not the other, and nobody argued
either. Allowing interleaving would make span matching much harder to falsify.

**G4. How far apart are two operations before they are two decisions?** —
**decided: five lines**, after the question was measured. 76 of 96 same-run
merge groups spanned more than five lines and read as over-merges. Enforced by
`repair_option_splits.py`, audited as V6, now 2 survivors.

**G5. How is one distillation compared to another?** — **decided: lenient**,
with verbatim and core reported beside it.

> The single largest lever in the method: **0.176 verbatim, 0.713 lenient,
> 0.895 core** on one extraction. The agent led with verbatim and was
> corrected — *"the boundaries can move slightly without affecting downstream
> work."*

---

## H · Options

**H1/H2. Recurrence and singletons** — **decided: singletons kept, called
novel options**, the rare-variant analogue. 64% of options are singletons, and
excluding them moves by-option fork agreement from 0.31 to 0.69 — a change in
the question, not an improvement in the answer.

**H3. May one run hold an option twice?** — **decided: no**, across stages no,
across positions yes. This is what G4 enforces.

**H4. Are novel options in the similarity statistic?** — **decided: yes.**
Excluding singletons flatters it.

*Implicit and unexamined:* the Jaccard threshold of 0.5 that governs every
cross-build option match. It was the default and has never had a sensitivity
check.

---

## I · Forks

**I1. Minimum options, singleton forks** — implicit: 2 and yes.

**I2. Must a run pick exactly one option?** — **decided: yes, and the violation
is reported rather than repaired.** 86% of runs violate exclusivity, dominated
by one fork at 158 of 223. Answering yes does not make it true; it makes V2 an
audited exhibit instead of a silent assumption.

**I3. Which forks are pivotal?** — **decided: ≥25% coverage and >1.5 effective
options.** Measured: **18** decision points are reached by ≥25% of runs, and
**17** clear both conditions under `eff_all`, which counts not reaching the
fork as a level; the earlier test, over reaching runs only, found 11 of the 18.
The two counts are different populations and both get quoted.

**I5. When is the stage assigned?** — implicit: at the fork, revised after
repair.

---

## J · Reproducibility, and what it may do

**J1. What does agreement mean at each layer?** — decisions: lenient (G5).
Options and forks: both, all forks and pivotal-only, reported apart.

**J2. May the agent tune the method to improve stability?** — **decided: no**,
and the refusal is encoded in `policy.json` rather than left as good intentions.

> *"stability is a signal for the human to review, not a target for you to
> hit."*
>
> Fork induction can be pushed toward ARI 1.0 by merging almost nothing. Two
> cases are on file where a principled change moved agreement for reasons
> unrelated to validity: core-first fork formation made it worse, and the
> option-split repair improves it partly because one deterministic transform is
> applied to both builds.
>
> Tuning requires a pre-registered candidate set, a held-out split, and an
> external criterion. The human benchmark is the intended criterion. It ran on
> 6 September (`reviews/human-benchmark/RESULTS.md`): at the options layer two
> raters agree at 0.818 and two builds at 0.849, so that layer is at the level
> of human agreement; no tuning toward higher self-agreement is authorised.

**J3. How many replicates?** — **decided: 5 per parent, before the first
build.** That gives 4 df; 2 per parent would have given 1.

**J4. Which audits block?** — **decided: none.** Most carry no null, and
treating them as gates would convert a weak signal into a hard decision.
*Implicit:* a review queue cap of 60, which is a guess about human attention —
V1 alone queues 561 pairs.

---

## K · What the garden is used for

Persona effects; what pivotal forks predict out of sample; where novel options
sit; BH multiplicity correction; and — added during the work — whether the
charting method reproduces at all.

---

## What the intake would have changed

Three things, had it been run first.

**D3 would have been caught.** "Is there an extractor, or must one be written?"
has an obvious answer that nobody asked, and the 52 unprovenanced outcome
records are the cost.

**A3 would have been priced up front** rather than discovered late — 19 of 31
teams changes what the study can claim, and it should have shaped the design
rather than the limitations section.

**E2 would have been recorded before the results.** It is written above from
memory, which is exactly the weakness the question exists to prevent. Treat it
as illustrative here and as binding in a new study.
