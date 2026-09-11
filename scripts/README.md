# scripts/ — what each one does and what it depends on

46 scripts. [`../docs/WORKFLOW.md`](../docs/WORKFLOW.md) gives the pipeline in
running order; this is the dependency view — which script imports which, who
produces what another consumes, and the three patterns that explain the rest.

## Four foundations, imported by nearly everything

| module | role | why it is separate |
|---|---|---|
| `paths.py` | every path in one place | Scripts import it rather than deriving their own. Several read a vocabulary another one writes, and when two disagree about where it lives nothing crashes — it reads the wrong vocabulary and reports numbers that look fine |
| `llm.py` | the only module that talks to a model | Caching, retries, schema and invariant validation. Transport failures retry unchanged; content failures retry with the specific complaint appended. Conflating the two once cost 154 of 204 runs in one burst |
| `vocab.py` | resolves which garden file belongs to which vocabulary tag | Filenames carry lineage; this is the one place that decodes it |
| `exhibit.py` | the evidence contract every new check writes through | Enforces worst-first exhibits and refuses a REVIEW with nothing to show |

`trace.py` is the fifth, and the one to reach for first when reading anything:
it walks a fork, option, decision or run back to its source lines. Nothing else
joins those files for you.

## The dependency graph

Arrows point from consumer to producer. Only cross-script imports are shown.

```
distill.py ──▶ llm, paths                    relink.py ──▶ distill, llm, paths
cluster.py ──▶ llm, paths                    cluster_up.py ──▶ cluster, llm, paths

repair_clusters.py   ──▶ audit_clusters      merge_options.py ──▶ audit_granularity, vocab
                                             merge_forks.py   ──▶ audit_lineage, vocab
finalize_vocab.py    ──▶ vocab               induce_forks.py  ──▶ audit_lineage, paths

shapley_v2.py ◀── audit_shapley, fork_graph
fork_graph.py ◀── circle.py
garden.py     ◀── audit_garden.py
trace.py, exhibit.py ◀── audit_vocab.py
```

Two things worth reading off it.

**The repair scripts import the audits, not the other way round.** That is the
run/apply split: an audit makes the model calls and writes its verdicts, then a
repair script reads those verdicts and rewrites the vocabulary. `merge_options`
and `merge_forks` never call a model. The judgement is inspectable before it is
applied, and re-applying costs nothing.

**`shapley_v2.py` is imported for its design matrix, not its results.** Four
scripts build a run × fork table and it is defined once, so a change to how
*absent* is encoded propagates everywhere instead of to three of four places.

## By job

### Extract — raw scripts to per-run records
| script | writes |
|---|---|
| `distill.py run\|all` | `data/distilled/<run>/{code_spans,prose_spans,links,record}.json`, `summary.md` |
| `distill.py index` | `data/corpus/*.tsv`, `index.md` |
| `relink.py` | rebuilds links and everything derived, under the shipped prompt |

`distill.py` is the only script that reads the raw corpora. Everything
downstream works from `data/distilled/`, which is why most of the pipeline runs
with no external data.

### Cluster — decisions to options to forks
| script | writes |
|---|---|
| `cluster_up.py` | `data/vocabulary/bottom_up_<tag>.json` |
| `cluster.py silent\|misaligned` | `data/analysis/{silent,misaligned}.json` |
| `repair_clusters.py` | split-only repairs |
| `merge_options.py` | `<tag>.merged.json` |
| `merge_forks.py` | `<tag>.forkmerged.json` |
| `induce_forks.py` | `<tag>.induced.json` |
| `finalize_vocab.py` | stage labels on the finished vocabulary |
| `compare_vocab.py` | every stage side by side |

**Order is load-bearing** — options, forks, options *again*, induce. The second
option pass is not redundant: while two forks were still duplicates their
option lists could not see each other. `cluster.py`'s `forks` and `options`
modes are superseded by `cluster_up.py`; only `silent` and `misaligned` are
current.

### Analyse
| script | answers |
|---|---|
| `stability.py` | which forks are settled, which contested |
| `novelty.py`, `novelty_curve.py` | who invents options, does it move the answer |
| `iteration.py` | how often analyses return to an earlier stage, and what triggers it |
| `garden.py` | node classes, conditional structure, path coverage |
| `shapley_v2.py` | which forks move the reported outcome |
| `fork_graph.py` | do forks co-occur or co-determine beyond chance |
| `rationale.py` | forks clustered by what they rest on |
| `ablation.py` | can decisions be recovered from prose alone |

### Audit
`audit_clusters` (A1–A9) · `audit_iteration` (I1–I6) · `audit_garden` (G1–G6) ·
`audit_shapley` (H1–H6) · `audit_ablation` (E1–E6) · `audit_granularity` ·
`audit_lineage` · `audit_vocab` (V1–V5)

The audits are pipeline stages, not optional checks — they have overturned
reported results. `audit_vocab` writes through `exhibit.py` and ships the items,
worst-first; the older sets emit verdicts and statistics, and retrofitting them
is open work.

### Draw
`fork_atlas.py` · `fork_graph.py` · `circle.py` · `iteration.py`
· `novelty_curve.py` · `forkscope.py`

All write to `figures/`. `forkscope.py` inlines `iteration.svg` and
`novelty_curve.svg`, so those two are rendered first.

### Drive and check
| script | |
|---|---|
| `build_all.py` | runs the stages in order; `--repair` adds the vocabulary repair chain |
| `_selfcheck.py` | asserts the package is complete and internally consistent |
| `prune_cache.py` | moves unreachable cached answers out of the package |
| `trace.py` | walks any object back to source |

## Conventions worth knowing before editing

**`--corpus <tag>` everywhere.** The tag selects the vocabulary, and mixing
tags does not crash — it silently answers a different question. Default is the
headline tag in `paths.FINAL_TAG`.

**Two-phase scripts take `run` then `apply`.** `run` makes the model calls and
writes verdicts; `apply` rewrites the vocabulary from them.

**Permutation tests escalate.** A permutation *p* cannot fall below 1/(B+1),
and a multiplicity-corrected threshold often sits below the floor of a cheap
screen — so a test can report "nothing significant" by construction. Every
permutation test here raises its draw count for anything surviving a screen.
This bug appeared four separate times; assume it recurs.

**Seeds are fixed and stated.** Sampling and bootstraps are seeded. The model
is not — the CLI exposes no temperature or seed, so determinism comes from the
cache.

## Checking your change did not break the package

```bash
python3 scripts/_selfcheck.py
```

It fails if a script is undocumented, a prompt is uncalled, a documentation
link is dead, a data directory lacks a README, or the vocabulary and its node
table disagree. It has caught each of those at least once.
