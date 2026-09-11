# Corpus brief — instructions to agents that will generate a corpus

**Status: written, never used.** No corpus in this repository was generated
under this brief. It is a design, offered to whoever runs the first generated
study, and it should be treated as untested until then.

When a study generates its own corpus rather than collecting one, the intake
can happen first and its output can instruct the generating agents. The point
is to make what they leave behind **parseable**, not to shape what they decide.

## The line

| may be specified | must not be |
|---|---|
| write the final script to a named file | which model family to use |
| write a report naming what you did and why | which covariates to adjust for |
| keep the script that produced the reported numbers | how to handle missing data |
| state your estimand and effect measure explicitly | what robustness checks to run |
| do not delete intermediate steps you actually ran | what to conclude |

Left column: **artifacts**. Right column: **analysis**.

Constraining artifacts costs nothing analytically. Constraining analysis
destroys the object of study — a multiverse whose axes were handed to the
analysts is a specification curve wearing a costume.

If a brief item cannot be placed clearly in the left column, leave it out.

---

## The brief

Copy from here down, fill the bracketed parts, and give it to the agents.

> ### Your task
>
> Analyse `[dataset]` to answer: **[the question]**
>
> Beyond this paragraph, **every analytic choice is yours.** Nothing below
> constrains what you decide — only what you leave behind. Where you are unsure
> which of several defensible approaches to take, take the one you judge best
> and say why; do not converge on what you imagine is expected.
>
> ### What to leave behind
>
> **`analysis.[ext]`** — the script that produced the numbers you report. It
> must run end to end from the raw data. If you explored and then simplified,
> this is the simplified version, and see the note on exploration below.
>
> **`report.md`** — what you did and why. For each substantive choice, state
> the choice, the alternatives you considered, and your reason. Where you used
> a default without deliberating, say so plainly — *"I used the package
> default"* is a complete and useful answer, and one that is routinely
> omitted.
>
> **`estimate.json`** — the headline result, structured:
>
> ```json
> {"estimand": "what you estimated, in words",
>  "estimate": 0.0, "scale": "odds_ratio | risk_difference | ...",
>  "ci_low": 0.0, "ci_high": 0.0,
>  "conclusion": "supported | not_supported | inconclusive",
>  "notes": "anything a reader needs to interpret the above"}
> ```
>
> **`exploration/`** *(optional)* — scripts for things you tried and did not
> report. Keep them. An abandoned branch is evidence about the analysis, and
> deleting it is the single most common way a decision becomes invisible.
>
> ### Two things that are easy to get wrong
>
> **Do not tidy the decision out of the script.** If you set a threshold, leave
> it as a named value where you set it. Inlining it into the expression that
> uses it makes it unrecoverable.
>
> **Report what you did, not what you would recommend.** If your script drops
> rows and your report says you imputed, the two disagree and the disagreement
> will be found.

---

## Why each item earns its place

Each one corresponds to a specific cost paid in the soccer study.

| item | what it would have prevented |
|---|---|
| a named script, required | **12 of 31 human teams deposited no script** and contribute zero decisions — the largest caveat in that study |
| `estimate.json` | outcomes were assembled per run outside the pipeline; **52 of 207 records have no provenance** and never can |
| stating the estimand | effect measures arrive on mixed scales and must be converted after the fact, imperfectly |
| *"I used the default"* | defaults used without comment are recorded as silent decisions — true, but a stated default is a stronger record than an inferred one |
| keeping exploration | robustness refits are currently inferred from co-occurrence patterns rather than observed |
| not inlining thresholds | a threshold folded into an expression is harder to recover as its own decision |

## What this cannot fix

A brief improves the *record*, not the *analysis*. It will not make agents
disagree less, will not make their reasoning better, and must not try.

And it introduces a hazard worth naming: a corpus generated under a brief is
**not exchangeable** with one collected in the wild. Its artifacts are more
complete and its silent-decision rate will be lower — because it was asked to
write things down, not because its analysts were more forthcoming. Any
comparison across the two must say so, and any study that uses a brief should
record it beside `study.json` so the comparison is possible at all.
