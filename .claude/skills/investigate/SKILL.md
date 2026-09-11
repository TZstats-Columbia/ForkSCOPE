---
name: investigate
description: >-
  Answer a question about one fork, option, decision or run by walking the
  evidence chain to its source. Use when the user asks why a fork has so many
  options, what a number rests on, where a decision came from, or to trace any
  claim in the results.
---

Answer a specific question by walking the chain, not by reasoning about it.
Argument: a handle, a fork or option label, a run id, or a question naming one.

    fork -> options -> decisions -> run + line -> source

`scripts/trace.py` is the only thing that joins these files. Use it before
forming a view.

## Find the thing

```bash
python3 scripts/trace.py fork "discretiz"                  # substring -> candidates
python3 scripts/trace.py fork "fork:0cc97d1e" --limit 20
python3 scripts/trace.py option "average the two raters"
python3 scripts/trace.py run team-10
python3 scripts/trace.py resolve dec:team-10@8
```

Ambiguity is listed, never guessed. `--json` for structured output, `--limit`
to widen, `--source` for the literal lines.

In Python, when one question needs many lookups:

```python
import sys; sys.path.insert(0, "scripts")
from trace import Tracer
t = Tracer()
t.fork(t.forks("discretiz")[0])
```

## Four rungs offline, the fifth needs the corpus

Operation descriptions, run ids and line numbers resolve from what is
committed. The literal source lines do not — the corpora are third-party and
not vendored:

```bash
export FORKSCOPE_RAW_AI=/path/to/agentic-forking-path
python3 scripts/trace.py option "..." --source
```

Most questions are answerable from the operation description. Say plainly when
one is not.

## Things worth knowing before you conclude

**Labels are rewritten by every merge stage.** `forks("discretiz")` returns two
hits on the current headline vocabulary and none on `ai+human.merged` — and it
returned a different count on the tag before this one, which is the lesson
rather than a footnote to it. Never carry a label between stages, never quote a
hit count from memory, and search within the vocabulary you actually loaded.

**A fork with many options may be contested or mis-clustered.** The shapes are
identical. Read the options; if they are the same action in different words,
that is an under-merge and belongs in the V1 queue.

**Co-occurrence is decisive where it fires.** Two options at one fork chosen by
the same run means that fork is not a single-choice slot — check V2 before
treating its modal share as meaningful.

**`option_raw` is dual-typed** in the vocabularies on disk. Read it through
`trace.raw_labels(option)`; `sorted()` on a string yields characters.

## Answering

Give the answer, then the chain that supports it, with handles so the person
can re-walk it. If the chain does not settle the question, say what it would
take — usually a larger adjudication sample or the raw corpus — and offer
`/challenge`.

**A visitor may be asking this without having read anything.** They did not
write the intake and did not answer a review round, so a handle alone is not an
answer to them. Point them at `figures/forkscope.html` for the fork in context,
and at [`README.md`](../../../README.md) if the question is really about what the
method claims rather than about this fork.

If the question is about a *finding* rather than a fork — whether a result holds,
how confident we are — that is `/challenge`, which escalates the test. This skill
walks the chain; it does not re-run the evidence.
