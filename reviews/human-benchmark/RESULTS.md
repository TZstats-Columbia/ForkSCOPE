# Human benchmark — results

Reportable findings only.

---

## What the benchmark is for

Every reproducibility number in `stability/` is a **self-agreement** rate: we
ran the pipeline twice and measured how much the two runs matched. That kind of
number has two blind spots. It cannot be interpreted without knowing how much
two careful people would agree, and it cannot detect a mistake both runs make,
because two runs that are wrong in the same way agree perfectly.

Three people answered the same questions the pipeline answered, on the same
items, without seeing its answers. That gives us both missing pieces.

## Design

Three raters worked independently, in a fixed order, and did not discuss any
item until all sheets were returned. All three sheets came back complete.

| part | items | question put to the rater |
|---|---:|---|
| 1 | 43 pairs | do these two lines describe the same operation on data? |
| 2 | 60 pairs | are these two choices alternatives at the same slot? |
| 3 | 30 forks | is this fork right, and if not, how should it be re-merged? |

Three conventions the raters fixed before starting, all of which affect how the
numbers below should be read:

- **`unsure` means unjudgeable.** Not "I am uncertain" but "the item does not
  say what these two lines *do*, so there is no judgement to attempt." It is a
  property of the item. It is never counted as disagreement and never enters a
  difficulty score. See Part 2 below, where it turns out to be a finding.
- **Confidence runs 1 to 5**, 1 low and 5 high. Raters used different parts of
  the scale (means 4.86, 3.88, 4.17), so it is converted to a within-rater
  z-score before averaging.
- **Same/different was applied strictly.** A rater said "same" only where
  taking one option genuinely rules out the other. This matters for reading the
  contradictions in Part 2: a majority "same" is a strong signal, a majority
  "different" a weaker one.

### Where the packet came from

Generated 29 August 2026 by `review_sheet.py` at commit `f75f965`, and
**reproduced byte-for-byte** from that commit, including the answer key.

| | |
|---|---|
| build A | `bottom_up_ai+human.merged.forkmerged.merged.induced.r3.json` (before the `.osplit` repair) |
| build B | the same file from the `B-vocab` replicate |

**Everything a rater read came from build A.** Build B never appears on a
sheet; it is used only to sort items into strata, according to whether it
happened to make the same call as A. So every human judgement is a judgement
about build A.

| stratum | meaning |
|---|---|
| `stable_same` | both runs grouped the pair |
| `stable_diff` | both runs kept the pair apart |
| `unstable` | the two runs disagreed |

---

## How the raters were used, and how every number is computed

Several agreement measures are possible here and they do not give the same
answer. This section fixes which one each number is, so that nothing below has
to be taken on trust.

### The three raters

All three rated **the same items** — the same 43 pairs, 60 pairs and 30 forks.
They are not a sample of raters and nothing here generalises to other raters;
with three people, a rate like 0.833 means 5 of 6 rater-pairs, and its
uncertainty is wide.

Each rater's sheet was **shuffled independently** (seed + rater index), so row
order cannot create a common anchor. Parts were completed in order 1, 2, 3, and
raters did not discuss any item until all sheets were in.

The raters are **not** pooled into a single "human answer" except where a
majority is explicitly named. Where the text says *majority*, it means a strict
majority of that item's committed raters.

### Notation

For item *i* and rater *r*, the verdict is `same`, `different`, or
`unjudgeable`. Write:

- **C(i)** — the raters who committed on item *i*, that is, did not answer
  `unjudgeable`.
- **a(i)** — build A's call on item *i*, `same` or `different`.
- **b(i)** — build B's call.

Strata are defined by a and b: `stable_same` is a = b = same, `stable_diff` is
a = b = different, `unstable` is a ≠ b.

### Per-item versus pooled, and why it matters

Two averages are possible, and here they differ by up to 0.085:

- **per-item** — score each item, then average the item scores. Every item
  counts once.
- **pooled** — add up all matching judgement-pairs and divide by all
  judgement-pairs. An item all three raters could judge then carries three
  times the weight of one only two could.

**Per-item is reported first**, because items were the sampling unit — 13 or 20
were drawn per stratum — and because judgeability is not random: it tracks a
specific kind of item, the bare covariate lists. Pooling would quietly
up-weight the judgeable part of the sample. Pooled values are printed in
brackets throughout so the choice is visible.

