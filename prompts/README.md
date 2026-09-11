# prompts/ — the adjudications, and why they are versioned

Sixteen prompts, plus `30_silent_identity`, which the charting pipeline does
not call: `stability/scripts/q1c_adjudicate.py` uses it for the semantic
adjudication of silent decisions. Each is a question the pipeline asks a model many times over
many items, and each is **pinned**: the cache key includes a hash of the prompt
text, so editing a file here orphans every answer the old wording produced.

That is the point. These are not conversational instructions, they are the
measuring instrument, and an instrument that changes silently between readings
is not one. Versioning them beside the cache is what lets a re-run return the
committed answers rather than freshly adjudicated ones.

```bash
python3 -c "import sys;sys.path.insert(0,'scripts');from llm import prompt_hash;print(prompt_hash('03_link'))"
python3 scripts/prune_cache.py     # what the shipped prompts can still reach
```

## What each one asks

**Extraction** — one call per run, over raw source.

| prompt | asks | called by | model |
|---|---|---|---|
| `01_segment_code` | partition a script into decisions and typed introns | `distill.py` | sonnet |
| `02_segment_prose` | partition a write-up into claims and typed non-claims | `distill.py` | sonnet |
| `03_link` | which claim describes which decision, and do they agree | `distill.py`, `relink.py` | opus |

`01` must be **exhaustive and exclusive** — every line in exactly one span.
`02` is exhaustive but *not* exclusive, because one sentence can assert two
things and a line of code cannot. Both are enforced as retryable invariants,
not checked afterwards.

**Typology** — categories induced from items, never chosen in advance.

| prompt | asks | called by | model |
|---|---|---|---|
| `10_induce_types` | what categories are actually present in this sample | `cluster.py` | opus |
| `11_assign_types` | assign every item, `NEW` allowed and encouraged | `cluster.py` | sonnet |

`NEW` is encouraged because a residual NEW rate is the measurement: a typology
that does not fit the data has to be able to say so.

**Vocabulary** — decisions → options → forks.

| prompt | asks | called by | model |
|---|---|---|---|
| `12_group_batch` | group a batch of decisions by the action they perform | `cluster_up.py` | sonnet |
| `13_merge_groups` | are these two groups the same action | `cluster_up.py` | sonnet |
| `22_induce_forks` | which options are rivals answering one question | `induce_forks.py` | opus |

`22` is the hard one, and it leads with the two cases that break surface
similarity in opposite directions: *drop rows with no rating* / *impute from
the other rater* are one fork despite sharing no words; *drop rows with no
rating* / *drop goalkeepers* are two despite reading almost identically. Its
operational test is foreclosure — could one analyst, in one script, do both?

**Adjudication for repair** — these produce judgements; other scripts apply them.

| prompt | asks | called by | model |
|---|---|---|---|
| `19_option_granularity` | within one fork, which options are the same action | `audit_granularity.py` | opus |
| `20_option_purity` | do these decisions all belong under this option | `audit_lineage.py` | opus |
| `21_fork_identity` | are these two forks the same question | `audit_lineage.py` | opus |

**This is the run/apply split, and it matters.** `audit_granularity.py` and
`audit_lineage.py` make the model calls and write their verdicts; then
`merge_options.py` and `merge_forks.py` read those verdicts and rewrite the
vocabulary. Neither merge script calls a model. So the judgement is auditable
before it is applied, and applying it again costs nothing.

**Interpretation** — small passes over the finished vocabulary.

| prompt | asks | called by | model |
|---|---|---|---|
| `14_fork_stage` | which DSLC stage does this fork belong to | `finalize_vocab.py`, `iteration.py` | opus |
| `15_fork_relation` | how are these two forks related | `garden.py` | opus |
| `16_align_channels` | does this prose span describe this code decision | `ablation.py` | opus |
| `17_fork_rationale` | what assumption does this fork rest on | `rationale.py` | opus |
| `18_merge_tags` | fold these rationale tags together | `rationale.py` | opus |

`14` is given the fork label and **nothing else** — no line number, no
position, no neighbours. The iteration analysis compares stage against
position, so a stage inferred from position would make it circular. That it
still recovers pipeline order (Spearman ≈ +0.59) is what licenses reading a
deviation as a deviation.

## Model choice

Sonnet does the bulk mechanical passes — segmentation, batch grouping,
assignment against a fixed typology. Opus does every pass where the answer is a
judgement that changes the vocabulary. That split is per-call and recorded in
`cache/llm_runs/`, so it is checkable rather than asserted:

```bash
python3 -c "
import json,glob,collections
c=collections.Counter()
for f in glob.glob('cache/llm_runs/*.jsonl'):
    for l in open(f,encoding='utf-8'):
        if l.strip():
            r=json.loads(l); c[(r['prompt'],r['model'])]+=1
for k,v in sorted(c.items()): print(f'{v:>5}  {k[0]:<24}{k[1]}')"
```

## Editing one

Three things follow, and the third is the one people miss.

1. Its hash changes, so every answer the old text produced becomes unreachable.
2. `prune_cache.py` will report those as superseded and move them out.
3. **The shipped data was produced by the old text and is now inconsistent with
   the prompt beside it.** Re-run the affected stage. `relink.py` exists for
   exactly this case on `03_link`, where the drift went unnoticed until the
   cache was audited.

## What is not here

No prompt has a temperature or a seed — the CLI exposes neither, which is why
the cache rather than decoding parameters is the determinism mechanism. And no
prompt carries the retry logic: transport failures retry with the prompt
unchanged, content failures retry with the specific complaint appended, and
both live in `llm.py` where they cannot be bypassed.
