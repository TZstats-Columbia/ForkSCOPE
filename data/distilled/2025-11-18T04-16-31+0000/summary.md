# 2025-11-18T04-16-31+0000  (ai)

- code: 334 lines, 40% exon (132 lines in 22 decisions)
- intron: print 81, comment 51, plot 38, glue 19, import 9, config 4
- prose: 329 lines, 117 claims (34 action, 83 result)
- links: 67 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 22
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 3
- R_only_consistent_negative: 6
- result_claims_deferred: 83

## All decisions

- `34` [high] **linked x2** — pull in the full soccer dyad dataset from a fixed CSV path as the analysis universe
- `36-38` [high] **linked x2** — collapse two raters' skin-tone codings into a single continuous score by averaging them
- `39-41` [high] **linked x4** — collapse the red-card count into a yes/no outcome for whether a player was ever sent off
- `42-49, 93-95, 302-305` [high] **linked x2** — carve the continuous skin-tone score into light/middle/dark buckets at the 0.25/0.75 cutoffs, then recode dark vs light into the 0/1 exposure used everywhere downstream, and mark those same cutoffs on the distribution plot
- `50-52` [high] **linked x2** — drop every dyad whose skin tone lands in the excluded 'middle' bucket, keeping only clear light/dark players
- `58-74` [high] **linked x1** — fold dozens of free-text position labels down into four coarse role buckets via keyword matching
- `80-86` [high] **linked x1** — settle on the covariate/adjustment set carried into the model (games, position, height, weight, league, cards, goals, plus id fields) and subset the frame to just those columns
- `87-89` [high] **linked x2** — require complete height and weight data, discarding any dyad missing either
- `90` [high] **linked x1** — exclude players whose position couldn't be classified into one of the four buckets
- `96-102` [high] **linked x2** — z-score the continuous covariates so their regression coefficients are on a comparable scale
- `124-128` [medium] **linked x2** — compute the raw, unadjusted gap in red-card rates between dark- and light-skinned players as a naive baseline comparison
- `134-137` [high] **linked x2** — pick a chi-square test of independence to judge whether the unadjusted skin-tone/red-card association is real
- `145-147` [high] **linked x1** — fix the regression formula that defines the adjustment set and functional form used for both the primary and secondary models
- `148-152` [high] **linked x11** — commit to a linear probability model as the primary estimator, with standard errors clustered on player to handle repeated dyads
- `165, 194` [medium] **linked x2** — adopt a 0.05 alpha cutoff to label the LPM and logit effects as statistically significant or not
- `172-177` [high] **linked x6** — refit the same specification as a logistic regression (again cluster-robust on player) as a secondary check on the LPM
- `184-188` [medium] **linked x6** — convert the logit coefficient and its interval onto the odds-ratio scale for reporting
- `195-206` [high] **linked x3** — get a marginal risk-difference estimate off the logit model by predicting every dyad twice under forced dark/light exposure and averaging the gap
- `217-220` [medium] **linked x2** — check the LPM for the classic linear-probability failure mode of predictions falling outside 0-1
- `222-234` [high] **linked x2** — screen the model's covariates for multicollinearity using variance inflation factors
- `241-248` [high] **linked x3** — rerun the LPM on the subset of dyads whose predicted probabilities stayed within bounds, as a robustness check on the main estimate
- `274-278` [low] **linked x8** — declare the hypothesis unsupported based on the effect size, its significance, and the CI crossing zero
