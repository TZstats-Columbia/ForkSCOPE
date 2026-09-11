# 2025-11-22T12-45-22+0000  (ai)

- code: 310 lines, 48% exon (150 lines in 23 decisions)
- intron: print 113, comment 35, import 8, config 4
- prose: 300 lines, 87 claims (36 action, 51 result)
- links: 38 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 5
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 4
- result_claims_deferred: 51

## Silent decisions — executed, never disclosed

- **28** [high] load the raw player-referee dyad dataset from CSV as the analysis starting point
- **54** [high] recode skin_group into a binary is_dark exposure indicator with Light as the reference level
- **77-78** [low] strip spaces from column names before building model formulas
- **179-180** [medium] discard bootstrap resamples with fewer than 10 dyads in either exposure group as too imbalanced to fit
- **261** [high] switch to HC1 heteroskedasticity-robust SEs instead of player-clustered SEs for the single-game-excluded model

## All decisions

- `28` [high] **SILENT** — load the raw player-referee dyad dataset from CSV as the analysis starting point
- `30-32` [high] **linked x1** — average the two raters' skin-tone scores into a single skin_tone measure
- `33-35` [high] **linked x1** — drop rows lacking a skin_tone rating before further analysis
- `37-44` [high] **linked x2** — bucket skin_tone into Light (<=0.25) and Dark (>=0.50) groups, leaving the 0.25-0.50 band unlabeled
- `45-47` [high] **linked x2** — drop dyads whose skin_group wasn't classified, forming the analytic sample
- `52-53` [high] **linked x1** — collapse redCards into a binary any-red-card outcome (count>0) rather than modeling card counts
- `54` [high] **SILENT** — recode skin_group into a binary is_dark exposure indicator with Light as the reference level
- `55` [medium] **linked x2** — log-transform games played to use as an exposure-adjustment covariate
- `77-78` [low] **SILENT** — strip spaces from column names before building model formulas
- `79-89` [high] **linked x1** — one-hot encode position and leagueCountry, dropping the first level as reference category
- `90-92` [high] **linked x2** — restrict the modeling sample to complete cases on height and weight, ignoring missingness elsewhere
- `100-113` [high] **linked x5** — specify and fit the primary adjusted logistic regression of any_red_card on is_dark plus exposure, physical, style, position and league covariates, with SEs clustered by player
- `124-127` [high] **linked x4** — convert the is_dark coefficient to an odds ratio with a normal-approximation (1.96 SE) Wald confidence interval
- `137-150` [high] **linked x4** — estimate the adjusted risk difference via marginal standardization: predict outcomes under counterfactual all-dark and all-light exposure and difference the mean predicted probabilities
- `160-178, 181-197` [high] **linked x2** — cluster-bootstrap by resampling players (not dyads) 500 times and refitting the logistic model on each resample without cluster-robust SEs (maxiter capped at 50) to build a sampling distribution for the risk difference
- `179-180` [medium] **SILENT** — discard bootstrap resamples with fewer than 10 dyads in either exposure group as too imbalanced to fit
- `199-203` [high] **linked x2** — derive the bootstrap 95% CI and SE from the 2.5th/97.5th percentiles of the resampled risk differences
- `208-210` [high] **linked x1** — compute a two-sided bootstrap p-value from the proportion of resampled effects crossing zero
- `217-218, 220-230` [high] **linked x2** — refit the primary-style model using continuous skin_tone instead of the binary group, as a sensitivity check
- `236, 238-251` [high] **linked x2** — restrict to the most extreme skin tones (0 vs 1.0) and refit the model on that subsample as a sensitivity check
- `257-258, 260` [high] **linked x2** — exclude player-referee dyads with only a single game as a sensitivity check
- `261` [high] **SILENT** — switch to HC1 heteroskedasticity-robust SEs instead of player-clustered SEs for the single-game-excluded model
- `301, 306` [high] **linked x2** — declare the hypothesis 'supported' using the joint criterion p<0.05 and bootstrap CI lower bound above zero
