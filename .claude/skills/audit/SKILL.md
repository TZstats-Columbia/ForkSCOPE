---
name: audit
description: >-
  Run the check sets over a built study, report verdicts with their evidence,
  and refuse to certify results whose checks did not pass. Use when the user
  asks to audit, verify, or check a build, or before reporting any analysis
  number.
---

Run the checks and report what they say. Argument: an optional check set
(`A`, `R`, `I`, `G`, `H`, `E`, `V`) to run just one.

You are reporting evidence, not producing reassurance. A check that passes is
worth one line; a check that returns REVIEW is worth the exhibit behind it.

Read [`docs/AUDITING.md`](../../../docs/AUDITING.md) before interpreting any
result. It is eight questions, each from a failure this project made, and two
of them — entanglement and selection — will change how you read the numbers
these scripts print.

## Run

**Seven of these are free against the committed cache. Two are not.** Measured,
not assumed — say which you ran.

```bash
# free: no model calls, seconds each
python3 scripts/_selfcheck.py                       # structural gate
python3 scripts/audit_vocab.py                      # V1–V7, the exhibits
python3 scripts/check_outcomes.py                   # outcomes vs their fragments
python3 scripts/audit_clusters.py   --corpus <tag>  # A1–A9
python3 scripts/audit_iteration.py  --corpus <tag>  # I1–I6
python3 scripts/audit_garden.py     --corpus <tag>  # G1–G6
python3 scripts/audit_shapley.py    --corpus <tag>  # H1–H6
python3 scripts/audit_ablation.py                   # E1–E6

# SPENDS MONEY on any tag whose answers are not already cached
python3 scripts/audit_lineage.py    --corpus <tag>
python3 scripts/audit_granularity.py --corpus <tag> --sample 40
```

Start with `audit_vocab.py` and `_selfcheck.py`: neither calls a model, and
between them they catch most structural breakage for free.

**`audit_lineage` and `audit_granularity` adjudicate with a model** — they call
`20_option_purity`, `21_fork_identity`, and one call per sampled fork. On a tag
whose adjudications are not in the cache they are uncached from the first item,
and with the CLI unavailable they will appear to hang rather than fail, because
`llm.py` retries three times with backoff on every call. That is spend, not a
bug. Budget for them or skip them, and say which you did.

**`audit_garden` needs its sibling map first.** It reads
`garden_siblings_<tag>.json` and dies with `FileNotFoundError` if that tag has
none. Generating it is free:

```bash
python3 scripts/garden.py siblings --corpus <tag>
```

## What policy says about auditing

`policy.json:audit` records three decisions, and the first two surprise people:

| entry | soccer | |
|---|---|---|
| `checks` | V1–V7 | the named V set. A/R/I/G/H/E run too and are not enumerated there |
| `blocking` | **empty** | **decided.** No check blocks a build. Most carry no null and rank for human attention; treating them as gates would convert a weak signal into a hard decision |
| `review_queue_max` | 60 | **implicit** — a guess at what a person will actually read, never checked against what a person did read. It is on the `_open` list |

So a REVIEW verdict is not a failure state and must not be reported as one. What
it obliges you to do is produce the exhibit, not to stop.

Read these from the file. A study that is not soccer sets its own, and a check
you ran that is not in `checks` should be reported as extra rather than folded
in silently.

## Reading a verdict

**`REVIEW` does not mean broken.** Several checks are left failing on purpose
and two of the failures *are* the finding:

- **H1** — the gap between the surrogate's in-sample and cross-validated R².
  Only the cross-validated figures are reported; the gap is the result, not a
  defect to tune away.
- **G4** — no conditional structure survives its null. A *power* result at this
  corpus size, not a claim that the space is flat.
- **E2** — the ablation matcher pairs unrelated runs at 82% of the within-run
  rate, so the headline agreement cannot be read as a pass on its own.
- **V2** — 43 of 317 forks have runs that took two options, and 199 of 223
  analyses do it somewhere. Three causes share the shape and only reading
  separates them. `policy.json:forks.exclusivity_required` is `true` on purpose:
  setting it does not make it true, it makes the violation an audited exhibit
  rather than a constraint that would have hidden it.

Before calling a REVIEW new, check the Limitations section of
[`report/REPORT.md`](../../../report/REPORT.md) for whether it is already known
and why it stands.

## Two ways a number here misleads

**Entanglement.** Several checks lean on a signal the pipeline used to *build*
the vocabulary — co-occurrence above all. Their agreement is partly the
pipeline agreeing with itself, and their disagreement needs decomposing before
it means anything. Reports written through `exhibit.py` carry
`entangled_with`; three of the five V-checks are non-empty. The adjudicating
audits (`lineage`, `garden` G1) are entangled and do not yet say so in their
own output — LIMITATIONS §8 works through what that cost.

**Selection.** A count over a worst-first exhibit is conditioned on the ranking
that produced it. Report it as a queue and its depth. "27 of 30 fork pairs are
one question" is true and is *not* a 90% duplicate rate: those 30 were chosen
as the likeliest duplicates.

## What you must refuse

- **Do not report an analysis number whose audit you have not run.**
- **Do not describe a queue as clean because nothing was read.** V1, V3 and V4
  rank by weak signals; a short queue is not evidence of absence, and each
  exhibit says so in its own note.
- **Do not quote the Shapley bootstrap CIs.** `strength` is a mean of absolute
  values, so its interval cannot cover zero regardless of the data. Use the
  permutation null in `shapley_audit_*.json`.
- **Do not tune a threshold until a check passes.** If a verdict looks wrong,
  the exhibit is the argument — bring it.

## Reporting

Lead with what failed. For every REVIEW, give the claim, the number, and one or
two exhibit rows with their handles so the reader can walk them:

```bash
python3 scripts/trace.py resolve fork:8d07b365
```

End with what was *not* checked. Coverage matters more than the pass rate.
