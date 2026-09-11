# 2025-11-22T04-02-51+0000  (ai)

- code: 189 lines, 47% exon (88 lines in 14 decisions)
- intron: print 65, comment 25, import 9, config 2
- prose: 247 lines, 134 claims (54 action, 80 result)
- links: 81 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 13
- result_claims_deferred: 80

## All decisions

- `20-21` [high] **linked x2** — pull the analysis data from a specific soccer dyads CSV file
- `25-27` [high] **linked x1** — collapse the two raters' scores into a single skin-tone score by averaging them
- `28-29, 31` [medium] **linked x1** — check agreement between the two raters via Pearson correlation on dyads where both rated
- `34-37` [high] **linked x4** — dichotomize the continuous skin-tone score into dark vs light using a 0.5 cutoff
- `38-40` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `45-46` [high] **linked x3** — limit the working sample to dyads that have a skin-tone rating at all
- `64-67` [high] **linked x6** — drop dyads with missing values on the chosen covariate set to form a complete-case sample
- `70-73` [high] **linked x16** — specify and fit a logistic regression of any red card on skin-tone exposure adjusted for games, position, league and body size
- `79-91` [high] **linked x10** — estimate the adjusted risk difference via marginal standardization: predict outcomes setting exposure to all-light and all-dark and difference the average predicted probabilities
- `92-115` [high] **linked x4** — derive the standard error, CI, z-statistic and p-value for the standardized risk difference using the delta method
- `132-138` [medium] **linked x9** — report the exposure effect on the odds ratio scale by exponentiating the logistic coefficient and its Wald CI
- `150-155` [high] **linked x7** — refit the primary model with standard errors clustered by player instead of assuming independent dyads
- `163-166, 167` [high] **linked x6** — re-specify exposure as the continuous skin-tone score instead of the binary threshold and refit
- `178-185` [high] **linked x10** — stratify the model by league, refitting the exposure-outcome model separately within each of four countries
