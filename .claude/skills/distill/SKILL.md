---
name: distill
description: >-
  Stage S — segment every artifact in the corpus into typed spans and align the
  prose to the code, producing the per-run decision records the rest of the
  pipeline is built on. Use when extraction needs running, re-running, or
  checking on a sample, before /chart and before /settle distill.
---

Extract the decisions. Argument: `all`, or one run id.

This is the layer everything else inherits. A fork that extraction never saw
cannot be recovered by any downstream repair, and an over-eager span becomes an
option nobody can trace. **Distillation is settled at its own gate, separately
from charting**, because the two fail independently — see `/settle`.

## What a decision is, and what it is not

An **operation on data that could have gone otherwise.** Fixed, not
configurable. A corpus that appears to need the definition changed is a finding
about the instrument, to be reported — not a parameter to set.

Every line of every artifact is typed. Lines that act are **exons**; prints,
comments, imports and plot theming are **introns**. Nothing is skipped, so
coverage is an invariant rather than a hope. On soccer the median artifact is
38.5% exon: most of a script is not decisions.

Prose is read separately and aligned to the code. **What fails to align is the
product.** An operation the code performs and the write-up never mentions is a
*silent decision*; a pair that disagrees is *misaligned*. These are counted, not
illustrated.

## Run it

```bash
python3 scripts/distill.py all --limit 2          # smoke test: two runs
python3 scripts/distill.py all --corpus ai        # one corpus
python3 scripts/distill.py all                    # everything
python3 scripts/distill.py run <run-id>           # one run
python3 scripts/distill.py index                  # rebuild the index
```

**Always `--limit 2` first.** If a glob matches nothing, or an artifact named in
`study.json` is not in a run directory, it surfaces here for two model calls
instead of two hundred. This is the check that pays for itself most often.

`--stratify N` draws N runs spread evenly over persona arms. Use it for any
sample you intend to quote — an unstratified head of the corpus is one
workspace's habits, not the corpus.

`--force` re-extracts past the cache. It writes to the same cache keys, so
running it in place **replaces the extraction a built garden rests on**. If what
you want is a second independent extraction to compare against the first, that
is `/replicate distill`, which isolates at the filesystem level. Do not
improvise it with `--force`.

## What policy governs this stage

From `policy.json:decisions` — every one of these is a fork in *our* pipeline,
and each records whether it was decided or defaulted into:

| entry | soccer value | |
|---|---|---|
| `artifacts_used` | `["code"]` | the garden is code-anchored |
| `prose_role` | `silent_only` | **decided** — prose spans reproduce at ARI 0.480 against 0.895 core for code, which is why |
| `similarity_level` | `lenient` | **decided**, and the single largest lever in the method |
| `same_run_repeat_span_lines` | 5 | **decided** after V6 measured it: 76 of 96 same-run merge groups spanned more than five lines and were over-merges on reading |
| `disjoint_spans_allowed` | true | |
| `interleaving_allowed` | false | **implicit** — nobody argued it, and it constrains what extraction can express. On the `_open` list |

Read them from the file rather than from this table; a study that is not soccer
has its own.

## Check the sample before charting on it

```bash
python3 scripts/_selfcheck.py
python3 scripts/trace.py run <run-id>            # the run's whole path
```

Read two or three runs end to end. The failure this catches is not a crash — it
is an extraction that completed and typed the wrong thing, and no statistic
downstream will tell you.

Worth looking at specifically:

- **A run with almost no decisions.** Usually a prose-only deposit or an
  unfetched Git-LFS pointer, which is valid UTF-8, ~130 bytes, and silently
  becomes a run with no report. `fetch_corpus.py verify` catches the second.
- **A decision whose span covers half the script.** An over-merge at the source,
  before any clustering could be blamed for it.
- **The silent set.** Are these really undisclosed in this field, or
  conventional and unremarked? That is domain knowledge, and it belongs to the
  owner — surface it at `/walk`, do not decide it here.

## What you must refuse

- **Do not edit anything in `prompts/`.** The cache is keyed on prompt text. An
  edit orphans every answer that wording produced and silently decouples the
  shipped data from the prompt beside it.
- **Do not widen the definition of a decision for a corpus.** Record the
  pressure to, and report it.
- **Do not quote a reproducibility figure without its level.** 0.176 verbatim
  and 0.895 core are the same extraction. A stability figure without its
  matching level is not a figure.
- **Do not report extraction as settled.** That is a human's decision, taken at
  `/settle distill`, and it is recorded with a content hash.

## Reporting

Runs attempted, runs with a script, decisions extracted, median % exon, and the
silent and misaligned counts. Then cost, from `cache/llm_runs/`.

**Sum the attempts, not the rows.** Each row carries `attempt`; a row with
`attempt: 3` means three calls were paid for. Rows with `ok: false` are the
retries, logged with the error that caused them. Reporting only the successful
rows undercounted soccer-C by 47% -- $6.71 against $9.84 on ten runs -- and
that undercount reached an owner as an approved budget. Report the retry rate
beside the cost; it is the thing that moves it.

Say how many runs contributed **zero** decisions and why. In soccer 12 of 31
human teams deposited no script, and that became the largest caveat in the
project — it is a fact about the corpus, and it belongs in the first sentence
rather than a footnote.

Hand off to `/settle distill`, then `/chart`.
