# ablation/ — validation gate 5.4

*Can decisions be recovered from prose alone?* This decides whether the twelve
human teams that deposited no script can enter the analysis at all.

All three are written by `ablation.py`.

| file | |
|---|---|
| `sample.json` | which runs were tested — `seed`, `frac`, `n_eligible`, `runs` |
| `matches.json` | code decisions matched against the **same** run's prose |
| `matches_null.json` | run *i*'s code against run *j*'s prose — the calibration |

Verdicts: [`../audits/ablation.json`](../audits/ablation.json).

## Read the null before the headline

| | |
|---|---|
| recall — code decisions prose also found | 0.593 |
| agreement — matched pairs choosing the same option | 0.952 |
| **null — mismatched runs** | **0.489** |

The matcher pairs *unrelated* runs at 82% of the within-run rate. Every run
analyses the same dataset and makes many of the same decisions, so a cross-run
match is often a real correspondence — just not evidence that prose recovered
*this* run's choice. **The 0.952 cannot be read as a pass on its own.**

What survives calibration is agreement *conditional on matching*: 0.952
within-run against 0.649 cross-run.

So: **prose is accurate where it speaks, and silent often.** 40.7% of code
decisions are never mentioned. The human corpus is weaker on both counts
(recall 0.534 vs 0.642; agreement 0.847 vs 0.921). Prose-only teams could enter
at coarser granularity; they are not equivalent to code-backed runs.

This is why `matches_null.json` exists as a first-class output rather than a
diagnostic. A matching metric without a mismatched-run baseline measures how
similar the corpus is to itself.
