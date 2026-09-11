# 2025-11-20T23-33-39+0000  (ai)

- code: 286 lines, 34% exon (96 lines in 19 decisions)
- intron: print 85, comment 44, plot 35, glue 15, import 10, config 1
- prose: 246 lines, 87 claims (60 action, 27 result)
- links: 52 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 14
- result_claims_deferred: 27

## Silent decisions — executed, never disclosed

- **70-74** [medium] choose which columns (outcome, exposure, covariates, IDs) are carried into the regression dataset
- **132-137, 171-177, 201-204** [medium] derive p-values and 95% confidence intervals via a normal-approximation (Wald) z-test with cluster-robust SEs

## Misaligned — code and prose disagree

- code: collapse red card counts into a binary any-red-card outcome using a >0 threshold
  - prose: direct red cards and second-yellow-card reds were pooled into a single binary red-card outcome
  - why: claim says direct reds and second-yellow reds were pooled, but code derives redCard_any solely from the redCards column (>0) with no yellowReds included

## All decisions

- `20-22` [high] **linked x3** — read the raw player-referee dyad dataset from CSV as the analysis population/source
- `25-27` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `28-30` [high] **linked x1** — drop dyads missing either rater's skin-tone score before deriving categories
- `40-48` [high] **linked x3** — bin continuous skinTone into light/medium/dark groups using cutpoints 0.25 and 0.75
- `52-54` [high] **linked x2** — drop the medium skin-tone group, restricting the analytic sample to light vs dark only
- `60-62` [high] **linked x3** — collapse red card counts into a binary any-red-card outcome using a >0 threshold
- `63-65` [high] **linked x1** — recode the skin-tone category into a binary dark-vs-light exposure indicator
- `70-74` [medium] **SILENT** — choose which columns (outcome, exposure, covariates, IDs) are carried into the regression dataset
- `79-80` [high] **linked x4** — drop any remaining rows with missing values on the selected regression variables
- `86-88` [high] **linked x3** — log-transform games count (with +1 offset) to use as an exposure control
- `97-102` [medium] **linked x2** — compute the unadjusted red-card rate for each skin-tone group as the naive/crude comparison
- `116-118, 157-159` [high] **linked x7** — pick the covariate adjustment set (player position, league country, log-games) applied to both the primary and secondary models
- `119-121, 194` [high] **linked x4** — model the binary outcome with a linear probability (OLS) specification rather than a nonlinear link
- `122-126, 163-165, 195-197` [high] **linked x4** — cluster standard errors by player to account for repeated dyads per player
- `132-137, 171-177, 201-204` [medium] **SILENT** — derive p-values and 95% confidence intervals via a normal-approximation (Wald) z-test with cluster-robust SEs
- `138-142` [low] **linked x2** — rescale the linear-probability coefficient and CI from proportions to percentage points for reporting
- `160-162` [high] **linked x5** — fit a separate logistic-regression specification as a secondary/robustness check on the same outcome
- `191-193` [high] **linked x3** — extend the model with referee implicit/explicit bias measures as an added sensitivity specification
- `234-237` [high] **linked x4** — declare the hypothesis supported or not using a p<0.05 significance threshold on the primary estimate
