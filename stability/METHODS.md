# Stability — methods, paper-ready

Source text for the paper's stability section. Numbers here are traceable to
`data/*.json`.

---

## 1. The question

The pipeline's reproducibility guarantee is a content-addressed cache: an
unchanged stage re-run returns byte-identical output because it reads the cache,
not the model. That guarantee is real but narrow. It says *a re-run reproduces
the earlier answer*; it does not say *two independent runs would have agreed*.
The model is reached through a CLI exposing neither temperature nor seed, so
run-to-run variability is not controllable — only measurable.

Measuring it requires deliberately defeating the cache, which is why it is a
separate exercise rather than a property the pipeline reports about itself.

## 2. Replicate versus scope change

Two builds can differ for two unrelated reasons, and the artifacts look the same
either way:

- a **replicate** re-calls the model on identical corpora and identical
  distilled input, so every difference is run-to-run variability;
- a **scope change** pools different corpora, so differences confound
  variability with the effect of the corpus.

Every comparison script reads the corpora from the vocabulary headers,
classifies the comparison, and writes the verdict into its output. The audit
refuses to accept a scope comparison in place of a replicate.

## 3. Isolation

The obvious way to force fresh calls — `nocache=True` — skips the cache *read*
but still *writes* to the same key, so running it in place would overwrite the
baseline while measuring it. Replicates therefore run under a separate study
root with an empty cache: every call misses, and the baseline is out of reach by
filesystem layout rather than by remembering a flag.

A vocabulary replicate copies `data/distilled` in, so stage 3's input is
byte-identical to the baseline's and any downstream difference is vocabulary
variability alone.

## 4. Estimators

### 4.1 Partition agreement

Both builds partition the **same decision instances**, keyed on
`(run, line, text-prefix)` — verified identical across builds. Vocabulary
agreement is therefore exact arithmetic on two labelings of one item set,
requiring no matching heuristic and no model calls.

This matters because the obvious alternative — matching option labels by string
or embedding similarity — imports the failure the pipeline rejects for
clustering: ~95% of option labels are unique, so a lexical match rate measures
phrasing, not agreement. Semantic adjudication is used only to *classify*
disagreements, never to produce the headline.

Three metrics, chosen because they fail differently:

- **Adjusted Rand Index** — chance-corrected agreement on whether each *pair* of
  instances is co-clustered. Symmetric, 0 at chance, 1 at identity, insensitive
  to the shape of the disagreement.
- **Variation of Information**, `H(A|B) + H(B|A)` in bits — a true metric on the
  space of partitions, so it obeys the triangle inequality (ARI does not), which
  matters once there are three builds. Reported normalised by `log₂ n` so it is
  comparable across item sets of different size.
- **B-cubed precision/recall/F₁** — per-instance, so it decomposes. Precision
  above recall means B *split* what A held together; recall above precision
  means B *merged* what A held apart.

Direction is derived from two independent signals — B-cubed asymmetry and the
raw cluster count — and reported as `AMBIGUOUS` when they disagree, rather than
asserted from a gap inside the noise.

### 4.2 Distillation agreement

The code segmentation is an exhaustive, exclusive partition of lines `1..n`
(enforced as a retryable invariant, not checked afterwards), so two
segmentations of one script are two labelings of a fixed item set and per-line
agreement is exact. Prose is exhaustive but *not* exclusive — one sentence may
assert two things — so the prose channel is compared on counts and span
boundaries rather than as a partition.

Counts are reported separately from structure: silent decisions and
misalignments are *residues* of an alignment, and a residue is more fragile than
the thing it is left over from.

### 4.3 Highway agreement

Fork labels are re-induced on every build, so the same question returns worded
differently and label matching would score a rewording as a miss. Forks are
instead matched by the instances they share — each A-fork to the B-fork holding
most of its instances — with the Jaccard overlap reported so a weak match is
visible. The mapping is deliberately not a bijection: forks legitimately split
and merge, and forcing one-to-one would hide exactly that.

Traffic agreement is Spearman rank correlation over the overlapping dyads. The
question is whether *busy routes stay busy*, not whether counts are identical.

## 5. Results

Two replicates were run: a 30-run distillation screen ($64) and a full pooled
vocabulary rebuild ($184). Both under a separate study root with an empty cache;
the baseline cache was verified unchanged at 2,274 entries throughout.

### 5.0 One finding, stated once

