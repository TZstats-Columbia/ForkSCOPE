# 2025-11-26T19-10-13+0000  (ai)

- code: 271 lines, 35% exon (95 lines in 19 decisions)
- intron: print 95, comment 68, import 8, config 3, glue 2
- prose: 188 lines, 81 claims (42 action, 39 result)
- links: 50 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 4
- result_claims_deferred: 39

## Silent decisions — executed, never disclosed

- **70-73** [medium] mean-impute missing height and weight and rescale both to z-scores, though neither standardized variable ends up in a fitted formula

## All decisions

- `34` [high] **linked x2** — load the full player-referee dyad table from a fixed CSV path with no filtering at read time
- `38-39` [high] **linked x1** — average the two independent raters' scores into one continuous skin-tone measure
- `41-42` [high] **linked x3** — drop dyads that are missing a rating from either rater before any modeling
- `50` [low] **linked x2** — quantify how much the two raters agree using a Pearson correlation between their scores
- `60-61` [high] **linked x4** — binarize the continuous skin-tone score into dark vs. light at a 0.25 cutoff
- `63-64` [high] **linked x1** — collapse red-card counts into a yes/no indicator for whether any red card occurred in the dyad
- `66-67` [high] **linked x2** — log-transform games played (with a +1 offset) to use as an exposure-adjustment covariate
- `70-73` [medium] **SILENT** — mean-impute missing height and weight and rescale both to z-scores, though neither standardized variable ends up in a fitted formula
- `75-84` [high] **linked x1** — regroup the detailed position labels into four coarse buckets (Defender, Midfielder, Attacker, Goalkeeper)
- `86-88` [high] **linked x2** — one-hot encode position group and league country, keeping every category dummy instead of dropping a reference level
- `97-98` [low] **linked x1** — report a crude, unadjusted red-card-rate gap between dark- and light-skinned players as a baseline comparison
- `109-113` [high] **linked x6** — choose the covariate adjustment set (exposure, position, league) and fit a logistic regression of any-red-card on dark skin plus those covariates
- `126-131, 133-135, 137-140` [high] **linked x7** — estimate the adjusted risk difference by marginal standardization: set dark_skin to 1 then 0 for every dyad, predict outcome probabilities under each, and average the difference
- `146-149, 151-155, 157-160, 162-165, 167-169, 171-173, 175-177` [high] **linked x5** — derive the standard error, confidence interval, and p-value for the risk difference analytically via the delta method (gradient of the counterfactual predictions propagated through the model's parameter covariance) rather than resampling
- `191-194` [high] **linked x6** — convert the dark_skin coefficient into an odds ratio with a CI and p-value as a secondary effect measure
- `209-212` [high] **linked x1** — check robustness by excluding goalkeepers and refitting the same adjusted model on the remaining players
- `219-223` [high] **linked x1** — check robustness by refitting with the continuous skin-tone score in place of the binarized dark/light indicator
- `229-232` [high] **linked x1** — check robustness by restricting to dyads with at least 2 games as a data-quality filter and refitting
- `260, 265, 267` [high] **linked x4** — set the rule for declaring the hypothesis 'supported': two-sided p<0.05, with the primary branch additionally requiring the risk-difference CI to exclude zero in the hypothesized direction