### The three columns

**`rater × rater`** — for each item with at least two committed raters, the
share of rater-pairs within C(i) giving the same verdict; averaged over items.
With all three committed this is over 3 pairs; with two, over 1 pair. Items
where fewer than two committed are excluded, not scored zero.

**`rater × build A`** — for each item with at least one committed rater, the
share of C(i) whose verdict equals a(i); averaged over items. Note the unit
differs from the column beside it — rater-against-A judgements rather than
rater-against-rater pairs — but both are "the probability that two independent
judgements of the same item match", so they are comparable in kind.

**`A × B`** — 1 if a(i) = b(i), else 0. **This is 1.00, 1.00 and 0.00 by the
definition of the strata and is not a measurement.** It is printed only so that
fact is visible.

**`unjudgeable`** — the share of all (item, rater) cells in the stratum
answered `unjudgeable`. Denominator is items × 3.

### Everything else

**Endorsement** (the 19/19 and 0.833 figures in Part 2). An item counts if its
committed raters have a strict majority; ties and all-unjudgeable items are
excluded. Endorsement is the share of counted items whose majority equals a(i).
Because a lone committed rater can form a "majority", the figure is also
reported requiring two and three committed raters.

**Binomial *p*** — exact two-sided binomial on the count of items whose
majority said `same`, against a null of 0.5. It asks whether the majority
verdict is distinguishable from a coin flip, nothing more.

