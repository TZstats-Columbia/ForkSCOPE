# analysis/ — every reported number

47 files. Each is named `<analysis>_<vocabulary tag>.json`, and the tag decides
which garden it describes. **Every reported result uses the longest tag,**
`ai+human.merged.forkmerged.merged.induced.r3.osplit` — written `<FINAL>` below.

Files carrying an earlier tag are kept for lineage — the node tables and the
adjudications each repair pass produced — and `compare_vocab.py` reads them to
show the chain from 463 forks (441 nodes once siblings are collapsed) to 317. Quote results only from the `<FINAL>`
files.

Nothing here is a conclusion. Each file pairs with an audit in
[`../audits/`](../audits/) that tests whether its numbers survive a null, and
in several cases they do not.

## The main outputs

| file | made by | question | key fields |
|---|---|---|---|
| `garden_<FINAL>.json` | `garden.py` | what is the garden? | `nodes_detail` (one per fork: `runs`, `coverage`, `options`, `stage`), `universal`, `gates` |
| `stability_<FINAL>.json` | `stability.py` | where do analysts agree? | `forks` (modal share, effective options), `stable_share`, `by_arm`, `spectrum` |
| `shapley_<FINAL>.json`, `.pivotal.json`, `.novelty.json` | `shapley_v2.py` | do choices predict the answer? | `players`, `payouts`, `lambda_grid`, `bootstrap` — the expanded player set, the 17 pivotal forks alone, and novelty as an added player |
| `iteration_<FINAL>.json` | `iteration.py` | does the lifecycle loop? | `return_rate`, `runs_with_return`, `back_pairs`, `triggers` |
| `fork_graph_<FINAL>.json` | `fork_graph.py` | are forks related? | `co_reach`, `co_choice`, each with its threshold |
| `novelty_<FINAL>.json`, `novelty_curve_<FINAL>.json` | `novelty.py`, `novelty_curve.py` | who invents new options, and does it move the answer? | `by_fork`, `by_arm`, `run_scores`; the binned curve |
| `circle_<FINAL>.json` | `circle.py` | which routes do personas take? | `routes_drawn`, `enrichment`, `persona_share` |
| `fork_stage_<FINAL>.json` | `finalize_vocab.py` | which DSLC stage is each fork? | flat map: fork label → stage |

## Residue — where several findings live

| file | |
|---|---|
| `silent.json` | `cluster.py silent` — decisions made in code that no prose claim mentions — 333 across 148 forks, 15 categories |
| `misaligned.json` | `cluster.py misaligned` — code and write-up describing the same operation differently — 95 items, 9 categories |

Both are the *residue of an alignment* rather than something searched for
directly, which is why they can be counted instead of illustrated. Each has
`items`, `categories`, `n_runs`.

## Intermediate — clustering provenance

Read these when you want to know *why* two things merged.

| file | |
|---|---|
| `l1_ai.json`, `l1_human.json` | first-layer local grouping (`items`, `groups`) — the input `cluster_up.py` rebuilds the vocabulary from |
| `garden_ai.json`, `garden_ai+human.json` | node tables for the earlier vocabulary stages. Structural, not analyses: `compare_vocab.py` needs them to show 441 → 317 |
| `garden_siblings_*`, `fork_stage_*` | sibling collapses and stage labels for those stages |
| `option_merge_*.json` | per-fork paraphrase adjudications (`forks`, `failures`) |
| `fork_merge_*.json` | pairwise fork same/different verdicts |
| `induced_forks_*.json` | the purpose-grouping pass (`decision_points`, `violations`) |
| `ablation.json` | the code-ablation gate's summary; the audited copy is `../audits/ablation.json` |

## Reading a fork's numbers without parsing JSON

```bash
python3 ../../scripts/trace.py fork "discretized into categories?"
python3 ../../scripts/stability.py --corpus ai+human.merged.forkmerged.merged.induced.r3.osplit
```

## Two traps

**Do not mix tags.** `garden_ai.json` and `garden_<FINAL>.json` are both real
and describe different vocabularies. Joining across them produces numbers that
look fine and mean nothing.

**Do not quote the Shapley bootstrap CIs.** `strength` is a mean of absolute
values, so its bootstrap interval **cannot cover zero** regardless of the data
— it is not a test. Use the permutation null in
[`../audits/shapley_audit_<FINAL>.json`](../audits/) instead. The
cross-validated R² there is what to quote: on the 17 pivotal forks, +0.262 for
the verdict, +0.246 for *z*, +0.032 for log(OR) and +0.046 for interval width.
