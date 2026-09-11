# 2025-11-22T14-57-09+0000  (ai)

- code: 350 lines, 38% exon (134 lines in 16 decisions)
- intron: print 128, comment 59, import 14, glue 11, config 4
- prose: 234 lines, 64 claims (23 action, 41 result)
- links: 33 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 2
- R_only_consistent_negative: 4
- result_claims_deferred: 41

## Silent decisions — executed, never disclosed

- **58-62** [high] derive player age from birthday relative to a chosen 2012-10-01 season-midpoint reference date, coercing unparseable birthdates to missing
- **106-111** [medium] compute the unadjusted (crude) red-card rate per game separately for the dark and light skin-tone groups as a raw comparison
- **333-341** [high] populate the final results summary table with fixed literal IRR/CI/p-value numbers rather than the values computed earlier in the script

## All decisions

- `43-45` [medium] **linked x1** — load the player-referee dyad dataset from a fixed CSV file, fixing the data source and scope for the whole analysis
- `47-49` [high] **linked x1** — average the two raters' skin-tone scores into one continuous skin_tone variable
- `50-53` [medium] **linked x1** — restrict to dyads with both ratings present and quantify rater agreement via Spearman correlation
- `55-57` [high] **linked x1** — dichotomize skin tone into dark vs light exposure groups at a 0.5 cutoff
- `58-62` [high] **SILENT** — derive player age from birthday relative to a chosen 2012-10-01 season-midpoint reference date, coercing unparseable birthdates to missing
- `71-73, 75-80` [high] **linked x4** — restrict the analysis sample to complete cases with non-missing skin tone, position, height, and weight
- `106-111` [medium] **SILENT** — compute the unadjusted (crude) red-card rate per game separately for the dark and light skin-tone groups as a raw comparison
- `124-127, 137-139, 267-268` [high] **linked x3** — model red-card counts with a Poisson GLM using log(games) as an offset, so the model targets a per-game rate rather than a raw count; reused for the main fit, its refit, and each league-specific fit
- `131-133, 263-266` [high] **linked x3** — choose the model's adjustment set: dark_binary plus height, weight, age, categorical position, and (except when stratifying by league) categorical league country
- `153-172` [high] **linked x4** — combine player-clustered and referee-clustered sandwich covariances (minus an HC1 covariance) into a two-way (player + referee) clustered standard error
- `179-184` [high] **linked x1** — compute a Wald-style z statistic, p-value, and 95% CI for the dark_binary coefficient using a normal approximation with the two-way clustered SE
- `197-224` [high] **linked x4** — estimate the adjusted risk difference as an average marginal effect via counterfactual substitution (predict each dyad's rate under both exposure values and average the difference), with SE via the delta method
- `239-243, 269-276` [high] **linked x6** — express the exposure effect as an incidence rate ratio by exponentiating the Poisson coefficient and its CI bounds, both overall and per league
- `258-262` [low] **linked x2** — stratify the sensitivity analysis into four named leagues (England, France, Germany, Spain) and subset the data for each
- `317-318, 320, 323` [high] **linked x2** — declare the finding 'supported' only when p<0.05 and the risk-difference CI excludes zero, otherwise 'not supported'/'inconclusive'
- `333-341` [high] **SILENT** — populate the final results summary table with fixed literal IRR/CI/p-value numbers rather than the values computed earlier in the script
