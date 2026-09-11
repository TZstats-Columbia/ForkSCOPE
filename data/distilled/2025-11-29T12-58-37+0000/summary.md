# 2025-11-29T12-58-37+0000  (ai)

- code: 330 lines, 30% exon (100 lines in 15 decisions)
- intron: print 171, comment 40, import 6, glue 5, config 4, other 4
- prose: 228 lines, 87 claims (48 action, 39 result)
- links: 54 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 9
- result_claims_deferred: 39

## Silent decisions — executed, never disclosed

- **33** [high] load the raw player-referee dyad dataset from CSV as the analysis input

## All decisions

- `33` [high] **SILENT** — load the raw player-referee dyad dataset from CSV as the analysis input
- `42-44` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skin_tone measure
- `48-50` [high] **linked x2** — drop dyads with no skin-tone rating from the working sample
- `52-54` [high] **linked x1** — collapse the red-card count into a binary any-red-card indicator
- `56-61, 72-74` [high] **linked x10** — carve out the two most extreme skin-tone groups (score 0 vs score>=0.75) and restrict the primary analysis to only those dyads
- `62-64, 200` [high] **linked x1** — build an alternate binary skin-tone split at the 0.25 cutoff
- `65-71` [high] **linked x4** — fill missing covariate values with an 'Unknown' category or the column median/mean instead of dropping those rows
- `120-127` [high] **linked x11** — specify and fit the primary logistic regression of any_red on the extreme skin-tone contrast plus games, position, and referee bias covariates
- `138-142` [medium] **linked x3** — exponentiate the logit coefficient and its Wald interval into an odds ratio for reporting
- `143-150, 205-211, 226-232, 247-253, 268-274` [high] **linked x10** — convert each model's logit coefficient into a percentage-point risk difference via the delta-method variance approximation and treat it as the headline effect size
- `162, 216, 237, 258, 279` [medium] **linked x3** — call a result 'significant' whenever its p-value clears the 0.05 cutoff
- `201-204` [high] **linked x3** — fit the first sensitivity model using the 0.25 dark-skin cutoff and dropping the position control
- `222-225` [high] **linked x2** — fit a sensitivity model treating skin tone as a continuous predictor rather than categorical
- `243-246` [high] **linked x1** — refit the primary extreme-contrast model with the position covariate removed
- `264-267` [high] **linked x2** — refit the primary model adding yellow cards as an extra control for player aggression
