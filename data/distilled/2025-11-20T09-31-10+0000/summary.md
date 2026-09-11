# 2025-11-20T09-31-10+0000  (ai)

- code: 309 lines, 45% exon (139 lines in 16 decisions)
- intron: print 115, comment 44, import 6, config 5
- prose: 241 lines, 114 claims (44 action, 70 result)
- links: 64 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 10
- result_claims_deferred: 70

## All decisions

- `23-24` [high] **linked x1** — read the raw player-referee dyad dataset from the soccer CSV file, fixing the data source and scope of the whole analysis
- `28-30` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skin_avg measure
- `31-33` [high] **linked x2** — drop dyads lacking a skin-tone rating, restricting the analytic population to rated players only
- `36-37` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome
- `38-53, 54-55` [high] **linked x1** — bucket free-text player position strings into five coarse categories, with an Unknown catch-all
- `61-63` [high] **linked x7** — set the dark-skin exposure cutoff at skin_avg >= 0.25, splitting players into light vs dark groups
- `72-76` [high] **linked x4** — choose which variables enter the model and require complete cases on them, dropping dyads with any missing covariate
- `90-91, 94-96` [medium] **linked x3** — compute unadjusted red-card rates per skin-tone group and the raw (unadjusted) risk difference as a descriptive comparison
- `108-115` [high] **linked x7** — pick the primary logistic regression's adjustment set (games, height, weight, position category, league country) and fit the model
- `121-129` [high] **linked x9** — convert the dark_skin coefficient into an odds ratio with a normal-approximation 95% CI, framed as the secondary estimand
- `146-158` [high] **linked x7** — standardize predicted red-card probabilities by setting everyone's exposure to dark vs light and differencing the averaged model predictions (g-computation), yielding the primary risk-difference estimand
- `162-165, 168-193, 194-198` [high] **linked x8** — derive the risk difference's confidence interval via a 500-draw parametric bootstrap over the model's coefficient covariance, rebuilding predictions from the design matrix and taking 2.5/97.5 percentiles
- `216-229` [high] **linked x3** — refit the primary model under two alternative dark-skin thresholds (0.375 and 0.125) as a sensitivity check on the exposure cutoff
- `238-243` [high] **linked x3** — refit the model adding yellowCards as a covariate, testing sensitivity to adjusting for a possible mediator
- `251-256` [high] **linked x3** — refit the model using skin_avg as a continuous predictor instead of the binarized dark_skin indicator
- `295-301` [high] **linked x3** — declare the hypothesis 'supported' based on whether the bootstrap CI lower bound for the risk difference exceeds zero
