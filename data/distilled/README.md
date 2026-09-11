# distilled/ — one folder per run

235 folders, one per analysis, named by run id — an ISO timestamp for AI runs
(`2025-11-29T01-11-34+0000`), `team-NN` for human teams. This is the extraction
layer: everything downstream is built from it, and nothing here has been
clustered yet.

> 235 folders but 223 runs in the reported vocabulary. Twelve human teams
> deposited no script. They contribute prose spans and **zero decisions**,
> because extraction is code-anchored. It is the
> largest threat to any AI-versus-human claim in this project.

## Five files per run

All written by `distill.py run`; `relink.py` rewrites the last three when
`03_link` changes.

| file | |
|---|---|
| `summary.md` | **start here** — human-readable, one run at a glance |
| `record.json` | the run's identity, counts, and its silent decisions |
| `code_spans.json` | the script, partitioned |
| `prose_spans.json` | the write-up, partitioned |
| `links.json` | which claim describes which decision |

### `code_spans.json` — exhaustive and exclusive

```json
{"n_lines": 301,
 "spans": [{"id": 5, "kind": "decision", "lines": [[30, 31]],
            "operation": "load the raw player-referee dyad dataset",
            "targets": ["df"], "confidence": "high"},
           {"id": 1, "kind": "intron", "subtype": "comment",
            "lines": [[1, 12]], "note": "module docstring"}]}
```

Every line lands in exactly one span. `kind` is `decision` or `intron`, and
introns are **typed rather than discarded** — `print`, `comment`, `import`,
`config` — because "this line does nothing analytically interesting" is a claim
that should be inspectable. The partition is enforced as a retryable invariant
during extraction, not checked afterwards.

`lines` is a list of ranges because a decision need not be contiguous: a
variable created at line 30 and used at line 140 is one decision.

### `prose_spans.json` — exhaustive, **not** exclusive

Same shape. Not exclusive because one sentence can assert two things and a line
of code cannot.

### `links.json`

```json
{"links": [{"decision_id": 5, "claim_id": 12, "agreement": "agree",
            "confidence": "high", "note": "…"}]}
```

**What fails to link is the point.** A decision no claim mentions is *silent*;
a linked pair that disagrees is a *misalignment*. Both are recovered from the
residue of an alignment, which is why they can be counted rather than
illustrated. Corpus-wide rollups: `../analysis/silent.json`,
`../analysis/misaligned.json`.

### `record.json`

`run_id`, `corpus`, `arm`, `artifacts` (the source filenames), `coverage`,
`counts`, `presence`, plus `silent_decisions[]` and `misalignments[]` inline.

`arm` is the persona brief the AI run was given — `standard`, `positive`,
`negative`, `confirmation_seeking`, `strong_confirmation_seeking` — or `human`.
It is the only assigned variable in the study; everything else is
observational.

## Reading a run

```bash
cat data/distilled/2025-11-29T01-11-34+0000/summary.md

# the same run as a path through the garden, with fork and stage per line
python3 scripts/trace.py run 2025-11-29T01-11-34+0000
```

```
run:2025-11-29T01-11-34+0000  ai / confirmation_seeking
  22 decisions on the vocabulary · 1 silent · 0 misaligned
  line   30  [data_collectio] load the raw, unfiltered player-referee dyad dataset
  line   37  [data_cleaning ] average the two raters into one continuous score
  line   39  [eda           ] Pearson correlation only
```

## What is not here

**The original scripts.** Spans carry line ranges and an operation description,
not the source text — the corpora are third-party and not vendored
([`../raw/MANIFEST.md`](../raw/MANIFEST.md)). Most review questions are
answerable from the operation description alone. For the literal lines:

```bash
export FORKSCOPE_RAW_AI=/path/to/agentic-forking-path
python3 scripts/trace.py option "average the two raters" --source
```
