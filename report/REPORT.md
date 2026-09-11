# ForkSCOPE — technical report for the soccer case study

*A technical report about the pipeline it describes. **Hand-written, not generated**: every number in it is transcribed by a person or an agent reading the artifacts, and nothing re-derives them when a build moves. A load-bearing figure should be re-derived from the artifact cited beside it.*


Study **soccer** · vocabulary tag `ai+human.merged.forkmerged.merged.induced.r3.osplit`

---

## Contents

- [Terminology](#terminology)
- [Introduction](#introduction)
  - [The problem](#the-problem)
  - [Why a fixed schema is the wrong instrument](#why-a-fixed-schema-is-the-wrong-instrument)
  - [What this paper describes](#what-this-paper-describes)
  - [Contributions](#contributions)
- [Corpora](#corpora)
  - [The AI corpus](#the-ai-corpus)
  - [The human corpus](#the-human-corpus)
  - [What is deliberately not used as input](#what-is-deliberately-not-used-as-input)
- [Stage 1: Distillation](#stage-1-distillation)
  - [What counts as a decision](#what-counts-as-a-decision)
  - [The exon/intron partition](#the-exonintron-partition)
  - [Coverage as a retryable invariant](#coverage-as-a-retryable-invariant)
  - [Linking, and the residue that is the finding](#linking-and-the-residue-that-is-the-finding)
  - [The per-run record](#the-per-run-record)
  - [Prose-length filter](#prose-length-filter)
- [Stages 3–6: Vocabulary induction](#stages-36-vocabulary-induction)
  - [Two levels, two criteria](#two-levels-two-criteria)
  - [Bottom-up clustering: no embeddings, no cap](#bottom-up-clustering-no-embeddings-no-cap)
  - [The foreclosure test](#the-foreclosure-test)
  - [The structural veto](#the-structural-veto)
  - [Transitivity is earned, not assumed](#transitivity-is-earned-not-assumed)
  - [Normalisation and the split-never-merge asymmetry](#normalisation-and-the-split-never-merge-asymmetry)
  - [The repair chain and its stopping rule](#the-repair-chain-and-its-stopping-rule)
- [Lifecycle stage assignment](#lifecycle-stage-assignment)
  - [Blinding, and why it is necessary](#blinding-and-why-it-is-necessary)
- [Validation of the blind assignment](#validation-of-the-blind-assignment)
- [Measurement](#measurement)
  - [The frequency-spectrum framing](#the-frequency-spectrum-framing)
  - [Three counting rules](#three-counting-rules)
  - [Concentration statistics](#concentration-statistics)
  - [Novelty](#novelty)
  - [Novelty dose-response](#novelty-dose-response)
  - [Lifecycle iteration](#lifecycle-iteration)
  - [Garden structure: siblings and gates](#garden-structure-siblings-and-gates)
  - [Shapley attribution](#shapley-attribution)
- [Visualization as analysis](#visualization-as-analysis)
  - [The circle: stages as sectors, runs as closed tours](#the-circle-stages-as-sectors-runs-as-closed-tours)
  - [The fork atlas: four panels](#the-fork-atlas-four-panels)
  - [Interactive viewers](#interactive-viewers)
  - [Figure provenance](#figure-provenance)
- [Validation](#validation)
  - [Audit companions](#audit-companions)
  - [Audit design principles](#audit-design-principles)
  - [Gate 5.4: code ablation](#gate-54-code-ablation)
- [Reproducibility](#reproducibility)
  - [Determinism without temperature or seed](#determinism-without-temperature-or-seed)
  - [Seeding and resampling](#seeding-and-resampling)
  - [Vocabulary lineage](#vocabulary-lineage)
  - [Provenance classes](#provenance-classes)
  - [Two hazards in this scheme](#two-hazards-in-this-scheme)
- [The charting collaboration](#the-charting-collaboration)
  - [Three gates](#three-gates)
  - [The decisions a human made](#the-decisions-a-human-made)
  - [Errors, by how they present](#errors-by-how-they-present)
- [Measuring agreement between two extractions](#measuring-agreement-between-two-extractions)
  - [The problem](#the-problem)
  - [Four levels](#four-levels)
  - [The gap is the measurement](#the-gap-is-the-measurement)
  - [What is not claimed](#what-is-not-claimed)
- [The induced map against a curated one](#the-induced-map-against-a-curated-one)
- [Stability under replication](#stability-under-replication)
  - [Replicate versus scope change](#replicate-versus-scope-change)
  - [Estimators](#estimators)
  - [Results](#results)
  - [Instability as an audit signal](#instability-as-an-audit-signal)
  - [Limitations of this measurement](#limitations-of-this-measurement)
  - [Fork formation replicated against itself](#fork-formation-replicated-against-itself)
- [The induced map against a curated one](#the-induced-map-against-a-curated-one)
  - [Two maps of different shape](#two-maps-of-different-shape)
  - [Recovery and addition, adjudicated](#recovery-and-addition-adjudicated)
  - [The one node not recovered is the result, not the exception](#the-one-node-not-recovered-is-the-result-not-the-exception)
  - [What the curated pipeline discarded](#what-the-curated-pipeline-discarded)
  - [What this does and does not license](#what-this-does-and-does-not-license)
- [Prose as lossy compression of an analysis](#prose-as-lossy-compression-of-an-analysis)
  - [Three independent measurements of the loss](#three-independent-measurements-of-the-loss)
  - [Why verification is hard, seen twice](#why-verification-is-hard-seen-twice)
  - [What is robust and what is not](#what-is-robust-and-what-is-not)
  - [The consequence for instrument design](#the-consequence-for-instrument-design)
- [Reliability: what the measurements license](#reliability-what-the-measurements-license)
  - [What is not model-mediated](#what-is-not-model-mediated)
  - [Measured reproducibility, by layer](#measured-reproducibility-by-layer)
  - [Three properties that survive replication](#three-properties-that-survive-replication)
  - [What we therefore do not claim](#what-we-therefore-do-not-claim)
  - [Threats we cannot currently rule out](#threats-we-cannot-currently-rule-out)
  - [Agreement is not validity](#agreement-is-not-validity)
- [Limitations](#limitations)
  - [Writing order is not thinking order](#writing-order-is-not-thinking-order)
  - [Stage assignment is a model judgement](#stage-assignment-is-a-model-judgement)
  - [Code-anchoring excludes prose-only analyses](#code-anchoring-excludes-prose-only-analyses)
  - [Additivity in the attribution model](#additivity-in-the-attribution-model)
  - [Everything on the outcome side is observational](#everything-on-the-outcome-side-is-observational)
  - [Under-merge is preferred, and it is still an error](#under-merge-is-preferred-and-it-is-still-an-error)
  - [One corpus, one dataset, one question](#one-corpus-one-dataset-one-question)
- [Constants and thresholds](#constants-and-thresholds)
- [Prompt inventory and stage map](#prompt-inventory-and-stage-map)
  - [Prompts](#prompts)
  - [Workflow stages](#workflow-stages)
  - [Vocabulary tag grammar](#vocabulary-tag-grammar)
- [References](#references)

---
When many analysts are given one dataset and one question, they produce many different analyses. The standard way to study this variation is to fix a schema of decision points in advance and score each analysis against it. That design answers only the questions the schema anticipated, and its blind spots are invisible by construction. This paper describes an end-to-end method that instead *induces* the decision vocabulary from the analyses themselves.

The method has three parts. First, *distillation* segments every analysis artifact—script and write-up—into an exhaustive, typed partition, aligns the two channels, and treats what fails to align as the finding: operations the code performs and the prose never mentions (*silent decisions*), and operations the two channels describe incompatibly (*misalignments*). Second, *vocabulary induction* clusters concrete choices into options and options into decision points bottom-up, with no embeddings and no cap on the number of categories, using a foreclosure criterion—could one analyst do both?—rather than surface similarity, and a co-occurrence constraint that vetoes semantically attractive but structurally impossible merges. Third, *measurement* reads statistics off the resulting option-frequency spectrum, treated explicitly as a site frequency spectrum: concentration at a decision point, rare-variant novelty, lifecycle iteration, conditional branching structure, and Shapley attribution of reported outcomes to decision points.

We give the estimators in full, and we describe the validation architecture: every analysis stage ships with a named audit, and a code-ablation gate tests whether decisions can be recovered from prose alone before any cross-corpus claim is permitted. We also document the visualization methods as analyses in their own right rather than as presentation. Finally we report two reproducibility hazards found by auditing the pipeline against itself: a cache keyed on a model *alias* rather than a resolved version, and a metadata recovery step whose silent fallback depends on an untracked input. Both are properties of the method worth stating plainly, because both would be invisible in the outputs.

## Terminology

Three levels, and two kinds of run. Used consistently throughout.

| term | what it is |
|---|---|
| **raw decision point** | one operation on data, extracted from one analysis. The unit distillation produces |
| **decision option** | a concrete choice that recurs. A cluster of raw decision points that mean the same thing |
| **decision fork** | a slot where an analyst must pick one option. A cluster of options that are rivals |
| **analysis** | one analyst's work on the shared task. The corpus is a collection of these |
| **replicate** | one re-run of *our* pipeline, used to measure whether it reproduces |

The distinction between the last two is load-bearing. Variability *across
analyses* is the object of study; variability *across replicates* is a property
of the instrument, and conflating them would report our own noise as a finding
about analysts.

## Introduction

### The problem

A single dataset and a single research question do not determine a single analysis. Between the data and the reported estimate lies a long sequence of choices—which records to exclude, how to code the exposure, which covariates to adjust for, what to report as the headline—and at each one a competent analyst could have chosen otherwise. [gelman2013garden] named the resulting structure the *garden of forking paths*; [steegen2016] and [simmons2011] showed how much the terminal estimate can move as one walks different paths through it.

Many-analyst studies make the variation observable by running the garden in parallel. [silberzahn2018] gave 29 teams one dataset and one question; [botvinik2020] did the same with 70 neuroimaging teams; [breznau2022] with 73. In every case the spread of reported results was large enough to matter, and in every case the natural follow-up question was the same: *which* decisions drove the spread?

### Why a fixed schema is the wrong instrument

The usual way to answer that question is to enumerate the decision points in advance—a fixed schema of `k` slots—and code each analysis against it. This is tractable, comparable across teams, and immediately quantitative. It is also circular in a way that is easy to miss: the schema determines what can be found, so a decision nobody anticipated cannot be recorded, and its absence from the results is indistinguishable from its absence from the analyses.

The corpus studied here ships with exactly such an extraction, performed by the corpus's original authors. Across its 207 soccer runs it carries **21 distinct decision-point keys**, of which **11 constitute the operative codebook** — each assigned in 206 or 207 of the 207 runs — while the remaining 10 are residue from a single run that was never unified onto the shared taxonomy. Of the 1{,}120 items its own extractor recovered across the 207 runs, **a third landed in an `unmapped_decisions` bucket**. That residue is a direct measurement of what a fixed schema cannot hold, and it is why the present method never reads that file as input (*sec:corpus*).

Two qualifications, both from the upstream code. First, the schema is **not fixed a priori**: `scripts/pipeline/taxonomy.py` generates it per dataset by LLM compression and *"auto-selects the most informative decision points by Shannon entropy"*, discarding low-frequency ones — so 11 is an output of entropy selection, not a design constant, and the discarded tail is selected against by construction. Second, the mapping is **saturating**: all 2{,}268 assignments carry a substantive value and none is `other`, `none`, or `not applicable`, so the resulting matrix is complete and cannot express *"this analyst never faced this decision"* — the state that the present method treats as a level in its own right (*sec:shapley*).


### What this paper describes

We describe a method for recovering the decision map of an analysis corpus without stipulating it first. The pipeline has three parts, and the paper is organised around them:

1. **Distillation** (*sec:extraction*). Each analysis is segmented into an exhaustive, typed partition of its script and its write-up. The two channels are then aligned, and the *residue* of that alignment—what one channel contains and the other does not—is the primary finding rather than a diagnostic.
2. **Vocabulary induction** (*sec:vocabulary*, *sec:stages*). Concrete choices are clustered bottom-up into *options*, and options into *decision points*, with no embeddings, no similarity threshold and no cap on the number of categories. The criterion for two options being rivals is *foreclosure*—taking one rules out the other—not lexical or semantic similarity, which gets the question wrong in both directions. A structural co-occurrence constraint acts as a veto on merges that semantics proposes.
3. **Measurement** (*sec:analysis*, *sec:visualization*). The option-frequency spectrum is read as a site frequency spectrum: modal concentration, effective option counts, singleton novelty as a rare-variant tail, and options confined to one experimental arm as private alleles. That framing brings its own correction—ascertainment bias—which is why every richness quantity is reported after exact rarefaction.

Two further concerns run through all three parts and get their own sections. *sec:validation* describes the validation architecture: each analysis script has a named audit companion whose checks are reported with the result, and a code-ablation gate that must clear before any cross-corpus comparison is permitted. *sec:reproducibility* describes how determinism is obtained from a model that exposes neither temperature nor seed, and reports two hazards in that scheme that we found by auditing it.

### Contributions

1. A schema-free extraction method in which decision coverage is enforced as a *retryable invariant* rather than measured after the fact, so that “the parser did not look here” becomes a disputable claim rather than a silent omission (*sec:extraction*).
2. A vocabulary induction procedure combining a semantic foreclosure test with a structural cannot-link constraint derived from co-occurrence, plus a convergent repair chain with a stated stopping rule (*sec:vocabulary*).
3. A validation architecture in which no reported number comes from a command typed once, and an explicit account of two reproducibility hazards that survived it (*sec:validation*, *sec:reproducibility*).

## Corpora

Two source corpora are consumed. Neither is redistributed with the pipeline; both are published elsewhere under their own terms, so the repository records exactly what it read and where to obtain it. Everything downstream of these two inputs is retained, so all analyses can be re-run and audited without refetching the raw material. The raw corpora are needed only to re-run distillation (*sec:extraction*), which is the single stage that reads them.

### The AI corpus

The first corpus comprises 207 independent agentic analyses of the [silberzahn2018] soccer dataset, produced by the AWS *agentic forking paths* study and released as `amazon-science/agentic-forking-path`. Each run was generated by `bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0` and occupies one workspace directory. Three artifacts per run are read:

| **Artifact** | **Role** | **Present** | **Note** |
|---|---|---|---|
| `final_analysis.py` | code | 207 | the script the run wrote and executed |
| `mirrored_report.txt` | prose | 206 | one file is empty, so 205 are usable |
| `transcript.json` | trace | 207 | reasoning and tool trace |

*Raw artifacts read from each AI run.*

Applying the prose-length filter (*sec:extraction*) leaves **204 usable runs**. Each run carries a *persona arm*—an experimental condition recorded as a directory name in the workspace path—taking one of five values: `standard`, `positive`, `negative`, `confirmation_seeking`, and `strong_confirmation_seeking`. The arm is a property of corpus layout rather than of the analysis content, which has a consequence for reproducibility discussed in *sec:repro-arm*.

### The human corpus

The second corpus is the original many-analysts study: 31 analyst teams independently analysing the same dataset [silberzahn2018]. Three artifacts per team are read: a saved script (`script.txt`, in R, Stata, SPSS, Stan or Python), the Stage-3 survey response, and the post-feedback manuscript. Of the two prose channels, the larger is taken as primary and the other carried as a secondary channel.

#### The 19-of-31 consequence

Decision extraction in this method is *code-anchored*: a decision is an operation on data, recovered from a script. Prose is read to establish what was *claimed*, which is how silent decisions and misalignments are found, but a claim is not itself a decision record.

Only 19 of the 31 teams deposited a script. The 12 teams without one therefore contribute **no decisions**, and every pooled analysis rests on 19 human teams, not 31. Those teams do contribute **1,123 prose spans**, which the code-ablation gate uses. Of the twelve, **eleven were distilled**; the twelfth, `team-14`, has a directory but no `record.json` and contributes nothing at all, so the prose-only group is 11 in the data even though 12 teams lack a script. This is a real limitation rather than an incidental one, and it is the reason the ablation gate of *sec:ablation* exists: until that gate clears, no claim comparing the AI and human corpora is safe.


### What is deliberately not used as input

Both source corpora ship with their original authors' own derived analyses. Neither is read by this pipeline, and the exclusion is enforced by a data file (`data/raw/inputs.json`) that distillation consults, rather than by convention:

- `decisions_mapped.json` is the AWS team's own decision extraction against a fixed 21-slot schema. Using it as input would import the taxonomy this project exists to avoid and would destroy the free-discovery claim. As noted in *sec:intro*, it remains valuable as an independent comparison *after* the vocabulary exists.
- `sonnet_llmj.txt` is likewise a derived judgement and is not read.

The distinction the manifest encodes is between *raw* artifacts—produced by the analysis run itself—and *derived* artifacts, which are somebody else's analysis *of* the run. Feeding a derived artifact to the parser would launder an external taxonomy into the induced vocabulary, so the boundary is enforced mechanically.

## Stage 1: Distillation

Distillation converts one analysis—a script plus a write-up—into one structured record. It is the only stage that reads raw material, and the only stage whose output every later stage depends on.

### What counts as a decision

> **Definition (Decision).** A *decision* is an operation on data that could have gone otherwise: a fork at which a competent analyst could have chosen differently. It is not a step in the code.

This distinction does the work. A step-by-step narration of a script produces a summary; a decision map records only the forks. The operative test is counterfactual—*could a competent analyst have done something else here?*—and it is applied per operation, not per line.

### The exon/intron partition

The useful analogy is genetic. A decision is a *gene* whose *exons* are the lines implementing it. Exons need not be contiguous: a variable created on line 30 and used on line 140 is one decision spanning both. Every other line is an *intron* and must still be *typed*—configuration, glue, printing, comment—rather than discarded, because “this line does nothing analytically interesting” is itself a claim that ought to be inspectable.

Two prompts perform the segmentation, and they impose deliberately different contracts:

> **Invariant (Code partition).** `01_segment_code` partitions a script **exhaustively and exclusively**: every line lands in exactly one span, and no line lands twice.

> **Invariant (Prose partition).** `02_segment_prose` partitions the write-up into claims and typed non-claims, **exhaustively but not exclusively**.

The asymmetry is substantive rather than a relaxation for convenience. A line of code belongs to one decision; prose does not work that way. A single sentence routinely asserts two separable things—“we averaged the raters and dropped unrated players”—and demanding an exclusive partition of prose would fight the medium and force arbitrary splits.

Claims additionally carry a *polarity* (`did`, `did_not`, and non-assertive types). A claim with polarity `did` or `did_not` is a decision stated in prose. This is what makes the code-ablation gate of *sec:ablation* cheap: the prose channel is blind to the script *by construction*, because prompt `02` never sees it.

### Coverage as a retryable invariant

Partition coverage is not measured after the fact and reported as a diagnostic. It is enforced in the model-call retry path: a response that fails to partition `1..n` is rejected with a *specific* complaint—which lines are missing or doubled—and re-asked with that complaint appended.

The reason is that coverage is the basis of every downstream claim. If the segmenter may silently skip a region of the script, then a decision absent from the record is ambiguous between “the analyst did not make it” and “the parser did not look there,” and no count is interpretable. Enforcing exhaustiveness as a precondition converts the second possibility into a hard failure.

A JSON schema cannot express “these line ranges must partition `1..n`,” so the invariant is supplied as a callable semantic check evaluated in the same informed-retry loop as schema validation (*sec:reproducibility*).

### Linking, and the residue that is the finding

Prompt `03_link` aligns code decisions to prose claims *within* a run. The alignment itself is not the product; what fails to align is.

> **Definition (Silent decision).** An operation the code performs that no claim in the write-up mentions.

> **Definition (Misalignment).** A code decision and a prose claim that describe the same operation incompatibly.

Both are recovered as the *residue* of an alignment rather than searched for directly. This is what allows them to be counted rather than merely illustrated: a silent decision is defined by the failure of a procedure applied uniformly to every run, not by an analyst noticing an omission.

The link step, the silent-decision derivation and the misalignment derivation share exactly one implementation. Two would drift, and the drift would be invisible in the resulting numbers.

### The per-run record

The stage emits one `record.json` per run containing the typed code partition, the typed prose partition, the links, the silent decisions, the misalignments, and run-level metadata (corpus, arm, code length, exon share). Corpus roll-up (`distill.py index`) then aggregates these into the per-corpus tables: coverage, silent decisions, misalignments, and per-arm summaries.

Record writing is idempotent and skip-on-exist: a run whose `record.json` is already present is returned unchanged unless a force flag is set. This makes the stage cheap to re-enter, and has one consequence for provenance discussed in *sec:repro-arm*.

### Prose-length filter

A run enters distillation only if it has both a code artifact and a prose artifact exceeding 400 bytes. On the AI corpus this filter takes 207 workspaces to **204** usable runs. The threshold exists because a prose channel too short to contain claims cannot contribute to the residue analysis, and admitting it would depress silent-decision rates for arithmetic rather than substantive reasons.

## Stages 3–6: Vocabulary induction

Distillation yields per-run decisions phrased in each run's own words. Turning those into a comparable vocabulary requires two clustering problems to be solved in sequence, and they are *different* problems answered by different criteria.

### Two levels, two criteria

> **Definition (Option).** An *option* is one concrete choice. Two decisions belong to the same option when substituting one description for the other would not change what a reader believes the analysis did.

> **Definition (\Fork{}).** A *decision point* is a slot at which an analyst must pick one alternative and, having picked it, cannot take the others.

Options group by *same action*; decision points group by *same purpose*. The second criterion cuts against surface similarity in both directions, which is why no lexical or embedding method can supply it:

| **Pair** | **Verdict** |
|---|---|
| *drop rows with no rating* / *impute from the other rater* — no shared words, opposite operations, but the same slot | **one** decision point |
| *drop rows with no rating* / *drop goalkeepers* — near-identical phrasing, same operation, but different slots | **two** decision points |

*Surface similarity gets decision point identity backwards in both directions. The second row is the damaging case: it manufactures a decision point nobody faced.*

### Bottom-up clustering: no embeddings, no cap

Options are induced in three layers (`cluster_up.py`): L1 local grouping, L2 label merging, L3 question merging. Two design choices are load-bearing.

**No vector or string metric.** Roughly 95% of option labels in this corpus are unique, so no embedding or edit-distance threshold separates them usefully. An earlier top-down attempt that sampled a fraction of items and capped the category count was discarded: capping categories is precisely the fixed-schema move of *sec:intro*, reintroduced as a hyperparameter.

**L1 per corpus, L2/L3 over the union.** L1 batching depends on sorting the whole item set, so adding the human teams to a pooled sort would reshuffle every batch and invalidate the cached AI calls. Splitting the phase keeps local work stable and is the correct shape regardless: L1 is local grouping, L2 is global merging.

Clustering is performed *pooled* for any AI-versus-human claim. Clustering the corpora separately yields two incomparable vocabularies—the failure mode of an earlier version of this work, in which the human side came out roughly ten times finer-grained per record than the AI side, so that no comparison between them meant anything.

### The foreclosure test

`22_induce_forks` groups options by purpose using an operational test:

> Could one competent analyst, in one script, do **both**? Yes `\Rightarrow` different decision points. Taking one rules out the other `\Rightarrow` same decision point.

with an explicit carve-out for robustness refits: “dichotomise at 0.25 then refit at 0.50” is one analyst reporting a sensitivity analysis, not one analyst taking two options at one slot.

This step was added after an audit found that fork labels had been a *by-product* of option merging rather than the output of a clustering step: an earlier prompt emitted a fork label per option group in isolation and never compared the labels to each other. Induction from purpose is the missing step.

### The structural veto

Options at one decision point are alternatives, so they should rarely co-occur in a single run. Measured on this corpus, same-decision point option pairs almost never co-occur, while different-decision point pairs frequently do. This is a *cannot-link* constraint, and it is used three ways:

1. to *score* which decision point pairs are worth adjudicating by model call;
2. as *evidence* presented to the adjudicator; and
3. as a *test* of the result—any group whose options co-occur in `≥ 2` runs is split, by graph colouring, with no model calls.

The constraint is nearly necessary and far from sufficient, so the ordering is strict: **semantics proposes and co-occurrence vetoes, never the reverse**.

### Transitivity is earned, not assumed

`merge_forks.py` grows merge groups edge by edge under two brakes:

- an explicit **veto** wherever a pair was adjudicated *different*; and
- a **density floor**: a decision point must be judged the same as at least `60%` of a group's members before joining it.

The veto alone is insufficient. Only a small fraction of all pairs are ever adjudicated, so most pairs inside a growing component were never examined and no veto can fire; pure transitive closure then chains through pairs nobody judged. The density floor is what prevents a single ambiguous edge from fusing two large components.

### Normalisation and the split-never-merge asymmetry

`repair_clusters.py` applies numeric and set normalisation: `>0` and `>=1` are the same rule on integers, and `\{0.25\}` versus `\{0.25, 0.75\}` is one two-sided rule rather than three distinct ones. Splitting on these fabricates singletons, which would then be counted as novelty (*sec:novelty*).

Repair passes **split only, never merge**, unless a human reviewer explicitly directs a merge. The two errors are not symmetric:

| **Over-merge** | invisible in the output, unrecoverable |
|---|---|
| **Under-merge** | visible in the output, fixable later |

An over-merged decision point presents as a single well-populated question and there is nothing in the output to indicate that two questions were fused. An under-merged pair presents as two suspiciously similar decision points that never co-occur—the signature the sibling screen of *sec:garden* detects.

### The repair chain and its stopping rule

L2/L3 leave two errors that the automated checks cannot see. The repair chain addresses them in a fixed order that was established empirically and at the cost of real errors:

1. **options first** — collapse paraphrase within a decision point (`19_option_granularity`). Given one decision point and the twenty options recorded under it, “which of these are the same action?” is far better posed than comparing items across the whole corpus.
2. **decision points second** — merge duplicate decision points (`21_fork_identity`).
3. **options again** — duplicate decision points had hidden duplicate options from each other; this pass found 146 further merges that were never comparable until their decision points were united.
4. **induce last** — re-derive decision points from option purpose (`22_induce_forks`).
5. **then iterate** — induction re-derives fork labels, and any duplicate it creates is invisible to the merge pass that already ran. The merge passes therefore repeat until one changes nothing.

Each pass writes a **new tag** rather than overwriting, so every number ever reported remains reproducible from the vocabulary that produced it, and the filename records the lineage (e.g. `ai.merged.forkmerged.merged.induced.r3`). Rounds are named `.rN` rather than by appending one suffix per pass, which had grown tags to 77 characters that did not say which round was which.

**Stopping rule.** Let `F_i` be the number of decision points after round `i`. The chain stops when

```
\frac{F_{i-1} - F_i}{F_{i-1}} \;\leq\; \tau,
  \qquad \tau = 0.02,
```

capped at three rounds. Exact equality would be the natural test and is the wrong one: `merge_forks` adjudicates every pair above a fixed score, and relabelling shifts scores, so each round surfaces a few fresh candidates from the tail. The sequence asymptotes without reaching zero, and a loop demanding a strict fixpoint would run to the cap on every corpus while implying a convergence it never achieved. If the cap is reached without satisfying `eq:converge`, the pipeline prints an explicit instruction to report where it stopped and how much the last round moved, and *not* to describe the vocabulary as converged.

**Observed convergence.** The stopping rule `eq:converge` is evaluated on decision points, not options, because decision points are what the merge passes adjudicate. On the AI-only corpus the chain moved `245 → 210 → 201 → 199` decision points across rounds 1–3—that is `14.3%`, then `4.3%`, then `1.0%`—satisfying `eq:converge` at round 3. The option layer contracted alongside it, `832 → 675 → 651 → 639`. On the pooled corpus the same rule stopped at round 3 from `375 → 329 → 321 → 317`.

The two layers move together but not identically, which is why the rule names one of them: options merge *within* a decision point, so the option count can fall while the decision point count is unchanged, and a rule reading the option layer would report progress that the adjudication did not make.

## Lifecycle stage assignment

Each decision point is assigned one of six data-science lifecycle (DSLC) stages:

`problem_formulation` `\cdot` `data_collection` `\cdot` `data_cleaning` `\cdot` `eda` `\cdot` `modeling` `\cdot` `communication`

Assignment is by **the job the question does, not where it appears** (`14_fork_stage`).

### Blinding, and why it is necessary

The prompt is given the decision point label and **nothing else**: no line number, no position within the script, no neighbouring decision points. This is deliberate and it is what makes the iteration analysis of *sec:iteration* non-circular.

That analysis compares a decision's *stage* against its *position* in the script, and counts a *return* whenever the stage order runs backwards relative to the writing order. If the stage label were inferred from position, returns could not exist by construction and the measured return rate would be an artifact of the labelling procedure rather than a property of the analyses.

#### ForkSCOPE: one viewer over three units of analysis

The figures above each answer one question well, and none lets a reader move
between the levels the study has. `figures/forkscope.html` (`scripts/forkscope.py`)
puts them in one page:

- **The Garden** — every decision point, filtered by keyword, by runs reached,
  by persona, or restricted to the highways
- **Pivotal Forks** — the coverage × effective-options plane with both
  thresholds drawn as movable lines, so the reporting bar is visible rather than
  a number in a caption
- **Corpus Viewer** — one row per run: persona, length, % exon, decisions,
  silent decisions, odds ratio, conclusion; sortable, with each script's
  exon/intron map inline

It computes no statistic of its own. A viewer that recomputed would be a second
implementation to keep in agreement with the first, and % exon is already
`coverage.code.functional_share`, written at distillation — median **39.0%**, over the **223 runs that have a script**. (38.1% over the 204 AI runs alone.)


## Validation of the blind assignment

The blinding creates an obligation to show that the labels nonetheless carry real sequence information—otherwise a measured “return” could simply be labelling noise. Two checks establish this:

- The blind assignment reproduces the pipeline order anyway: Spearman `ρ = +0.593` between assigned stage index and observed median position (check I3 in `audit_iteration.py`, on the canonical vocabulary — this previously read `\approx +0.66` and `+0.657`).
- Precedence used by the garden analysis (*sec:garden*) is derived from median observed position, which is independent of the stage labels, and validated against them at the same `ρ`.

A correlation of this size is the licence to read a *deviation* from pipeline order as a deviation rather than as labelling error. It is deliberately not higher: a `ρ` near `1` would indicate the stage label was recoverable from position and therefore carrying no independent information.

## Measurement

All statistics in this section are computed on the induced vocabulary with no model calls, and are therefore deterministic given the vocabulary tag. Where resampling is used it is seeded (*sec:reproducibility*).

### The frequency-spectrum framing

An option's *frequency*—how many runs chose it—is the quantity the whole pipeline exists to produce. We read the resulting distribution as a **site frequency spectrum**, and the population-genetics analogy is used directly rather than decoratively:

| **Genetics** | **Here** |
|---|---|
| site frequency spectrum | option frequency spectrum at a decision point |
| singleton / rare variant | option chosen by exactly one run |
| private allele | option confined to one persona arm |
| ascertainment bias | richness growing with sample size |

The analogy is adopted with its correction attached: because richness grows with sample size, **no richness quantity is compared across arms without correcting for their size** (see Novelty below).

### Three counting rules

Three conventions prevent the most common errors, and each was adopted after the corresponding failure was observed.

**Runs, not decisions.** A run that dichotomises twice in one script must not count twice toward an option's frequency. Every count is over *distinct run identifiers*.

**Coverage before comparison.** Concentration measured on three runs is not a measurement. A decision point enters any stability statistic only if it is reached by at least

```
\texttt{MIN\_RUNS} = 10
```

runs. On the pooled headline vocabulary, **276 of 317** decision points fall below that gate, leaving **41 measurable** decision points on which every concentration statistic in this paper rests. The excluded 276 are reported separately as coverage rather than folded in; including them would let decision points reached by three or four runs dominate any average.

The gate is not a minor filter, and its size is itself a finding: the corpus is a short shoulder of decisions almost everyone faces and a long tail almost nobody does (*sec:atlas*, panel A). Statistics computed over the whole decision point set would describe the tail, which is exactly where measurement is weakest.

### Concentration statistics

Let a decision point be reached by `\nruns` runs distributed over options with shares `p_1 ≥ p_2 ≥ … ≥ p_m`, `\sum_i p_i = 1`.

**Modal share.** `p1 = p_1`, the share taken by the most common option. A decision point where 95% of runs take one option is not a decision point in practice, whatever its option count.

**Effective number of options.** We use the inverse Herfindahl–Hirschman index [hirschman1964]:

```
\eff \;=\; \frac{1}{\hhi} \;=\; \frac{1}{\sum_{i=1}^{m} p_i^2}.
```

This reads as “how many options this decision point behaves like.” A 95/5 split scores `N_eff = 1.11`, not `2`; an even three-way split scores exactly `3`. The distinction `eq:eff` draws is the one raw option counts destroy: a decision point can be *universal and settled* (a convention—everyone faces it, everyone resolves it identically) or *universal and split* (a live researcher degree of freedom). These are opposite situations that a raw count reports in the same column.

**Stable options.** An option is *stable* at a decision point when it is taken by at least

```
\texttt{STABLE\_SHARE} = 0.10 \quad\text{of the \fork{}'s runs, and at least}\quad
  \texttt{STABLE\_FLOOR} = 3 \quad\text{runs.}
```

The floor is what prevents “1 of 4 runs” from qualifying as stable on share alone.

### Novelty

> **Definition (Novel option).** An option chosen by exactly one run, at a decision point reached by at least `MIN_RUNS` runs.

The rare tail is the point of a multiverse study, and it is the reason the clustering was built with no cap on option count (*sec:vocabulary*). Three questions are asked, in increasing order of how easily they are overclaimed.

**What.** Which decision points do novel options concentrate in, and are they cosmetic variation or substantive divergence?

**Who.** Does any persona arm reach for novel options more often, once corrected for having more runs and longer scripts? Novelty is normalised *per decision*: a run recording 30 decisions has more opportunities to be unusual than one recording 12, so raw novel counts would largely measure script length. Private options—confined to a single arm—are reported per run, and richness is rarefied per `eq:rarefy`.

**So what.** Does a run taking unusual paths report a different answer? This is the question worth caring about and the one most easily overclaimed, so the design is deliberately conservative:

- The outcome side is an **independent extraction** that never touched the decision vocabulary. Effect size and verdict were read off each run's report separately from anything in this pipeline, so a correlation is not the clustering marking its own homework.
- The comparison is **observational**. Runs were not assigned their novelty, and a persona brief influences both the choices and the reported verdict, so arm is reported alongside rather than controlled away. Everything reported is an association.
- Uncertainty is a **bootstrap over runs** (`B = 4000`, percentile intervals), not a parametric test, because the novelty score is a bounded ratio with a lumpy distribution.

### Novelty dose-response

A median split reports one contrast and hides everything else: if the novelty–outcome relation is U-shaped, or flat until a threshold, or driven by a few extreme runs, a two-group comparison shows nothing and is read as “no effect.” Runs are therefore binned into **novelty quintiles**, with the outcome reported per bin with a bootstrap interval (`B = 3000`), alongside both Pearson (linear) and Spearman (monotone) correlations.

The two coefficients are reported together because their *contrast* is diagnostic: a Spearman clearly larger than Pearson is the signature of a monotone-but-curved relation, while both near zero with a visibly non-flat curve points to non-monotonicity.

Position within the script is normalised by each script's own length before binning, because scripts range from **5 to 600 lines** (81 to 591 among the AI runs; median 344, p5–p95 138–449) and raw line numbers are not comparable across runs — this previously read "164 to 507", a range no subset of `data/corpus/coverage.tsv` produces.

### Lifecycle iteration

The lifecycle is drawn as a pipeline and everyone says it iterates, but the iteration is rarely measured, because measuring it requires two things at once: a stage label for every decision, and the order in which decisions were actually written. This corpus has both (*sec:stages*).

> **Definition (Return).** A decision whose DSLC stage is earlier than that of the decision preceding it in the script, separated by more than “TIE_LINES` = 2` lines.

Walking each run in written order and counting returns gives, per run: how many times it went back, how far, and from which stage to which.

**Triggers as rates, not counts.** The *trigger* is the decision immediately preceding a return. It is reported as a **rate**—returns per opportunity—rather than a count, because a decision point appearing in 200 runs precedes more returns than one appearing in 10 whatever its content, so raw counts would be a frequency table in disguise. A decision point needs “MIN_OPP` = 15` successors for its rate to be reported. On this corpus the two orderings do **not** tell different stories: the largest raw trigger — *"which effect-size measure is used to express the exposure's effect on red cards?"*, 161 returns over 195 opportunities — is also the sharpest, at rate `0.826`, which is the maximum over all 37 qualifying triggers. (This previously read that the largest was a common decision point at `0.87` while the sharpest was a rarer one at `0.98`; no trigger in this build has either rate, and the contrast the sentence drew is not supported here. The argument for reporting rates rather than counts stands on its own and does not depend on the two orderings differing.)

**The tie filter.** Two decisions extracted from the same line have no real order, and whichever the sort places second creates a spurious return half the time. Returns spanning `≤ `TIE_LINES“ lines are dropped, which removes about 4% of the raw count.

**The null.** The observed return rate is compared against a permutation null in which decision order is shuffled within runs. On this corpus the observed rate is 44% of what random ordering would give (observed 0.186 against a null mean of 0.327): scripts are strongly forward-ordered, and returns are the *residue* of that ordering, not the baseline. Reporting a raw return rate without this null would invite reading a number below chance as evidence of frequent iteration.

### Garden structure: siblings and gates

A garden *branches*. “At what cut-point?” is not a decision every analyst faces—it is a decision created by having chosen to dichotomise. Treating decision points as independent dimensions yields a lattice, not a garden. Mapping the garden means recovering which decision points are unavoidable and which exist only downstream of a prior choice.

Two screens are run, because the two structures have *opposite* signatures:

| **Structure** | **Co-occurrence** | **What it is** |
|---|---|---|
| **Sibling** | near-zero | one question split into two labels by L3; each run was filed under one label
 or the other. The expected residue of preferring under-merge
 (*sec:vocabulary*). |
| **Gate** | high | `B` is reachable only after choosing option `a` at `A`; runs reaching `A` and
 *not* choosing `a` essentially never reach `B`. |

*Siblings and gates are distinguished by co-occurrence, in opposite directions.* Siblings are screened by near-zero co-occurrence plus label similarity and adjudicated by model call (`15_fork_relation`). Gates are screened by conditional reachability with **Fisher's exact test** and **Benjamini–Hochberg FDR** control [benjamini1995], over pairs that do co-occur. Running only one screen yields a wrong map in a predictable direction: unmerged siblings masquerade as structure, and untested gates leave the garden flat.

Precedence between decision points is taken from median observed position, which is independent of the DSLC labels and validated against them (*sec:stages*).

### Shapley attribution

The final question is how much each decision point contributes to the outcome a run reported. This is a cooperative-game attribution problem [shapley1953, lundberg2017], played over the garden nodes.

**Levels, and why *absent** is one.* A *level* of a decision point is an option chosen by at least “MIN_LEVEL` = 10` runs; rarer options collapse into `other`. No option is read—only counted—so the coarsening is algorithmic rather than a hand-written reading of what the options mean, which is the step at which a result can be authored rather than measured.

Critically, **not reaching a decision point is itself a level**. Requiring complete rows would leave 68 of 204 runs and, worse, would discard the most common thing a run does at a decision point, which is not arrive at it. Not reaching a decision point is a choice—the same silent decision this method treats as a finding everywhere else (*sec:residue*).

**Admission by contrast, not coverage.** Once `absent` is a level, coverage is the wrong admission test: a decision point where 20 runs dichotomised and 184 never went near it is a perfectly good binary contrast. A decision point therefore plays when at least “MIN_LEVELS` = 2` of its levels have `≥ `MIN_LEVEL“ runs, counting `absent`, with at least one being a named option so that nothing qualifies on “did not do it” versus “did something miscellaneous.” Replacing a coverage gate with this contrast gate roughly doubles the player set.

#### Correction: the cross-validation was broken

An earlier version of this report stated that verdict, effect size and z do not
predict out of sample, and that only CI width does. **That was an artifact of a
bug in `cv_r2`, not a finding.**

Each fold rebuilt its design matrix from the analyses in that fold, and
`design()` emits only the levels *present* in the ids it is given. Train and
test folds therefore produced different column sets, which the code truncated to
the shorter width and multiplied — aligning columns by **position rather than
identity**. On this study that misaligned 41–48 of roughly 50 columns in all
five folds, so a coefficient fitted for one option was applied to the indicator
of another and the cross-validated R² measured nothing.

Because λ is *selected* by cross-validation, the damage propagated: with every λ
scoring equally badly the selector took the most regularised (λ = 1000), which
also depressed the in-sample fit.

Corrected, with one design built over all analyses and rows indexed by fold:

| payout | CV R² before | CV R² after |
|---|---:|---:|
| verdict | −0.0086 | **+0.2934** |
| log(OR) | −0.0080 | **+0.0808** |
| z | −0.0124 | **+0.3072** |
| CI width | +0.0008 | **+0.0381** |

λ selected per payout: 30, 30, 10, 100. Player set 36, design `204 × 91`.
Source: `data/audits/shapley_audit_ai+human.merged.forkmerged.merged.induced.r3.osplit.json`
(after) and `…induced.r3.json` (before).


**The decision forks do predict the reported conclusion out of sample.** This
reverses the study's recorded prediction, which is preserved in `study.json`
with the correction attached.

What does *not* change is the per-player picture: **8 of 36 players beat the
permutation null at p < 0.05**, carrying 15 significant (payout, fork) pairs
out of 144. The ensemble predicts; individual attributions remain mostly
indistinguishable from noise, and those are different claims. Restricted to the
17 pivotal forks the same statement is 3 of 17 players and 6 pairs — a weaker
result on a smaller player set, reported here as its own number rather than
substituted for the one above.

**Both variants, since both answer questions asked of this study:**

| | players | verdict | log(OR) | z | CI width | sig players |
|---|---:|---:|---:|---:|---:|---:|
| contrast set (canonical) | 36 | +0.2934 | +0.0808 | +0.3072 | +0.0381 | 8 |
| restricted to pivotal | 17 | +0.2622 | +0.0317 | +0.2457 | +0.0462 | 3 |

Restricting to pivotal forks costs attribution on every payout except CI width
and removes five of the eight significant players. The section below works
through which players those are, and it is the reason the contrast set is the
one reported.

#### What restricting to pivotal forks would have cost

Attribution runs over the **contrast** player set — every fork with two
estimable levels, counting *did not reach* as one — and not over the 17 pivotal
forks. Restricting it to the reported population looks like coherence and was
tested rather than assumed.

Across the four payouts, **eight forks carry at least one attribution that beats
the permutation null. Five of the eight are not pivotal**, and they account for
nine of the fifteen significant (payout, fork) pairs.

| fork | reach | cov | eff_all | eff_reached | options | significant on |
|---|---:|---:|---:|---:|---:|---|
| middle (Medium) skin-tone category | 22 | 0.10 | 1.22 | **1.00** | **1** | verdict, ci_width, z |
| adjustment set expanded as robustness check | 17 | 0.08 | 1.16 | **1.00** | **1** | log(OR), z |
| goalkeepers included or excluded | 26 | 0.12 | 1.26 | 1.17 | 2 | log(OR), z |
| covariates the primary model adjusts for | 15 | 0.07 | 1.15 | 1.77 | 4 | verdict |
| agreement between raters quantified | 33 | 0.15 | 1.37 | **3.64** | 6 | z |

**Read the `options` column.** Two of these forks have exactly *one* recorded
option: every analysis that handled the Medium skin-tone category dropped it and
kept only Light; every analysis that expanded its adjustment set added a
covariate. In the choice sense they are not forks at all — they are **did or did
not**, and the contrast carrying their signal is *absent versus present*.

That is precisely what `eff_all` is built to score low. A fork reached by 22 of
223 analyses is dominated by its absent level, so `eff_all` = 1.22 and it falls
below any pivotal bar. The measure is not wrong; it answers *is this fork
contested*, and these forks are not contested — they are **rare and
consequential**, which is a different property.

`which covariates does the primary model adjust for` is the sharpest case: 11 of
its 15 analyses are `unadjusted, no covariates (crude OR)`. The attribution is
not about *which* adjustment set was chosen. It is about whether the analysis
adjusted at all.

**So the two questions need two filters.** `eff_all > 1.5` selects what the
garden reports as contested; contrast selection selects what can be attributed.
Using the pivotal set for both would have dropped every row in the table above.

**A limit that travels with these five.** They are reached by 7–15% of analyses,
so each attribution rests on 15–33 rows. The defensible reading is *whether
analysts did this at all separates their conclusions*, not a claim about the
corpus at large. `ci_width` on the Medium category, at strength +0.0015, is
significant and small.

#### Is a tree better than the additive surrogate?

The ridge surrogate is additive and cannot represent an interaction — "the
cutpoint only matters if you also cluster". Whether that costs anything is
measurable, and the clean contrast is not ridge against a forest, which
confounds linear-versus-tree with additive-versus-not. Gradient boosting with
**stumps is additive by construction**; depth ≥ 2 is not. The gap between them
isolates the interaction contribution.

Same design, same folds, same seed:

| payout | ridge | stumps (additive) | depth 3 | forest | interaction gain |
|---|---:|---:|---:|---:|---:|
| verdict | **0.262** | 0.213 | 0.064 | 0.254 | −0.149 |
| log(OR) | **0.032** | −0.079 | −0.636 | −0.028 | −0.557 |
| z | **0.246** | 0.236 | 0.114 | 0.209 | −0.122 |
| CI width | **0.046** | −0.018 | −0.075 | −0.015 | −0.057 |

**Interaction gain is negative on every payout**: allowing depth makes
out-of-sample prediction worse, substantially so for log(OR). Ridge also beats
additive stumps everywhere, which is expected rather than surprising — with
purely categorical one-hot columns, linear-on-indicators *is* the saturated
additive model, and boosted stumps only approximate it more noisily.

So additivity is not hiding structure here, and the per-fork attribution is not
understating how choices combine. That is a positive result for the method
rather than an absence of one.

**The honest limit:** this is 204 analyses over 56 sparse columns. Interactions
may exist and be unmeasurable at that size. The claim is *no detectable
interaction signal at this n*, not *no interactions*. `surrogate_form.py`.

#### Which forks play

A fork is admitted as a player when at least two of its levels have at least
`MIN_LEVEL` runs, counting *not reaching the fork* as a level. This replaced an
earlier coverage gate, and the replacement is deliberate: not reaching a fork is
not missing data but a choice — the same silent decision treated as a finding
elsewhere — and a fork where 20 analyses dichotomised and 184 never went near it
is a perfectly good binary contrast.

That leaves an incoherence worth testing: the study *reports* on pivotal forks,
while attribution ran over a larger contrast-selected set. Both were computed.

| payout | contrast (36 players) | | pivotal (17 players) | |
|---|---|---|---|---|
| | R² | CV R² | R² | CV R² |
| verdict | 0.4858 | **+0.2934** | 0.4722 | **+0.2622** |
| log(OR) | 0.2892 | **+0.0808** | 0.1096 | **+0.0317** |
| z | 0.5691 | **+0.3072** | 0.4554 | **+0.2457** |
| CI width | 0.1462 | +0.0381 | 0.2058 | **+0.0462** |

Designs `204 × 91` and `204 × 56`; λ selected per payout by cross-validation.


The seventeen pivotal forks are a strict subset of the thirty-six and the
leading attribution is unchanged — standard-error estimation dominates the
verdict payout in both, at **+0.1146** (p = 0.000) on the contrast set and
**+0.1635** (p = 0.000) restricted. But **conclusions do move**, in both
directions, and that is the reason to report the wider set:

- **Verdict, z and log(OR) all predict out of sample**, on either selection.
  The former claim that they do not was an artifact.
- **Restricting to pivotal forks costs prediction on three payouts of four** —
  verdict 0.2934 → 0.2622, z 0.3072 → 0.2457, and log(OR) 0.0808 → 0.0317, the
  last a loss of about 60%. It buys prediction only on CI width
  (0.0381 → 0.0462).
- **It also removes five of the eight forks that beat the permutation null**,
  and nine of the fifteen significant (payout, fork) pairs.

So restricting does not buy coherence for free, and the earlier sentence *"the
study uses the pivotal set"* no longer describes what is reported: attribution
is reported over the contrast set, with the pivotal restriction shown beside it
as a sensitivity.

**CI width remains the weakest-predicted payout, not the strongest.** The
earlier reading — that what analysts move is precision rather than direction —
inverted once the cross-validation was fixed: the verdict is now the
best-predicted payout on the contrast set (+0.2934 against +0.0381). The
leading player is the same either way, and it is how standard errors are
estimated.

**Estimator.** A ridge surrogate [hoerl1970] is fit on one-hot level indicators in closed form, with the intercept unpenalised. Because the surrogate is additive, the Shapley value has a closed form—no sampling over coalitions is required:

```
\shap_j(x) \;=\; \mathrm{contrib}_j(x_j) \;-\; \overline{\mathrm{contrib}}_j,
```

i.e.\ the fitted contribution of the level this run took at decision point `j`, minus the mean contribution over runs at that decision point.

Payouts are computed for the reported verdict, `\log(\mathrm{OR})`, the `z` statistic, and the confidence-interval width. Uncertainty is a bootstrap over runs, `B = 2000`, percentile 95% intervals. The ridge penalty `\lambda` is **chosen by cross-validation per payout** over the grid `\{1, 3, 10, 30, 100, 300, 1000\}` rather than fixed: on the `204 × 91` design, `\lambda = 1` is essentially unregularised. (This previously read `204 × 83`, a figure from an earlier player set; the design shape is reported by `H4` in the Shapley audit and is `[204, 91]` for the canonical tag, `[204, 56]` restricted to pivotal.)

**The additivity assumption.** Equation `eq:shapley` holds because the surrogate is additive, and an additive surrogate *cannot* represent an interaction such as “dichotomising only matters if you also cluster.” This is an assumption, not a finding. The companion audit reports how much of each payout the surrogate actually explains, which is the quantity that bounds how much the attribution can be trusted.

## Visualization as analysis

The figures in this project are not renderings of results computed elsewhere. In several cases the layout *is* the estimator: a position on the page is the solution to an optimisation problem, and reading distance off the figure is reading a statistic. This section documents them as methods.

Three conventions apply throughout and are stated once here.

- **Area encodes traffic.** Node radius is `\sqrt{\text{runs}}`, so that *area* is proportional to the number of runs passing through. Radius-proportional sizing would square the visual weight of the largest nodes twice over.
- **Sparse edges are omitted, not thinned.** Only routes walked by at least `MIN_LINK` runs are drawn. On this corpus 87.7% of decision points (278 of 317) are reached by under 5% of runs — this previously read 84%, a figure traceable to a docstring in `scripts/circle.py` rather than to any artifact; connecting them all produces a hairball that hides the structure. Omitted nodes remain visible as unconnected dots, which is the honest presentation—the decision point exists and was rarely walked.
- **Colour carries one signal.** Structural elements are monochrome (shades of a single hue for stages) so that persona colour is the only categorical signal competing for attention.

### The circle: stages as sectors, runs as closed tours

The circular map assigns each DSLC stage an angular sector, places decision points as nodes within their sector, and draws runs as routes.

**Why a circle.** A circle has no privileged end. This suits a lifecycle that the iteration analysis (*sec:iteration*) shows to be forward-ordered at only 44% of what random ordering would give—that is, substantially but not overwhelmingly sequential. A left-to-right pipeline diagram would assert an ordering the data only partly supports.

**The closure edge.** Each run's last decision point is linked back to its first, so a run is a closed tour rather than a line with two loose ends. This edge is drawn *dashed*, because it is a presentational device and not an observed transition—a distinction the figure must carry, or the closure would be read as a measured return.

**The analysis the colouring enables.** Once routes are coloured by persona, the natural question is whether the colours separate: does a persona walk a route the others do not? Every earlier persona comparison in this project asked what arms *chose*; this asks where they *went*, which no other analysis answers. It is tested per (route, persona) against the persona's overall share of runs.

### The fork atlas: four panels

The flow views answer “what did runs do.” The atlas answers “which decisions are worth arguing about,” which needs different pictures. Each panel separates something the summary tables run together.

- **A — The fan.** — Every node ranked by coverage on a log axis. The claim that a handful of decisions are faced by almost everyone while several hundred are faced by almost nobody is one line here, and the shape—a short shoulder then a cliff—is the finding.
- **B — The map.** — Coverage against effective number of options `eq:eff`. This is the panel that matters, because it separates *universal and settled* from *universal and split*—opposite situations that every scalar summary reports identically.
- **C — The spectrum.** — For the highest-coverage decision points, option shares sorted descending with the singleton tail marked. Distinguishes “one modal choice plus noise” from “genuinely divided,” which panel B compresses into a single number.
- **D — Where disagreement lives.** — Effective options per DSLC stage. If the lifecycle has a contested phase, it appears here.

Panels B, C and D exclude decision points below `MIN_RUNS`, for the reason given in *sec:counting*.

### Interactive viewers

One HTML viewer is generated, `figures/forkscope.html`, with four tabs: the Garden (every decision point on a ring by lifecycle stage, with the highways analyses travelled), Pivotal Forks (the atlas panels and the attribution tables), Lifecycle (the iteration analysis) and Corpus Viewer (one analysis at a time, its exon/intron map and the decision points it visited). It computes no statistic of its own: every number on it is read from an artifact under `data/`, and `scripts/forkscope.py` regenerates it in seconds.

### Figure provenance

Figure filenames in this project do *not* carry the vocabulary tag, while the underlying analysis files do (*sec:repair*). A rebuild against a different corpus scope therefore overwrites figures in place with visually similar output computed on different runs. We flag this as a methodological hazard rather than a cosmetic one: it is the one place in the pipeline where provenance is carried by the build command rather than by the artifact. Any figure reproduced in a publication should be exported with its vocabulary tag recorded alongside.

## Validation

Two mechanisms carry the validation burden: every analysis stage ships with a named audit that runs beside it, and a single gate decides whether the two corpora may be pooled at all.

### Audit companions

Stages 5 and 6 of the workflow exist so that **no reported number comes from a command someone typed once**. Each analysis script has an audit companion that runs immediately after it and prints named checks; a stage whose audit fails stops the workflow.

| **Family** | **Checks** | **Script** | **Subject** |
|---|---|---|---|
| A | A1–A9 | `audit_clusters.py` | the induced clustering |
| R | R1–R4 | `repair_clusters.py` | normalisation and exclusivity splits |
| I | I1–I6 | `audit_iteration.py` | returns, triggers, and the stage/position check |
| G | G1–G6 | `audit_garden.py` | siblings, gates, and tree structure |
| H | H1–H6 | `audit_shapley.py` | surrogate fit and attribution stability |
| E | E1–E6 | `audit_ablation.py` | the code-ablation gate |

*Audit families. Each runs beside its analysis, not on request.*

The pairing is not decoration. The iteration analysis reports a headline return rate that is meaningless without its permutation null (*sec:iteration*), so the two ship together and the null cannot be omitted by running one command and not the other.

### Audit design principles

The audit suite is built around a set of questions that each arose from a specific failure in this project. They are worth stating because they generalise beyond it.

1. **Could this measure see the failure it is ruling out?** A check that cannot fail is not evidence.
2. **Does this check use a signal the pipeline used to build the thing?** If so it marks its own homework—the reason DSLC stage is assigned blind to position (*sec:stages*).
3. **Was this sample drawn, or selected?**
4. **Can the test resolve the threshold it is compared against?** A permutation `p` cannot fall below `1/(B+1)`, which is what motivates the escalation of draw counts in every permutation test here.
5. **Does the statistic mean what the sentence says?**
6. **Is the claim's scope the test's scope?**
7. **Has this check ever actually run—here, on this?**
8. **Are you checking the property, or something correlated with it?**

A methodological rule follows from these and is enforced procedurally: iterate on the *build*, never on the *thresholds*. Adjusting a cutoff until a check passes manufactures the result.

### Gate 5.4: code ablation

#### The question

Decision extraction is code-anchored (*sec:corpus*), so the pooled analysis carries only 19 of 31 human teams while the prose-only teams contribute zero decisions and **1,123 prose spans** across the 11 of them that were distilled. Before any AI-versus-human claim can be made, one question must be answered: *can decisions be recovered from prose alone?*

The gate as specified: hide the script for 30% of runs that have one, re-derive the decisions from prose, and require that at least

```
\texttt{GATE} = 0.85
```

of them land in the same option; otherwise the analysis must be split rather than pooled.

#### Why the ablation is already built

No re-extraction is performed. Prompt `02` segments the write-up *having never seen the script*, and its claims carry polarity (*sec:extraction*). Every run therefore already carries two independent accounts of itself:

| **code channel** | `code_spans.json`, `kind == "decision"` |
|---|---|
| **prose channel** | `prose_spans.json`, `kind == "claim"`,
 polarity `∈ \{`did`, `did_not`\}` |

The prose channel is blind to the code **by construction, not by a procedure applied afterwards**. This is a stronger design than hiding files and re-running, because there is no path by which the script could leak into the prose segmentation through a cache.

#### What is measured

Four quantities, deliberately separated because they fail differently:

- **Recall** — of the decisions the code channel found, how many does prose find?
- **Agreement** — of the decisions both channels found, how many are the *same option*?
- **Conflict** — how many are the same question with a *different* answer? This is the quantity that would invalidate pooling.
- **Vaguer** — same choice, too underspecified to pin to an option. Not a disagreement—a loss of resolution, bearing on the granularity at which prose-only runs could be pooled.

The separation of *conflict* from *recall* is the important one: prose being silent is a coverage problem, whereas prose contradicting the code is a validity problem, and only the second invalidates pooling.

#### The E-checks

| **Check** | **Passes when** | **Rules out** |
|---|---|---|
| E1 blinding | flipped fraction `∈ [0.35, 0.65]` | the judge favouring whichever channel is presented first; channel order is
 randomised per run and agreement compared across the two orders |
| E2 leniency | null recall `< 0.25 ×` observed | a judge that matches anything: run `i`'s code is matched against run `j`'s
 prose, where every match is false by construction |
| E3 length | `|ρ_{\text{prose}}| < 0.5` | recall being driven by how much prose a run happens to contain |
| E4 corpus split | *both* corpora clear `GATE` | a pooled average that passes while one corpus fails—the case the check
 exists to catch |
| E5 spread | `≥ 60%` of runs individually clear `GATE` | an aggregate carried by a few large runs |
| E6 degeneracy | `0.05 < \text{recall} < 0.95`, top run's share `< 0.15` | matching everything, matching nothing, or one run dominating |

*The six ablation checks. E2 and E4 are the load-bearing ones: E2 calibrates the agreement rate against a null in which all matches are false, and E4 prevents pooling on a favourable average.*

E2 deserves emphasis. Without a mismatched-run null, an agreement rate has no calibration at all: a permissive judge produces a high agreement rate on unrelated pairs just as readily as on related ones. The null is what converts the within-run rate from a number into evidence.

E4 is the check that carries the pooling decision. A pooled average can clear `GATE` while one corpus fails it, and pooling is licensed only if *both* clear independently.

## Reproducibility

### Determinism without temperature or seed

The model is reached through a command-line interface that exposes **neither a temperature nor a seed**. Determinism therefore cannot come from decoding parameters, and comes instead from a content-addressed cache. Each response is stored under

```
\text{key} \;=\; \mathrm{sha256}\big(
    \text{prompt} \,\|\, \text{model} \,\|\, \text{payload} \,\|\, \text{schema}
  \big),
```

so re-running an unchanged stage costs nothing and returns byte-identical output. **The cache, not the model, is what makes this reproducible.** Editing a prompt changes its hash and invalidates the affected entries automatically, which is the intended behaviour.

A single module is the only code that talks to a model. It separates two failure kinds that require opposite responses:

- **Transport failures** (rate limits, timeouts, non-zero exit): the call never produced content, so the remedy is to wait and retry with the prompt unchanged, and the attempt budget is not consumed.
- **Content failures** (unparseable output, schema violation, failed semantic invariant): the remedy is to retry with the *specific* complaint appended, so the retry is informed rather than a coin flip.

Conflating the two once cost 154 of 204 runs in a single throttling burst: instant retries inside a rate-limit window exhausted the content-attempt budget without ever reaching the model.

Semantic invariants a JSON schema cannot express—“these line ranges must partition `1..n`”—are enforced in the same retry path (*sec:retryable*). Because such a check is a callable and cannot enter the cache key `eq:cachekey`, it is *re-applied to cached results* on read: a cached entry that fails a since-tightened invariant is discarded and the call redone. Without this, tightening an invariant would silently grandfather in every record already cached under the looser rule.

### Seeding and resampling

All sampling and bootstrapping is seeded (“SEED` = 20260822` throughout). Stratified sampling over persona arms is deterministic by construction—arms in fixed order, runs sorted within arm, round-robin—so no random number generator is involved and the sample is identical on every machine.

### Vocabulary lineage

Every repair pass writes a new tag rather than overwriting (*sec:repair*), and each analysis output records the vocabulary file it was computed from. A reported number can therefore always be traced to the vocabulary that produced it, and superseded vocabularies remain on disk. This is what makes it possible to recompute a historical figure rather than merely describe it.

### Provenance classes

Runs added to the garden after the initial build carry a provenance tag:

| `corpus` | extracted from an analysis a real analyst wrote |
|---|---|
| `itinerary` | assembled entirely from options the corpus contains |
| `authored` | contains an operation no run in the corpus performed |

Non-corpus runs *count*: an assembled run is a person's deliberate choice, executed, which is what a corpus run also is. Excluding them would treat a human's choice as less real than an analyst's and would mean the garden could never grow. What provenance buys is the ability to *tell*: every concentration statistic is reported both ways once any non-corpus run exists, so a headline that moves is visible. The hazard was never that assembled runs count; it is a number drifting silently as paths are walked, and the remedy for that is visibility rather than exclusion.

### Two hazards in this scheme

Auditing the pipeline against itself surfaced two reproducibility hazards that the mechanisms above do *not* cover. Both are properties of the method rather than incidental bugs, and both are invisible in the outputs, so we state them explicitly.

#### The cache key records a model alias, not a version

In `eq:cachekey` the `model` component is the *alias* string passed to the CLI (e.g.\ `sonnet` for bulk extraction, `opus` for adjudication), not a resolved model version. The cache entry and the call log both record the alias. No concrete version identifier for the extraction model appears anywhere in the repository.

The consequence is that if an alias is re-pointed to a newer model, existing entries continue to hit while new calls are served by a different model, and a single dataset can silently mix model versions with nothing recording the mix. The cache guarantees *that a re-run reproduces the earlier answer*; it does not guarantee *that two runs were performed by the same model*.

We observed the practical form of this. Re-executing the downstream stages five days after the original build, on an identical 80-run sample with identical inputs (1{,}363 code decisions, 3{,}329 prose spans), reproduced only 688 of 864 matched decisions exactly—79.6% stability, or 87.2% among decisions matched in both runs. The disagreement was directional rather than symmetric: 25 transitions from `same_option` to `vaguer` and 8 to `same_fork_different_option`, against only 7 in the reverse direction. Strict agreement fell from `0.9517` to `0.9077` and check E4 moved from PASS to REVIEW.

We cannot determine from the recorded artifacts whether the alias resolved to the same model version on both dates, because that information was never recorded. Ordinary sampling nondeterminism would also produce disagreement, though it would be less likely to be so one-sided. The methodological recommendation is therefore unambiguous: **record the resolved model version and client version at call time, and place the version—not the alias—in the cache key**. A genuine run-to-run variability study should then be conducted deliberately, by disabling the cache and comparing, rather than inferred from an incidental rebuild.

#### Metadata recovery depends on an untracked input

Persona arm is a property of *where a run lives* in the source corpus (*sec:corpus*), recovered by globbing the raw corpus directory. Records written before the arm field existed carry no arm, and the roll-up step recovers it by re-reading the corpus layout rather than by re-running any model call—which is correct in principle, since the arm is always derivable and never worth a model call to restore.

The hazard is the failure mode. The raw corpora are fetched rather than vendored, so the source directory may be absent. When it is, the recovery lookup returns nothing and the fallback silently retains the record's existing value—which, for these records, equals the corpus name. There is no exception and no warning.

The observable consequence is a spurious seventh arm named `ai` holding 43 runs that in fact belong to the five personas. The same committed data, the same code, and the same command produce different per-arm tables depending only on whether an untracked directory happens to be present on the machine. Totals are conserved exactly, so nothing in the output indicates a problem; only the arm attribution is wrong, and it is wrong in a direction that matters, because the unattributed runs were the noisiest in the corpus.

Two remedies follow: repair the arm at source in the per-run records rather than recovering it downstream on every read, and make a failed recovery a loud failure rather than a silent fallback. More generally, *any* pipeline step that reconstructs metadata from an optional input should treat the absence of that input as an error, because the alternative is a plausible-looking result computed from a degraded label.

## The charting collaboration

Charting a garden is itself an analysis, with its own forking paths. Every
threshold in this report is a point where a competent analyst could have chosen
otherwise, and the pipeline cannot choose for them. This section records who
decided what.

### Three gates

| gate | when | artifact |
|---|---|---|
| **Scope** | before any run | `study.json`, `policy.json`, `INTAKE.md` |
| **Settle distillation** | after extraction, before charting | `locks/distill.lock.json` |
| **Settle charting** | after the vocabulary and its audits | `locks/chart.lock.json` |

A lock stores a **content hash** of the layer it settles, not a note. The
failure it prevents is silent: re-run distillation after settling it and every
charting number rests on an extraction nobody reviewed, with nothing erroring
and every figure rendering.

Distillation is settled. Charting is **not**, and that is the correct state. It
was previously described here as *blocked on the human benchmark*; that
benchmark has since run (see [Reliability: what the measurements
license](#reliability-what-the-measurements-license)), and its fork-layer result
does not clear the gate — human raters agree no better on stable fork pairs than
unstable ones, so fork instability is not accounted for by ambiguity a person
can see. Charting remains unsettled on that evidence rather than for want of it.

### The decisions a human made

Recorded in `policy.json`, each marked *decided* or *implicit*, where implicit
means a default nobody argued with.

| decision | value | consequence if set otherwise |
|---|---|---|
| distillation similarity level | lenient | verbatim 0.176, core 0.895 — a five-fold swing in the headline |
| same-run span threshold | 5 lines | 76 of 96 same-run merges are over-merges above it |
| singleton options | kept, as *novel options* | excluding them moves by-option fork agreement 0.31 → 0.69 |
| exclusivity required | yes, violation reported | **86% of runs** violate it, dominated by the skin-tone exposure fork at 158 of 223; the rule makes V2 an exhibit, not a constraint. |
| pivotal threshold | coverage ≥ 25% and **>1.5 effective options** (`policy.json:forks.pivotal`) | **17 forks qualify**; 18 clear the coverage floor alone |
| stability's role | **diagnostic, not objective** | tuning for it is refused without a held-out split and external criterion |
| replicates per parent | 5, pre-committed | 2 would give 1 df, an sd compatible with anything |

The last two are the load-bearing ones. Fork induction can be driven toward
ARI 1.0 by merging almost nothing, which raises the number and destroys what it
measures; and extending a replicate batch after seeing the spread is optional
stopping on the quantity being reported.

**Four** decisions remain **implicit and unexamined**, listed in
`policy.json:_open`: the Jaccard threshold of 0.5 governing every cross-build
option match, the review-queue cap of 60, the prohibition on interleaved spans,
and the unmeasured reliability of `outcomes.json`. A fifth was found and closed
on 2026-09-08: several scripts had computed their own effective options by
summing run-set sizes per option, which counts an analysis once per option it
holds and inflates the figure. Effective options is now defined once, in
`vocab.fork_stats`, as one vote per analysis at its modal option, and every
reported figure reads that definition; the superseded "11 pivotal forks" figure
in *tab:policy* above was that defect's symptom. The human-benchmark packet was
generated before the sweep, so the effective-option counts printed on its
sheets predate the canonical definition.

### Errors, by how they present

Three classes, needing three mechanisms — treating them alike is why problems
surfaced late. **Loud-wrong** crashes and gets preflight. **Unknowable** needs a
person and gets a ranked, capped queue. **Silent-wrong** completes with the
wrong content and gets a guard at the point of use, never a report: passing the
natural `--corpus ai,human` renders the *unrepaired* vocabulary with every stage
exiting 0. The full taxonomy is in `docs/DECIDING.md`.

## Measuring agreement between two extractions

Before any stability number can be interpreted, a prior question has to be settled: *what does it mean for two extractions to agree?* The answer is less obvious than it appears, and the choice of metric changes the conclusion more than the data does.

### The problem

Ask a model to segment the same script twice and it finds substantially the same operations while drawing slightly different boundaries around them. A decision spanning lines 44–51 in one build spans 44–52 in the other, because a blank line or a trailing `print` was judged part of the operation or not.

Every strict partition metric—Adjusted Rand Index, Variation of Information, exact per-line agreement—charges that one-line difference at close to the same rate as it would charge finding a *completely different* decision. Such a metric answers “did the two builds draw identical boundaries?” when the question that matters downstream is “did the two builds find the same decisions?” Those are different questions with different answers, and conflating them is a measurement error rather than a modelling choice.

### Four levels

We therefore match extracted spans across builds at four levels of strictness, and report all of them. Let `L_A` and `L_B` be the sets of source lines covered by two spans.

| **Level** | **Rule** | **Question it answers** |
|---|---|---|
| verbatim | `L_A = L_B` | would the two builds produce byte-identical artifacts? |
| lenient | `J(L_A, L_B) ≥ \tau` | did both builds find this decision, allowing the boundary to move? |
| core | `|L_A ∩ L_B| / \min(|L_A|,|L_B|) ≥ \tau` | did both find it, allowing one to split or absorb what the other kept whole? |
| text | token overlap of descriptions | and do they describe the same operation? (a lexical check, not a claim) |

*Agreement levels, with `J` the Jaccard index and `\tau = 0.5` throughout. Matching is greedy on descending overlap and is deterministic.*

The *core* level is deliberately asymmetric. A three-line span wholly inside a thirty-line one scores `1.0` by containment and `0.1` by Jaccard, and containment is the right reading when one build split a decision the other kept whole: the smaller operation was found, not missed.

### The gap is the measurement

On a replicate of the distillation stage, the three levels disagree sharply:

| **Level** | **Matched** | **Precision** | **Recall** | **`F_1`** |
|---|---|---|---|---|
| verbatim | 97 | 0.178 | 0.174 | 0.176 |
| lenient | 393 | 0.721 | 0.706 | 0.713 |
| core | 493 | 0.905 | 0.885 | 0.895 |

*Decision-level agreement between two independent distillations of the same **30** runs (557 decisions in one build, 545 in the other). Median boundary jitter among leniently matched pairs: **1 line**. **75%** of lenient matches are not verbatim. Source: `stability/data/q1_distill.json`.*


A verbatim-only report (`F_1 = 0.18`) would conclude that extraction is hopelessly unreliable. A permissive-only report (`F_1 = 0.89`) would conclude it is nearly perfect. Neither is the finding. **The finding is that the two builds recover largely the same decisions and disagree about where those decisions end**, and it is visible only because both levels are reported together. The median disagreement among matched pairs is a single line.

We state the consequence generally, because it is not specific to this corpus. Any study reporting LLM extraction reliability with a strict metric alone will report instability that is mostly boundary jitter; any study using a permissive metric alone will conceal genuine disagreement. The pair, and the gap between them, is the honest form.

### What is not claimed

None of these levels is semantic adjudication. Line overlap is a structural proxy and token overlap is lexical; two spans can overlap heavily and mean different things, and the text-overlap figure is evidence *against* a match rather than proof of one. The proper use of these levels is to reduce the number of pairs a model or a person must judge—the same pattern the ablation gate uses (*sec:ablation*)—not to replace that judgement.

The bracket should be read as a bracket. Containment is permissive enough that `0.895` is best treated as an upper bound and `0.713` as the defensible headline; the true agreement is bounded, not pinned. (These read `0.886` and `0.653` before the 2026-09-08 correction above.)

## Stability under replication

*sec:reproducibility* described how determinism is obtained from a model that exposes neither temperature nor seed: a content-addressed cache `eq:cachekey`. That guarantee is real but narrow. It establishes that *a re-run reproduces the earlier answer*; it does not establish that *two independent runs would have agreed*. This section measures the latter.

### Replicate versus scope change

Two builds can differ for two unrelated reasons, and the artifacts are indistinguishable either way:

- a **replicate** re-calls the model on identical corpora and identical distilled input, so every difference is run-to-run variability;
- a **scope change** pools different corpora, so differences confound variability with the effect of the corpus.

Conflating the two is the central hazard here, so each comparison reads the corpora from the vocabulary headers, classifies itself, and records the verdict; the accompanying audit declines to accept a scope comparison in place of a replicate.

**Isolation.** Forcing fresh calls with `nocache` would be wrong: it skips the cache *read* but still *writes* to the same key, so a replicate run in place would overwrite the baseline while measuring it. Replicates therefore run under a separate study root with an empty cache – every call misses, and the baseline is unreachable by filesystem layout rather than by remembering a flag.

### Estimators

**Partition agreement.** Both builds partition the *same* decision instances, keyed on run, line and a text prefix, and verified identical across builds. Vocabulary agreement is therefore exact arithmetic on two labelings of one item set, needing no matching heuristic and no model calls. This matters because the obvious alternative—matching option labels by string or embedding similarity—reimports the failure the pipeline rejects for clustering (*sec:vocabulary*): roughly 95% of option labels are unique, so a lexical match rate measures phrasing rather than agreement. Semantic adjudication is reserved for *classifying* disagreements as merge, split or genuine difference.

Three metrics are reported because they fail differently. The **Adjusted Rand Index** gives chance-corrected agreement on whether each pair of instances is co-clustered. **Variation of Information**, `H(A|B) + H(B|A)`, is a true metric on the space of partitions and so obeys the triangle inequality—which ARI does not, and which matters once there are three builds to compare. **B-cubed** precision and recall are per-instance and therefore decompose: precision above recall means the second build *split* what the first held together; recall above precision means it *merged* what the first held apart. Direction is taken from two independent signals—the B-cubed asymmetry and the raw cluster count—and reported as ambiguous when they disagree, rather than asserted from a gap inside the noise.

**Distillation agreement.** Code segmentation is an exhaustive, exclusive partition of lines `1..n` (*sec:retryable*), so two segmentations of one script are two labelings of a fixed item set and per-line agreement is exact. Prose is exhaustive but not exclusive, so that channel is compared on counts and span boundaries instead. Counts are reported separately from structure, because silent decisions and misalignments are *residues* of an alignment (*sec:residue*) and a residue is more fragile than what it is left over from.

**Highway agreement.** Fork labels are re-induced on every build, so the same question returns worded differently and label matching would score a rewording as a miss. Forks are matched instead by the instances they share, with the Jaccard overlap reported so a weak match stays visible; the mapping is deliberately not a bijection, since forks legitimately split and merge and forcing one-to-one would conceal exactly that. Traffic agreement is Spearman rank correlation over overlapping dyads: the question is whether busy routes stay busy, not whether counts are identical.

### Results

#### The alignment judge

Prompt `16` was called twice on an identical 80-run sample—the same 1{,}363 code decisions and 3{,}329 prose spans—five days apart, with no change to corpus, code or prompt.

| **Quantity** | **Value** |
|---|---|
| matched in either run (union) | 864 |
| identical partner *and* verdict | 688 |
| same partner, different verdict | 33 |
| different partner, same verdict | 61 |
| both differ | 7 |
| agreement conditioned on both matching | 0.872 |
| **stability over the union** | **0.796** |

*Alignment-judge stability across two genuine replicates. The union is the honest denominator; conditioning on decisions both runs matched selects the easy cases.*

The verdict transitions are asymmetric, which makes this a **severity shift** rather than symmetric noise: 25 moves from `same_option` to `vaguer` and 8 to `same_fork_different_option`, against 7 in the reverse direction. Downstream, strict agreement fell from `0.9517` to `0.9077` and gate check **E4 moved from PASS to REVIEW** (*sec:ablation*)—a gate verdict changing between two runs of identical code on identical data. Whether the 176 disagreements are edge cases is a question about content rather than one a summary statistic answers, so a stratified sample is provided for human adjudication.

#### One finding, stated once

The measurements that follow are instances of a single result, and it is the central methodological claim of this paper:

> **Aggregate structure on the well-populated core is reproducible. The rare tail is not. And the filters that make analysis possible are the same filters that select the reproducible population.**

The last clause is the uncomfortable half. The coverage gate “MIN_RUNS` = 10` (*sec:counting*), the fork-matching threshold, and the reporting filter on effective options were each introduced for independent analytical reasons. Each turns out to exclude precisely the population where the pipeline does not reproduce. The reported analyses are therefore better supported than the whole-vocabulary numbers suggest, and those exclusions are doing more work than their stated rationale claimed.

#### The vocabulary, measured layer by layer

The vocabulary is two stacked clusterings—decisions into options, options into decision points—and a decision point score computed over decision instances conflates them: if two builds split an option differently, its instances land in different decision points even when both builds made the identical decision point judgement. Measuring each step over the items it actually clusters separates them.

| **Layer** | **Items** | **ARI** |
|---|---|---|
| options over decisions | 3{,}946 | 0.853 |
| decision points over options, unweighted | 497 | 0.307 |
| decision points over options, instance-weighted | — | 0.852 |
| *(confounded)* decision points over decisions | 3{,}946 | *0.695* |

*Layered agreement. The confounded figure sits between the two weightings, as it must.*

The gap between weightings is size. 64% of matched options are singletons, 194 of 255 decision points hold exactly one option, and by-option ARI rises monotonically with option size—`0.31` at `≥ 1` instance, `0.69` at `≥ 5`. Decision point induction is a coin flip *for the rare tail* and about as reproducible as option merging for the options that carry the corpus. Per run, where no cross-run matching is needed, option grouping is essentially perfect (median ARI `1.000`; 175 of 223 runs identical) while decision point grouping is not (median `0.590`).

#### Repair converges the builds

Repair contracts the vocabulary (`463 → 317` decision points in one build, `489 → 351` in the other), and contraction changes agreement mechanically. A null that randomly merges each base vocabulary to the repaired granularity, matching the observed cluster-size distribution, separates the two:

| **Level** | **Base** | **After repair** | **Null** | **`z`** |
|---|---|---|---|---|
| option ARI | 0.646 | 0.853 | `0.187 ± 0.014` | 46.8 |
| decision point ARI | 0.565 | 0.695 | `0.219 ± 0.004` | 122.0 |

*Repair against a size-matched random contraction, 200 draws, `p < 0.005` at both levels.*

Repair is a genuine canonicaliser rather than granularity arithmetic. Note the direction of the confound: random contraction *destroys* agreement between two different builds (`0.565 → 0.219`), so repair must overcome a mechanism that would otherwise cost it a third of its agreement.

#### The decision points{ results are reported on}

Reported analyses cover decision points with coverage `≥ 25%` and effective options `> 1.5`. Qualification is computed independently in each build—never by applying one build's list to the other, which would assume the answer.

Of the ten qualifying decision points in the first build, **seven** qualify again in the second (four of them merged two-to-one, the recoverable direction; three scattered). Where both builds consider a decision point important they agree almost exactly on its membership (ARI `0.975`). Their *statistics* drift considerably more than their membership: median change in effective options `0.22`, maximum `10.75` (these previously read `0.67` and `11.36`; `0.67` was the first row of the fork list, not the median).

So *which* decision points matter is roughly `70%` reproducible; *what they contain* is highly reproducible once both builds agree they matter; *how contested they look* is not, and effective-option counts should be quoted as ranks or with stated uncertainty. With `n = 10`, every rate moves by `0.1` per decision point.

#### Highways and personas

Among the **42 comparable routes**—of 225 drawn—traffic rank correlation is `ρ = 0.951` against a permutation null shuffling traffic across the same dyads (`z = 6.08`, `p < 0.001`). Stratified by traffic, the low half (3–13 runs) reproduces at `ρ = 0.904` and the high half at `0.880`, so the correlation is not carried by a few large edges.

The denominator must be stated. 180 of 225 routes could not be compared because an endpoint decision point had no confident match, and those routes are systematically sparser (median traffic 5 against 13; rank-sum `z = +4.36`). Their reproducibility is *unmeasured*, not measured-and-good.

Per-cell persona enrichment does not reproduce—1 of 10 survives, at identical corpus scope. But an omnibus test asking whether runs of the same persona walk more similar routes is strongly positive and stable across builds (`z = 10.25` and `10.46`; `+11`–`12%` over the between-persona baseline; `p < 0.001`), and survives a different vocabulary granularity. **Personas do walk different routes**; *which particular edge* carries the signal is not identifiable at this sample size. The enriched cells are scan output and belong in an exhibit rather than among the findings.

#### Scope effect, reported separately

Comparing the pooled and AI-only vocabularies isolates the effect of the human corpus, not run-to-run variability, and is labelled accordingly: option-level ARI `0.865` (VI `1.17` bits, B-cubed `F_1 = 0.786`) and fork-level ARI `0.756` (`F_1 = 0.709`).

Two findings are worth carrying forward. First, **the highways are more stable than the vocabulary that carries them**: only 29% of forks match at Jaccard `≥ 0.5`, yet among the 64 dyads that do match, traffic rank correlation is `0.928`. The route structure survives a re-wording of its parts.

Second, **the pooled persona null is mis-calibrated**. Only 1 of 10 persona enrichments reproduces, and the cause is arithmetic rather than noise: removing 19 human runs raises every AI persona's corpus share by exactly `× 1.0931`, and recomputing each enrichment against the corrected baseline weakens all ten by factors of `1.5` to `5.4`. The `human` label sits in the persona shuffle pool (*sec:circle*) although no human run can carry a persona, which deflates every persona's expected share and overstates enrichment. Persona claims should be read on the AI-only build.

### Instability as an audit signal

An unstable merge is a suspect merge. Where one build groups two decisions into a single option and another does not, the pipeline has answered “same action?” both ways, which is exactly the evidence a human review round wants and is obtained free once two builds exist.

The response follows the asymmetry already established in *sec:vocabulary*: over-merge is invisible in the output and unrecoverable, under-merge is visible and fixable. An unstable pair therefore defaults to **unmerged** and routes to review. Majority vote across three builds would silently retain two-of-three merges, which is precisely the over-merge that the split-never-merge rule exists to prevent. Thresholds are set from the first replicate and stated as such; they are not adjusted until checks pass, which would manufacture the result (*sec:validation*).

### Limitations of this measurement

- **One replicate pair per stage.** Distillation and vocabulary stability **have** been measured on genuine replicates — `stability/data/q1_distill.json` (30 runs, `comparison_type: replicate`) and `stability/data/q3_replicate_r3.json` — and this report quotes both. The limitation is narrower than previously stated here: it is that each rests on a *single* replicate pair, so the figures carry no interval, and the scope comparison does not substitute for more pairs. (This bullet previously read that both "remain unmeasured", contradicting the numbers reported two sections above it.)
- **`K = 2` cannot attribute.** With two builds a disagreement cannot be assigned to either, and an unstable merge is indistinguishable from a one-off. Three builds are the minimum for the audit signal to identify rather than merely detect.
- **The model version is unrecorded.** Because the cache key holds a model alias rather than a resolved version (*sec:repro-alias*), we cannot establish that two builds were served by the same model. The measured drift is therefore an *upper bound* on same-model variability.
- **Sampling.** The distillation screen covers 30 of 234 runs, stratified by arm. It can establish that distillation is broadly stable; it cannot bound the worst case.

### Fork formation replicated against itself

The measurements above compare two whole builds, which cannot separate two
readings: fork induction may be unstable in itself, or near-deterministic and
inheriting an options layer that already differed. Ten replicates settle it —
five over each of two parents, freezing the options layer and re-running only
fork formation (roughly $36 per replicate, $356 in all).

Within one parent the comparison is **exact**: every replicate labels the same
options file and the chain never renumbers an option, so it is a partition
comparison with no matching step — none of the machinery that makes the
between-build number arguable.

| | pairs | ARI | sd | df |
|---|---|---|---|---|
| within parent A | 10 | 0.595 | 0.071 | 9 |
| within parent B | 10 | 0.636 | 0.047 | 9 |
| between parents | 25 | 0.334 | 0.036 | — |

**Fork induction disagrees with itself at ARI 0.62 on byte-identical input.**
Decomposed as shortfall from perfect agreement, induction contributes 0.384 and
the differing options 0.282 — induction is the *larger* share, 58% of the total.
The reading the gap invites, that most disagreement is inherited and the options
layer is what to fix, is therefore wrong: a perfectly stable options layer still
lands at 0.62.

The decision-point count is not stable either. From identical frozen options:
299, 281, 302, 317, 297 for parent A and 298, 317, 314, 311, 303 for B. "317
decision points" is one draw from a spread of roughly 281–317, which also makes
the two parents' 317 and 351 about two standard deviations apart rather than a
structural difference.

**What this does not measure.** The replicates drop `merge_options`, so they are
a modified pipeline: fork-formation variance under frozen options, not
end-to-end variance. The parents' own fork layers came from the full loop and
are excluded from the statistics. And 0.62 now **does** have a ceiling to read
it against: two people do not agree at 1.0 either, but at the fork layer they
agree at 0.729 pool-weighted, and — unlike at the option layer — no better on
the pairs the builds agreed about than on the pairs they did not.

## The induced map against a curated one

The corpus arrives with a decision map already attached. Its original authors extracted one against a taxonomy of their own, and that map is shipped in every run directory as `decisions_mapped.json`. It has never been read by this pipeline: owner decision A2 excludes it from extraction, and open item 4 verified the exclusion held — `study.json` names two input artifacts, every distillation record shows only those, and the response cache contains no call that saw the file. The comparison below was made after both maps existed, when neither could influence the other. Reading it as a *target* is a different act from reading it as an *input*, and the distinction is what makes the comparison informative rather than circular.

**What the curated map contains.** Across the 207 soccer runs there are 21 distinct decision-point keys. Eleven constitute the operative codebook, each assigned in 206 or 207 of the 207 runs; the remaining ten appear in a single run that was never unified onto the shared taxonomy and retain that run's pre-compression labels. The codebook is not fixed in advance: `taxonomy.py` induces it per dataset by model-driven compression and *"auto-selects the most informative decision points by Shannon entropy"*, discarding low-frequency ones. Eleven is therefore an outcome of selection, and the tail is selected against by construction.

### Two maps of different shape

| | curated | induced (build A) |
|---|---:|---:|
| decision points | 11 | **317** |
| reached by ≥ 206 analyses | 11 | 3 |
| reached by ≥ 10 analyses | 11 | 41 |
| reached by exactly 1 analysis | 0 | **169** |
| median reach | 206 | **1** |
| total assignments | 2,268 | 3,410 |
| assignments valued `other` / `none` / n.a. | **0** | — |

The curated map is *saturating*: every analysis carries a substantive value on every axis, and not one of its 2,268 assignments is a null category. It is a complete matrix, and completeness is a property of the instrument rather than of the analyses — it cannot express the proposition *this analyst never faced this decision*, which the attribution model of *sec:shapley* treats as a level in its own right and finds to be the most common state at most decision points. The induced map has the opposite shape: a short head and a long tail, with more than half its decision points walked by a single analysis.

### Recovery and addition, adjudicated

Two questions follow, and only the second bears on whether discovery was worth the cost. *Recovery*: does the induced map contain each curated node? If not, discovery lost something curation kept. *Addition*: how much of the induced map has no curated counterpart?

Both were settled by adjudication rather than by label matching, using `21_fork_identity` — the same instrument the pipeline uses to decide decision-point identity *within* a build — over 312 pairs, 278 of them returned at high confidence. Label matching is not usable here and *sec:cross-build* measures why: on a cross-build comparison, pairs the adjudicator called the same had median cosine 0.28 and pairs it called different 0.27.

> **Recovery: 10 of 11 curated nodes (91%) have a counterpart among the induced decision points.**
> **Addition: 15 of the 25 most-walked induced points (60%) have no curated counterpart — 50% of run-appearances among that top 25.**

Discovery does not lose what curation kept. What it adds is the more interesting half, and it is not confined to rare decisions: the unmatched set includes which version of the source dataset is loaded (209 analyses), which effect-size measure expresses the result (175), how dyads with a missing skin-tone rating are handled (145), whether covariates are averaged or held at reference values when forming adjusted predictions (137), and what rule declares the effect statistically supported (119). These are not exotic. They are ordinary steps that a codebook of eleven slots had no slot for.

### The one node not recovered is the result, not the exception

`sample_definition.exclusion_criteria` is the single curated node with no induced counterpart, and the adjudicator refused every one of its 30 candidates at high confidence. Its reasons are consistent and they are correct: the induced map holds *"How are dyads with a missing skin-tone rating handled?"*, *"how are records with missing covariates handled?"*, *"are goalkeepers included or excluded?"* and several more, and the adjudicator declined each on the ground that the curated node *"spans broader sample exclusions (covariates, goalkeepers, leagues, imputation)"* while the induced one *"only resolves rater-level missingness mechanics."*

That node carries **80 distinct options**, more than twice any other, and its option strings are conjunctions rather than alternatives: *"Exclude missing on any covariate plus substantive exclusions"*, *"Exclude missing on any covariate plus substantive exclusion of medium skin tone"*, *"Exclude missing skin tone only (primary), with additional exclusions in sensitivity."* Composition of that kind is the signature this study uses to identify a decision point that is really several — an analyst can do both, so they are not competing options at one slot but choices at two.

So the failure to match is not a gap in the induced map. It is the induced map declining to represent a bundle as a single choice, and the adjudicator — which has no knowledge of either map's provenance — independently reaching the same reading from the option lists alone. The one apparent loss in the recovery direction is, on inspection, the clearest instance of what the method is for.

At the other extreme, `exposure_measurement.skin_tone_rater_aggregation` carries **exactly one option** across all 206 analyses that hold it. A decision point with no variation is a decision point on which no analyst chose anything, and it contributes nothing to a multiverse; the induced map splits the same territory into rater combination, numeric encoding, and agreement quantification, two of which vary.

### What the curated pipeline discarded

The comparison above is against what the curated taxonomy *kept*. Its own extraction found a great deal more. Of the 1,120 items its extractor recorded across the 207 runs, **a third were written to an `unmapped_decisions` bucket** rather than mapped onto any of the eleven nodes.

That residue is a direct measurement of what a fixed schema cannot hold, taken by the schema's own authors, and it is disproportionately the fine-grained end of the space: *"Specific dichotomization threshold of 0.5 for skin tone"*, *"Delta method used for standard errors of risk differences"*, *"Computation of adjusted risk difference via marginal effects (counterfactual predictions) as primary estimand"*, *"Dual inference approach: used different SE methods for different estimands"*, *"Two-sided vs one-sided testing"*. One entry records an analyst *"explicitly optimizing the skin tone threshold (0.25) to 'maximize the observed effect while remaining defensible'"* — an admission of a researcher degree of freedom being exercised deliberately, which the codebook had nowhere to put.

The disappearance of the cutpoint is visible in the curated pipeline's own files. The single run that escaped unification kept three separate pre-compression axes — `skin_tone_measurement`, `skin_tone_categorization`, and `dichotomization_threshold` — which the eleven-node taxonomy fuses into one `skin_tone_operationalization`. The induced map splits them too, and the entanglement of scale with cutpoint at that decision point is an open item in this study, raised independently of this comparison (*sec:open*). Two instruments and one un-compressed run agree that there is more than one decision there; the compression step removed it.

### What this does and does not license

**It is not a validation.** A matched pair says two inductions found the same question, not that either found the right one. Both maps are model-produced, and the adjudicator is a model of the same family.

**Recovery is a floor of unknown tightness.** Candidates are shortlisted by TF-IDF (25 per node) before adjudication, and this project has measured lexical similarity to be uninformative about decision-point identity. A curated node whose true counterpart shares no vocabulary with it never reaches the adjudicator. An unscreened run is 11 × 317 = 3,487 pairs and was not affordable; 91% should be read as *at least*, and the screen's own repair is documented below because it was got wrong first.

**Addition is bounded by the ranking that produced it.** *"15 of the top 25"* is conditioned on coverage-ranking, not a rate over all 317 decision points, and must be quoted with its denominator.

> **Method note.** A first version of this comparison reported recovery of 2 of 11. It was invalid. The curated labels are snake_case identifiers (`statistical_modeling.standard_error_method`) while the induced ones are natural-language questions, so tokenised as written the two sides shared no vocabulary, every cosine was zero, every ranking tied, and the sort fell back to index order — handing all eleven nodes the same three alphabetically-first candidates. Nine nodes were scored MISSED against a map that visibly contains them. The repair was to split identifiers into words and admit each decision point's option text into its document, after which 39% of pairs have non-zero cosine and the obviously-correct counterpart ranks first for most nodes. The failure is recorded because the broken run produced a plausible number — *2 of 11* would have read as a striking negative result and nothing in the output marked it as an artifact of the screen.

## Prose as lossy compression of an analysis

The stability results converge on a substantive claim about analysis reporting, not merely about this pipeline: **a written account of an analysis is a lossy compression of what the analysis did**, and the loss is large enough to be measured rather than assumed. This section assembles the evidence, states what it does and does not license, and draws the consequence for why a code-anchored instrument is worth building.

### Three independent measurements of the loss

**Prose recovers roughly half to two-thirds of the decisions.** The code-ablation gate (*sec:ablation*) matches each run's code channel against its prose channel, where the prose segmentation never saw the script. Recall—of the decisions the code channel found, how many the prose channel also found—is `0.64` for the AI corpus and `0.53` for the human corpus. Between a third and **more than half** of the operations an analysis performs are not recoverable from its own write-up.

**Human prose is lossier than machine prose.** The gap in *tab:e4-corpus* is consistent across both builds of the gate and is the reason check E4 exists: pooling is licensed only if both corpora clear the threshold independently.

| **Corpus** | **Runs** | **Recall** | **Agreement** | **Vague** | **Run** |
|---|---|---|---|---|---|
| AI | 61 | 0.622 | 0.964 | 0.028 | first |
| human | 19 | 0.480 | 0.889 | 0.052 | first |
| AI | 61 | 0.642 | 0.921 | 0.063 | second |
| human | 19 | 0.534 | 0.847 | 0.073 | second |

*Code-to-prose recovery by corpus. The alignment judgement (prompt 16) was run twice on the identical 80-run sample, five days apart. The first run is check E4 in `data/audits/ablation_audit.json`, whose verdicts are the ones written to `data/audits/ablation.json`; the second run's per-corpus figures are the ones the paper reports, and `stability/data/q2_ablation.json` records the comparison between the two. Under either run the human corpus recovers fewer of its own decisions and agrees less often about which option was taken. Conflict rate, first run: AI 0.007, human 0.059.*


**Silent decisions are common.** Directly, roughly one decision in twelve is performed and never mentioned: the corpus-level silent rate is `0.092` in one build and `0.072` in a replicate, and 21 or 22 of 30 runs contain at least one silent decision. The phenomenon is not confined to a few careless analyses.

### Why verification is hard, seen twice

Two independent stability results point at the same mechanism, and it is worth noting that they were measured separately and agree.

First, the alignment judge drifts *asymmetrically* (*sec:stability*). Across two runs on identical inputs, 25 pairs moved from `same_option` to `vaguer` and 8 to `same_fork_different_option`, against only 7 moving back. The verdict `vaguer` means precisely: the prose describes the same choice but too underspecified to pin which option was taken.

Second, silent-decision detection reproduces at `F_1 = 0.489`, and—this is the part that matters—**semantic adjudication does not improve on the structural figure**. We asked a model, blinded to which build was which, to align the two lists of silent decisions allowing arbitrary rewording; it returned `0.4889` against a structural `0.4889`. The disagreement is therefore not boundary jitter and not a measurement artifact: the two extractions genuinely identify *different operations* as unmentioned.

Both observations have one explanation. When a write-up is underspecified, whether it “mentions” a given operation is a genuinely borderline judgement, and borderline judgements do not reproduce. The instability of the residue is a *symptom* of the lossiness, not an alternative to it.

### What is robust and what is not

The distinction matters for how these findings should be quoted, and the stability measurement is what makes it statable.

| **Robust** | **Not robust** |
|---|---|
| That prose loses decisions | The precise loss rate |
| That the loss is substantial (`\sim`1 in 12 unmentioned; a third to a half unrecoverable) | Which *specific* decision was silent in a given run |
| That human prose loses more than machine prose | The exact count in any one run |

*Aggregate claims survive replication; item-level claims do not.*

Concretely: the silent rate moved from `0.092` to `0.072` between builds—the same order of magnitude, not the same number—and per-run counts correlate at Spearman `+0.57`. By contrast the decision layer itself moved only `-2.2%` in total with per-run correlation `+0.82`. A paper may therefore report *that* analyses routinely leave decisions unstated, and roughly how often; it should not report that a particular decision in a particular run was the silent one without noting that a second extraction would likely have named a different one.

### The consequence for instrument design

If a written account were a faithful record of an analysis, a decision map could be built by reading write-ups, and this pipeline would be unnecessary machinery. The measurements above say it is not faithful: a third to a half of the decisions are not recoverable from the prose at all, and the human corpus is worse than the machine corpus on every channel measured.

Code is not a summary of the analysis; it *is* the analysis, and it is therefore the only channel that records what was actually done rather than what the analyst chose or remembered to say. That is the argument for anchoring extraction in code, and *sec:stability* supplies its empirical counterpart: the code-derived decision layer reproduces at lenient `F_1 = 0.713` (core `0.895`, median boundary jitter one line), while the prose-derived residues reproduce at `0.489`. The channel the garden is built on is the stable one, and by the code trace of *sec:vocabulary* it is the *only* channel the garden reads.

Two honest counterweights belong beside that argument rather than after it. Code-anchoring is exactly why 12 of 31 human teams contribute no decisions (*sec:corpus*), so reliability is bought with coverage. And the residue findings—the silent decisions that most vividly demonstrate the loss—are themselves the least reproducible output the pipeline produces. The instrument shows convincingly *that* analyses under-report themselves; it is a blunt instrument for saying exactly *what* any single analysis failed to report.

## Reliability: what the measurements license

Every stage of this pipeline that requires judgement is performed by a language model. That invites a reasonable question—*is the result reliable?*—and the question as posed cannot be answered, because reliability is not a property of the instrument but of a particular claim made with it. The same extraction that firmly supports “analyses routinely leave decisions unstated” does not support “this decision point has 49 options.”

This section therefore does not defend the pipeline. It states what was measured, what each measurement licenses, and what we consequently do not claim.

### What is not model-mediated

It is worth separating out the parts of the pipeline that involve no model judgement at all, because the framing “it is all LLM” is inaccurate in ways that matter for what a reader can check.

- **Coverage is an enforced invariant, not a reported diagnostic.** The code segmentation must partition lines `1..n` exhaustively and exclusively; a response that fails is rejected with a specific complaint and re-asked (*sec:retryable*). “The parser did not look here” is therefore a hard failure rather than a silent omission, which is what makes an absent decision interpretable at all.
- **Every decision is anchored to source lines.** A reader can open the analysis script and check any record against the code that produced it. Nothing rests on a claim about a run that cannot be traced to that run's own text.
- **The nulls are structural.** Curveball fixed-margin randomisation (`fork_graph.py`), label permutation, and the size-matched random contraction of *sec:stability* involve no model.
- **The exclusivity constraint and its enforcement** are pure structure: options co-occurring in a run are split by graph colouring, with no adjudication (*sec:veto*).

Model judgement enters at four points—segmenting code and prose, linking the two channels, grouping decisions into options, and grouping options into decision points—and each was measured separately.

### Measured reproducibility, by layer

Two independent builds were produced under isolated study roots (*sec:stability*). Agreement is reported at every layer, and the layers differ by more than any single summary would suggest.

| **Layer** | **Agreement** | **What it means** |
|---|---|---|
| decisions | `0.713` | lenient `F_1`; median boundary jitter **one line**; verbatim `0.176` and
 core `0.895` bracket it |
| options | `0.853` | ARI over shared decision instances; per-run median ARI `1.000`, with 175 of
 223 runs identical |
| decision points | `0.63`–`0.77` | run-geometry correlation; membership agreement is lower, `0.47` lenient |
| residues | `0.489` | silent decisions, semantically adjudicated—equal to the structural figure,
 so not a measurement artifact |

*Reproducibility falls monotonically with abstraction: concrete operations extract most reliably, grouping them into options less so, grouping options into rival slots least.*

That ordering is itself evidence the measurements are meaningful. It is what one expects if each layer adds a judgement, and it matches which prompt does what: the foreclosure test (*sec:vocabulary*) is the hardest question the pipeline asks and the only one with no lexical anchor.

### Three properties that survive replication

**The trunk, though not the tail.** The two builds recovered 317 and 351 decision points. Conditioned on coverage, however, they converge exactly: 40 of 40 decision points at `≥ 11` runs and 18 of 18 at `≥ 25%` coverage. The entire divergence lives in the rare tail, and the reported analyses exclude that tail by the independently-motivated gate “MIN_RUNS` = 10` (*sec:counting*).

**The geometry, not the labels.** Every reported analysis consumes run-level structure—which decision points a run touched—rather than decision point identity. That structure reproduces: Mantel `r = 0.766` at the decision point level and `0.857` at the option level against a permutation null at zero, `z \approx 15`–`19`. Under the conservative construction (clusters of `≥ 5` runs, run size partialled out) the figures are `0.632` and `0.762`.

**Specific findings, re-derived independently.** The persona–route association is significant in both builds at `z = 10.25` and `10.46` and survives a change of vocabulary granularity. Traffic ranks on comparable highway routes correlate at `ρ = 0.951`. The repair chain beats a size-matched random contraction at `z = 122`, which rules out the reading that any contraction to that granularity would score as well.

### What we therefore do not claim

| **Supported** | **Not supported** |
|---|---|
| that analyses under-report their own decisions, and roughly how often | that a *particular* decision in a particular run went unstated |
| that the corpus has this many broadly-faced decision points | that a named decision point has `N` options or effective options `X` |
| that personas walk different routes | which *edge* carries the persona signal |
| that decision points differ in how contested they are | a ranking of the most contested |

*The boundary is consistent across every layer: corpus-level structure survives replication, item-level attribution does not.*

That boundary is the paper's central methodological finding as much as any substantive result, and it generalises: **aggregate structure on the well-populated core is reproducible, the rare tail is not, and the filters that make analysis tractable are the same filters that select the reproducible population.** The last clause is uncomfortable and is stated as a caveat on the analyses rather than as a defence of them—the coverage gate, the matching threshold and the reporting filter were each introduced for independent reasons, and each excludes precisely where the pipeline does not reproduce.

### Threats we cannot currently rule out

**The human baseline, now measured.** A model self-agreement of `0.70` is poor if two trained analysts agree at `0.95` and at ceiling if they agree at `0.70`. The pairwise adjudication instrument — three raters on the same items, blinded to build identity and to the model's answers, reading registered in advance — **has since been run**, and it places the model at the human ceiling rather than below it:

| layer | humans, stable pairs | humans, unstable pairs | gap |
|---|---:|---:|---:|
| option | 0.782 | 0.641 | **+0.141** |
| fork | 0.750 | 0.754 | −0.004 |

*Human–human pairwise agreement, 3 raters, per-item on committed answers. Pool-weighted: option humans `0.818` against model `0.849` (gap 0.030); fork humans `0.729`. Source: `stability/results/human_benchmark.json`; no gold failures.*

The registered hypothesis was that *"if humans also split on the unstable pairs, model instability tracks genuine ambiguity; if humans agree confidently where the builds disagree, it is model noise."* At the **option** layer the first reading holds: human agreement falls by 0.141 exactly where the builds disagree, and on the unstable stratum humans reach only `0.487` raw (`0.655` on committed answers) against a model–model agreement of `0.0`. Instability there is tracking something the humans find genuinely ambiguous.

At the **fork** layer it does not hold: humans agree no better on stable pairs than unstable ones (gap −0.004), so fork-level instability is **not** explained by human-visible ambiguity, and the model's fork disagreements remain unexplained by this instrument.

Read against these, the model is not the weak link at the option layer — it agrees with itself slightly *more* than two humans agree with each other (0.849 against 0.818). That does not license calling the extraction reliable; it relocates the limit, from the model to the question. The strata are small (13 to 20 rated pairs each, 3 raters) and this is one instrument, not a literature.


**A gate verdict changed between runs.** Check E4 of the code-ablation gate (*sec:ablation*) moved from PASS to REVIEW between two runs of identical code on identical data, as the alignment judge drifted asymmetrically toward `vaguer`. We report the gate with the run it was computed on and do not treat a single PASS as durable.

**Model version is unrecorded for the first build.** The cache key holds a model *alias* rather than a resolved version (*sec:repro-alias*), so we cannot establish that the two builds were served by the same model. Some part of the measured drift may be version drift, which makes every figure here an *upper bound* on same-model variability. The resolved version is now recorded on every call; this cannot be applied retroactively.

**Candidate generation limits what can be merged.** Decision point merging adjudicates only pairs passing a lexical similarity screen. Measured against the merges the second build made independently, that screen has recall `0.439`—it never presents the model with more than half the pairs another run of the same pipeline judged to be one question. This bounds the merge pass from below and is a defect in the instrument rather than in the model.

**Two builds cannot attribute a disagreement.** With `K = 2`, a disputed merge cannot be assigned to either build, and an unstable merge is indistinguishable from a one-off. Three builds are the minimum for the audit signal to identify rather than merely detect.

### Agreement is not validity

A final distinction, because it is easy to lose. Everything above measures whether two runs of the pipeline *agree*. None of it measures whether they are *right*, and the two come apart in ways we can demonstrate: 23 option pairs are placed at one decision point by both builds while co-occurring in the same runs, which contradicts the definition of a decision point; and options merging two decisions written hundreds of lines apart—a primary analysis and a robustness refit—are stable across builds and wrong in both.

Stability and correctness are independent axes. The audit families (*sec:validation*) address the second within a single build; the human instrument addresses it across builds. Neither is a substitute for the other, and a reproducible pipeline that reproduces an error is exactly as wrong as an unreproducible one.

## Limitations

Several limitations are structural rather than incidental: they follow from what the method measures and cannot be removed by collecting more of the same data.

### Writing order is not thinking order

The iteration analysis (*sec:iteration*) measures the *artifact*, not the process. A script is often reorganised before it is saved, so a clean forward-ordered script can conceal iteration that genuinely occurred, and a measured return may be tidying rather than rework. The measure therefore **undercounts**, and the direction of the bias is known but its magnitude is not.

### Stage assignment is a model judgement

DSLC stage is assigned by a model (*sec:stages*). The blinding to position prevents circularity with the iteration analysis, and check I3 confirms the labels recover the pipeline order at `ρ \approx +0.59`, which is evidence that they carry real sequence information. It is not evidence that any individual label is correct.

### Code-anchoring excludes prose-only analyses

Because a decision is recovered from a script, the 12 human teams that deposited no script contribute no decisions, and every pooled analysis rests on 19 teams (*sec:corpus*). The ablation gate (*sec:ablation*) exists to measure the cost of this exclusion rather than to remove it. Note that in the most recent build the human corpus **passes** that gate on its own — E4 is `PASS`, with human agreement 0.889 against a 0.85 threshold, though on the narrowest margin of any corpus in the study. (This previously read that the human corpus *fails* E4; it does not, and the claim is withdrawn.) The check that is currently in `REVIEW` is **E2**, the leniency null: the ablation matcher pairs *unrelated* runs at 0.4894 against a within-run 0.5928, a ratio of 1.21 where the gate asks for under 0.25. That is the load-bearing failure, and it means the headline code-to-prose agreement cannot be read as a pass on its own — a constraint on the same pooled claims, arriving through a different check than this passage previously named.

### Additivity in the attribution model

The Shapley decomposition `eq:shapley` has a closed form because the surrogate is additive, and an additive surrogate cannot represent interactions between decision points. Where analysts' choices genuinely interact—a coarsening that matters only in combination with a particular model specification—the attribution will distribute the interaction across the main effects. The companion audit reports the share of each payout the surrogate explains, which bounds how far the attribution can be trusted, but it does not recover the missing interaction.

### Everything on the outcome side is observational

Runs were not assigned their novelty, their persona brief influences both the choices they make and the verdict they report, and no randomisation separates these. All novelty–outcome relations (*sec:novelty*, *sec:novelty-curve*) are associations, and arm is reported alongside rather than adjusted away, because adjusting for a variable that sits on the causal path between the treatment and the outcome would be worse than not adjusting at all.

### Under-merge is preferred, and it is still an error

The clustering deliberately prefers under-merge to over-merge because the two errors have asymmetric recoverability (*sec:vocabulary*). Preferring it does not make it free: residual under-merge inflates the decision point count, depresses per-decision point coverage, and manufactures apparent siblings. The sibling screen (*sec:garden*) detects the residue but cannot be assumed to remove all of it, and a decision point count should be read as an upper bound.

### One corpus, one dataset, one question

Everything reported here concerns analyses of a single dataset answering a single research question. The *method* is intended to generalise; the induced vocabulary is specific to this corpus by design, and the concentration and novelty statistics describe these analysts on this problem. Whether the observed structure—a short shoulder of near-universal decisions and a long tail of rare ones—is a property of analysis in general or of this dataset is not answerable from one corpus.

## Constants and thresholds

Every numeric constant used by the pipeline, with the script that defines it. Values are those in force at the time of writing; each is a single named constant in source rather than an inline literal, so this table can be regenerated mechanically.

| **Constant** | **Value** | **Defined in** | **Role** |
|---|---|---|---|
| *Extraction* | | | |
| prose size floor | 400 bytes | `distill.py` | minimum usable prose artifact |
| `MAX_RETRIES` | 3 | `llm.py` | informed content retries |
| `TRANSPORT_TRIES` | 6 | `llm.py` | transport retries, not charged to attempts |
| `TIMEOUT_S` | 900 | `llm.py` | per-call timeout |
| *Vocabulary induction* | | | |
| density floor | 0.60 | `merge_forks.py` | share of a group a decision point must match to join |
| `MAX_REPAIR_ROUNDS` | 3 | `build_all.py` | cap on the repair chain |
| `CONVERGED_AT` | 0.02 | `build_all.py` | stopping rule `eq:converge` |
| *Concentration and novelty* | | | |
| `MIN_RUNS` | 10 | `stability.py` | decision point coverage gate |
| `STABLE_SHARE` | 0.10 | `stability.py` | share for an option to be stable |
| `STABLE_FLOOR` | 3 | `stability.py` | minimum runs for stability |
| `B` (novelty) | 4000 | `novelty.py` | bootstrap resamples |
| `B` (dose-response) | 3000 | `novelty_curve.py` | bootstrap resamples |
| *Iteration* | | | |
| `TIE_LINES` | 2 | `iteration.py` | returns within this span are artifacts |
| `MIN_OPP` | 15 | `iteration.py` | successors needed for a trigger rate |
| *Seeding* | | | |
| `SEED` | 20260822 | several | global seed |
| *Attribution* | | | |
| `MIN_LEVEL` | 10 | `shapley_v2.py` | runs a level needs to exist |
| `MIN_LEVELS` | 2 | `shapley_v2.py` | levels a decision point needs to play |
| `B` (Shapley) | 2000 | `shapley_v2.py` | bootstrap over runs |
| `\lambda` grid | `\{1,3,10,30,100,300,1000\}` | `shapley_v2.py` | cross-validated per payout |
| *Ablation gate* | | | |
| `GATE` | 0.85 | `ablation.py` | agreement required to license pooling |
| sample fraction | 0.30 | `ablation.py` | share of two-channel runs sampled |
| E1 band | `[0.35, 0.65]` | `audit_ablation.py` | acceptable channel-flip fraction |
| E2 ratio | null `< 0.25×` | `audit_ablation.py` | leniency null margin |
| E3 bound | `|ρ| < 0.5` | `audit_ablation.py` | length-confound bound |
| E5 share | `≥ 0.60` | `audit_ablation.py` | runs individually clearing the gate |
| E6 bounds | `0.05 < r < 0.95`; share `< 0.15` | `audit_ablation.py` | degeneracy bounds |

## Prompt inventory and stage map

### Prompts

Each prompt is a versioned file. Its content is hashed into the cache key `eq:cachekey`, so editing a prompt invalidates exactly the entries that depended on it.

| **Prompt** | **Used by** | **Role** |
|---|---|---|
| `01_segment_code` | `distill.py` | exhaustive, exclusive code partition |
| `02_segment_prose` | `distill.py` | exhaustive claim partition with polarity |
| `03_link` | `distill.py` | align channels; residue gives silent/misaligned |
| `10_induce_types` | `cluster.py` | induce categories for typed items |
| `11_assign_types` | `cluster.py` | assign items to induced categories |
| `12_group_batch` | `cluster_up.py` | L1 local grouping |
| `13_merge_groups` | `cluster_up.py` | L2/L3 merging |
| `14_fork_stage` | `finalize_vocab.py` | DSLC stage, blind to position |
| `15_fork_relation` | `garden.py` | sibling adjudication |
| `16_align_channels` | `ablation.py` | code/prose matching for gate 5.4 |
| `17_fork_rationale` | `rationale.py` | stated vs.\ inferred rationale |
| `18_merge_tags` | `rationale.py` | tag consolidation |
| `19_option_granularity` | `audit_granularity.py` | collapse paraphrase within a decision point |
| `20_option_purity` | `audit_lineage.py` | option coherence check |
| `21_fork_identity` | `audit_lineage.py` | are two decision points one question? |
| `22_induce_forks` | `induce_forks.py` | group options by purpose (foreclosure) |

### Workflow stages

The full workflow, in execution order. Every stage is idempotent.

| **#** | **Stage** | **Produces** |
|---|---|---|
| 1 | distill | artifacts `→` exons/introns `→` links `→` per-run record |
| 2 | index | per-run records `→` corpus tables |
| 3 | l1 | decisions `→` local groups, per corpus, no cap |
| 4 | build | L2 + L3 over the union `→` options `→` decision points |
| 5a | audit clusters | A1–A9 |
| 5b | repair clusters | R1–R4 splits |
| 6-1 | options: collapse paraphrase | `.merged` |
| 6-2 | decision points: merge duplicates | `.forkmerged` |
| 6-3 | options: re-merge across united decision points | `.merged` |
| 6-4 | decision points: re-induce from purpose | `.induced` |
| 6-5.`i` | merge/re-merge to fixpoint | `.r`i`f`, `.r`i“ |
| 6-6 | finalize vocabulary | coverage, position, stages |
| 6a–6k | analyses + audits | stability, novelty, dose-response, iteration, garden, Shapley |
| 7c–7f | figures | atlas, graph, circle; `forkscope.py` then renders the viewer |
| 8a–8e | gate 5.4 | ablation sample, match, null, report, E1–E6 |

### Vocabulary tag grammar

A vocabulary tag records its own lineage. Reading left to right:

`ai.merged.forkmerged.merged.induced.r3`

- `ai` — corpus scope (`ai`, `human`, or `ai+human`)
- `.merged` — an option-merge pass
- `.forkmerged` — a decision point-merge pass
- `.induced` — decision points re-induced from option purpose
- `.r`N“ — fixpoint round `N`; `.r`N`f` is that round's decision point-merge half

Analyses are written to files carrying the tag of the vocabulary they were computed from, which is what makes a superseded number recomputable rather than merely citable. Figures are the exception (*sec:fig-provenance*).

## References

- **[afp2025]** {Amazon Science}. Agentic Forking Paths. **.
- **[benjamini1995]** Benjamini, Yoav and Hochberg, Yosef. Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *Journal of the Royal Statistical Society, Series B*.
- **[botvinik2020]** Botvinik-Nezer, Rotem and Holzmeister, Felix and Camerer, Colin F. and others. Variability in the Analysis of a Single Neuroimaging Dataset by Many Teams. *Nature* 2020.
- **[breznau2022]** Breznau, Nate and Rinke, Eike Mark and Wuttke, Alexander and others. Observing Many Researchers Using the Same Data and Hypothesis Reveals a Hidden Universe of Uncertainty. *Proceedings of the National Academy of Sciences* 2022.
- **[efron1993]** Efron, Bradley and Tibshirani, Robert J.. An Introduction to the Bootstrap. *Chapman and Hall/CRC*.
- **[gelman2013garden]** Gelman, Andrew and Loken, Eric. The Garden of Forking Paths: Why Multiple Comparisons Can Be a Problem, Even When There Is No ``Fishing Expedition'' or ``p-hacking'' and the Research Hypothesis Was Posited Ahead of Time. *Department of Statistics, Columbia University*.
- **[hirschman1964]** Hirschman, Albert O.. The Paternity of an Index. *The American Economic Review*.
- **[hoerl1970]** Hoerl, Arthur E. and Kennard, Robert W.. Ridge Regression: Biased Estimation for Nonorthogonal Problems. *Technometrics* 1970.
- **[lundberg2017]** Lundberg, Scott M. and Lee, Su-In. A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems 30*.
- **[shapley1953]** Shapley, Lloyd S.. A Value for $n$-Person Games. *Contributions to the Theory of Games, Volume II*.
- **[silberzahn2018]** Silberzahn, R. and Uhlmann, E. L. and Martin, D. P. and others. Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results. *Advances in Methods and Practices in Psychological Science* 2018.
- **[simmons2011]** Simmons, Joseph P. and Nelson, Leif D. and Simonsohn, Uri. False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting Anything as Significant. *Psychological Science* 2011.
- **[steegen2016]** Steegen, Sara and Tuerlinckx, Francis and Gelman, Andrew and Vanpaemel, Wolf. Increasing Transparency Through a Multiverse Analysis. *Perspectives on Psychological Science* 2016.
- **[strona2014]** Strona, Giovanni and Nappo, Domenico and Boccacci, Francesco and Fattorini, Simone and San-Miguel-Ayanz, Jesus. A Fast and Unbiased Procedure to Randomize Ecological Binary Matrices with Fixed Row and Column Totals. *Nature Communications* 2014.