Every measurement below is an instance of the same result, and it is the
central methodological claim of this section:

> **Aggregate structure on the well-populated core is reproducible. The rare
> tail is not. And the filters that make analysis possible are the same filters
> that select the reproducible population.**

That last clause is the uncomfortable half. `MIN_RUNS = 10`, the fork-matching
threshold, and the coverage gate were each introduced for independent
analytical reasons, and each turns out to exclude precisely the population
where the pipeline does not reproduce. The reported analyses are therefore
better supported than the whole-vocabulary numbers suggest, and the exclusions
are doing more work than their stated rationale claimed.

### 5.1 The alignment judge

Prompt `16` called twice on an identical 80-run sample — the same 1,363 code
decisions and 3,329 prose spans — five days apart, with no change to corpus,
code or prompt.

| quantity | value |
|---|---:|
| matched in either run (union) | 864 |
| identical partner and verdict | 688 |
| agreement conditioned on both matching | 0.872 |
| **stability over the union** | **0.796** |

Verdict transitions are asymmetric — 25 `same_option`→`vaguer` and 8
→`same_fork_different_option` against 7 back — making this a severity shift
rather than symmetric noise. Downstream, strict agreement fell 0.9517 → 0.9077
and gate check **E4 moved PASS → REVIEW**: a gate verdict changing between two
runs of identical code on identical data.

### 5.2 Distillation

30 runs distilled independently. Scored at all three levels (§4.1):

| level | rule | F1 |
|---|---|---:|
| verbatim | identical line sets | 0.176 |
| **lenient** | Jaccard ≥ 0.5 | **0.713** |
| core | containment ≥ 0.5 | 0.895 |

Median boundary jitter among matched pairs: **1 line**; 75% of lenient matches
are not verbatim. The code channel's exon/intron typing agrees at 0.886, while
the **prose channel is the least stable thing measured (ARI 0.480)**.

Residues do not follow the decision layer. Silent decisions reproduce at
**F1 0.489**, and semantic adjudication — a model, blinded to build order,
allowed to match on meaning rather than line overlap — returned 0.4889 against
a structural 0.4889. The disagreement is therefore neither jitter nor a
measurement artifact: the two builds flag genuinely different operations as
unmentioned.

### 5.3 Vocabulary

The vocabulary is two stacked clusterings, and measuring each over the items it
actually clusters separates them:

| layer | items | ARI |
|---|---:|---:|
| options over decisions | 3,946 | **0.853** |
| forks over options, unweighted | 497 | **0.307** |
| forks over options, instance-weighted | — | **0.852** |
| *(confounded)* forks over decisions | 3,946 | *0.695* |

The gap between the two weightings is size: 64% of matched options are
singletons, 194 of 255 forks hold exactly one option, and by-option ARI rises
monotonically with option size (0.31 at ≥1 instance, 0.69 at ≥5). Fork
induction is a coin flip **for the rare tail** and about as reproducible as
option merging for the options that carry the corpus.

Per run — two partitions of one run's own decisions, needing no cross-run
matching — the same split appears sharply:

| level | mean ARI | median ARI | same cluster count |
|---|---:|---:|---:|
| option | 0.807 | **1.000** | 175 / 223 |
| fork | 0.546 | 0.590 | 65 / 223 |

**Within a single run, option grouping is essentially perfect.**

Dispersion (how many clusters of the other build hold 90% of each) shows the
one-to-one framing was too harsh: only **28 of 317 forks (8.8%) scatter**; 213
are intact and 76 split into two or three. A split is the recoverable direction
under this project's asymmetry.

### 5.4 Does repair converge the builds?

Repair is a contraction (463 → 317 forks in one build, 489 → 351 in the other),
and contraction changes agreement mechanically, so the question needs a null:
randomly merge each base vocabulary to the repaired granularity, matching the
observed cluster-size distribution.

| level | base | after repair | random-contraction null | z |
|---|---:|---:|---:|---:|
| option ARI | 0.646 | **0.853** | 0.187 ± 0.014 | 46.8 |
| fork ARI | 0.565 | **0.695** | 0.219 ± 0.004 | 122.0 |

p < 0.005 at both levels (empirical floor, 200 draws). **Repair is a genuine
canonicaliser**, not granularity arithmetic. Note the direction of the
confound: random contraction *destroys* agreement between different builds
(0.565 → 0.219), so repair has to overcome a mechanism that would otherwise
cost it a third of its agreement.

