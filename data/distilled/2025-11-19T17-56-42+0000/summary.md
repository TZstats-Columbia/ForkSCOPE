# 2025-11-19T17-56-42+0000  (ai)

- code: 274 lines, 45% exon (123 lines in 22 decisions)
- intron: print 103, comment 36, import 8, config 2, glue 2
- prose: 244 lines, 87 claims (32 action, 55 result)
- links: 49 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 4
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 11
- result_claims_deferred: 55

## Silent decisions — executed, never disclosed

- **83-99, 198** [high] bucket free-text position strings into Goalkeeper/Defender/Midfielder/Forward/Unknown via keyword matching
- **109-111, 205** [high] one-hot encode position and league categories keeping all levels (no reference level dropped)
- **196-197** [high] build a separate sample for the continuous-exposure check using all rows with a non-missing skin-tone score, not just the dichotomized dark/light rows
- **215-218** [medium] pull the skin-tone marginal effect out of the margeff array by a hard-coded position index

## All decisions

- `31-32` [high] **linked x2** — pick the source CSV file that defines the entire analysis dataset
- `35-36` [high] **linked x1** — collapse two raters' scores into a single skin-tone measure by averaging
- `37-39` [low] **linked x2** — restrict to dyads with both ratings present before computing rater agreement
- `42-46, 50-52` [high] **linked x6** — cut the continuous skin-tone score into dark/light groups at fixed thresholds, leaving the middle band unclassified and dropping it from the working sample
- `47-49` [high] **linked x1** — collapse the red-card count/type into a single yes/no outcome for any red card
- `68-70` [medium] **linked x3** — split the analysis sample into dark/light groups to report a raw, pre-adjustment comparison
- `83-99, 198` [high] **SILENT** — bucket free-text position strings into Goalkeeper/Defender/Midfielder/Forward/Unknown via keyword matching
- `100-103, 199-200` [high] **linked x2** — fill missing height and weight with the sample mean rather than dropping or modeling missingness
- `104-108, 202-204` [high] **linked x1** — z-score height, weight, and games so covariates are on comparable scales
- `109-111, 205` [high] **SILENT** — one-hot encode position and league categories keeping all levels (no reference level dropped)
- `121-124, 206-210` [high] **linked x3** — choose the adjustment set of covariates (position, league, height, weight, games) accompanying the exposure in the outcome model
- `125-128` [high] **linked x4** — fit a logistic regression as the outcome model with standard errors clustered by player
- `133-138` [high] **linked x5** — report the average marginal effect (risk-difference scale) rather than the raw log-odds coefficient as the headline estimand
- `148-153` [medium] **linked x2** — additionally exponentiate the coefficient into an odds ratio as a secondary summary
- `170-177` [high] **linked x5** — refit with standard errors clustered by referee instead of player as a sensitivity check
- `184-189` [high] **linked x2** — refit with heteroskedasticity-robust (HC1) errors and no clustering as a further sensitivity check
- `196-197` [high] **SILENT** — build a separate sample for the continuous-exposure check using all rows with a non-missing skin-tone score, not just the dichotomized dark/light rows
- `201` [high] **linked x1** — standardize the continuous skin-tone score for use as a continuous exposure
- `211-214` [high] **linked x4** — refit the outcome model using the continuous skin-tone exposure in place of the binary one, still clustered by player
- `215-218` [medium] **SILENT** — pull the skin-tone marginal effect out of the margeff array by a hard-coded position index
- `219-225` [high] **linked x1** — rescale the continuous marginal effect into a dark-vs-light comparison by picking 0.875 and 0.125 as the representative contrast values
- `261-269` [high] **linked x4** — declare the hypothesis supported or not using a rule requiring both p>0.05 and a CI lower bound below zero, and label the outcome accordingly
