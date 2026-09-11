# data/ — how to read the outputs

Everything here is derived. The two source corpora are not vendored; see
[`raw/MANIFEST.md`](raw/MANIFEST.md). Every file below regenerates from them
via the scripts named in [`../docs/WORKFLOW.md`](../docs/WORKFLOW.md).

## The shape of the whole thing

One arrow, left to right, is the entire pipeline:

```
raw scripts ──▶ distilled/ ──▶ corpus/ ──▶ vocabulary/ ──▶ analysis/ ──▶ figures
                per run        indexed     the garden      results
                                              │
                                    audits/ ──┘   checks on each of the above
```

| directory | what it holds | made by | read it when |
|---|---|---|---|
| [`raw/`](raw/) | pointers to the two source corpora, not the corpora | — (fetched) | you want to rebuild from scratch |
| [`distilled/`](distilled/) | one folder per run: its code, prose, and the links between | `distill.py`, `relink.py` | you are inspecting a single analysis |
| [`corpus/`](corpus/) | flat TSVs across all runs | `distill.py index` | you want a spreadsheet |
| [`vocabulary/`](vocabulary/) | decisions → options → forks, one file per repair stage | `cluster_up.py` + the repair chain | you want the garden itself |
| [`analysis/`](analysis/) | every analysis output | one script each — see its README | you want a reported number |
| [`audits/`](audits/) | verdicts **and the evidence for them** | the `audit_*.py` scripts | you want to know whether to believe it |
| [`ablation/`](ablation/) | validation gate 5.4 working files | `ablation.py` | you are checking whether prose alone suffices |
| `outcomes/` | the effect size and conclusion each run reported | **no generator** — see its README | you are linking choices to answers |

## Start here, three ways

**Just looking?** Open [`../figures/forkscope.html`](../figures/forkscope.html) in a
browser, then read [`../report/REPORT.md`](../report/REPORT.md).

**Checking a claim?** Open [`audits/vocab_exhibits.md`](audits/vocab_exhibits.md).
It is a review queue, ordered worst-first — the cases closest to breaking each
claim, never a representative sample.

**Following a thread?** Use the tracer. Nothing else in the repo joins these
files for you:

```bash
python3 ../scripts/trace.py fork "discretiz"          # list matching forks
python3 ../scripts/trace.py fork "fork:0cc97d1e"      # its options, worst-first
python3 ../scripts/trace.py option "average the two raters"
python3 ../scripts/trace.py run 2025-11-29T01-11-34+0000
```

Every audit exhibit cites **handles** (`fork:a1b2c3d4`, `opt:…`,
`dec:<run>@<line>`, `run:<id>`) which resolve directly:

```bash
python3 ../scripts/trace.py resolve fork:8d07b365
```

## The one thing to understand before reading a filename

Filenames carry **vocabulary lineage**, and mixing stages silently gives wrong
answers. The headline vocabulary is:

```
ai+human.merged.forkmerged.merged.induced.r3
```

read left to right as: pooled corpora → paraphrase options collapsed →
duplicate forks merged → options collapsed again now that duplicates are
united → forks re-derived from option purpose.

Every stage is kept rather than overwritten, so any number traces to the
vocabulary that produced it. `garden_ai.json` and
`garden_ai+human.merged.forkmerged.merged.induced.r3.json` are both real and
answer different questions. **The reported results are the longest tag.**

```bash
python3 ../scripts/compare_vocab.py     # every stage side by side
```

## Three vocabulary words

| term | means |
|---|---|
| **decision** | one operation on data that could have gone otherwise, in one run |
| **option** | the same action across runs, in different words — 3,946 decisions → 777 options |
| **fork** | a slot where rival options answer one question — 777 options → 317 forks |

A *fork* is called a **decision point** in the prose docs. Same thing; the code
and data keys use `fork` everywhere.

## Counts, so you can tell whether a file is the one you want

| | |
|---|---|
| runs | 223 (204 AI, 19 human teams) |
| decisions | 3,946 |
| options | 777 |
| forks | 317 — of which **41** are reached by ≥10 runs and are measurable |
| runs with an extracted outcome | 207 (AI only) |

The gap between 317 forks and 41 measurable ones is not an oversight: agreement
measured on four runs is not a measurement. The other 276 are reported as
coverage and never as agreement.

## Before you quote a number

Read the Limitations section of [`../report/REPORT.md`](../report/REPORT.md). Several checks are
left **failing on purpose**, and two of the failures are the finding rather
than a defect. In particular the Shapley bootstrap CIs in
`analysis/shapley_*.json` are a mean of absolute values and **structurally
cannot cover zero** — they are not a test, and the permutation null in
`audits/shapley_audit_*.json` replaces them.