**Pool-weighted agreement** (Part 1's 0.818 and 0.849). Each stratum is
reweighted by its share of the full candidate pool the packet sampled from:
w = pool size / total pool. The human figure is Σ w × (that stratum's pooled
`rater × rater`); the pipeline figure is Σ w × (1 if the stratum is stable else
0), which reduces to the pool share that is stable. Both are over the same
pool. **This is computed for Part 1 only** — see the limits on Part 2's pool.

**Difficulty and AUC.** Difficulty of item *i* is
`(1 − rater × rater agreement on i) − z(confidence)/4`, where confidence is
z-scored within rater before averaging. `unjudgeable` does **not** enter it.
Items with fewer than two committed raters are excluded. The AUC is the
probability that a randomly drawn `unstable` item scores harder than a randomly
drawn stable one, ties counted as half; *p* is a permutation null shuffling the
stable/unstable labels 20,000 times.

**Part 3.** Verdicts are normalised first (`overmerged` and `over-merged` are
one label). `rater × rater` is pooled pairwise agreement over 30 forks × 3
rater-pairs = 90 comparisons. Endorsement is the share of the 90 (rater, fork)
judgements answering `correct`.

### Measures deliberately not used

- **Majority-versus-individual agreement.** With three raters the majority is
  right by construction and the figure rises with rater count, which would
  flatter the human side for having more people.
- **A pooled model rate for Part 2.** Its pool is restricted and partly
  synthetic; see the limits section.
- **Chance-corrected coefficients (ARI, kappa).** None of the figures here are
  chance-corrected, so none of them may be placed beside ARI 0.307, 0.334 or
  0.62.

---

## The three-way comparison

Three agreement rates on identical items. Read across each row. Figures are
per-item averages, with the pooled alternative in brackets; both are defined
above.

**Part 1 — same action?**

| stratum | items | unjudgeable | rater × rater | rater × build A | A × B |
|---|---:|---:|---:|---:|---:|
| both runs grouped | 13 | 0.051 | 0.744 [0.829] | 0.769 [0.784] | 1.00 |
| both runs separated | 13 | 0.026 | 0.821 [0.865] | 0.885 [0.895] | 1.00 |
| runs disagreed | 13 | 0.128 | 0.641 [0.655] | **0.462** [0.471] | 0.00 |

**Part 2 — same decision point?**

| stratum | items | unjudgeable | rater × rater | rater × build A | A × B |
|---|---:|---:|---:|---:|---:|
| both runs grouped | 20 | 0.117 | 0.833 [0.854] | **0.925** [0.925] | 1.00 |
| both runs separated | 20 | 0.051 | 0.667 [0.692] | 0.717 [0.714] | 1.00 |
| runs disagreed | 20 | 0.117 | 0.754 [0.702] | **0.450** [0.491] | 0.00 |

The two weightings agree on every reading below. The one place they diverge
materially is Part 2's `unstable` row, where per-item raises `rater × rater`
from 0.702 to 0.754 — that stratum holds several items only two raters could
judge, and pooling under-weights them.

**Part 3 — is this fork right?** Build B is not involved; the audit shows build
A's forks only.

| | |
|---|---:|
| forks | 30 |
| rater endorses build A's fork (calls it correct) | **0.711** (64 of 90 judgements) |
| rater × rater, exact verdict | 0.511 |
| unjudgeable | 0.078 |

### How to read the `A × B` column

**It is 1.00 or 0.00 by construction and is not a measurement.** The strata
were *defined* by whether A and B matched, so of course the two runs agree
perfectly on two of them and not at all on the third. Comparing that column
against `rater × rater` would be comparing a definition to a measurement.

The meaningful comparison is `rater × build A` against `rater × rater`: does a
person agree with the pipeline about as often as with another person?

### The three things that column shows

**1 · Where the two runs agree, the pipeline performs like a person.** In every
stable stratum, a rater agrees with build A at least as often as with another
rater (0.769 vs 0.744; 0.885 vs 0.821; 0.925 vs 0.833; 0.717 vs 0.667). In Part
2's `stable_same` the gap is widest: build A matched the raters 0.925 of the
time while the raters matched each other 0.833.

**2 · Where the two runs disagree, build A is a coin flip.** `rater × A` falls
to 0.462 and 0.450 — indistinguishable from guessing, on both weightings. The
disputed pairs are not merely unstable; on them, build A's call carries no
information about what a person would say. This is the clearest statement the
benchmark supports about what instability costs.

Note that `rater × rater` does *not* fall the same way in Part 2: raters still
agree 0.754 with each other on the pairs the two runs disputed. So the raters
are not simply finding those items impossible — build A is out of step with
them there while they remain broadly in step with each other.

**3 · The raters accept most of build A's forks but disagree about what is
wrong with the rest.** Part 3's endorsement rate is 0.711 while exact verdict
agreement is 0.511. They largely agree the map is right, and disagree about how
to describe the errors — which is why Part 3 is better read as a worksheet than
as a test.

---

## Part 1 — the options layer has reached the level of human agreement

Part 1's pool is every within-fork pair in build A. Unlike Part 2 it contains a
real population of pairs both runs separated, so both humans and pipeline can
be scored over the same set and the strata reweighted back to it:

| | agreement over the pool |
|---|---:|
| two people | 0.818 |
| two pipeline runs | **0.849** |

Two runs agree with each other slightly more often than two people do. Making
this layer more self-consistent would only make it more consistent than people
are, which is not evidence of anything. **There is no headroom left here.**

Disagreement at this layer looks like the task being hard rather than the
pipeline being careless, though the effect is smaller than a first reading
suggested. Raters agree less on the pairs the two runs disputed than on the
pairs they agreed about — 0.641 against 0.782, a gap of **+0.141** — and on the
disputed pairs the human majority splits 0.455 / 0.545, an even coin-flip
(*p* = 1.00).

> The pre-registered thresholds called a gap above +0.15 "instability tracks
> genuine ambiguity" and below +0.05 "instability is not tracking difficulty".
> **+0.141 falls in the undeclared middle**, so by the rule fixed in advance
> neither reading is supported and the direction is suggestive only.
>
> An earlier reading of this packet put the gap at +0.295 and claimed the first
> reading. That figure counted `unjudgeable` as disagreement, and unjudgeable
> items are concentrated in the disputed stratum (0.128 of cells, against 0.051
> and 0.026 in the other two) — so it penalised exactly the stratum under test
> and manufactured half the gap.

## Part 2 — where the pipeline agrees with itself, it is also correct

Taking the human majority as the reference:

| what build A did | pairs | human majority did the same | binomial *p* |
|---|---:|---:|---:|
| grouped them | 19 | **1.000** | < 0.0001 |
| kept them apart | 18 | 0.833 | 0.008 |

**All 19 fork pairs that both runs placed in the same fork, the human majority
also grouped** — and under a strict standard, where "same" was reserved for
options that genuinely rule each other out. The result holds at every level of
stringency: 19/19 when one rater committed, 17/17 when two did, 15/15 when all
three did.

This is what a second pipeline run could never show. Two runs making the same
mistake would agree perfectly with each other.

### The six pairs where the humans contradict both runs

These are the only places in the packet where an error *shared* by both runs
can become visible.

**Both runs separated them; the raters call them rivals at one slot** — the
pipeline has cut one question into several:

| pair | verdicts | |
|---|---|---|
| F026 | 3/3 same | "median-impute height/weight + impute bias scores with zero" vs "impute missing bias score with the country/group mean" |
| F030 | 3/3 same | "median-impute height/weight/age + impute bias scores with column median" vs "impute missing bias score with the country/group mean" |
| F040 | 2/3 same | smoothed per-game red-card rate vs combined bookings score |
| O019 | 2/3 same | two ways of quantifying inter-rater agreement |

F026 and F030 are unanimous, and they straddle two forks that build A keeps
apart: *"how are records with missing covariates handled"* and *"how are
records with a missing referee bias score handled"*. **Both raters who used
Part 3's audit independently flagged the second of those as under-merged.** Two
different sheets, filled in in a fixed order, point at the same join.

**Both runs grouped them; the raters call them different questions:**

| pair | verdicts | |
|---|---|---|
| O012 | 3/3 different | building a counterfactual dataset vs estimating the adjusted risk difference by marginal standardization |
| O009 | 2/3 different | "require ≥3 games, later re-testing the cutoff at 4" vs "require ≥3 games" |

O009 is the packet's own carve-out working as intended: a robustness refit at
another setting is a sensitivity analysis, not a second option at one slot.
Build A merged the two.

### `unjudgeable` is a finding about the option labels

12 items drew an `unjudgeable`, and they are one kind of item: **a pair of bare
covariate lists.** For example, "position only" against "games, height, weight,
age, yellowCards, goals, position, league". Neither has a verb; neither says
which step of the analysis it belongs to. A reader cannot tell whether these
are two rival adjustment sets at one fork or the covariate sets of two
different models.

**All twelve come from just two forks:**

| fork | items |
|---|---:|
| which covariates make up the model's adjustment set? | 9 |
| Which control variables and functional forms enter the regression model? | 3 |

These are the same two forks Part 3 flagged first. So `unjudgeable` is not rater
hesitancy and not noise — it counts option labels that name a *set of
variables* without naming an *operation*, and it localises them precisely.

### Fork disputes are not where the raters struggle

The same comparison at the fork layer, on the same basis:

| | rater × rater |
|---|---:|
| pairs both runs handled the same way | 0.750 |
| pairs the two runs disputed | **0.754** |
| gap | **−0.004** |

**Raters agree on the disputed fork pairs as readily as on any others.** By the
pre-registered rule (a gap below +0.05), that is the "instability is not
tracking how hard the question is" reading, and it is the one stratum
comparison in this packet that lands cleanly inside a declared threshold rather
than in the middle.

It also fits the `rater × build A` column: on that same stratum build A matches
the raters at 0.450 while the raters match each other at 0.754. The disputed
fork pairs are items people handle without difficulty and build A does not.

Caveat: 20 items, three raters. This is a descriptive comparison of two cells,
not a test, and the inferential version of the same question — below — does not
reach significance.

### Whether fork instability tracks human difficulty: the inferential test

We scored how hard each item was from the raters' answers alone and asked
whether that score picks out the pairs the two runs disputed. An AUC of 0.5
means no relationship.

| | AUC | permutation *p* |
|---|---:|---:|
| Part 1, items every rater could judge | 0.606 | 0.382 |
| Part 2, items every rater could judge | 0.632 | 0.162 |
| both parts pooled | 0.624 | 0.087 |

**Nothing here reaches significance**, and at these sample sizes the benchmark
cannot detect a modest relationship. More items would help; more raters would
not.

The difficulty index behind these figures is disagreement *and* confidence.
Disagreement alone — which is what the stratum comparison above uses — gives a
Part 2 AUC of **0.499**, agreeing with the −0.004 gap that fork disputes are
unrelated to human disagreement. The 0.632 above is what confidence adds: on
the disputed pairs raters were somewhat less confident even while still
agreeing. That is a weak, non-significant hint and nothing should be built on
it, but it is the reason the two measures do not read identically.

An earlier draft of this document reported the 0.499 as its headline fork
result. It was right by accident: two errors were cancelling. Items nobody
could judge were scored as the *easiest* in the set rather than excluded, and
the unjudgeable count was folded into difficulty. The stratum comparison above
is now the statement to quote, because it is computed on one basis that is
stated and does not depend on how a composite index is assembled.

The stronger and better-supported claim about instability is item 2 of the
three-way reading above: on disputed pairs, build A agrees with the raters at
0.491, which is chance.

## Part 3 — what to change: the forks are split along the wrong lines

Part 3 was designed as an audit with three labels. In practice the labels
mattered less than the free text. 14 of 30 forks drew a comment; 8 carry a
specific instruction, and they all say the same thing:

> "Transformation of games should be its own fork. The rest of transformation
> can be organized."
>
> "Can be re-organized into one fork about how to transform variables (which to
> transform and how) and another forks on what to include."
>
> "Could be separated into model categories and covariate categories."

