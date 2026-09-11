---
name: refine
description: >-
  Phase 3 — apply the answers from a review round, record what each one
  changed, and re-run the audits. Use after /review, before quoting any number.
---

Apply what the human decided. Argument: an optional round number.

```bash
python3 scripts/review_round.py read      # pull the answers in
python3 scripts/review_round.py status
```

## Apply one answer at a time

For each answered question: make the change, then write what you did back into
the round's JSON as `applied`, with the file and the count. A round that has
been applied should read as a record of what changed and why.

The usual moves:

| answer | do |
|---|---|
| merge two forks | `merge_forks.py` with the pair; density floor still applies |
| keep separate | nothing — record it, so the pair is not re-queued next round |
| split an option | `repair_clusters.py`; splits only |
| genuinely multi-select | record on the fork; **stop reporting modal share for it** |
| clustering artifact | `enforce_exclusivity.py`, or a targeted split |
| need more evidence | `/challenge`, and leave the question open |

**Split, never merge, unless a human said merge.** Repairs default to splitting
because over-merge is invisible in the output and unrecoverable, while
under-merge is visible and fixable later. A merge needs an explicit answer
behind it, and the round is where that lives.

**A repair may not move a policy value.** `policy.json` holds the method
decisions — the span floor, the similarity threshold, the pivotal criterion, the
exclusivity rule — and they were set by a human at intake with what each one
cost. Applying a review answer changes the *vocabulary*; changing a threshold
because the answer would be easier to apply that way changes the *instrument*,
and the result is no longer the study that was reviewed. If an answer cannot be
applied without moving a policy value, that is a question for the next round,
not a repair.

## Then re-run everything the change touched

```bash
python3 scripts/finalize_vocab.py --corpus <tag>
python3 scripts/audit_vocab.py
python3 scripts/_selfcheck.py
```

Any analysis computed on the old vocabulary is now stale. Re-run it or mark it
stale — do not leave a figure beside a vocabulary that no longer produced it.

## Check nothing regressed

```bash
python3 scripts/compare_vocab.py
```

The new stage should appear as a small, explicable change. A large one means
something merged transitively, which is the failure the density floor exists to
prevent — investigate before continuing.

## Finalising

After this the numbers are quotable, so:

- update `report/REPORT.md` with `interpreter`, including its Limitations
  section, with anything the round exposed
- if a published claim changed, **retract in place** — mark the old claim with
  the reason and leave the body readable. Silently editing a number destroys the
  record of having been wrong, and this project has four corrections on file
  whose value is precisely that they are visible: the cross-validation bug that
  reversed a headline finding is written up with the wrong number beside the
  right one. `/report` carries the same rule into `report/REPORT.md`

Report: questions applied, what changed, what is now stale, what is still open.
