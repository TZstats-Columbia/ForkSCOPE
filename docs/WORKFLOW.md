# Workflow — which script produces which file

**This is the charting workflow only** — the scripts that turn raw analyses
into a decision map, and which file each one writes. The other workflows are
not scripts and are documented elsewhere: the phases and who acts in each are
in [`LIFECYCLE.md`](LIFECYCLE.md), and each is driven by a skill in
`.claude/skills/` — `/intake`, `/review`, `/refine`, `/walk`, `/itinerary`,
`/inspect`, `/challenge`, `/investigate`, `/audit`.


Nine stages. Every artifact in `data/` and `figures/` is produced by exactly one
script listed here; if a file is not named below, it is not part of the
pipeline.

Read the columns as: **stage → script → what it reads → what it writes**.

```
raw corpora                    (data/raw — fetched, see MANIFEST.md)
   │
   ├─ 1  distill ──────────────► data/distilled/  data/corpus/
   │
   ├─ 2  cluster ──────────────► data/vocabulary/bottom_up_<corpus>.json
   │
   ├─ 3  audit + repair ───────► data/audits/
   │
   ├─ 4  vocabulary repair ────► data/vocabulary/bottom_up_<corpus>.<chain>.json
   │
   ├─ 5  finalize ─────────────► data/analysis/garden_*.json  fork_stage_*.json
   │
   ├─ 6  analyse ──────────────► data/analysis/
   │
   ├─ 7  audit the analyses ───► data/audits/
   │
   ├─ 8  figures ──────────────► figures/
   │
   └─ 9  validation gate ──────► data/ablation/  data/audits/ablation.json
```

One command runs the whole thing:

```bash
python3 scripts/build_all.py --corpus ai,human --repair --gate
```

---

## Stage 1 — distill

| script | reads | writes |
|---|---|---|
| `distill.py all --corpus ai` | AI corpus (`FORKSCOPE_RAW_AI`) | `data/distilled/<run>/` |
| `distill.py all --corpus human` | `data/raw/human_corpus/` | `data/distilled/team-NN/` |
| `distill.py index` | all records | `data/corpus/` |

Per run: `code_spans.json`, `prose_spans.json`, `record.json`.

**S1 segmentation** (`01_segment_code`, `02_segment_prose`) partitions each
artifact exhaustively — every line lands in a decision or a typed non-decision.
Coverage is enforced as a retryable invariant, not checked afterwards, because
it is the basis of every downstream claim. Code spans are exclusive; prose is
exhaustive but **not** exclusive, since one sentence can assert two things.

**S2 linking** (`03_link`) aligns code decisions to prose claims. The residue is
the finding: a decision with no matching claim is *silent*; a pair that
disagrees is *misaligned*.

## Stage 2 — cluster

| script | reads | writes |
|---|---|---|
| `cluster_up.py l1 --corpus ai` | `data/distilled/` | `data/analysis/l1_ai.json` |
| `cluster_up.py l1 --corpus human` | `data/distilled/` | `data/analysis/l1_human.json` |
| `cluster_up.py build --corpus ai,human` | both L1 files | `data/vocabulary/bottom_up_ai+human.json` |

Bottom-up, no cap on option count, no embeddings — 95% of option labels are
unique, so no vector or string metric carries this vocabulary.

**L1 runs per corpus, L2/L3 over the union.** L1 batching depends on sorting the
whole item set, so adding the human teams to a pooled sort would reshuffle every
batch and invalidate the cached AI calls. Splitting is also the right shape: L1
is local grouping, L2 is global merging.

**Cluster pooled for any AI-vs-human claim.** Clustering separately yields two
incomparable vocabularies.

## Stage 3 — audit and repair the clustering

| script | writes | what it checks |
|---|---|---|
| `audit_clusters.py` | `data/audits/audit_<tag>.json` | A1–A9 |
| `repair_clusters.py` | updates the vocabulary | R1–R4, **splits only** |

R1–R4 never merge. Over-merge is invisible in the output and unrecoverable;
under-merge is visible and fixable later.

## Stage 4 — vocabulary repair

Four passes, each writing a **new tag** rather than overwriting, so every number
ever reported stays reproducible from the vocabulary that produced it. The
filename carries the lineage.

| # | script | prompt | writes |
|---|---|---|---|
| 4a | `merge_options.py` | `19_option_granularity` | `…merged.json` |
| 4b | `merge_forks.py` | `21_fork_identity` | `…forkmerged.json` |
| 4c | `merge_options.py` | `19_option_granularity` | `…merged.json` |
| 4d | `induce_forks.py` | `22_induce_forks` | `…induced.json` |

**Order is load-bearing.** Options are collapsed first, then duplicate decision
points merged — and then options are collapsed *again*, because while duplicate
forks stood, the same action sitting in two of them was never compared to
itself. That second pass collapses options no earlier pass could see.

