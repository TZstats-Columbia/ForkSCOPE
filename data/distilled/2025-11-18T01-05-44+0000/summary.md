# 2025-11-18T01-05-44+0000  (ai)

- code: 357 lines, 22% exon (78 lines in 14 decisions)
- intron: print 147, plot 59, comment 57, import 9, glue 6, config 1
- prose: 243 lines, 73 claims (40 action, 33 result)
- links: 47 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 9
- result_claims_deferred: 33

## Silent decisions — executed, never disclosed

- **161-162, 197-198, 276-277** [medium] build every reported 95% interval with a fixed normal-approximation multiplier of 1.96 rather than an exact or resampled critical value

## All decisions

- `30-31` [high] **linked x3** — read the raw player-referee dyad CSV in as the entire analysis population
- `34-35` [high] **linked x1** — average rater1 and rater2 into one continuous skinTone score
- `45-51, 262-263` [high] **linked x2** — cut continuous skinTone into Light/Medium/Dark buckets using 0.375 and 0.625 breakpoints, and later redraw those same breakpoints as reference lines on the histogram
- `52-57, 73-74` [high] **linked x5** — collapse the three-level bucket into a light(0)/dark(1) indicator (sending Medium to missing), then drop every row whose indicator is missing from the modeling frame
- `58-60` [high] **linked x1** — turn the red-card count into a binary any-red-card flag
- `80, 82` [high] **linked x3** — further restrict the modeling frame to dyads with a known player position
- `88` [high] **linked x3** — put the games-played covariate on a log scale before it enters the model
- `107-111` [medium] **linked x1** — compute the raw, unadjusted red-card-rate difference between dark and light groups as a reference point before adjustment
- `125-126` [high] **linked x6** — pick the outcome-model specification: red card on the skin-tone indicator plus position, league country, and log(games) as the adjustment set
- `143-160, 163-164` [high] **linked x11** — fit the adjustment-set formula as an OLS linear probability model and build its reported standard error as a two-way player+referee cluster-robust estimate, combining separately player-clustered, referee-clustered, and HC3 fits (Cameron-Gelbach-Miller)
- `161-162, 197-198, 276-277` [medium] **SILENT** — build every reported 95% interval with a fixed normal-approximation multiplier of 1.96 rather than an exact or resampled critical value
- `174, 205, 342, 344` [medium] **linked x4** — declare an effect statistically significant / the hypothesis supported by comparing its p-value against a fixed 0.05 cutoff
- `192-196, 199` [high] **linked x6** — additionally fit a logistic regression on the same formula and re-express its coefficient as an odds ratio via exponentiation
- `207-214` [high] **linked x1** — estimate a risk-difference-scale effect from the logistic fit by predicting outcomes under counterfactual dark=0 and dark=1 for every row and averaging the gap
