---
name: challenge
description: >-
  Demand more evidence for one specific claim — escalate its test, enlarge its
  sample, or re-adjudicate it. Use when the user doubts a reported result, asks
  how confident we are, or asks for a claim to be checked harder.
---

Take one claim and try harder to break it. Argument: the claim, a check id, or
a handle.

Every lever below is real and costs something. Name the cost before spending
it, and report what the escalation actually changed — including when it
changed nothing, which is the more common and more useful outcome.

## Pick the lever the claim needs

**A permutation p that hit its floor.** A permutation p cannot fall below
1/(B+1), and a BH-corrected threshold often sits under a cheap screen's floor,
so a test can report "nothing significant" *by construction*. Check the `PERM`
constant in the script that produced the claim (`fork_graph.py`, `grounds.py`,
`circle.py`, `audit_garden.py`, `audit_shapley.py`); `circle.py` already
escalates survivors via `PERM_DEEP`. Raising a constant re-runs a
CPU-bound test with no model calls — cheap, and the first thing to try.

**An adjudication measured on a sample.** Enlarge it:

```bash
python3 scripts/audit_granularity.py --corpus <tag> --sample 120
python3 scripts/audit_vocab.py --show 60
```

`audit_granularity` calls a model per fork and is stratified by run count, so
the strata shift as the sample grows. Report the new stratum counts, not just
the headline.

**A judgement you want to know is stable.** `llm.py` supports `nocache=True`:
re-ask a pass and compare it with itself. **No pass has ever been run twice**,
and this is the largest outstanding methodological gap. A challenge that measures it closes
that gap as a side effect — say so when proposing it.

**A claim about one fork.** Do not escalate a corpus-wide test; walk the chain
with `/investigate`. Reading twenty options settles most fork-level doubts
faster and cheaper than any statistic.

## Rules

**Escalate the test, never the threshold.** If more evidence does not move a
claim, the claim was weak — say that. Adjusting a cutoff until something passes
is manufacturing the result.

**A policy value is not a threshold you may move.** `policy.json` records the
method decisions a human made at intake, with what each one cost. Re-running a
challenge under a different pivotal criterion or a different similarity level
answers a different question, and if that is the challenge worth running, say so
and put it to the owner as a new decision — do not fold it into the escalation.
`policy.json:_open` lists the values nobody has sensitivity-checked; a challenge
against one of those is legitimate and unusually valuable, and it should be
reported as *"this value has never been checked, here is what it does"* rather
than as a result about the claim it touched.

**A stronger test that still fails is a finding.** Report it as one. H1 and G4
stand as REVIEW for exactly this reason.

**Do not re-run everything.** Identify the one script behind the claim. A full
rebuild to check one number wastes hours and buys nothing.

**Say what it cost.** Model calls and wall time, from `cache/llm_runs/`.

## Reporting

Before: the claim and its evidence. What you escalated and why that lever.
After: the new number. Then the verdict — **held**, **weakened**, or
**overturned** — and if overturned, what else rests on it. Record the outcome
in the audit report or LIMITATIONS; a challenge nobody can find later has to be
repeated.
