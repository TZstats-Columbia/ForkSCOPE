# 2025-11-22T03-06-18+0000  (ai)

- code: 288 lines, 32% exon (93 lines in 15 decisions)
- intron: print 120, plot 47, comment 11, import 9, config 5, glue 3
- prose: 285 lines, 118 claims (58 action, 60 result)
- links: 50 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 24
- result_claims_deferred: 60

## Silent decisions — executed, never disclosed

- **90** [high] compute the unadjusted risk difference as the raw gap between group red-card rates

## All decisions

- `30-31` [high] **linked x3** — load the full soccer player-referee dyad dataset from CSV as the analysis population
- `34-36` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skintone variable
- `37-38` [high] **linked x1** — exclude dyads lacking a skin-tone rating from further analysis
- `41-42` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome per dyad
- `43-45` [high] **linked x2** — split continuous skin tone into a dark/light binary group at a 0.5 cutoff
- `46-53` [high] **linked x2** — restrict the analysis sample to complete cases on height, weight, position, and meanIAT
- `65-73` [low] **linked x4** — tabulate group-level summary statistics (red card sum/count/rate and other covariate means) split by skin-tone group
- `90` [high] **SILENT** — compute the unadjusted risk difference as the raw gap between group red-card rates
- `98-99` [high] **linked x4** — specify the covariate adjustment set for the outcome model (dark_skin plus games, height, weight, goals, meanIAT, meanExp, position, leagueCountry)
- `104-109` [high] **linked x12** — fit the adjustment model as a logistic regression with standard errors clustered on player
- `115, 120-133` [high] **linked x6** — estimate the adjusted risk difference via g-computation: predict outcomes under everyone-dark and everyone-light counterfactuals and difference the averaged predicted probabilities
- `139-165` [high] **linked x3** — derive the standard error and 95% confidence interval for the risk difference analytically via the delta method (model gradient through the variance-covariance matrix)
- `166-168` [medium] **linked x2** — test the risk difference against the null using a two-sided normal-approximation p-value
- `177, 182-189` [high] **linked x5** — report the secondary estimand as an odds ratio by exponentiating the model coefficient and its Wald confidence interval/p-value
- `282` [high] **linked x3** — label the hypothesis as supported using a p<0.10 threshold rather than the conventional 0.05 level