**4b guards transitivity twice**: an explicit veto where a pair was adjudicated
*different*, and a density floor requiring a fork to be judged the same as 60%
of a group before joining it. Only a small fraction of all fork pairs are ever
adjudicated, so absence of contrary evidence is not evidence.

**4d is the real clustering step.** Options are grouped by *purpose* — rival
answers to one question — with foreclosure as the test: could one analyst do
both in one script? That criterion cuts against surface similarity in both
directions, which is why no lexical method substitutes for it:

- *drop rows with no rating* / *impute from the other rater* — **one** fork
- *drop rows with no rating* / *drop goalkeepers* — **two** forks

| script | purpose |
|---|---|
| `compare_vocab.py` | prints every vocabulary stage side by side |

## Stage 5 — finalize

| script | writes |
|---|---|
| `finalize_vocab.py --corpus <tag>` | `data/analysis/garden_<tag>.json`, `fork_stage_<tag>.json` |

Coverage and script position are **recomputed**, not inherited — both change
when forks merge. DSLC stages (`14_fork_stage`) are assigned only for fork
labels that are new; unchanged labels keep theirs.

Stage assignment is deliberately **blind to script position**, so that
comparing stage against position later is not circular.

## Stage 6 — analyse

| script | writes | question |
|---|---|---|
| `stability.py` | `stability_<tag>.json` | which decision points are settled, which contested |
| `novelty.py` | `novelty_<tag>.json` | what novel options are, who takes them, do they move the answer |
| `novelty_curve.py` | `figures/novelty_curve.svg` | dose–response and stage bands |
| `iteration.py run` | `iteration_<tag>.json` | how often analyses return to an earlier stage, and what triggers it |
| `garden.py siblings\|map` | `garden_*.json` | node classes, conditional structure, path coverage |
| `shapley_v2.py` | `shapley_<tag>.json` | which decision points move the reported outcome |
| `fork_graph.py` | `fork_graph_<tag>.json` | do decision points co-occur or co-determine beyond chance |
| `rationale.py` | `rationale_*.json` | decision points clustered by what they rest on |
| `cluster.py silent` | `silent.json` | what kinds of decision go undisclosed |
| `cluster.py misaligned` | `misaligned.json` | what kinds of code/prose disagreement occur |

`cluster.py` induces a typology from the items themselves and then assigns
every item to it, allowing `NEW` throughout; the residual NEW rate after
re-assignment is reported, so a typology that does not fit the data says so.
Its `forks` and `options` modes are superseded by `cluster_up.py` and the
repair chain in stage 4 — only `silent` and `misaligned` are current.

## Stage 7 — audit the analyses

Each analysis ships with an audit that runs beside it. The audits have
overturned reported results, so they are stages rather than optional checks.

| script | checks | writes |
|---|---|---|
| `audit_iteration.py` | I1–I6 | `iteration_audit_<tag>.json` |
| `audit_garden.py` | G1–G6 | `garden_audit_<tag>.json` |
| `audit_shapley.py` | H1–H6 | `shapley_audit_<tag>.json` |
| `audit_granularity.py` | option redundancy | `granularity_audit_<tag>.json` |
| `audit_lineage.py` | decision→option purity, option→fork identity | `lineage_audit_<tag>.json` |
| `audit_vocab.py` | V1–V5, the vocabulary's own falsification exhibits | `vocab_exhibits.json` + `.md` |

### The evidence contract

Every check emits four things, not one: a **verdict**, the **measurement** and
the null it was compared against, the **exhibits** — the actual items — and
**handles** that walk each item back to source lines.

Two rules are enforced in `exhibit.py` rather than left to discipline:

- **Exhibits are worst-first.** `exhibit()` requires a `worst` key function and
  sorts by it, so there is no way to attach a representative sample. A check
  earning trust shows the cases closest to breaking it.
- **A REVIEW verdict with no exhibits is an error** and `Report.write()`
  refuses it. A check that fails and cannot show what failed is not reviewable.

A weak signal is a legitimate sort key for human attention and is never
evidence of absence. Checks that rank by one say so in the exhibit's note and
do not claim PASS on its strength.

## Stage 8 — figures

| script | writes |
|---|---|
| `circle.py` | `figures/circle.html` |
| `fork_atlas.py` | `figures/fork_atlas.svg` |
| `fork_graph.py` | `figures/fork_graph.svg` |
| `iteration.py run` | `figures/iteration.svg` |
| `novelty_curve.py` | `figures/novelty_curve.svg` |

## Stage 9 — validation gate

| script | writes | question |
|---|---|---|
| `ablation.py sample\|match\|report` | `data/ablation/`, `data/audits/ablation.json` | can decisions be recovered from prose alone? |
| `audit_ablation.py` | `data/audits/ablation_audit.json` | E1–E6, including the mismatched-run null |

