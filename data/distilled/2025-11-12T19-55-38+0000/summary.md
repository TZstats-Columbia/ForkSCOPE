# 2025-11-12T19-55-38+0000  (ai)

- code: 444 lines, 38% exon (168 lines in 20 decisions)
- intron: print 134, plot 63, comment 60, import 7, glue 7, config 5
- prose: 295 lines, 95 claims (34 action, 61 result)
- links: 61 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 5
- result_claims_deferred: 61

## Silent decisions — executed, never disclosed

- **33** [medium] load the raw player-referee dyad soccer dataset from CSV
- **83-85** [high] encode dark-skin group membership as a binary exposure variable
- **92-95** [high] select and restrict the columns carried into the modeling dataset

## All decisions

- `33` [medium] **SILENT** — load the raw player-referee dyad soccer dataset from CSV
- `35-37` [high] **linked x1** — average the two independent raters' scores into one continuous skinTone measure
- `43-51, 55-56` [high] **linked x5** — define Light/Dark skin tone groups using 0.25/0.75 cutoffs on the averaged rating and drop the excluded middle range from the analysis sample
- `52-54` [high] **linked x1** — flag any dyad that received a red card as a binary outcome
- `64-67` [high] **linked x1** — compute player age at the fixed 2012 reference year from parsed birthdate
- `68-82` [high] **linked x1** — bucket free-text player positions into Defensive/Goalkeeper/Attacking/Midfield/Missing categories
- `83-85` [high] **SILENT** — encode dark-skin group membership as a binary exposure variable
- `92-95` [high] **SILENT** — select and restrict the columns carried into the modeling dataset
- `96-98` [high] **linked x1** — drop dyads with missing position category from the model dataset
- `99-102` [high] **linked x2** — one-hot encode position and league category with the first level dropped as reference
- `122-132` [high] **linked x1** — compute the unadjusted risk difference between groups with a normal-approximation SE, z-test, and 95% Wald confidence interval
- `147-150` [high] **linked x6** — specify the covariate/adjustment set for the outcome regression model
- `155-161` [high] **linked x12** — fit a logistic regression model with cluster-robust standard errors clustered by player
- `174, 176-190` [high] **linked x8** — estimate the adjusted risk difference via marginal standardization: predict outcomes under counterfactual all-dark vs all-light exposure and average the predicted probabilities
- `195-196, 198-237` [medium] **linked x5** — obtain the CI and p-value for the adjusted risk difference via a parametric bootstrap that resamples the darkSkin coefficient from its asymptotic normal distribution, holding other coefficients fixed, and takes the 2.5/97.5 percentiles
- `253-256` [high] **linked x5** — report the secondary estimand as an adjusted odds ratio with model-based Wald confidence interval and p-value
- `283-290` [high] **linked x4** — sensitivity check restricting the comparison to only the most extreme skin tone ratings (0 vs 1)
- `295-301` [high] **linked x4** — sensitivity check using a median split of skin tone instead of the 0.25/0.75 cutoffs
- `311-319` [medium] **linked x2** — recompute the unadjusted risk difference within each league subgroup
- `327-335` [medium] **linked x2** — recompute the unadjusted risk difference within each position subgroup
