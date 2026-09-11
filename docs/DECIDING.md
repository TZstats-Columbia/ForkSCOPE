# Deciding — and how errors reach the garden owner

`AUDITING.md` asks whether a number can be believed. This asks a different
question: **what does the person running the study have to do, and how much of
it is unnecessarily hard?**

Both halves come from what actually happened over this study. The garden owner
had to do two things, and neither was made easy for them:

1. make method decisions they had no prior opinion about
2. catch the agent's mistakes

The second is the one to be embarrassed about. A collaboration where the human
is the backstop for the agent's errors is one where the human's attention is
spent on the wrong thing.

---

## Part 1 · Three classes of error, three different mechanisms

Treating these alike is why errors reached the owner late.

### Loud-wrong — it crashes

Phase 2 died three times: missing directories, an undocumented two-pass
requirement, an input that was never copied. Each cost forty minutes and no
money.

**Mechanism: preflight.** Check every input before spending anything, and report
*all* gaps rather than the first. `replicate.py:preflight()` exists because
those three failures each surfaced a different missing file.

This class is self-limiting and cheap. It is not the problem.

### Silent-wrong — it completes and the content is wrong

The dangerous class, and every instance in this project looked like success:

| what happened | what it looked like |
|---|---|
| `--corpus ai,human` rendered the **unrepaired** vocabulary | every figure stage exited 0 |
| `n_forks` header stale for six of ten files | a headline quoting a file header instead of a count |
| B replicates would have read **A's** garden | both sides completed; agreement inflated |
| the committed audit described a vocabulary not in the repo | the audit passed |
| `head -n f > /tmp/x \|\| head -n f > _i.md` | 162 lines of `INTAKE.md` deleted |

**Mechanism: a guard at the point of use — never a report.** A report is read
by someone already suspicious. The guard has to fire for someone who is not:

- `build_figures.py` prints a banner naming the gap between the tag asked for
  and `final_tag`, with both decision-point counts
- `settle.py` stores a content hash, so a settled layer that moves says so
  without anyone asking
- `replicate.py` refuses a root holding more than one vocabulary, because the
  extra one would be read instead of re-derived and report perfect agreement

The test for this class: **if this went wrong right now, what would the operator
see?** If the answer is "a plausible number", write a guard.

### Unknowable — it needs a person

Whether two forks are one question. Whether an option bundles two decisions.
These are not errors; they are the work.

**Mechanism: a ranked queue with a cap.** V1 alone queues 561 pairs, which is
not a queue — it is a way of not being read. The cap
(`policy.json:audit.review_queue_max`) is an admission that attention is finite,
and it should be set to what a person will actually read.

---

## Part 2 · Making the decisions easier

### Nobody has a prior opinion about a threshold

"What is the minimum number of decision points for a recurring option?" is
unanswerable cold, and asking it produces a shrug and a default.

The same question with its consequence attached is easy:

> How should two distillations of one run be compared — verbatim spans, or with
> room for boundaries to move? On this corpus: **0.176 verbatim, 0.713 lenient,
> 0.895 core.** Same pipeline, same data. Which do you want to be able to claim?

That is a **decision card**, and it has four parts:

1. **what it decides** — in one line, in the owner's terms
2. **the options** — discrete where they are discrete
3. **what each costs, measured on this corpus** — not in general
4. **a recommendation**, stated as a recommendation and overrulable

The best decisions in this study came from the owner asking a question the
agent had not surfaced — *"how do you grade reproducibility? verbatim or
lenient?"* The choice existed, it was load-bearing, and nothing announced it.
That is the failure decision cards prevent.

### Every number arrives with its alternative and its denominator

The agent quoted **0.176** as *the* reproducibility number. It is a fact about
where span boundaries fall, not about whether extraction reproduces, and the
same run scored 0.895 at the level the owner had already chosen.

The contract:

> **0.713** lenient · verbatim 0.176, core 0.895 · n = 30 runs, stratified

Level, alternatives, denominator. A stability figure without its matching level
is not a figure.

### Say which way to err

Over-merge is invisible and unrecoverable; under-merge is visible and fixable.
When a call is close, **that asymmetry is the advice** — it converts a judgement
the owner cannot make into one they can.

Generalise it: every decision card names the reversible direction.

### Keep a standing list of what is not known

`policy.json:_open` holds four: the Jaccard threshold nobody sensitivity-checked,
the queue cap that is a guess about attention, the interleaving rule nobody
argued, and the unmeasured reliability of `outcomes.json`.

Surface that list **at every gate**. An open question that is only visible in a
file nobody opens is not open, it is forgotten.

---

## Part 3 · What the agent owes the owner

**Never make them the backstop.** If an operation can silently destroy or
corrupt, guard it. Reading a file back after writing it is cheap; git recovering
it afterwards is luck.

**Show the correction, not a corrected story.** The variance decomposition was
first reported with the conclusion inverted. The useful record is that the
threshold compared the wrong pair of numbers — not a clean paragraph that never
mentions it.

**Say what a decision licenses.** "Settling distillation means charting numbers
will be quoted without re-opening extraction." Agreeing to something should be
agreeing to something.

**Never settle a question on their behalf.** No autonomous run writes a lock. A
lock the agent wrote records no human judgement, and its only effect is to make
an open question look closed.

**Report progress during long work, and keep it short.** A four-hour batch that
says nothing until it finishes leaves the owner unable to intervene while
intervening is still cheap. A status table and the one or two numbers that
changed — not prose, not a narration of every step:

```
  [4/9] A5   $18.81 ok   317 -> 336 -> 299   (4849s elapsed)
```

The test is whether they could stop the run on what you just told them.

**Flag the singular thing, unprompted.** The most valuable observations in this
study were not answers to questions. They were noticing that a number was odd
and saying so:

- the root cache held exactly 207 entries not in the package, and
  `cache_superseded/` held exactly 207 — the coincidence that proved the
  directory was redundant rather than a second archive
- `18` appeared as both "coverage ≥25%" and "coverage ≥25% **and** >1.5
  effective options", which is how two different populations came to share one
  number in the README
- the call log recorded `model_resolved: claude-opus-4-8` — the alias `opus`
  was not resolving to what the report was about to claim
- $248 of cache sat in one untracked directory on one machine, the same
  single-copy exposure the owner had already acted on for the corpus

None was asked for. Each changed something. **An anomaly noticed and not
mentioned is a decision made silently on the owner's behalf** — which is the
thing this whole document is against.
