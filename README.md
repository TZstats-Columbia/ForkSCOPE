# ForkSCOPE

**S**egment · **C**anonicalize · **O**rganize · **P**lot · **E**valuate

Given many independent analyses of one dataset and one question, ForkSCOPE
charts their garden of forking paths bottom-up, from the code and the write-ups
themselves: every fork where an analyst could have chosen otherwise, the option
each analysis took, and what that did to the reported answer. No taxonomy is
fixed before or after generation, and every summary links back to the source
spans that support it.

This repository is the package and the case study behind *ForkSCOPE: Charting
the Agentic Garden of Forking Paths*: the pipeline, its pinned prompts, the
skills and agents that drive it, every intermediate artifact, the model-response
cache that makes a re-run byte-identical and free, the technical report, and the
interactive viewer.

| | |
|---|---|
| analyses charted | **223** — 204 agentic runs, 19 human teams with a script |
| raw decision points | **3,946** |
| options | **777** |
| forks | **317** |
| measurable forks (≥ 10 analyses) | **41** |
| pivotal forks (`eff_all` > 1.5) | **17** |
| headline vocabulary | `ai+human.merged.forkmerged.merged.induced.r3.osplit` |

The headline vocabulary is recorded as `final_tag` in [`study.json`](study.json).
Every reported number carries the tag of the vocabulary it was computed from.

---

## Step 1 — the source corpora are not in this repository

Neither corpus is ours to redistribute. The agentic corpus is published by its
authors under their own terms; the human corpus is participant-supplied
material from a human-subjects study. Both live **outside** the repository and
are read from two environment variables.

```bash
python3 scripts/fetch_corpus.py status                     # what you have
python3 scripts/fetch_corpus.py fetch    --dest ../corpus  # AI corpus + dataset
python3 scripts/fetch_corpus.py checksum --dest ../corpus  # record what you got
python3 scripts/fetch_corpus.py verify   --dest ../corpus  # confirm it matches

export FORKSCOPE_RAW_AI=$(pwd)/../corpus/afp
export FORKSCOPE_RAW_HUMAN=$(pwd)/../corpus/human_corpus
```

| corpus | source | fetched by |
|---|---|---|
| agentic, 207 runs | `amazon-science/agentic-forking-path`, pinned at commit `d489f03`, sparse-checked-out and LFS-pulled for the `claude-sonnet-4-5` `sample_soccer` slice, all five personas | the script |
| soccer dataset | OSF node `c9mkx` | the script |
| human, 31 teams | Silberzahn et al. 2018, *Many analysts, one data set*, the `team-NN` directories on OSF | **you**, under the original study's terms |

[`data/raw/MANIFEST.md`](data/raw/MANIFEST.md) records exactly what is read
from each, and [`data/raw/CHECKSUMS.txt`](data/raw/CHECKSUMS.txt) holds a
SHA-256 for all 697 artifacts the pipeline consumes, so `verify` turns "we used
this corpus" into a claim that can be checked. It also catches the one failure
that happened here: an unfetched Git-LFS pointer is valid UTF-8 of about 130
bytes and silently becomes a run with an empty report.

**You only need the corpora to re-run stage 1 (distill).** Everything
downstream is committed. [`NOT-INCLUDED.md`](NOT-INCLUDED.md) lists the few
other things that are not here and why.

---

## What is here

```
scripts/            the pipeline: distill, cluster, repair, analyse, audit, draw
prompts/            the sixteen pinned prompts the pipeline calls; the cache is keyed on their text
.claude/skills/     the fourteen skills that drive the pipeline (Table 2 of the paper)
.claude/agents/     the auditor and the interpreter
templates/          what a second study must declare
docs/               WORKFLOW (which script writes which file), METHODS, AUDITING, DECIDING, LIFECYCLE, DESIGN
study.json          the study manifest: corpora, artifacts, arms, domain context
policy.json         the method decisions charting rests on, each marked decided or implicit
INTAKE.md           the intake consultation, reconstructed
data/               every intermediate artifact; each directory has its own README
  raw/              pointers to the corpora and their checksums, not the corpora
  distilled/        one directory per run: code spans, prose spans, links, record
  corpus/           flat tables across all runs
  vocabulary/       decisions -> options -> forks, one file per repair stage
  analysis/         every analysis output
  audits/           every audit verdict, with the exhibits that license it
  ablation/         the code-ablation gate's working files
  outcomes/         the effect size and verdict each agentic run reported
cache/              2,791 model responses, content-addressed, and the per-call log
locks/              the settled distillation layer, by content hash
replicates/         manifests and results of the ten fork-formation replicates
stability/          the reproducibility measurements: scripts, data, results, methods
reviews/            the human-benchmark packet, its key, and the results
report/             the technical report
figures/            the viewer, the fork atlas, and the two figures the viewer inlines
```

## Reproduce

Everything downstream of the raw corpora is committed, so every analysis, audit
and figure re-runs with no corpus and no model access. The `claude` CLI exposes
neither a temperature nor a seed, so reproducibility comes from the cache: every
response is stored under a hash of the prompt text, model, payload and schema,
and an unchanged stage is a cache hit that returns byte-identical output.

```bash
pip install -r requirements.txt                 # Python 3.12+, numpy, scipy
python3 scripts/_selfcheck.py                   # 21 assertions on the package
python3 scripts/stability.py  --corpus ai+human.merged.forkmerged.merged.induced.r3.osplit
python3 scripts/compare_vocab.py                # every vocabulary stage side by side
python3 scripts/build_figures.py                # the figures, from data/ only
python3 scripts/forkscope.py                    # -> figures/forkscope.html
```

To prove a run spent nothing, take the `claude` CLI off `PATH`: cache hits are
unaffected and an uncached call fails instead of quietly costing money.

