# Fork replicates

Ten builds that freeze one build's **options** and re-run only **fork
formation**, five from each of two parents.

## The question

Builds A and B agree well about options and badly about forks:

| layer | A vs B |
|---|---|
| decisions -> options | ARI 0.853 |
| options -> forks | by-option ARI 0.307 |

Two readings fit that equally well, and they imply opposite fixes:

- **fork induction is unstable in itself** — it would disagree with itself even
  given byte-identical options, and no amount of improvement upstream helps
- **fork induction inherits** — it is near-deterministic, and what looks like
  fork instability is an options layer that already differed

A and B cannot separate these, because their options differ. Freezing the
options and re-running only fork formation can: the spread **within** one parent
is fork induction's own contribution, and the gap to the **between**-parent
number is what the options layer contributes.

## Layout

```
A1..A5/      replicates over A's options       manifests only
B1..B5/      replicates over B's options       manifests only
results/     the decomposition
```

**The parents live outside the package**, beside the builds they came from:

```
../../replicates/A-parent/     build A's frozen options   777 options, 317 forks
../../replicates/B-root/       build B, promoted          800 options, 351 forks
```

That is not tidiness. Build A's parent was a **byte-for-byte copy** of
`data/vocabulary/bottom_up_<final_tag>.json` — the package already ships it.
Build B's was a whole second study root: 2,556 files and 21 MB, including its
own model-response cache, committed and pushed before anyone read the file
list. A parent is either a duplicate of something the package has or a build
that belongs with the other builds; neither case wants a copy inside.

Only manifests, `results/` and this file are tracked. The replicate roots
themselves — caches, copied data, vocabularies — are ignored.

Both parents are post-repair (`.osplit`): `repair_option_splits.py` is free and
structural, and freezing un-repaired options would bake 76-of-96 known
over-merges into all ten builds. See `promote_repair.py` for how that repair
entered the study.

## Running them

Inside the **LLM container** — `distill-dev` has no `claude` CLI and dies on the
manifest step:

```bash
python3 stability/scripts/fork_replicate_batch.py \
  --parent A=../../replicates/A-parent/bottom_up_<tag>.json \
  --parent B=../../replicates/B-root/data/vocabulary/bottom_up_<tag>.json:../../replicates/B-root \
  --n 5
python3 stability/scripts/fork_variance.py --root replicates \
  --json replicates/results/fork_variance.json
```

The `:<path to B's study root>` suffix is load-bearing. `merge_forks` reads
`garden_<tag>.json`, and a B replicate given A's garden would agree with the
other B replicates for a reason that has nothing to do with fork induction.

The batch is resumable: a replicate whose manifest records a `final_tag` is
skipped, so a crash overnight loses at most the build in flight. A failed build
keeps its cache, so the retry is nearly free and the money already spent stays
visible.

## Why five per parent, decided before the first run

This is a variance estimate, and variance is what needs replicates. At *k*
builds a parent contributes *k−1* degrees of freedom:

| per parent | df | 95% CI on an sd |
|---|---|---|
| 3 | 2 | ~0.5× to 3× |
| 6 | 5 | ~0.7× to 1.8× |

At 2 df the interval is too wide to support any claim in either direction. This
is one of the few places where more runs buy the result rather than a tighter
version of it.

`--n` was **pre-committed**. Running a few, looking at the spread, and extending
if it seemed large would be optional stopping on a variance estimate — biasing
the exact quantity being reported. A later batch is a new pre-registered
experiment reported separately, not an extension of this one.

## What these do not measure

The replicates drop `merge_options` from the repair loop. That is what isolates
fork formation, and it also makes them a **modified pipeline**: this is
fork-formation variance under frozen options, not end-to-end pipeline variance.

The parents' own fork layers were built by the full loop and are therefore
**not exchangeable** with the replicates. They are reference points, and are
excluded from the variance statistics rather than counted as a sixth build.

Applying one deterministic repair to both parents can also raise their
agreement for a trivial reason. `repair_option_splits.py` reads only each
build's own membership and line numbers, never the other build's, so it is not
circular — but any agreement measured after it must be reported against the
pre-repair number.

## Cost

$35.64 and roughly 40 minutes per replicate, measured from build B's own call
log rather than estimated: `22_induce_forks` $13.83 and `21_fork_identity`
$21.81. The full repair loop would be $109.60 each, because the dropped
`merge_options` pass is 655 opus calls on its own.

Nothing here is committed except manifests and the frozen parent vocabularies.
The caches are worth hundreds of dollars and are reproducible only by spending
it again; see `.gitignore`, whose `!*/` line is load-bearing.