The vocabulary mixes together two questions that should be kept apart: **which
variables go into the model**, and **how each variable is transformed before it
goes in.** That confusion runs across at least six forks:

| fork | effective options |
|---|---:|
| which covariates make up the model's adjustment set | 13.50 |
| Which control variables and functional forms enter the regression model | 8.27 |
| In what form is the yellow-card covariate entered | 4.19 |
| which regression model, estimator, and SE scheme specifies the primary effect | 3.20 |
| how is games-played entered into the model | 3.00 |
| how are continuous predictors transformed and z-scored | 2.23 |

The dominant complaint was *under*-merging — a fork that is only part of a
question living elsewhere, meaning the pipeline has cut one question into
several. Two other results point the same way: the four contradictions above
where raters say separated pairs are rivals, and the fact that the unjudgeable
labels come from this same cluster.

**Part 3's labels have been replaced for future rounds.** Raters now choose
`correct`, `split`, `absorb`, `move` or `unsure`, and fill in a required
`remerge` column saying what should happen. The scorer prints these as a queue
of proposals rather than as an agreement score.

**None of this has been applied.** Acting on it re-opens the vocabulary and
every number downstream of it.

---

## Limits, stated

**We still have no human comparison for the ARI 0.62 figure.** Build B is the
*vocabulary* replicate, so its options differ from build A's and Part 2
compares them only after matching. That makes this the different-options
comparison (ARI 0.307 by option, 0.334 between parents). The 0.62 figure comes
from a different experiment — ten fork replicates on identical frozen options,
with no matching step — which this packet predates. Closing the gap needs a
packet built from two fork replicates of a single parent. No model calls, and
the replicates already exist.

