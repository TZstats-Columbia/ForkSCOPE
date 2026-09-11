# 2025-11-20T22-17-42+0000  (ai)

- code: 424 lines, 52% exon (222 lines in 21 decisions)
- intron: print 99, comment 46, plot 43, import 9, config 5
- prose: 250 lines, 99 claims (41 action, 58 result)
- links: 62 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 6
- result_claims_deferred: 58

## Silent decisions — executed, never disclosed

- **88-91** [medium] choose which columns are carried into the modeling dataset (outcome, exposure, adjustment covariates, clustering/grouping ids)
- **346-352** [medium] compute normal-approximation (Wald) confidence intervals on the raw red-card rate per skin-tone group for the bar chart error bars

## All decisions

- `30-31` [high] **linked x1** — load the match-level soccer dataset from a fixed CSV path as the analysis source
- `40-41` [high] **linked x2** — restrict to dyads where both raters supplied a skin-tone rating, dropping incomplete cases
- `44-45` [low] **linked x2** — check agreement between the two skin-tone raters via a Pearson correlation
- `48-50` [high] **linked x1** — average the two raters' scores into one continuous skin-tone measure
- `51-53` [high] **linked x2** — collapse red-card counts into a binary indicator of whether the dyad ever received a red card
- `54-61, 73-75, 81-83` [high] **linked x8** — band the continuous skin-tone score into light/medium/dark at 0.25 and 0.75, drop the medium band from the primary comparison, and recode the remaining two bands into a dark_skin indicator
- `76-80` [high] **linked x2** — drop dyads with missing player position since position is needed for adjustment
- `88-91` [medium] **SILENT** — choose which columns are carried into the modeling dataset (outcome, exposure, adjustment covariates, clustering/grouping ids)
- `104-111` [high] **linked x1** — summarize the unadjusted association as a risk difference (percentage-point gap in red-card rate) between dark- and light-skinned players
- `112-118, 119-125` [medium] **linked x1** — pick which covariates and which categorical breakdown to inspect for balance across the skin-tone groups
- `134-140` [high] **linked x7** — specify the primary regression's adjustment set as games, player position, and league country alongside the skin-tone exposure
- `141-144` [high] **linked x2** — model the binary red-card outcome with an (unclustered) logistic regression
- `145-157, 166-176, 284-292, 315-317` [high] **linked x1** — report the exposure effect as an odds ratio with a 95% Wald interval built from the coefficient and its standard error
- `158-165` [high] **linked x6** — refit the same logistic model with standard errors clustered on player instead of assuming independent observations
- `186-205` [high] **linked x10** — obtain the adjusted risk difference by predicting outcomes for the whole sample under counterfactual all-dark and all-light exposure and differencing the average predicted probabilities
- `215-246, 250-257` [high] **linked x6** — quantify uncertainty in the adjusted risk difference by resampling dyads with replacement 1000 times, refitting the model each time, and taking the percentile interval and two-sided proportion p-value of the resampled differences
- `273-277` [high] **linked x1** — build a separate sensitivity sample that keeps the full skin-tone range, only dropping missing position rather than the medium band
- `278-283` [high] **linked x2** — refit the outcome model using the continuous skin-tone score as exposure instead of the binary dark/light contrast, again with player-clustered SE
- `293-314, 318-320` [high] **linked x4** — re-run the adjusted association separately within each of four league countries, dropping league country from the covariates and only fitting a model when a country has enough dark-skinned observations with at least one red card
- `346-352` [medium] **SILENT** — compute normal-approximation (Wald) confidence intervals on the raw red-card rate per skin-tone group for the bar chart error bars
- `411-414, 417-419` [high] **linked x3** — declare the hypothesis supported or not by thresholding the bootstrap p-value against alpha = 0.05
