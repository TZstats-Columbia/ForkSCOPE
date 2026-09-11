# How to audit — eight lessons, each from a failure here

Every item below is a mistake this project actually made, most of them caught
by a person asking a question the system had not thought to ask itself. They
are written as questions to put to a check before believing it, and four of
them are now enforced in `exhibit.py` rather than left to judgement.

The organising observation: **a check can fail in ways that look exactly like
passing.** Nothing in a number tells you whether the measure could have seen
the failure, whether it shares an assumption with the thing it checks, or
whether it ever ran. That is what makes auditing hard, and it is why these are
questions rather than a rubric.

---

## Before believing a PASS

### 1 · Could this measure see the failure it is ruling out?

> A statistic reported that **2.7%** of within-fork option pairs were
> near-duplicates, offered as reassurance. The measure was token overlap, which
> cannot see that *"compute the mean of the two rater columns"* and
> *"average the two raters' scores"* are one action. Two whole forks were
> duplicates. A person found it in minutes by reading the option lists.

Before reporting nothing found, construct a violation and ask whether this
measure would register it. If you can build one it would miss, you have
measured *findability*, not absence.

The same error recurred while fixing an unrelated bug: `_importcheck.py` was
written to catch a path constant aimed at the wrong tree, and its first version
tested whether the path was **inside the package**. It passed with the bug
reintroduced — `soccer/v2/clusters` *is* inside the package root, it simply is
not there. Blind measures are not a beginner mistake; they are the default.

**Enforced:** `blind_to()` is required before a `PASS`. *"nothing — exhaustive
over the population"* is a legitimate answer, and asserting it is the point.

### 2 · Does this check use a signal the pipeline used to build the thing?

> The identity audit reported **27 of 30** label-similar fork pairs as one
> question, which read as a repair failure. But the repair uses co-occurrence
> as a cannot-link constraint, and the audit does not see it. **17 of the 27
> were pairs the repair had deliberately refused to merge.** The share of
> co-occurring pairs among "same" verdicts rose from 43% pre-repair to 63%
> after — enrichment, not degradation.

An entangled check is not worthless; it is not *independent*. When it agrees
with the pipeline, that is partly the pipeline agreeing with itself. When it
disagrees — as here — the disagreement is informative but must be decomposed:
17 pairs were a real tension, 10 were genuine misses.

This is the failure mode the evidence contract did **not** cover. Worst-first
exhibits catch a blind measure; they do nothing about an entangled one, because
the items are real and the ordering is honest.

**Enforced:** `uses()` declares the check's evidence, `BUILD_SIGNALS` names what
the pipeline builds with, and a `PASS` while entangled is refused. Three of the
five V-checks turn out to be entangled.

### 3 · Was this sample drawn, or selected?

> "27 of 30" is not a 90% duplicate rate. Those 30 pairs were chosen *because*
> they were the most label-similar — the likeliest duplicates by construction.
> The number says the top of the ranking is dense. It says nothing about the
> other 70,000 pairs.

Any statistic over a worst-first exhibit is conditioned on the selection that
produced it. Report it as **a queue and its depth**, never as a rate. If you
want a rate, you need a random draw, and you should say which you took.

---

## Before believing a number

### 4 · Can the test resolve the threshold it is compared against?

> A permutation *p* cannot fall below 1/(B+1). Under BH correction the
> threshold routinely sat *below* the floor of a cheap screen, so "nothing
> significant" was produced **by construction**. Four separate occurrences, one
> reported before it was caught.

Check the arithmetic before the result: smallest achievable *p* against the
corrected threshold. If the first is larger, the test cannot return the answer
it is about to report. Escalate the draw count for anything surviving a screen.

### 5 · Does the statistic mean what the sentence says?

> The Shapley `strength` is a mean of absolute values. Bootstrapping it gives
> an interval that **cannot cover zero regardless of the data**. It is not a
> test, and quoting it as one would be quoting an artifact.

Read the estimator, not its name. A confidence interval that cannot contain the
null, an R² that cannot go down, an agreement rate with no disagreement in its
denominator — each is a number that looks like evidence and is not.

### 6 · Is the claim's scope the test's scope?

> Asked how we knew the clustering had not **under**-merged, the honest answer
> was that it had been checked only *within* a fork — and while two forks were
> duplicates, their option lists could not see each other. A check had run; a
> different claim had been reported.

Also: an in-sample fit with ~50 parameters on 204 rows is not evidence of
prediction. Cross-validate, or say the number is descriptive.

---

## Before believing the check exists

### 7 · Has this check ever actually run — here, on this?

> `audit_granularity.py` and `audit_lineage.py` were documented in WORKFLOW,
> present in `scripts/`, listed in the audits README, and pointed at a
> directory that does not exist in the package. Both failed on first contact.
> `audit_clusters.py` did run — and required `--json` to save, so its report
> was printed, read, and lost. That is why A1–A9 existed for a vocabulary the
> paper does not report.

Documentation cannot catch this: they were documented. Presence cannot: they
were present. Only execution can, which is why `_importcheck.py` imports every
script and resolves its paths, and why `audit_clusters.py` now saves by default.

And run it on **the artifact you are reporting**, not an earlier one. Six of
the check sets had only ever run on a superseded vocabulary.

### 8 · Are you checking the property, or something correlated with it?

> `_selfcheck` verified that every prompt was **represented** in the cache. The
> claim it was standing behind was that a re-run returns the committed answers
> — which needs every entry to be **reachable**. 86% were; 206 answers came
> from a prompt no longer shipped. The weaker property passed while the claim
> was false.

Write the claim as a sentence, then ask what would have to be true for it to
hold. Check that, not its neighbour.

---

## What this adds up to

The four enforced rules — worst-first exhibits, no `REVIEW` without exhibits,
no `PASS` without a declared blind spot, no `PASS` while entangled — exist
because prose guidance did not hold. Each was written after the corresponding
failure, and each is a refusal rather than a warning, because a warning in a
long report is not read.

The four unenforced ones are harder to mechanise and worth asking every time:
selection, resolution, estimator semantics, and scope.

A last honest note. **A person found every one of these**, usually with a
one-line question — *"the options from the two first forks look identical"*,
*"how did you know they didn't under-merge?"*, *"maybe this is because the
headline results have been audited and fixed?"* No audit caught its own blind
spot, and no agent proposed the entanglement question. The lesson is not that
auditing can be automated to the point of trustworthiness. It is that the
system's job is to make a skeptical question cheap to answer — which is what
handles, exhibits, and traceable evidence are for.
