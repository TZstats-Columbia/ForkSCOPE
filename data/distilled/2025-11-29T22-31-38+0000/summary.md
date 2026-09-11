# 2025-11-29T22-31-38+0000  (ai)

- code: 354 lines, 49% exon (175 lines in 20 decisions)
- intron: print 120, comment 47, import 8, config 4
- prose: 256 lines, 88 claims (54 action, 34 result)
- links: 64 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 14
- result_claims_deferred: 34

## All decisions

- `34-36` [high] **linked x2** — load the player-referee dyad dataset from a fixed CSV path as the entire analytic universe
- `39-42` [high] **linked x2** — average the two raters' independent skin-tone scores into a single continuous skinTone_avg measure
- `43-47` [medium] **linked x2** — quantify rater agreement with a Pearson correlation on dyads where both ratings are present
- `48-53` [high] **linked x5** — drop every dyad lacking a skin-tone rating from the working sample and tally how many were dropped
- `63-67` [high] **linked x6** — dichotomize the continuous skin-tone score at 0.25 into a dark_skin indicator
- `68-70` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `71-73` [high] **linked x3** — log-transform games played to serve as an exposure-opportunity covariate
- `74-91` [high] **linked x2** — bucket free-text position strings into five coarse role categories by keyword matching and apply it to every player
- `123-132` [high] **linked x7** — fit a logistic regression of any-red-card on the dark-skin indicator, adjusting for position, league country and log(games)
- `151-170, 171-172` [high] **linked x5** — standardize the fitted model by predicting outcomes under exposure fixed to 0 and to 1 for everyone, then difference the averaged predictions to get an adjusted risk difference
- `185-208, 209-210` [high] **linked x4** — resample dyads with replacement 200 times, refit the model on each replicate, and collect the resulting risk differences
- `211-215` [high] **linked x2** — take the 2.5th/97.5th percentiles of the bootstrap distribution as a 95% confidence interval
- `221-224` [high] **linked x3** — derive a two-sided p-value from a Wald z-statistic built from the point estimate and bootstrap standard error
- `232-236` [high] **linked x5** — exponentiate the model's dark-skin coefficient and its Wald confidence bounds to report as an odds ratio
- `249-254, 255-260` [high] **linked x2** — redefine the dark-skin cutoff at 0.375 instead of 0.25, refit the adjusted model, and recompute the standardized risk difference
- `265-269, 270-275` [high] **linked x2** — swap the binarized exposure for the raw continuous skin-tone score and recompute the standardized 0-to-1 risk difference
- `280-284` [high] **linked x2** — switch the outcome and model family to a Poisson regression on the raw red-card count with games as an offset
- `288-295` [high] **linked x3** — refit the primary model with standard errors clustered on player identity instead of the default
- `300-307` [high] **linked x3** — refit the primary model with standard errors clustered on referee identity instead of on player
- `338-349` [high] **linked x3** — declare the hypothesis supported only when the p-value is below 0.05 and the risk difference is positive, otherwise not supported
