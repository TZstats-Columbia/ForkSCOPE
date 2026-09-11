# 2025-11-22T04-24-20+0000  (ai)

- code: 545 lines, 31% exon (167 lines in 22 decisions)
- intron: glue 139, print 125, plot 89, comment 14, import 8, config 3
- prose: 252 lines, 135 claims (49 action, 86 result)
- links: 96 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 5
- result_claims_deferred: 86

## Silent decisions — executed, never disclosed

- **119-122** [medium] compute the crude red-card rate separately for the light- and dark-skin groups
- **307-308** [low] silently skip and flag any country whose model fails to converge instead of halting the run

## All decisions

- `31-32` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path
- `51-52` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `53-55` [high] **linked x2** — collapse red-card counts into a binary any-red-card outcome
- `61-62` [high] **linked x1** — drop dyads lacking a skin-tone rating from the analysis population
- `64-68` [high] **linked x7** — dichotomize skin tone at the 0.5 midpoint into a dark/light exposure variable
- `69-86` [medium] **linked x1** — regroup the detailed playing positions into four broad position categories
- `87-93` [high] **linked x6** — fix the set of modeling variables and drop any remaining rows with missing values on them
- `104-105` [high] **linked x2** — log-transform the games-played exposure variable to address skew
- `106-110` [high] **linked x4** — z-score standardize height, weight, and yellow-card counts
- `119-122` [medium] **SILENT** — compute the crude red-card rate separately for the light- and dark-skin groups
- `128-135` [high] **linked x1** — express the unadjusted comparison as a risk difference with a normal-approximation 95% CI and two-sided z-test
- `150-153` [high] **linked x8** — specify the covariate adjustment set for the primary outcome model (position group, log exposure, height, weight, yellow cards, league)
- `154-160` [high] **linked x7** — fit a logistic regression with standard errors clustered by player rather than treating dyads as independent observations
- `164-169` [medium] **linked x5** — report the dark-skin effect on the odds-ratio scale by exponentiating the fitted coefficient
- `183-187` [high] **linked x8** — designate the average marginal effect (dy/dx, evaluated overall) as the primary risk-difference estimand
- `195-198` [medium] **linked x2** — estimate standardized predicted probabilities by setting darkSkin to 1 vs 0 for every dyad and averaging
- `212-215, 220-233` [high] **linked x8** — restrict to an extreme-groups comparison (skin tone <0.25 vs >=0.75), dropping the middle range, and refit the adjusted model with average marginal effects on that subsample
- `247-259` [high] **linked x9** — re-specify the exposure as continuous skin tone instead of the dichotomized variable and refit the adjusted model
- `273-291` [high] **linked x14** — stratify the adjusted model by league country, fitting a separate model per country instead of pooling with a league fixed effect
- `307-308` [low] **SILENT** — silently skip and flag any country whose model fails to converge instead of halting the run
- `317-318, 320-332` [high] **linked x7** — exclude dyads refereed in more than 10 games and refit the adjusted model with average marginal effects on the remainder
- `357-372` [high] **linked x1** — run a variance-inflation-factor multicollinearity check on the model covariates (dummy-coded) and adopt VIF<10 as the concern threshold
