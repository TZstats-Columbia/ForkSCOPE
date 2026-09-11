# 2025-11-15T23-57-58+0000  (ai)

- code: 399 lines, 30% exon (120 lines in 23 decisions)
- intron: print 126, comment 86, plot 51, import 8, config 5, glue 3
- prose: 276 lines, 120 claims (47 action, 73 result)
- links: 56 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 16
- result_claims_deferred: 73

## Silent decisions — executed, never disclosed

- **332-333** [medium] compute normal-approximation (Wald) confidence intervals for the odds ratios from their log-scale standard errors, for the forest-style comparison plot
- **351** [medium] restrict the position-distribution panel to the 8 most common positions rather than showing all categories

## All decisions

- `27` [high] **linked x1** — read the raw player-referee dyad-level CSV file as the input dataset
- `37` [high] **linked x1** — average the two raters' skin-tone ratings into a single continuous skin_tone score
- `40-41` [medium] **linked x2** — compute Pearson correlation between the two raters to assess inter-rater reliability
- `47-49` [high] **linked x2** — bucket the continuous skin_tone score into light/medium/dark categories using 0.25 and 0.75 cutoffs
- `57` [high] **linked x1** — drop medium-toned dyads, keeping only light and dark extremes for the primary analysis
- `64` [high] **linked x3** — collapse the red-card count into a binary any-red-card outcome indicator
- `67` [high] **linked x2** — recode skin category into a binary dark_skin exposure with light skin as the reference group
- `70` [high] **linked x4** — log-transform the games count to use as an adjustment covariate
- `73-77` [high] **linked x3** — restrict the working dataset to a chosen set of columns and drop any row with a missing value among them (complete-case analysis)
- `101-103` [medium] **linked x2** — compute the unadjusted (crude) difference in red-card rates between dark- and light-skin groups
- `116-122` [high] **linked x7** — fit the primary logistic regression of any red card on dark skin, adjusting for log games, position and league country, with standard errors clustered by player
- `131-132` [medium] **linked x6** — exponentiate the logistic coefficient and its confidence interval to express the exposure effect as an odds ratio
- `147-154` [high] **linked x4** — predict outcome probabilities under counterfactual all-light and all-dark exposure scenarios and difference the averages to obtain a covariate-adjusted risk difference (marginal standardization / g-computation)
- `168-199, 202` [high] **linked x1** — resample players with replacement (cluster bootstrap), refit the adjusted model and recompute the marginal-standardized risk difference on each of 200 resamples to build a sampling distribution
- `206-207` [high] **linked x3** — derive a 95% CI for the adjusted risk difference from the 2.5th/97.5th percentiles of the bootstrap distribution
- `210-214` [high] **linked x6** — derive a bias-corrected bootstrap CI using a normal-quantile bias-correction factor (z0) instead of the plain percentile method
- `217` [high] **linked x1** — derive a two-sided p-value from the share of bootstrap risk differences on each side of zero
- `239-242` [high] **linked x1** — fit a sensitivity model that adjusts only for log games, dropping position and league country from the adjustment set
- `245-248` [high] **linked x1** — fit a sensitivity model that adjusts for league country but omits position from the covariate set
- `251-255` [high] **linked x2** — refit the model using the continuous skin_tone score as the exposure instead of the binarized dark_skin indicator
- `258-284` [medium] **linked x3** — assemble a side-by-side table of coefficient, standard error, odds ratio and p-value across the four model specifications for comparison
- `332-333` [medium] **SILENT** — compute normal-approximation (Wald) confidence intervals for the odds ratios from their log-scale standard errors, for the forest-style comparison plot
- `351` [medium] **SILENT** — restrict the position-distribution panel to the 8 most common positions rather than showing all categories
