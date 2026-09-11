---
name: settle
description: >-
  Close a checkpoint — assemble the reproducibility evidence for one layer, put
  the settle-or-rerun question to a human, and record the answer as a lock with
  a content hash. Use after distillation and after charting, before building on
  either.
---

You are closing a question, not reporting a number. Argument: a layer
(`distill` or `chart`).

Two checkpoints exist because the layers fail independently. Distillation can be
good enough to build on while charting is not, and charting cannot be judged at
all until distillation is settled — otherwise a disagreement in the vocabulary
might be an extraction that moved underneath it.

## Show where it stands

```bash
python3 scripts/settle.py status
python3 scripts/settle.py verify           # re-hash the layer against its lock
```

`unlocked` means nobody has decided. `STALE` means somebody decided and the
layer has since moved — which is the state this whole mechanism exists to make
visible, because nothing else notices it.

`verify` is the one to run before quoting anything downstream. `status` reports
what the lock file says; `verify` re-hashes the layer and compares, which is the
difference between a claim and a check.

## Assemble the evidence for that layer

**distill** — how much a re-extraction of the same runs agrees with itself.

**Read the committed evidence first.** All three measurements already exist, and
for the packaged soccer study this is the whole of what you need:

```bash
python3 -m json.tool stability/data/q1_distill.json  | head -40   # span agreement
python3 -m json.tool stability/data/q1b_residue.json | head -20   # jitter -> options
python3 -m json.tool stability/data/q1c_semantic.json | head -20  # blinded read
```

Re-measuring needs **two builds to compare**, and each script takes both as
paths to a `data/distilled` directory — they do not discover them and they fail
with `error: the following arguments are required: --a, --b` if you omit them:

```bash
python3 stability/scripts/q1_distill.py  --a data/distilled --b <replicate>/data/distilled
python3 stability/scripts/q1b_residue.py --a data/distilled --b <replicate>/data/distilled
python3 stability/scripts/q1c_adjudicate.py --a data/distilled --b <replicate>/data/distilled
```

`q1c_adjudicate.py` **calls a model**; the other two do not. `<replicate>` is a
root built by `/replicate distill`, which spends about $60 for 30 runs — so if
the committed numbers answer the question, they are the answer.

**This gate carries its own conversation.** `review_round.py` is bound to
`vocab_exhibits.json` and has no `--layer` flag, so there is no distillation
round to open and no queue file to work from — the evidence above *is* the
material, and you put it to the owner here rather than routing them to
`/review`. Say that plainly if they ask why the two layers feel different.

**chart** — how much fork formation agrees with itself, and what the audits
queued.

```bash
python3 scripts/audit_vocab.py                          # V1-V7 exhibits
python3 -m json.tool replicates/results/fork_variance.json
```

**`fork_variance.py --root replicates` does not work in the shipped package.**
It reads each replicate's `manifest.json` for a `final_tag` and skips any
without one; the committed manifests have none, and the root the result file
names — `stability/replicates` — is not shipped at all. Only the *result* is.
So the number is available and the recomputation is not:

```bash
python3 stability/scripts/fork_variance.py --root <root with built replicates>
```

That root comes from `/replicate forks`, which costs about $21 per replicate.
Say which of the two you are quoting — the committed result or a fresh run —
because they are not the same claim.

## Put the question, with the number that decides it

**Quote the level, always.** The soccer corpus scores 0.176 verbatim and 0.895
core on one extraction. A stability figure without its matching level is not a
figure, and the level was chosen at intake — use that one and show the others
beside it.

**Say what is a limit and what is an artifact.** A low number that survives
blinded semantic adjudication is a real limit; one that does not is a matching
artifact. These lead to opposite decisions and only the adjudication separates
them.

**Say what the decision licenses.** Settling distillation means charting numbers
will be quoted without re-opening extraction. Say that, so agreeing to it is
agreeing to something.

**Offer re-running as a real option, with its price.** A distillation re-run is
roughly $60 for 30 runs and $450 for all of them. If the evidence does not
support settling, say so.

## Record it

```bash
python3 scripts/settle.py lock distill \
  --by "<who>" \
  --decision "<what they decided, and the reason, in their words>" \
  --evidence stability/data/q1_distill.json \
  --evidence stability/data/q1c_semantic.json
```

The decision is stored verbatim. Do not compress it into a verdict: *"lock it,
0.713 is enough at the lenient level, and the 0.489 silent figure bounds the
silent analysis only"* is the useful record, and `"settled"` is not.

Attach the evidence. A lock with no evidence cannot be revisited on its merits,
and it will need revisiting.

## Rules

**Never settle a layer yourself.** No autonomous run may call `settle.py lock`.
The mechanism exists to record a human judgement; a lock the agent wrote records
nothing.

**Bring the open questions to every gate.** `policy.json:_open` is the standing
list of what nobody has checked — on soccer, an unvalidated similarity
threshold, a queue cap that is a guess about attention, an interleaving rule
nobody argued, and the unmeasured reliability of `outcomes.json`. Read it out at
the gate. An open question visible only in a file nobody opens is not open, it
is forgotten, and a gate is the one moment someone is obliged to look.

**A stale lock is not an error to fix.** It means work downstream is resting on
something nobody has reviewed in its current form. Report it and re-open;
do not re-lock to make it quiet.

**Re-opening needs a reason too.** `settle.py unlock --why` keeps the old lock
in a history file. Deciding to reconsider is a decision.

**Do not settle a layer whose upstream is stale.** Charting judged against a
distillation that moved is measuring two things at once.

Close by reporting: what was settled, on what evidence, and what is still open.
