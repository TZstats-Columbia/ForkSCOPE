# `report/` — the technical report

**[`REPORT.md`](REPORT.md)** — one file, with a table of contents.

A technical report the agent maintains **for the person running the study**. It
states what the pipeline did, what the numbers are, and what they do not
support, in enough detail to be argued with.

**It is deliberately not your paper.** A paper makes a case to a field and
belongs to its authors; this reports a method and its measurements, and is
rewritten whenever the measurements change. Take from it what you need — the
numbers, the tables, a section's argument — but expect it to be rewritten under
you, and do not edit it as a draft of something else.

Study-scoped: this is *one study's* report and lives under `STUDY_ROOT`
alongside `data/` and `figures/`. A second study writes its own. See
`paths.py:REPORT`.

## Working with an AI on this

AI can scale up work and produce output fast. That is only worth having if a
person can still direct and check it — so the burden is on the AI to make
input, guidance and oversight **cheap**:

- **checkable evidence**, not summaries — every claim shipped with the thing
  that would break it
- **organised visualization**, so structure can be seen rather than described
- **exposed vagueness**, marking what is uncertain, defaulted or ambiguous in
  the AI's own work instead of smoothing it into confident prose

The asymmetry this answers: producing is cheap and checking is not. Scaling
output without scaling *checkability* turns oversight into a rubber stamp, and
an artifact too large to check is indistinguishable from an unchecked one.

Mechanics in [`../docs/DECIDING.md`](../docs/DECIDING.md). This report is one of the checkable artifacts: every number carries its level, its alternative and its denominator.

## Why Markdown, and why there is only one file

The report is regenerated whenever the measurements change, and that decides
the format. A LaTeX diff between two versions is unreadable — the substantive
change is buried in reflowed paragraphs and float placement — so the property
the document most needs, *showing what moved*, is the one LaTeX gives up.

It also drops the toolchain. A report nobody can read without `pdflatex` is a
report most readers meet as source, and the source is what sits in this folder
next to the figures it describes.

**Markdown is the source, not a rendering of one.** The LaTeX tree it was
converted from is deleted rather than kept alongside, because two sources drift
and the drift is silent — the same failure as a stale figure beside new data.
Edit `REPORT.md` directly. The one-time converter is recoverable from git if
the conversion itself ever needs re-examining.

What was given up is real and small: typeset equations (now fenced blocks read
as source), BibTeX (an inline References section), and numbered
cross-references (resolved to section titles, which are stable where numbers
are not).

## What must stay true of it

**Every number carries its matching level.** A stability figure quoted without
saying whether it is verbatim, lenient, or core is not a number.

**Every claim carries its denominator.** "18 decision points reached by ≥25% of
runs" and "317 decision points" describe the same build; which is the headline
is a choice, and the report says it is making one.