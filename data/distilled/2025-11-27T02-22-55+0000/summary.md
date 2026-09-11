# 2025-11-27T02-22-55+0000  (ai)

- code: 450 lines, 49% exon (221 lines in 23 decisions)
- intron: print 130, comment 49, plot 29, config 10, import 9, glue 2
- prose: 212 lines, 91 claims (44 action, 47 result)
- links: 66 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 4
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 9
- result_claims_deferred: 47

## Silent decisions — executed, never disclosed

- **368-371** [medium] bin skin_tone into nine display categories for the descriptive plot
- **372-378** [medium] compute the observed red-card rate and a Wald-type standard error for each skin-tone display bin
- **395** [low] back out an approximate standard error for the primary risk difference from the bootstrap CI width, assuming normality
- **396** [medium] substitute fixed placeholder standard error values for the sensitivity analyses in the forest plot instead of values derived from each model

## Misaligned — code and prose disagree

- code: bucket free-text position strings into four coarse role categories via string matching
  - prose: a 5-level position category covariate was used (Defensive, Forward/Attack, Midfielder, Goalkeeper, Unknown)
  - why: code buckets positions into four coarse role categories; claim describes a five-level position category variable
- code: bucket free-text position strings into four coarse role categories via string matching
  - prose: 12 detailed position categories were collapsed into 5 based on disciplinary risk profile
  - why: code produces four position categories; claim states twelve categories were collapsed into five

## All decisions

- `34-35` [high] **linked x2** — pick the input data file and treat every row in it as the analysis population
- `38-40` [high] **linked x1** — average the two independent raters' scores into a single skin_tone measure
- `41-44` [high] **linked x4** — drop dyads with no skin_tone rating from the analysis sample
- `48-51` [high] **linked x7** — dichotomize skin_tone at 0.25 to define the dark_skin exposure group, a cutoff chosen after looking at the data
- `52-54` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome
- `55-57` [high] **linked x3** — log-transform games played to serve as a control for exposure opportunity
- `58-73` [high] **linked x2** — bucket free-text position strings into four coarse role categories via string matching
- `74-76, 96, 98-99, 213-214, 237-238, 260, 263-264, 287-288` [high] **linked x3** — cluster standard errors by player identity in every model fit
- `94-95, 97` [high] **linked x6** — specify the primary model as logistic regression of any_red_card on dark_skin, adjusted for log_games and position category
- `112-119` [high] **linked x4** — report the exposure effect as an adjusted odds ratio by exponentiating the logit coefficient and its confidence interval
- `134-146` [high] **linked x5** — compute the adjusted risk difference via marginal standardization (g-computation), averaging predicted probabilities under both exposure levels
- `156-167, 170-192` [high] **linked x6** — derive the risk difference's 95% CI and p-value via parametric bootstrap simulation of the model's parameter distribution (10,000 draws)
- `206, 209-212, 216-225` [high] **linked x4** — re-run the model with an alternative dark-skin cutoff of 0.375 instead of 0.25
- `232, 236, 240-249` [high] **linked x3** — add league country as an extra covariate to the model
- `255, 259, 261-262, 266-275` [high] **linked x2** — restrict the analysis sample to player-referee dyads with at least 2 games together
- `282, 286, 290-293` [high] **linked x3** — refit the model using continuous skin_tone in place of the dichotomized exposure
- `300-308` [medium] **linked x2** — characterize the continuous skin_tone effect by contrasting predicted risk at its 75th vs 25th percentile
- `320-356` [medium] **linked x4** — choose which analyses, sample sizes, and statistics get placed side by side in the results summary table
- `368-371` [medium] **SILENT** — bin skin_tone into nine display categories for the descriptive plot
- `372-378` [medium] **SILENT** — compute the observed red-card rate and a Wald-type standard error for each skin-tone display bin
- `395` [low] **SILENT** — back out an approximate standard error for the primary risk difference from the bootstrap CI width, assuming normality
- `396` [medium] **SILENT** — substitute fixed placeholder standard error values for the sensitivity analyses in the forest plot instead of values derived from each model
- `440-445` [medium] **linked x3** — declare the hypothesis 'supported' from the primary analysis' p-value without adjusting for the four additional sensitivity comparisons