**There is no honest single head-to-head number for Part 2, and none should be
quoted.** Its candidate pool keeps only pairs that at least one run grouped and
then adds 118 artificial hard negatives. Scoring the pipeline over that pool
gives 0.187, but that figure mostly restates how the pool was built: 78% of it
is pairs the runs disagreed about, where their agreement is zero by definition.
The pool was assembled by looking at where the pipeline disagreed with itself
and nowhere else. `score_review` detects this and refuses to print such a
figure.

**The item-level difficulty tests are underpowered**, as noted above. More
items would help; more raters would not.

**The comparison is harder on the humans than on the pipeline.** The fork
adjudicator sees about 45 options at once, together with a table of how many
analyses use each pair of options together — which is most of the test the
rater was asked to apply from memory, computed and handed over. The rater saw
two sentences. Every human figure here is a floor on what a person with the
pipeline's context would achieve.

**The `eff_options` values printed on Part 3 predate the effective-options
correction.** 12 of 30 audited forks show a value that later changed. All six
forks named above changed by 0.35 or less, so that finding is not an artifact —
and an inflated diversity figure would push a rater toward *over*-merged, the
opposite of what was reported.

**One rater proposed no change to any of the 30 forks.** We did not ask whether
that reflects how they read the sheet or how they read the vocabulary, and we
should have. The other two agreed on whether to flag a fork 70% of the time.

**One of four attention-check items was not a valid check.** The "obviously the
same" items were built from pairs the *pipeline* had grouped, with nothing
verifying they also read that way to a person. One — a general instruction to
"choose the covariate/adjustment set" against a specific named list of
covariates — was called *different* by two of three raters, one at confidence
1. That is a hard item, not inattention, and treating it as a check would have
disqualified all three raters, removing the pipeline's critics and making it
look better. It is retired. `review_sheet` now requires such items to share at
least 60% of their wording, and `score_review` retires any check item a
majority answers against and treats `unjudgeable` as abstention. All three
sheets pass on the three remaining items.
