# 2025-11-20T22-37-30+0000  (ai)

- code: 276 lines, 38% exon (105 lines in 13 decisions)
- intron: print 94, comment 46, plot 17, import 10, config 3, glue 1
- prose: 290 lines, 95 claims (45 action, 50 result)
- links: 43 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 12
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 6
- result_claims_deferred: 50

## Silent decisions — executed, never disclosed

- **69-73** [high] choose which columns (outcome, group, covariates, ID fields) enter the modeling dataset

## All decisions

- `33` [high] **linked x2** — load the full player-referee dyad CSV as the study population with no upfront filtering
- `35-37` [high] **linked x1** — average the two independent raters' scores into one continuous skin-tone measure
- `38-40` [high] **linked x1** — collapse red-card count into a binary any-red-card outcome (redCards>0)
- `52-60, 80-82` [high] **linked x7** — dichotomize skin tone into light (<=0.25) vs dark (>=0.5), dropping the middle band entirely, then encode the retained groups as a 0/1 dark indicator
- `69-73` [high] **SILENT** — choose which columns (outcome, group, covariates, ID fields) enter the modeling dataset
- `74-76` [high] **linked x7** — restrict to complete cases on the selected variables, dropping any dyad with a missing value
- `83-86` [medium] **linked x1** — one-hot encode position and leagueCountry, keeping every level at creation time (drop_first=False)
- `109-117` [high] **linked x3** — assemble the regression design matrix: dark indicator plus continuous covariates plus dummy sets with one reference level per category dropped via [1:], and add an intercept column
- `118-123` [high] **linked x4** — fit a logistic regression of anyRedCard on the design matrix using cluster-robust standard errors clustered by player
- `139-154` [high] **linked x4** — estimate the g-computation adjusted risk difference by scoring the whole sample under counterfactual dark=1 and dark=0 and differencing the mean predicted probabilities
- `165-192` [high] **linked x2** — propagate parameter uncertainty by drawing 10,000 coefficient vectors from the fitted model's asymptotic multivariate-normal distribution and recomputing the risk difference for every draw
- `193-196` [high] **linked x4** — summarize the simulated risk-difference draws as a 2.5/97.5 percentile interval and derive a two-sided p-value from the share of draws on each side of zero
- `258-263, 267-271` [high] **linked x7** — declare the hypothesis supported only if p<0.05 AND the CI lower bound exceeds zero, reusing the same 0.05 cutoff to phrase the caveat when it is not met
