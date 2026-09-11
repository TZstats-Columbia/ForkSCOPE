# 2025-11-12T20-35-40+0000  (ai)

- code: 430 lines, 45% exon (195 lines in 23 decisions)
- intron: print 88, comment 67, plot 46, glue 19, import 10, config 5
- prose: 280 lines, 96 claims (39 action, 57 result)
- links: 63 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 23
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 6
- result_claims_deferred: 57

## Misaligned — code and prose disagree

- code: estimate cluster-robust standard errors clustered at the player level rather than assuming independent dyads
  - prose: player-level and referee-level clustering was addressed through cluster-robust standard errors
  - why: code clusters standard errors on player only; claim asserts referee-level clustering was also addressed

## All decisions

- `39-40` [medium] **linked x2** — choose the source file and scope of the raw dataset to load
- `43-45` [high] **linked x1** — collapse the two independent skin-tone ratings into a single average score
- `46-47` [high] **linked x1** — drop dyads lacking a rating from either rater before proceeding
- `50-53` [low] **linked x2** — quantify agreement between the two raters with a Pearson correlation to support pooling them
- `58-65, 69-70, 128-130` [high] **linked x3** — define the light/dark exposure contrast by thresholding average skin tone at 0.25/0.75, drop dyads in the middle range, and recode the result as a 0/1 exposure indicator for modeling
- `66-68` [high] **linked x1** — define the binary outcome as receipt of any red card, collapsing counts to a 0/1 indicator
- `84-92` [medium] **linked x3** — compute and report the crude (unadjusted) red-card rate difference between skin-tone groups before any adjustment
- `93-109` [high] **linked x1** — collapse the detailed playing-position strings into six coarser role categories for use as a covariate
- `114-121` [high] **linked x1** — exclude dyads missing any of the covariates required for the regression model
- `131-135` [medium] **linked x2** — one-hot encode categorical covariates (position category, league country) with a reference level dropped
- `147-152` [high] **linked x10** — specify the covariate adjustment set for the primary outcome model
- `153-155` [high] **linked x2** — choose logistic regression as the model family and set its fitting tolerance
- `156-160` [high] **linked x4** — estimate cluster-robust standard errors clustered at the player level rather than assuming independent dyads
- `177-188` [high] **linked x7** — compute the adjusted risk difference as an average marginal effect by predicting outcomes under counterfactual dark_skin=0 vs 1 for every dyad
- `202-236` [high] **linked x3** — run a cluster (player-level) bootstrap: resample players with replacement 500 times, refit the logistic model on each resample, and silently discard replicates whose fit fails
- `242-249` [high] **linked x3** — derive 95% confidence intervals for the risk difference and odds ratio using the bootstrap percentile method
- `250-253` [medium] **linked x2** — compute a two-sided p-value via a normal approximation using the bootstrap standard error rather than the percentile distribution directly
- `279-280` [low] **linked x2** — generate in-sample predicted probabilities from the fitted model for diagnostic assessment
- `285-288` [medium] **linked x1** — evaluate model calibration/accuracy using Brier score as the summary metric
- `289-296` [medium] **linked x1** — assess calibration by binning predicted probabilities into deciles and comparing mean predicted vs observed outcome per bin
- `308-325` [high] **linked x3** — run a sensitivity analysis re-specifying skin tone as a continuous exposure instead of the binary light/dark contrast
- `334-344` [medium] **linked x3** — run a post-hoc power calculation for the minimum detectable effect at 80% power and alpha=0.05
- `358-370` [high] **linked x5** — define the rule for declaring the hypothesis supported: significant only if the bootstrap p-value is below 0.05 and the CI excludes zero
