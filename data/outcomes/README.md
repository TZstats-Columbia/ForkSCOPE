# outcomes/ — what each run concluded

The payout side of the analysis: choices on one side, the answer on the other.

| file | made by | |
|---|---|---|
| `outcomes.json` | **no generator in this package** — see below | 207 records, one per run that reported a usable estimate |
| `fragments/` | same | 155 per-run JSONs, the provenance behind 155 of those records |

| field | |
|---|---|
| `repo_id` | the run id — joins to [`../distilled/`](../distilled/) and to `decisions[].run` in the vocabulary |
| `primary_estimand_type` | what the run estimated |
| `primary_estimate`, `or_scale_estimate` | the effect, and it converted to an odds-ratio scale |
| `ci_low`, `ci_high` | interval as reported |
| `conclusion` | the run's own verdict |
| `notes` | extraction caveats |

## This file has no producer, and that is a real gap

Five scripts read `outcomes.json` — `shapley_v2.py`, `audit_shapley.py`,
`iteration.py`, `novelty.py`, `novelty_curve.py`. Nothing writes it. It was
assembled per run, outside the pipeline, and cannot be regenerated from what
the package carries.

What can be done is verification. The per-run fragments are vendored here, and
they agree with the assembled file field for field:

```bash
python3 scripts/check_outcomes.py
```

```
records in outcomes.json     : 207
per-run fragments on disk    : 155
records verified against one : 155 (75%)
records with no fragment     : 52
fragments with no record     : 0
```

So three quarters of the file has provenance and **52 records have none**. They
are not wrong — they are unverifiable from what is committed.

`check_outcomes.py` deliberately checks rather than rebuilds. A script that
regenerated `outcomes.json` from the fragments would silently drop those 52
runs, which is worse than the gap it would appear to close.

## Two things that constrain what it can support

**Extraction was blind to the vocabulary.** Outcomes were pulled per run
without reference to any decision labels — deliberately, so outcome-linked
results are not the clustering grading its own work. It has not been re-derived
since, so it predates the current vocabulary.

**207, not 223.** Human teams have no extracted outcome. Any Shapley result
therefore uses the *pooled vocabulary* with *AI-only outcomes*, and is not an
AI-versus-human comparison. See the
Limitations section of [`../../report/REPORT.md`](../../report/REPORT.md).

The headline result on this file: the 17 pivotal forks predict the reported
verdict and *z* statistic out of sample (cross-validated R² **+0.262** and
**+0.246**) and the effect size poorly (**+0.032** for log(OR), **+0.046** for
interval width); see
`../analysis/shapley_ai+human.merged.forkmerged.merged.induced.r3.osplit.pivotal.json`.
