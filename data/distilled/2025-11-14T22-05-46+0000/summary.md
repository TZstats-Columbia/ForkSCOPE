# 2025-11-14T22-05-46+0000  (ai)

- code: 315 lines, 40% exon (125 lines in 20 decisions)
- intron: print 90, comment 80, glue 10, import 8, config 2
- prose: 265 lines, 114 claims (48 action, 66 result)
- links: 56 (3 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 6
- result_claims_deferred: 66

## Silent decisions — executed, never disclosed

- **53-54** [high] derive player age at a fixed reference year (2012) from birthday

## Misaligned — code and prose disagree

- code: cut continuous skin tone into Light/Dark categories at a 0.375 bin edge (despite the preceding comment citing 0.5) and derive a binary dark-skin indicator from it
  - prose: the averaged skin tone score was dichotomized into light (<0.5) versus dark (≥0.5)
  - why: claim dichotomizes at 0.5; code cuts at a 0.375 bin edge
- code: cut continuous skin tone into Light/Dark categories at a 0.375 bin edge (despite the preceding comment citing 0.5) and derive a binary dark-skin indicator from it
  - prose: the averaged skin tone score was dichotomized at a threshold of 0.5
  - why: claim states threshold of 0.5; code uses 0.375
- code: cut continuous skin tone into Light/Dark categories at a 0.375 bin edge (despite the preceding comment citing 0.5) and derive a binary dark-skin indicator from it
  - prose: the choice of 0.5 as the dichotomization threshold is acknowledged as somewhat arbitrary
  - why: claim names 0.5 as the dichotomization threshold; code actually cuts at 0.375

## All decisions

- `28` [high] **linked x2** — choose the input dataset and file path to load as the analysis population
- `32` [high] **linked x3** — average the two independent raters' scores into a single continuous skin-tone measure
- `35` [high] **linked x2** — drop dyads with missing skin-tone rating from the analysis sample
- `39` [high] **linked x2** — collapse red-card counts into a binary any-red-card outcome
- `42-46, 60, 86` [medium] **linked x3** — cut continuous skin tone into Light/Dark categories at a 0.375 bin edge (despite the preceding comment citing 0.5) and derive a binary dark-skin indicator from it
- `53-54` [high] **SILENT** — derive player age at a fixed reference year (2012) from birthday
- `57, 85` [high] **linked x1** — log-transform games played to use as the exposure/offset variable
- `67-73` [high] **linked x5** — restrict to complete cases across skin category, age, height, weight, and position covariates
- `81-84` [high] **linked x1** — z-standardize age, height, and weight before modeling
- `96-98` [medium] **linked x2** — summarize red-card rate by grouping on skin category and reporting sum/count/mean
- `103` [high] **linked x1** — compute the unadjusted (crude) risk difference as a percentage-point contrast between Dark and Light groups
- `115-116` [high] **linked x3** — specify the primary model's adjustment set (skin_dark, log_games, age/height/weight, position, league country)
- `121-126` [high] **linked x8** — fit a logistic regression with standard errors clustered by player
- `144-146, 149-152` [high] **linked x6** — designate the primary estimand as the average marginal effect (overall, dy/dx) of dark skin, extracted with its SE and CI
- `171-173` [high] **linked x5** — report a secondary estimand as the exponentiated coefficient (odds ratio) with its CI
- `190-191, 193-194, 196-201, 203-205` [high] **linked x2** — run a sensitivity analysis restricting to players with extreme (0 or 1) skin-tone ratings and refit the same adjusted model on the recoded exposure
- `213-214, 216-221, 223-225` [high] **linked x2** — run a sensitivity analysis treating skin tone as a continuous exposure instead of a binary category
- `233, 235-240, 242-244` [high] **linked x2** — run a sensitivity analysis with a minimal adjustment set containing only skin_dark and log_games
- `251-253, 255-261, 263-265` [high] **linked x4** — run a sensitivity analysis on the full sample without the complete-case covariate restriction, adjusting only for games
- `279-308` [medium] **linked x2** — assemble a summary table selecting which five model results and which statistics (N, RD, CI) to present side by side
