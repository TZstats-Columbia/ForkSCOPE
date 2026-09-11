# 2025-11-22T04-54-12+0000  (ai)

- code: 297 lines, 27% exon (80 lines in 22 decisions)
- intron: print 96, comment 90, glue 17, import 11, config 3
- prose: 283 lines, 96 claims (50 action, 46 result)
- links: 66 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 22
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 10
- result_claims_deferred: 46

## Misaligned — code and prose disagree

- code: refit the model clustering standard errors by referee instead of by player, as a robustness check
  - prose: the analysis does not account for correlation within referees
  - why: decision 66 refits standard errors clustered by referee, which does account for within-referee correlation, contradicting the claim that the analysis does not account for it

## All decisions

- `34` [high] **linked x3** — load the player-referee dyad dataset from a single fixed file path with no row filtering at read time
- `49` [high] **linked x3** — average the two raters' ratings into a single continuous skin-tone score
- `52` [high] **linked x3** — collapse red-card counts into a binary any-red-card outcome
- `66` [medium] **linked x2** — drop dyads with missing skin-tone rating before forming comparison groups
- `67-69` [high] **linked x3** — cut continuous skin tone into Light/Medium/Dark categories at fixed thresholds 0.25 and 0.5
- `72-73` [high] **linked x3** — discard the Medium skin-tone group and recode the remaining Light/Dark categories into a binary dark_skin exposure
- `80-82` [medium] **linked x1** — compute the crude group-mean red-card-rate difference between dark and light skin groups, unadjusted for covariates
- `97-111` [high] **linked x1** — collapse raw player position strings into four coarse role categories (plus Unknown) and apply that mapping to every row
- `114` [medium] **linked x2** — log1p-transform the games-played count
- `115-116` [medium] **linked x3** — z-score standardize height and weight
- `119-125` [high] **linked x5** — restrict the sample to complete cases on position category, height, weight, and meanIAT, excluding rows tagged Unknown position
- `140-142` [high] **linked x2** — one-hot encode position_cat and leagueCountry, dropping the first level of each as reference category
- `145-149` [high] **linked x3** — choose the adjustment set of covariates entered into the outcome model
- `155-156` [medium] **linked x2** — define player identity as the clustering unit for standard errors
- `157-159` [high] **linked x5** — fit the primary outcome model as an OLS linear probability model with player-clustered robust standard errors
- `178, 291-292` [medium] **linked x5** — treat p<0.05 as the cutoff for declaring the primary effect statistically significant and the hypothesis supported
- `188-191` [high] **linked x5** — fit a secondary logistic regression model, using the same covariates and player clustering, in place of the linear probability model
- `218-221` [low] **linked x1** — run a diagnostic checking whether the linear probability model's fitted probabilities fall outside [0,1]
- `224-229` [medium] **linked x1** — compute variance inflation factors on the non-constant predictors to screen for multicollinearity
- `239-240` [high] **linked x4** — refit the model clustering standard errors by referee instead of by player, as a robustness check
- `248-250` [high] **linked x4** — refit the model with no covariates besides dark_skin, as an unadjusted robustness comparison
- `259-266` [high] **linked x5** — stratify the crude risk-difference estimate by league country, restricted to England/France/Germany/Spain
