# 2025-11-20T22-11-22+0000  (ai)

- code: 347 lines, 41% exon (143 lines in 16 decisions)
- intron: print 138, comment 41, glue 11, import 10, config 4
- prose: 238 lines, 91 claims (28 action, 63 result)
- links: 17 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 6
- result_claims_deferred: 63

## Silent decisions — executed, never disclosed

- **32-34** [high] read the raw player-referee dyad CSV in as the full working dataset
- **55-58** [medium] parse birthday and derive age as a plain year subtraction from a fixed reference year (2012)

## All decisions

- `32-34` [high] **SILENT** — read the raw player-referee dyad CSV in as the full working dataset
- `37-38` [high] **linked x1** — average the two raters' scores into one continuous skin-tone measure
- `39-44` [low] **linked x1** — restrict to dyads with both ratings present and report Pearson correlation as an inter-rater agreement check
- `45-47` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome using a >=1 cutoff
- `48-54, 86-88` [high] **linked x1** — split continuous skin tone into Light/Dark categories at the 0.5 midpoint and encode a binary dark-skin exposure flag from it
- `55-58` [medium] **SILENT** — parse birthday and derive age as a plain year subtraction from a fixed reference year (2012)
- `67-69` [high] **linked x1** — drop dyads with no skin-tone rating from the analysis sample
- `73-78` [high] **linked x1** — further restrict the sample to dyads with non-missing position, height, and weight (complete-case restriction)
- `107` [medium] **linked x1** — compute the crude, unadjusted risk-difference contrast between dark- and light-skin groups for descriptive reporting
- `122-126, 274-277` [high] **linked x1** — choose which covariates enter the outcome model (games, height, weight, age, yellow cards, goals, position, league country) and their reference categories
- `136-138, 278-279` [high] **linked x2** — fit a logistic regression with heteroskedasticity-robust (HC1) standard errors and a fixed iteration cap
- `158-175, 287-300` [high] **linked x1** — estimate the adjusted risk difference via counterfactual average marginal effects: set the exposure to 1 then 0 for every row and average the predicted-probability gap
- `183-213, 214-215, 216-219, 220-225` [high] **linked x2** — resample dyads with replacement across 500 bootstrap iterations, refit the model each time, and derive the CI from the empirical percentiles plus a sign-based two-sided p-value from the resampled distribution
- `244-247, 285-286` [high] **linked x1** — exponentiate the logistic coefficient and its CI to report on the odds-ratio scale
- `266-269` [high] **linked x1** — redefine the exposure contrast as extreme skin-tone groups (<=0.25 vs >=0.75), discarding the middle of the distribution, for a sensitivity check
- `331-336` [high] **linked x2** — apply a p<0.05 cutoff together with the sign of the estimate to pick which directional conclusion sentence to print
