# 2025-11-22T14-12-20+0000  (ai)

- code: 262 lines, 52% exon (136 lines in 22 decisions)
- intron: print 80, comment 30, import 7, glue 5, config 4
- prose: 256 lines, 124 claims (37 action, 87 result)
- links: 58 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 22
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 9
- result_claims_deferred: 87

## All decisions

- `25-27` [high] **linked x2** — read the raw player-referee dyad csv as the full analysis population
- `29-31` [high] **linked x1** — average the two raters' skin-tone ratings into a single continuous skinTone score
- `32-36` [medium] **linked x2** — quantify inter-rater agreement via Pearson correlation and exact-match rate between the two raters
- `40-42` [high] **linked x1** — drop dyads with no averaged skin-tone score from the analysis population
- `44-51` [high] **linked x1** — bucket continuous skin tone into Light/Medium/Dark categories using 0.25 and 0.5 cut points
- `52-55` [high] **linked x3** — drop the Medium skin-tone group and recode the remaining groups into a binary darkSkin exposure indicator
- `56` [high] **linked x1** — collapse red card counts into a binary any-red-card outcome
- `57-59` [high] **linked x1** — restrict to complete cases by dropping dyads with missing position
- `60` [high] **linked x2** — log-transform games played for use as a model covariate
- `75-82` [high] **linked x4** — compute unadjusted red-card counts and rates separately for the light- and dark-skin groups
- `96-98` [high] **linked x7** — specify the adjusted logistic model formula relating any red card to dark skin, log games, position and league
- `102-107` [high] **linked x4** — fit the logistic model with standard errors clustered by player
- `113-114` [low] **linked x1** — take the model's default 95% confidence interval for the darkSkin coefficient
- `115-120` [medium] **linked x1** — designate the standardized risk difference as the study's primary estimand
- `121-133` [high] **linked x5** — estimate the adjusted risk difference by marginal standardization: predict outcome probability setting darkSkin to 1 and to 0 for every dyad and average the difference
- `138-163` [high] **linked x1** — cluster-bootstrap over players (200 resamples, refitting the logistic model with BFGS) to build an empirical distribution of the risk difference
- `164-165` [low] **linked x4** — take the 2.5th/97.5th percentiles of the bootstrap distribution as the 95% CI for the risk difference
- `170-175` [medium] **linked x3** — designate the adjusted odds ratio as a secondary estimand
- `188-200` [high] **linked x2** — redefine skin-tone exposure as >0.25 vs <=0.25, folding the Medium group into the dark side, and refit the adjusted clustered logistic model on this larger sample
- `206-213` [high] **linked x2** — refit the adjusted clustered logistic model using continuous skinTone instead of a dichotomized exposure
- `219-220, 222-230` [high] **linked x4** — refit the adjusted logistic model separately within each of four selected leagues, dropping league and player clustering from that model
- `244` [high] **linked x6** — declare the hypothesis supported only if p<0.05 and the risk difference is positive