To rebuild from the corpora, do Step 1, then:

```bash
python3 scripts/fetch_corpus.py verify --dest ../corpus
python3 scripts/build_all.py --corpus ai,human --repair --gate
```

Verify first. If `FORKSCOPE_RAW_AI` is unset the build does not fail loudly:
stage 1 finds no runs and the per-arm tables that follow look plausible and are
wrong.

## Where each result in the paper comes from

| in the paper | artifact | made by |
|---|---|---|
| Table 2, the skills | `.claude/skills/` | — |
| Figure 2, the workflow | `docs/WORKFLOW.md` | `scripts/build_all.py` |
| Figures 3, 4 — Corpus Viewer | `figures/forkscope.html`, Corpus Viewer tab; `data/distilled/<run>/` | `scripts/forkscope.py`, `scripts/distill.py` |
| Figures 5, 6, 7 — the Garden | `figures/forkscope.html`, The Garden tab; `data/analysis/circle_<tag>.json` | `scripts/forkscope.py`, `scripts/circle.py` |
| Figures 8, 11 — the fan and the map | `figures/forkscope.html`, Pivotal Forks tab; `figures/fork_atlas.svg`; `data/analysis/stability_<tag>.json` | `scripts/fork_atlas.py`, `scripts/stability.py` |
| Figures 9, 10 — the lifecycle | `figures/forkscope.html`, Lifecycle tab; `data/analysis/iteration_<tag>.json`; `data/audits/iteration_audit_<tag>.json` | `scripts/iteration.py`, `scripts/audit_iteration.py` |
| Table 3, the garden at a glance | `data/vocabulary/bottom_up_<tag>.json`; `data/analysis/stability_<tag>.json`; `data/corpus/silent_decisions.tsv` | `scripts/compare_vocab.py`, `scripts/stability.py` |
| §5.1 prose recall and silent decisions | `data/audits/ablation.json`, `data/audits/ablation_audit.json`; `stability/data/q2_ablation.json` | `scripts/ablation.py`, `scripts/audit_ablation.py` |
| Table 4, out-of-sample prediction | `data/analysis/shapley_<tag>.pivotal.json` and its audit | `scripts/shapley_v2.py`, `scripts/audit_shapley.py` |
| §6.1 reproducibility | `cache/`, `locks/`, `scripts/llm.py` | `scripts/settle.py` |
| §6.2 and Table 5, stability | `stability/data/q1_distill.json`, `layer_agreement.json`, `run_geometry.json`, `forks_that_matter.json`, `q4_replicate_r3.json`, `persona_assoc_*.json`; `replicates/results/fork_variance.json` | `stability/scripts/` |
| §6.3 the human benchmark | `reviews/human-benchmark/`, `stability/results/human_benchmark.json` | `stability/scripts/review_sheet.py`, `score_review.py` |
| §6.4 computation | `cache/llm_runs/` | `scripts/llm.py` |
| supplement, the codebook comparison | `stability/data/aws_compare.json` | `stability/scripts/aws_compare.py` |
| supplement, the case-study decisions | `policy.json`, `INTAKE.md` | `/intake` |
| supplement, the check verdicts | `data/audits/`, `stability/data/audit_stability.json` | the `audit_*.py` scripts |

`<tag>` is the headline vocabulary above. `scripts/trace.py` walks any fork,
option, decision or run back to its source lines:

```bash
python3 scripts/trace.py fork "skin-tone"          # forks matching a phrase
python3 scripts/trace.py resolve fork:8d07b365     # a handle from an audit exhibit
python3 scripts/trace.py run team-01
```

## The viewer

[`figures/forkscope.html`](figures/forkscope.html) is one self-contained page
with four tabs: **The Garden** (every fork on a ring by lifecycle stage, with
the highways analyses travelled), **Pivotal Forks** (which decisions are widely
faced and genuinely contested, and whether they move the answer), **Lifecycle**
(where the work sits by stage, and whether analyses go back) and **Corpus
Viewer** (one analysis at a time, its exon/intron map, and how it compares).
It computes no statistic of its own:
every number on it is read from an artifact under `data/`, and
`python3 scripts/forkscope.py` regenerates it in seconds.

## Skills and agents

Each recurring procedure is a skill in `.claude/skills/`, a Markdown file that a
person invokes by name (`/intake`, `/chart`, `/audit`, `/review`, `/refine`,
`/settle`, `/report`, `/walk`, `/investigate`, `/challenge`, `/itinerary`,
`/inspect`, `/distill`, `/replicate`) or that a command-line agent loads when a
task fits. Two agents in `.claude/agents/` augment the scripted checks: an
**auditor** that tries to refute a reported finding and an **interpreter** that
turns verdicts into prose without changing the numbers.
[`AGENTS.md`](AGENTS.md) holds the rules an agent works under here, and
[`docs/DECIDING.md`](docs/DECIDING.md) what a skill owes the person at each
gate.

## Working with an AI on this

Producing is cheap and checking is not. Scaling output without scaling
*checkability* turns oversight into a rubber stamp, so the burden here is on
the AI to make human input, guidance and oversight cheap: checkable evidence
rather than summaries, organised visualization rather than description, and
exposed vagueness, marking what is uncertain, defaulted or ambiguous instead
of smoothing it into confident prose. Every gate in the pipeline exists to keep
a person in a position to say no.

## The corpora

Silberzahn, R. et al. *Many analysts, one data set: making transparent how
variations in analytic choices affect results.* AMPPS 1(3), 2018 — the human
corpus and the dataset.

Bertran, M., Fogliato, R., Wu, Z. S. *Many AI analysts, one dataset: navigating
the agentic data science multiverse.* PNAS 123(29), 2026;
`amazon-science/agentic-forking-path` — the agentic corpus.