This decides whether prose-only runs can be admitted, which is why it exists:
extraction is code-anchored, so 12 human teams currently contribute no
decisions.

---

## Support modules

| script | role |
|---|---|
| `paths.py` | every path in one place. Scripts import it rather than deriving their own |
| `llm.py` | the only module that talks to a model. Caching, retries, schema validation |
| `vocab.py` | resolves which garden file belongs to which vocabulary |
| `trace.py` | walks any fork, option, decision or run back to its source lines |
| `exhibit.py` | the evidence contract every check writes through |
| `build_all.py` | runs stages 1–9 in order |
| `_selfcheck.py` | asserts the package is complete and internally consistent |
| `check_outcomes.py` | verifies `outcomes.json` against the per-run fragments behind it |
| `review_round.py` | opens a review round from the audit exhibits, and reads the human's answers back |
| `paths.py` | also the code/study seam — `CODE_ROOT` for the shared instrument, `STUDY_ROOT` for one study's data |
| `trace.py` | walks any fork, option, decision or run back to its source lines |

## Driving it

| invoke | does |
|---|---|
| `/chart` | the whole pipeline for one study |
| `/audit` | the check sets, with their evidence |
| `/review-garden` | the worst-first review queue |
| `/investigate` | walk one claim to its source lines |
| `/challenge` | escalate a test, enlarge a sample, re-adjudicate |

Agents: `auditor` verifies one finding adversarially; `interpreter` turns
verdicts into prose. What may be an agent and what must be a script is settled
in [`DESIGN.md`](DESIGN.md).

## Maintenance

The cache is the reproducibility mechanism, and it only works while the prompt
that produced an answer is the prompt still shipped — the cache key includes a
hash of the prompt text.

| script | purpose |
|---|---|
| `relink.py` | re-ask `03_link` where the committed answer predates a prompt edit, and rebuild every number derived from it. Needs no raw corpus: it works from the segmentations already on disk |
| `prune_cache.py` | move cached answers the shipped pipeline can no longer reach **out** of the package. Superseded work is project history, not evidence about this pipeline |
| `fix_vocab_counts.py` | recompute the `n_options` / `n_forks` headers from the options array. Written after six of ten vocabulary files were found still reporting their base counts, because every repair pass rewrites `options` and none updated the header. `--check` reports, `--apply` fixes |

Both `relink.py` and `prune_cache.py` default to a dry run.

## Acquisition, promotion, figures

| script | purpose |
|---|---|
| `fetch_corpus.py` | acquire the raw corpora from upstream and verify them. The corpus is not vendored — it is not ours to redistribute — so this is step 1 of running the package from scratch. `status`, `fetch`, `checksum`, `verify` |
| `promote_repair.py` | run a structural repair into `data/vocabulary`, rebuild every tag-keyed analysis and audit, re-render the figures, and rewrite `study.json:final_tag` **last**, so a failure anywhere above leaves the study pointing at a vocabulary whose analyses all exist |
| `settle.py` | record that a human has settled a layer, as a lock carrying a **content hash** of what they settled. A note would not do: the failure it prevents is silent — re-run distillation after settling it and every charting number rests on an extraction nobody reviewed, with nothing erroring. `status`, `lock`, `unlock`, `verify` |
| `forkscope_check.js` | run the generated viewer's JavaScript against a DOM stub and call every entry point. `node --check` proves it PARSES; this proves it RUNS. A ReferenceError in `drawG` once shipped silently -- the page loaded, tabs switched, and the ring numbering and every click handler were dead. Needs node; the analysis container has none |
| `forkscope.py` | render `figures/forkscope.html` — one viewer over the garden, the pivotal forks, and the corpus. Reads only artifacts the pipeline already wrote and computes no statistic of its own; a viewer that recomputed would be a second implementation to keep in agreement with the first |
| `build_figures.py` | render every figure for one study root from `final_tag`. Exists because the figure scripts take `--corpus`, and passing the obvious `ai,human` resolves to the *unrepaired* base vocabulary and draws a plausible wrong picture with every stage exiting 0. Defaults to `final_tag` and warns loudly when overridden |

## Reproducibility

The CLI exposes no temperature and no seed, so **the cache is what makes a
re-run return the previous run's answers**. `cache/llm_cache/` is keyed on
`sha256(prompt + model + payload + schema)` and is committed for that reason.

That also means a prompt edit invalidates exactly its own entries and nothing
else — which is correct, and why prompt text is versioned alongside the cache.

`cache/llm_runs/` is the per-call log: timing, tokens, cost, retry count.

Sampling and bootstraps are seeded. Permutation tests escalate their draw count
for anything that survives a screen, because a permutation *p* cannot fall
below 1/(B+1) and a multiplicity-corrected threshold often sits below the floor
of a cheap screen.
