# Working in this repository

Rules for an agent operating here. The *rationale* is in
[`docs/DESIGN.md`](docs/DESIGN.md); this is the short operational form.

## Orient first

```bash
python3 -c "import sys;sys.path.insert(0,'scripts');import paths as P;print(P.describe())"
python3 scripts/_selfcheck.py
```

`_selfcheck` is 21 assertions and takes seconds. Run it before and after any
change to scripts, prompts, or docs.

## The rules that are not style

**Do not edit a file in `prompts/`.** The cache is keyed on prompt text, so an
edit orphans every answer that wording produced and silently decouples the
shipped data from the prompt beside it. If a prompt is wrong, say so and use
`scripts/relink.py` as the model for re-deriving what depended on it.

**Do not quote a number you have not opened a file to get.** The counts changed
several times during this project; remembered figures are wrong.

**Do not report a `PASS` you cannot state a blind spot for.** `exhibit.py`
refuses it, and the refusal is the point — see
[`docs/AUDITING.md`](docs/AUDITING.md).

**Do not tune a threshold until a check passes.** If a verdict looks wrong, the
exhibit is the argument.

**Do not describe a ranked queue as clean.** V1, V3 and V4 rank by weak signals
that cannot see paraphrases sharing no words. Report depth read, not absence.

**Do not mix vocabulary tags.** Mixing does not crash; it answers a different
question. The headline tag is `study.json`'s `final_tag`.

## Which workflow you are in

[`docs/LIFECYCLE.md`](docs/LIFECYCLE.md) has nine phases and two human roles —
the **garden owner** (intake, review, refine, walk) and the **garden visitor**
(itinerary, inspect). Each phase is driven by a skill in `.claude/skills/`.

[`docs/WORKFLOW.md`](docs/WORKFLOW.md) covers the charting pipeline only:
which script writes which file.

## Before you finish

Say what you ran, what it returned, and what you did **not** check. If an audit
returns REVIEW, give the exhibit and its handle rather than the verdict alone.
