# The lifecycle — who acts, and what each phase produces

Charting a garden is not a pipeline run. It is nine phases, and a human acts
in five of them — in two distinct roles.

**The garden owner** builds the map and is answerable for it: intake, review,
refine, walk. **The garden visitor** uses it: itinerary, inspect. They may be
the same person and often are not — a visitor arrives after the map is
finished, did not write the intake, and did not answer the review.

Below: who acts in each phase, what artifact it leaves behind, and what has to
be true before the next one starts.

The artifacts matter as much as the order. A judgement made in conversation is
lost; a judgement written to a file can be cited, disagreed with, and reused by
someone who was not there.

| # | phase | who | produces | gate to the next |
|---|---|---|---|---|
| 0 | **intake** | owner + AI | `study.json`, `INTAKE.md` | corpora reachable; a two-run smoke test passes |
| 1 | **chart** | AI, iterative | vocabulary stages, analyses, **results v1** | `_selfcheck` passes; every audit has run |
| 2 | **review** | owner + AI | `reviews/round-NN.md` — AI's questions, the human's answers | every question answered or explicitly deferred |
| 3 | **refine** | AI | repaired vocabulary, updated docs, applied-notes in the round | audits re-run; nothing regressed |
| 4 | **walk** | owner | notes, and usually new questions | the human is satisfied the map is the corpus |
| 5 | **itinerary** | visitor + AI | a specified path, audited | no unexplained incompatibility |
| 6 | **run + report** | AI | a new run, its estimate, its provenance tag | it executed and produced an estimate |
| 7 | **inspect** | visitor + AI | a verdict on that run | agreement on what it shows |
| 8 | **file** | AI | the run added to the garden, tagged | provenance recorded; the statistics recomputed **with** it |

## 0 · Intake — owner + AI

`/intake`. The consultation: corpus, shared task, domain context, outcome side,
research questions, constraints.

Two files, and both matter. `study.json` is what the pipeline reads.
`INTAKE.md` is what the manifest cannot hold — what was asked, **what was not
known at the time**, and what the user predicted would matter.

## 1 · Chart — AI, and it iterates

`/chart` then `/audit`. **This loop is not one-shot.** An audit that returns
REVIEW may send you back to the repair chain; a vocabulary comparison may say
the wrong stage was chosen as headline. Expect several passes before results v1
is worth showing anyone.

Iterate on the *build*, never on the *thresholds*. Adjusting a cutoff until a
check passes manufactures the result.

Results v1 is a draft. Do not publish numbers from it.

## 2 · Review — owner + AI, and it goes both ways

This is the phase the whole design rests on, and it is **not** the AI
presenting findings.

```bash
python3 scripts/audit_vocab.py
python3 scripts/review_round.py new --n 12
```

The AI raises the questions it cannot settle — drawn from the audit exhibits,
already ordered worst-first — each stating **what each possible answer would
change**. If both answers lead to the same action, it is not a question.

The human answers in `reviews/round-NN.md`, comments freely, and asks their own
questions back. Then:

```bash
python3 scripts/review_round.py read
```

Why a file and not a conversation: an answer given in chat is applied once and
then lost. Nobody can later say who decided that two forks were one question,
or why — so it gets asked again, and may be answered differently.

Deferring is a legitimate answer. `need more evidence` routes to `/challenge`.

## 3 · Refine — AI

`/refine`. Apply the answers, record what each one changed, re-run the audits.

Repairs **split, never merge**, unless a human explicitly said to merge. The
asymmetry is not stylistic: over-merge is invisible in the output and
unrecoverable, under-merge is visible and fixable later.

Finalising means the numbers are quotable. Everything before this is a draft.

## 4 · Walk — owner

`/walk`. Exploratory, with no queue and no pending questions: does the map
look like the corpus this person knows?

Different from phase 2. Review works a ranked list of suspicious items; a walk
follows curiosity, which finds a different class of error — the fork that is
obviously missing, the stage that feels wrong, the option that reads oddly at a
place no metric flagged. **The rater-fork error was found this way**, by
reading two option lists side by side, after a statistic said everything was
fine.

A walk usually generates a new round. That is success, not failure.

## 5 · Itinerary — visitor + AI

`/itinerary`. Choose a path through the garden.

**The visitor was not in phases 0–4.** They did not write the intake and did
not answer the review. So the consultation must supply the context rather
than rely on it: what the study asked, what a fork is, what stable and novel
mean here, and which findings are already known to be weak.

## 6 · Run and report — AI

Build the analysis the path specifies, run it, report the estimate beside the
distribution of real runs that took the same path — usually none, and say so.

## 7 · Inspect — visitor + AI

Did it do what the itinerary said? Is the estimate plausible, and if it is
surprising, is that the path or a bug? **One run is one observation** and does
not update a finding.

## 8 · File — AI

Add it to the garden with its provenance tag:

| | |
|---|---|
| `corpus` | extracted from an analysis a real analyst wrote |
| `itinerary` | assembled entirely from options the corpus contains |
| `authored` | contains an operation no run in the corpus performed |

**The new run counts.** Recompute the statistics including it — an itinerary
run is a human's deliberate choice, executed, which is exactly what a corpus
run is. Excluding it would treat a person's choice as less real than an
analyst's, and would mean the garden can never grow.

What provenance buys is the ability to *tell*. `stability.py` reports every
concentration statistic both ways once any non-corpus run exists, so a headline
that moves is visible:

```
PROVENANCE  (221 corpus, 1 assembled)
                              all runs   corpus only    delta
  mean modal share               0.680         0.680   +0.000
  mean effective options         2.848         2.856   -0.008
```

The hazard was never that assembled runs count. It is a number that drifts
silently as paths are walked, and the fix for that is visibility, not
exclusion.

---

## The shape of it

Phases 0, 2, 4 and 7 need the owner or the visitor. Not for approval — for
judgement the pipeline cannot supply: what the corpus means, whether two questions are one,
whether the map matches the field, what path is worth walking, and whether a
result is believable.

Everything the AI does between them is either **frozen** — deterministic,
cached, reproducible — or an **audit that ships the evidence against itself**.

Both halves follow from one principle: the system is accountable to the source
material *and* to the person it supports, and neither obligation discharges the
other. The frozen half is what makes a claim about the corpus checkable; the
gates and the exhibits are what make it checkable **by the user**. That is the
subject of [`DESIGN.md`](DESIGN.md).

The loop back matters more than the sequence. Phase 4 feeds phase 2, phase 7
feeds phase 5, and a study that never loops has probably not been read.
