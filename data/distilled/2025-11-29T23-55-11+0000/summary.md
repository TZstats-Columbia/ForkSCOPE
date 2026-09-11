# 2025-11-29T23-55-11+0000  (ai)

- code: 393 lines, 40% exon (156 lines in 19 decisions)
- intron: print 130, glue 40, plot 28, comment 18, import 9, other 7, config 5
- prose: 203 lines, 97 claims (59 action, 38 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 18
- result_claims_deferred: 38

## Silent decisions — executed, never disclosed

- **93-97** [medium] compute the unadjusted red-card rate gap between the two extreme groups
- **315-321** [low] bin skin tone into quintiles for the descriptive plot
- **338-339** [low] color-code the effect-size bars by whether p < 0.05

## All decisions

- `30-31` [high] **linked x2** — load the raw player-referee dyad dataset from the given CSV path
- `39-41` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `42-44` [high] **linked x1** — collapse red-card counts into a binary any-red-card outcome
- `45-48` [low] **linked x1** — assess inter-rater agreement on skin tone via correlation on non-missing pairs
- `50-52` [high] **linked x4** — restrict to complete cases with a non-missing skin-tone rating
- `65-66, 69-73` [high] **linked x4** — z-standardize continuous covariates and fill missing height/weight with 0 after standardizing
- `85-88` [high] **linked x7** — restrict to extreme skin-tone groups (<0.25 vs >0.75) and build the very_dark indicator
- `93-97` [medium] **SILENT** — compute the unadjusted red-card rate gap between the two extreme groups
- `103-108` [high] **linked x4** — specify and fit the primary logistic regression with full covariate adjustment
- `127-129, 197, 208-210, 229, 242` [high] **linked x5** — express the exposure effect as an odds ratio by exponentiating the logistic coefficient
- `143-161, 195-196, 211-216, 227-228, 240-241` [high] **linked x3** — estimate the adjusted risk difference via g-computation/marginal standardization over counterfactual exposure values
- `166-171` [medium] **linked x5** — approximate the standard error and CI of the risk difference with a delta-method formula
- `190-194` [high] **linked x2** — redefine the exposure with an alternative dark-skin cutpoint (>0.625) applied to the full sample
- `205-207` [high] **linked x2** — model skin tone as a continuous exposure instead of a binary group
- `225-226` [high] **linked x2** — exclude goalkeepers from the sample as a robustness check
- `237-239` [high] **linked x3** — refit the model omitting the yellow-card covariate
- `255-305` [medium] **linked x6** — assemble a comparison table of N, OR, OR CI, RD, and p-value across all five specifications
- `315-321` [low] **SILENT** — bin skin tone into quintiles for the descriptive plot
- `338-339` [low] **SILENT** — color-code the effect-size bars by whether p < 0.05