### 5.5 The forks results are actually reported on

Reported analyses cover forks with coverage ≥ 25% and effective options > 1.5.
Qualification computed independently in each build:

| question | result |
|---|---|
| does the *set* reproduce? | **7 of 10** (4 merged 2→1 by B, 3 scattered) |
| do matched ones agree on membership? | **ARI 0.975** |
| do their statistics agree? | median Δ effective options **0.67**, max **11.36** |

So *which* decision points matter is ~70% reproducible; *what they contain* is
highly reproducible once both builds agree they matter; *how contested they
look* is not. Effective-option counts should be quoted as ranks or with stated
uncertainty. With n = 10, every rate moves by 0.1 per fork.

### 5.6 Highways and personas

Among the **42 comparable routes** — of 225 drawn — traffic rank correlation is
ρ = 0.951 against a permutation null shuffling traffic across the same dyads
(null mean 0.001, z = 6.08, p < 0.001). Stratifying by traffic, the low half
(3–13 runs) reproduces at ρ = 0.904 and the high half at 0.880, so the
correlation is not carried by a few large edges.

**The denominator matters and must be stated.** 180 of 225 routes could not be
compared because an endpoint fork had no confident match, and those routes are
systematically sparser (median traffic 5 vs 13; rank-sum z = +4.36). Their
reproducibility is *unmeasured*, not measured-and-good.

Per-cell persona enrichment does **not** reproduce: 1 of 10 survives, at
identical corpus scope. But an omnibus test — do runs of the same persona walk
more similar routes? — is strongly positive and stable:

| build | within | between | delta | z |
|---|---:|---:|---:|---:|
| A | 0.0905 | 0.0814 | +11.2% | 10.25 |
| B | 0.0898 | 0.0803 | +11.9% | 10.46 |
| A, pre-repair | — | 0.0302 | +14.8% | 7.74 |

**Personas do walk different routes**; *which particular edge* carries the
signal is not identifiable at this sample size. The 10 enriched cells are scan
output and should be demoted to an exhibit, not reported as findings.

## 6. Instability as an audit signal

An unstable merge is a suspect merge. Where build A groups two decisions into
one option and build B does not, the pipeline has answered "same action?" both
ways — the evidence a human review round wants, obtained free once two builds
exist.

The response follows the pipeline's existing asymmetry between error types:
over-merge is invisible in the output and unrecoverable, under-merge is visible
and fixable. An unstable pair therefore defaults to **unmerged** and routes to
review. Majority vote across three builds would silently retain 2-of-3 merges,
which is precisely the over-merge the split-never-merge rule exists to prevent.

Thresholds are set from the first replicate and stated as such. They are not
adjusted until checks pass: iterating on a cutoff until a check clears
manufactures the result, and the project's auditing guidance names it as the
failure to avoid.

## 7. Limitations

- **K = 2 cannot attribute.** With two builds a disagreement cannot be assigned
  to either, and an unstable merge is indistinguishable from a one-off. Three
  builds are the minimum for the audit signal to identify rather than merely
  detect — and it is why the arbitration rule, applied at K = 2, creates 805
  singletons and should not be adopted as a headline vocabulary.
- **Small denominators where it matters most.** The most decision-relevant
  measurement — the forks results are reported on — has n = 10. Every rate
  there moves by 0.1 per fork. It describes this pair of builds; it is not an
  estimate with a usable interval.
- **Unmeasured is not measured-and-good.** 180 of 225 routes and 232 of 729
  options could not be matched confidently, and those populations are
  systematically sparser than the ones that could. Their reproducibility is
  unknown, and every rate in §5 should be read with its denominator attached.
- **The human benchmark bounds these figures.** Model self-agreement of 0.7 is
  unimpressive against humans agreeing at 0.95 and at ceiling against humans
  agreeing at 0.7. The benchmark in `reviews/human-benchmark/` supplies that
  comparison: at the options layer two raters agree at 0.818 and two builds at
  0.849 (`stability/results/human_benchmark.json`).
- **The model version is unrecorded.** The cache key contains a model *alias*,
  not a resolved version, so we cannot establish that two builds were performed
  by the same model. The measured drift is therefore an upper bound on
  same-model variability: some of it may be version drift.
- **Sampling.** The distillation screen is 30 of 234 runs, stratified by arm.
  It can establish that distillation is broadly stable; it cannot bound the
  worst case.
