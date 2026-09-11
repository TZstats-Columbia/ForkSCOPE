# 2025-11-17T14-46-19+0000  (ai)

- code: 310 lines, 35% exon (108 lines in 16 decisions)
- intron: print 110, comment 37, plot 32, glue 8, other 7, import 5, config 3
- prose: 180 lines, 87 claims (38 action, 49 result)
- links: 46 (3 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 8
- result_claims_deferred: 49

## Silent decisions — executed, never disclosed

- **22-24** [high] load the player-referee dyad dataset from a fixed CSV path as the entire analysis input
- **266-268** [medium] bin the continuous skin-tone score into 9 groups to plot red-card rate against tone

## Misaligned — code and prose disagree

- code: bucket free-text position strings into five keyword-matched categories
  - prose: included player position, collapsed into 4 categories, as a covariate
  - why: code buckets positions into five keyword-matched categories; claim says four
- code: bucket free-text position strings into five keyword-matched categories
  - prose: aggregated 12 detailed positions into 4 broad position categories
  - why: code buckets positions into five categories; claim says twelve positions aggregated into four
- code: bucket free-text position strings into five keyword-matched categories
  - prose: collapsed player positions into 4 broad categories
  - why: code creates five position categories; claim says four

## All decisions

- `22-24` [high] **SILENT** — load the player-referee dyad dataset from a fixed CSV path as the entire analysis input
- `30-31` [high] **linked x1** — average the two raters' skin-tone scores into one continuous rating
- `34-36` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `37-54` [high] **linked x3** — bucket free-text position strings into five keyword-matched categories
- `55-60` [high] **linked x6** — restrict the working sample to rows with known skin tone and known position
- `61-63, 258` [high] **linked x3** — dichotomize the continuous skin-tone score at a 0.5 cutoff into dark vs. light groups
- `96, 99-100, 104-105` [low] **linked x1** — cross-tabulate skin-tone group against position and league to check covariate balance
- `116-118` [high] **linked x8** — specify the adjusted logistic regression formula: skin-tone exposure plus games, position, league, and yellow cards as covariates
- `119, 126-131` [high] **linked x4** — fit the primary logistic regression with standard errors clustered by player
- `144-154` [high] **linked x5** — compute the average marginal effect (risk difference) of skin tone as the primary estimand via overall dy/dx margins
- `170-173` [high] **linked x4** — exponentiate the logistic coefficient and its CI to report an adjusted odds ratio as a secondary estimand
- `186, 188-195` [high] **linked x2** — refit the same model clustering standard errors by referee instead of player, as a robustness check
- `200, 202-210` [high] **linked x2** — re-specify the exposure as continuous skin tone instead of the binary cutoff, as a robustness check
- `215, 217-220, 223-230` [high] **linked x1** — restrict the robustness sample to only the most extreme skin-tone scores (0.0 vs 1.0) and refit the model on that subset
- `266-268` [medium] **SILENT** — bin the continuous skin-tone score into 9 groups to plot red-card rate against tone
- `302-308` [high] **linked x4** — declare the hypothesis supported/not supported based on a p<0.05 threshold and whether the risk-difference CI excludes zero
