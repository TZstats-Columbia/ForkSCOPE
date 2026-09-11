# 2025-11-12T09-30-16+0000  (ai)

- code: 349 lines, 48% exon (166 lines in 23 decisions)
- intron: print 112, comment 56, import 9, config 3, glue 3
- prose: 308 lines, 87 claims (36 action, 51 result)
- links: 81 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 7
- result_claims_deferred: 51

## Silent decisions — executed, never disclosed

- **32-33** [medium] load the full soccer referee-player dyad dataset from a fixed CSV path with no additional row-level scope restriction
- **189-191** [medium] discard bootstrap draws whose resampled dataset has fewer than 1000 rows
- **192-205, 212-214** [high] rebuild the covariate design matrix for each bootstrap draw and refit the logistic GLM with a plain (non-cluster-robust) fit, silently skipping draws whose fit raises an exception

## All decisions

- `32-33` [medium] **SILENT** — load the full soccer referee-player dyad dataset from a fixed CSV path with no additional row-level scope restriction
- `44-48` [high] **linked x1** — restrict to dyads with both rater scores present and quantify inter-rater agreement via Pearson and Spearman correlation
- `54-56` [high] **linked x2** — average rater1 and rater2 into a single continuous skinTone score
- `57-59` [high] **linked x1** — drop dyads with missing skinTone, defining the complete-case exposure sample
- `61-63` [high] **linked x2** — collapse red card count into a binary any-red-card outcome, discarding count/severity information
- `64-66` [high] **linked x3** — dichotomize continuous skin tone into dark vs light using a strict >0.5 cut point
- `78-83` [high] **linked x5** — restrict the working table to a fixed set of columns and drop any remaining rows with missing values on them, defining the final analytic cohort
- `98-102` [medium] **linked x6** — compute descriptive aggregates (red card sum/mean, games sum/mean, unique player count) grouped by darkSkin
- `104-107` [high] **linked x2** — compute the unadjusted (crude) risk difference between dark- and light-skin groups
- `118-121` [high] **linked x2** — one-hot encode position and leagueCountry as dummy variables, dropping the first category as reference
- `122-128` [high] **linked x3** — assemble the adjustment set for the primary model from darkSkin, games, height, weight plus the position/league dummies
- `132-136` [high] **linked x6** — fit a binomial GLM (logistic regression) for anyRedCard with cluster-robust standard errors clustered on player
- `139-143` [high] **linked x5** — exponentiate the darkSkin coefficient and its Wald CI to report an adjusted odds ratio as the secondary estimand
- `158-170, 206-211` [high] **linked x7** — estimate the risk-difference estimand via marginal standardization / g-formula: set darkSkin to 1 and 0 for the whole sample (or bootstrap sample), predict outcome probabilities from the fitted model, and average the contrast
- `178-188` [high] **linked x2** — set up and run a cluster bootstrap over players: 1000 iterations resampling players with replacement and reconstructing the dyad-level sample from resampled players
- `189-191` [medium] **SILENT** — discard bootstrap draws whose resampled dataset has fewer than 1000 rows
- `192-205, 212-214` [high] **SILENT** — rebuild the covariate design matrix for each bootstrap draw and refit the logistic GLM with a plain (non-cluster-robust) fit, silently skipping draws whose fit raises an exception
- `215-219` [high] **linked x7** — form the bootstrap CI from the 2.5/97.5 percentiles of the bootstrap risk-difference distribution and derive a two-sided p-value from the share of draws on each side of zero
- `237-251` [high] **linked x4** — sensitivity check redefining the exposure threshold as skin tone >=0.5 instead of >0.5 and refitting the same adjusted cluster-robust logistic model
- `257-269` [high] **linked x4** — sensitivity check using continuous skinTone as the exposure instead of a binary cut, scaling the reported odds ratio to a 0.5-unit increase
- `275-291` [high] **linked x6** — sensitivity check expanding the adjustment set with referee-country fixed effects
- `301-308` [high] **linked x7** — compute Cohen's h effect size from the crude group proportions and bucket it into negligible/small/medium/large using fixed cutoffs (0.2/0.5/0.8)
- `342-344` [medium] **linked x6** — declare the hypothesis 'not supported' by applying a 0.05 significance threshold to the bootstrap p-value
