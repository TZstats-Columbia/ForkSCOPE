# Raw inputs

Two source corpora, neither vendored here. Both are third-party, both are
large, and both are published elsewhere under their own terms — so this
repository records exactly what it consumed and where to get it, rather than
redistributing it.

Everything downstream of these two inputs **is** in this repository, so the
analyses can be re-run and audited without fetching anything. You only need the
raw corpora to re-run **stage 1 (distill)**, which is the one stage that reads
them.

---

## 1. AI corpus — 207 agentic analysis runs

Independent LLM analyses of the Silberzahn et al. soccer dataset, produced by
the AWS *agentic forking paths* study.

- **Source:** `amazon-science/agentic-forking-path`
- **Model:** `bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0`
- **Expected location:** `data/raw/afp/`, or set `FORKSCOPE_RAW_AI` to wherever
  it is unpacked.
- **Path read:**
  `<root>/experiment_data/workspaces/*/bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0/sample_soccer/*`

| artifact | role | present | note |
|---|---|---:|---|
| `final_analysis.py` | code | 207 | the script the run wrote and executed |
| `mirrored_report.txt` | prose | 206 | the run's own report; one file is 0 bytes, so 205 are usable |
| `transcript.json` | trace | 207 | reasoning and tool trace. Content blocks are Python reprs, not JSON, so text must be extracted by pattern |

**Deliberately not used.** `decisions_mapped.json` is the AWS team's own
decision extraction against a fixed 21-slot schema. Using it as input would
import the taxonomy this project exists to avoid. It is worth reading as a
comparison: 33% of what their extractor found (1,120 items over 207 runs)
landed in `unmapped_decisions`, which is a ready-made inventory of what a fixed
schema cannot hold.

`sonnet_llmj.txt` is likewise their derived judgement and is not read.

## 2. Human corpus — 31 analyst teams

The original many-analysts study: independent teams analysing the same dataset.

- **Source:** OSF, Silberzahn et al., *Many analysts, one data set*
- **Expected location:** `data/raw/human_corpus/team-NN/`

| artifact | role | present | note |
|---|---|---:|---|
| `script.txt` | code | 19 | R, Stata, SPSS, Stan or Python saved as `.txt`. **12 teams deposited none** |
| `survey.txt` | prose | 28 | the Stage-3 questionnaire, field-structured |
| `report.txt` | prose | 29 | the post-feedback manuscript |

**Not redistributed here.** These are participant-supplied documents from a
human-subjects study; republishing them is a consent and licensing decision for
the original authors, not a default of this pipeline.

### The 19-of-31 consequence, stated plainly

Decision extraction is **code-anchored**: a decision is an operation on data,
recovered from a script. Prose is read to detect what was *claimed*, which is
how silent decisions and misalignments are found, but a claim is not itself a
decision record.

So the 12 teams with no script contribute **no decisions**, and the pooled
analysis rests on 19 human teams, not 31. Those 12 teams do contribute 1,123
prose spans, which the ablation gate uses.

This is a real limitation and the code-ablation gate exists to measure it. See
the Limitations section of `report/REPORT.md`.

---

## Fetching

Use `scripts/fetch_corpus.py` rather than doing this by hand — it pins the
commit, scopes the LFS pull, and checks for unfetched pointer files:

```bash
python3 scripts/fetch_corpus.py fetch    --dest ../corpus
python3 scripts/fetch_corpus.py checksum --dest ../corpus
python3 scripts/fetch_corpus.py verify   --dest ../corpus

export FORKSCOPE_RAW_AI=/path/to/corpus/afp
export FORKSCOPE_RAW_HUMAN=/path/to/corpus/human_corpus
```

The AI corpus is pinned at `d489f03b143fcaa9befb8cc443594ff63ec61eaa`; the
soccer dataset comes from OSF node `c9mkx`. The 31 human team directories are
**not** fetched automatically — see the consent note above.

### Integrity

`CHECKSUMS.txt` in this directory records SHA-256 and size for all **697**
artifacts any stage reads:

| | count |
|---|---:|
| `final_analysis.py` | 207 |
| `mirrored_report.txt` | 206 |
| `transcript.json` | 207 |
| `script.txt` / `survey.txt` / `report.txt` | 19 / 28 / 29 |
| `soccer_raw.csv` | 1 |

Naming a source and a commit says where bytes came from; it does not say the
bytes you have are the bytes we read. Upstream can be re-tagged, and a Git-LFS
pointer left unfetched is valid UTF-8 of ~130 bytes that parses cleanly and
silently turns a run into one with no report. That failure occurred here once.
`verify` catches it.

### Where this copy lives

On the machine that produced the published results, the corpora were mounted
from a Docker volume named `distill-corpus` (at `/corpus` inside the container),
which is why `inputs.json` records paths under `/corpus/afp/...`. A Docker
volume is **not** durable storage — `docker volume prune` removes any volume no
container is using, and the data sits inside the WSL2 VM disk where ordinary
file backup cannot see it. A plain-file copy is kept outside the repository,
and `CHECKSUMS.txt` is what ties any copy to the one the results were computed
from.

`inputs.json` in this directory is the machine-readable version of the two
tables above, and is what `distill.py` reads to decide which artifacts are raw
input and which are excluded as someone else's derived analysis.
