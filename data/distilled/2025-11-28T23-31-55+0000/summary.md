# 2025-11-28T23-31-55+0000  (ai)

- code: 291 lines, 50% exon (145 lines in 16 decisions)
- intron: print 105, comment 31, import 5, config 5
- prose: 256 lines, 91 claims (43 action, 48 result)
- links: 44 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 11
- result_claims_deferred: 48

## Silent decisions — executed, never disclosed

- **46-55** [high] derive player age from birthday using a fixed 2012 reference year, falling back to NaN on parse failure
- **241-244** [high] refit with minimal adjustment, dropping all covariates except log_games
- **256-259, 266-268** [high] rebuild and refit the model on the full sample including goalkeepers instead of the goalkeeper-excluded sample

## All decisions

- `29-30` [high] **linked x2** — load the raw player-referee dyad dataset from CSV as the analysis universe
- `34-36` [high] **linked x2** — drop dyads missing either rater's skin-tone score
- `40-42` [high] **linked x1** — average the two raters' skin-tone scores into one continuous skinTone measure
- `43-45` [high] **linked x1** — collapse red card count into a binary any-red-card outcome
- `46-55` [high] **SILENT** — derive player age from birthday using a fixed 2012 reference year, falling back to NaN on parse failure
- `56-60` [high] **linked x2** — drop dyads missing height or weight
- `63-81` [high] **linked x2** — collapse detailed playing positions into four categories and drop goalkeepers from the analysis sample
- `88-89, 93-102, 103-106, 260` [high] **linked x11** — search several skin-tone cutpoints and select the one (0.25) that maximizes the unadjusted effect, then apply it to build the darkSkin indicator (including in the full-sample sensitivity dataset)
- `115-116, 261` [high] **linked x2** — log-transform games played with a 0.5 offset as the exposure/control variable
- `117-121, 262-265` [high] **linked x4** — z-standardize age, height, and weight before entering them as covariates
- `146-153` [high] **linked x5** — fit a logistic regression of any red card on darkSkin adjusting for log games, age, height, weight, and league country
- `157-168, 169-173, 213-218, 230-235, 245-250, 269-274` [high] **linked x10** — summarize each fitted model's darkSkin effect as an average marginal (risk) difference via dydx and as an odds ratio exponentiating the coefficient
- `207-212` [high] **linked x1** — refit the model with an alternative skin-tone cutpoint of 0.5 instead of 0.25
- `225-229` [high] **linked x1** — refit the model adding position category as an additional covariate
- `241-244` [high] **SILENT** — refit with minimal adjustment, dropping all covariates except log_games
- `256-259, 266-268` [high] **SILENT** — rebuild and refit the model on the full sample including goalkeepers instead of the goalkeeper-excluded sample
