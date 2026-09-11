# vocabulary/ — the garden itself

Fourteen files, each a complete vocabulary at one stage of repair. This is the
central product: every analysis in `../analysis/` is computed from one of
these, and which one is encoded in its filename.

**The reported results use `bottom_up_ai+human.merged.forkmerged.merged.induced.r3.json`.**

## The files

| file | made by | forks | what changed |
|---|---|---|---|
| `bottom_up_ai.prerepair.json` | `cluster_up.py` | | AI corpus, before numeric/set normalisation |
| `bottom_up_ai.json` | `repair_clusters.py` | | AI corpus, repaired |
| `bottom_up_ai+human.json` | `cluster_up.py` | | both corpora pooled — the starting point |
| `…merged.json` | `merge_options.py` | | paraphrase options collapsed within each fork |
| `…merged.forkmerged.json` | `merge_forks.py` | | duplicate forks merged |
| `…merged.forkmerged.merged.json` | `merge_options.py` | | options collapsed **again**, now that duplicate forks are united and can see each other's options |
| `…merged.forkmerged.merged.induced.json` | `induce_forks.py` | 375 | forks re-derived from option *purpose* |
| `…induced.r1.json` | round 1 of the loop | 329 | fork merge, then options across the united forks |
| `…induced.r2.json` | round 2 | 321 | |
| `…induced.r3.json` | round 3 | **317** | a round moved ≤2% |
| `…induced.r3.osplit.json` | `promote_repair.py` | **317** | the same-run option split applied — **the headline** |

`.rNf` files are the mid-round state, after that round's fork merge and before
its option merge. They exist because each pass writes its output; nothing reads
them, and `compare_vocab.py` skips them.

Three things worth knowing about that table.

**The order is load-bearing.** Options are collapsed, then forks, then options
*again*. The second option pass is not redundant: while two forks were still
duplicates, their option lists were invisible to each other, so paraphrases
across them could not be seen. That pass found 146 further collapses.

**The rounds exist because the fixed order had a gap.** `induce_forks` re-derives
fork labels and ran last, so any duplicate it created was invisible to the fork
merge that had already run. A merge pass after induction found 103 more pairs
that were one question. The passes now loop until a round moves ≤2% of decision
points — three rounds here, 375 → 329 → 321 → 317.

```bash
python3 ../../scripts/compare_vocab.py     # all stages side by side
```

## Inside a file

```
corpora  n_decisions  n_runs  n_options  n_forks
forks       [ "how is the continuous rating discretized…", … ]
options     [ {…}, … ]          the join table — see below
decisions   [ {…}, … ]          one per extracted decision
repair · option_merge · fork_merge · fork_induction    provenance per stage
```

**`decisions[i]`** — `run`, `arm`, `text`, `line`. The `line` is a line number
in that run's script, which is how the chain reaches source.

**`options[j]`** — the join table, and the only place the three levels meet:

| field | |
|---|---|
| `option` | the canonical label for this action |
| `fork` | the question it answers |
| `n`, `runs` | how many runs chose it, and which |
| `members` | **indices into `decisions`** — this is the join |
| `option_raw` | the original labels folded in, before merging |
| `arms`, `corpora` | which persona arms and which corpus |

`members` is an index list, so `decisions[members[0]]` is a real decision. Never
reorder `decisions` without rewriting every `members` array.

> `option_raw` is written as a bare string by the rename step and as a list by
> the fold step in the vocabularies currently on disk. Read it through
> `trace.raw_labels(option)`, which normalises both — `sorted()` on a string
> silently yields a list of characters. Producers now write a list.

## Reading one rather than parsing one

```bash
python3 ../../scripts/trace.py fork "discretized into categories?"
python3 ../../scripts/trace.py option "average the two raters"
```

```python
import sys; sys.path.insert(0, "scripts")
from trace import Tracer

t = Tracer()                       # headline vocabulary
hits = t.forks("discretiz")        # substring search -> list of labels
t.fork(hits[0])                    # options, run counts, stage
t.option(t._oh["opt:53c963cf"])    # down to individual decisions

earlier = Tracer("ai+human.merged")   # any stage, by tag
```

**Labels are not stable across stages.** `forks("discretiz")` returns two
hits on the headline vocabulary and none on `ai+human.merged`, because merging
rewrote them. Always search within the stage you loaded rather than carrying a
label over from another one.

## Caveats that bite

**Fork labels are close but not identical across near-duplicates.** Two forks
match `discretiz`, differing by three words. Whether they should be one fork is
an open question — the ranked queue is `V3` in
[`../audits/vocab_exhibits.md`](../audits/vocab_exhibits.md).

**Not every fork is a single-choice slot.** 43 of 317 contain runs that took
two options. For genuinely multi-select forks — reporting both an odds ratio
and a risk difference — modal share and effective-option counts are not well
defined; check V2 in `../audits/vocab_exhibits.md` exhibits them.
