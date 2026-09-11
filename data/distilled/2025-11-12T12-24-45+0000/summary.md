# 2025-11-12T12-24-45+0000  (ai)

- code: 303 lines, 51% exon (155 lines in 15 decisions)
- intron: print 100, comment 38, import 9, config 1
- prose: 256 lines, 118 claims (50 action, 68 result)
- links: 56 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 15
- result_claims_deferred: 68

## Silent decisions — executed, never disclosed

- **218-225** [high] use continuous skin tone instead of the binarized exposure and refit the adjusted model
- **249-295** [medium] assemble a single summary table choosing which of the primary, secondary, stratified, and sensitivity estimates to report together and how to format them

## All decisions

- `29-31` [high] **linked x3** — load the raw referee-player dyad CSV as the working dataset
- `33-35` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `36-39` [high] **linked x4** — dichotomize continuous skin tone at the 0.5 midpoint into a light/dark binary exposure
- `40-42` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `43-45` [high] **linked x2** — normalize yellow cards by games played into a per-game rate covariate
- `46-49` [high] **linked x1** — derive player age as of the 2012 season from birthdate
- `50-52` [high] **linked x4** — restrict the analysis sample to dyads with non-missing skin tone ratings
- `90-95` [high] **linked x13** — select the adjustment covariate set and drop dyads with any missing value to form the complete-case modeling sample
- `103-117` [high] **linked x12** — fit a covariate-adjusted linear probability model with player-clustered standard errors and compute the Wald CI/p-value for the skin-tone effect
- `141-151` [high] **linked x4** — fit an adjusted logistic regression as an alternative model family for the same outcome/exposure and compute its odds ratio and CI
- `164-193` [high] **linked x7** — stratify the sample by league and refit the adjusted model separately within each of the four leagues, dropping the league term
- `206-213` [high] **linked x1** — recode the exposure using an alternative skin-tone cutoff of 0.375 and refit the adjusted model
- `218-225` [high] **SILENT** — use continuous skin tone instead of the binarized exposure and refit the adjusted model
- `230-236` [high] **linked x1** — drop the yellow-card-per-game covariate, treated as a possible mediator, and refit the adjusted model
- `249-295` [medium] **SILENT** — assemble a single summary table choosing which of the primary, secondary, stratified, and sensitivity estimates to report together and how to format them
