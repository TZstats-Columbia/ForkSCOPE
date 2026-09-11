# 2025-11-15T22-00-27+0000  (ai)

- code: 388 lines, 15% exon (59 lines in 16 decisions)
- intron: print 182, comment 85, plot 32, glue 15, import 9, config 5, other 1
- prose: 302 lines, 94 claims (41 action, 53 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 6
- result_claims_deferred: 53

## Silent decisions — executed, never disclosed

- **252** [high] restrict the interaction-sensitivity sample to dyads with non-missing referee implicit-bias score

## All decisions

- `36` [high] **linked x2** — read the raw player-referee dyad dataset from a fixed csv path as the entire analytic universe
- `42` [high] **linked x1** — collapse two independent skin-tone ratings into a single average score
- `49` [high] **linked x1** — drop dyads with missing skin-tone rating to form the clean analysis base
- `56-57, 60-61, 115` [high] **linked x6** — dichotomize continuous skin tone at 0.75/0.25 cutoffs, discard the middle range, and materialize the group as a numeric/label variable for modeling
- `78, 222, 304` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome for the dyad
- `101-103` [medium] **linked x1** — run an unadjusted chi-square test of association between skin group and any red card as a descriptive check
- `114, 223` [high] **linked x2** — log-transform number of games to model exposure in the regression
- `116, 224` [high] **linked x1** — recode missing player position as an explicit 'Missing' category rather than dropping those rows
- `119, 126-130` [high] **linked x16** — specify and fit the primary logistic regression with position/country/log-games covariates and standard errors clustered by player
- `157-159, 162, 165-166, 169-170, 243-245` [high] **linked x7** — compute the average marginal effect (risk difference) via the delta-method approximation, with a normal-approximation 95% CI and two-sided p-value, applied to both the primary and continuous-sensitivity models
- `195-197` [medium] **linked x5** — re-express the log-odds coefficient and its CI on the odds-ratio scale as the secondary estimand
- `225-232` [high] **linked x3** — run a sensitivity model using the continuous skin_tone_avg score in place of the binarized dark/light group, on the full (non-restricted) sample
- `252` [high] **SILENT** — restrict the interaction-sensitivity sample to dyads with non-missing referee implicit-bias score
- `255-262` [high] **linked x2** — only if the IAT-sample exceeds 10,000, fit an interaction model adding referee implicit bias and its interaction with skin tone
- `302-303` [medium] **linked x2** — bin the continuous skin-tone score into 8 equal-width bins for a descriptive plot
- `370, 373` [low] **linked x3** — apply a 0.05 significance threshold to the risk-difference p-value to declare the hypothesis supported or not
