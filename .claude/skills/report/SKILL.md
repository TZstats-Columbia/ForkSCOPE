---
name: report
description: >-
  Regenerate the technical report over the current build — refresh every number
  from the artifacts, rewrite the prose that carries it, and mark what moved.
  Use after /refine, after an audit changes a verdict, or whenever a quoted
  figure no longer matches the data.
---

Bring `report/REPORT.md` back into agreement with the build. Argument: an
optional section name to limit the pass to.

Read [`report/README.md`](../../../report/README.md) first. It states what must
stay true of the document, and two of its rules decide most of this work: the
report is **not the paper**, and it is **rewritten under its readers** whenever
the measurements change.

## The failure this exists to prevent

A number in the report and a different number in the data, both plausible, with
nothing that fires. It has happened here: `n_forks` stale in six of ten files
while a headline claimed 463 decision points, and a figure rendered from the
unrepaired vocabulary with every stage exiting 0.

So the pass is not "read the report and improve it". It is: **derive every
number again from the artifacts, then find where the prose disagrees.**

## 1 · Establish the build the report is about

```bash
python3 -c "import sys;sys.path.insert(0,'scripts');import paths as P;print(P.describe())"
python3 scripts/_selfcheck.py
python3 scripts/compare_vocab.py
python3 scripts/settle.py status
```

If a gate is `STALE`, say so in the report before anything else. A report over a
layer that moved after it was settled is describing two builds at once.

## 2 · Re-derive, never recall

Every count in the report comes from the vocabulary the study names as
`final_tag`, not from an earlier stage and not from memory:

```bash
python3 - <<'PY'
import json, sys; sys.path.insert(0, "scripts")
import paths as P, vocab
V = json.load(open(P.VOCAB / f"bottom_up_{P.FINAL_TAG}.json"))
fs = vocab.fork_stats(V)
print("tag        ", P.FINAL_TAG)
print("analyses   ", V["n_runs"])
print("decisions  ", V["n_decisions"])
print("options    ", V["n_options"])
print("forks      ", len(fs))
print("pivotal    ", sum(1 for s in fs.values() if s["eff_all"] > 1.5))
print("measurable ", sum(1 for s in fs.values() if s["reach"] >= 10))
PY
```

**The `forks` list in that file is longer than the fork count.** It carries
empty entries; `vocab.fork_stats` is the definition, and the header `n_forks`
agrees with it. Anything that reports `len(V["forks"])` is wrong by ~150.

Likewise **effective options is defined once**, in `vocab.fork_stats`: one vote
per analysis, its modal option at that fork. Four scripts historically summed
run-set sizes per option instead, which counts an analysis once per option it
holds and inflates the figure — `policy.json:_open` names the ones still
carrying it. If a section quotes an effective-options number, check which
definition produced it before repeating it.

## 3 · Rewrite the prose over the numbers

Use the **`interpreter`** agent for sections that state what failed. It exists
so the numbers are not adjusted and the failures are not softened.

Three rules the document is held to, and they are not style:

**Every number carries its matching level.** A stability figure quoted without
verbatim / lenient / core is not a number. The contract form:

> **0.713** lenient · verbatim 0.176, core 0.895 · n = 30 runs, stratified

**Every claim carries its denominator.** "18 decision points reached by ≥25% of
runs" and "317 decision points" describe the same build. Which is the headline
is a choice, and the report says it is making one.

**The limitations section is not a disclaimer.** It holds findings — that most
analyses violate exclusivity somewhere, that 12 of 31 human teams deposited no
script, that fork induction disagrees with itself at ARI 0.62 on identical
input. Those are results about the instrument and belong at full strength.

## 4 · Retract in place

If a published claim changed, **do not silently edit the number.** Mark the old
claim with the reason and leave the body readable. The record of having been
wrong is worth more than a clean paragraph — a methods paper that shows its own
error-finding working is more credible than one that does not, and this project
has four such corrections on file.

The cross-validation bug that reversed a headline finding is the model: the
wrong number is printed beside the right one, with what caused it.

## What you must refuse

- **Do not quote a number you have not opened a file to get.** The counts have
  moved several times in this project; remembered figures are wrong.
- **Do not report an analysis number whose audit has not run.** Invoke `/audit`
  first, and carry its REVIEW verdicts into the report rather than around them.
- **Do not treat this as a draft of the paper.** A paper makes a case to a field
  and belongs to its authors. If asked to shape the report toward an argument,
  say what the difference is and offer to write the argument separately.
- **Do not resolve a disagreement between the report and the data in the
  report's favour.** The artifacts win, always.

## Reporting

What moved, and by how much — old value beside new for every changed figure.
Which sections you did not touch. What is now stale elsewhere: the READMEs under
`data/` quote some of the same numbers and go stale in the same pass.
