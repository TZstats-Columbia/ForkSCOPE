# 2025-11-26T20-50-08+0000  (ai)

- code: 324 lines, 41% exon (133 lines in 18 decisions)
- intron: print 125, comment 51, import 5, config 5, glue 5
- prose: 266 lines, 91 claims (55 action, 36 result)
- links: 54 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 19
- result_claims_deferred: 36

## Silent decisions — executed, never disclosed

- **30-31** [medium] pick the raw file and treat the full contents as the analysis universe

## All decisions

- `30-31` [medium] **SILENT** — pick the raw file and treat the full contents as the analysis universe
- `34-35` [high] **linked x1** — collapse the two raters' scores into a single skin-tone measure by averaging them
- `46-49` [high] **linked x2** — drop dyads with any missing skin tone, height, or weight rather than imputing or keeping them
- `55-56` [high] **linked x1** — collapse the red-card count into a binary any-red-card indicator
- `71-75, 76-89, 95-99` [high] **linked x15** — scan a grid of dichotomization thresholds, compare unadjusted red-card rates at each, then lock in the 0.75 cutoff that gives the strongest split as the operational definition of 'dark skin'
- `110-119` [high] **linked x1** — collapse the detailed position field into four broad role categories via a hand-built mapping
- `120-123` [medium] **linked x3** — z-score height and weight instead of leaving them in raw units
- `124-126` [medium] **linked x2** — log-transform games played to address right skew rather than using the raw count
- `139, 149` [medium] **linked x2** — model the binary outcome with logistic regression rather than a linear probability model or another link
- `142-148` [high] **linked x7** — choose position, league country, height, weight, and log(games) as the adjustment set for the primary model
- `162-166` [high] **linked x4** — summarize the exposure effect as an average marginal risk difference by setting everyone to dark vs. light and averaging predicted probabilities
- `167-196` [high] **linked x2** — derive the uncertainty interval for the risk difference via a parametric bootstrap that resamples model coefficients from a multivariate normal 1000 times
- `212-216` [high] **linked x5** — report a second effect measure, the odds ratio, with a Wald normal-approximation confidence interval instead of the bootstrap used for the primary estimand
- `229-235` [high] **linked x1** — re-run the model with the exposure dichotomized at 0.5 instead of 0.75 as a robustness check
- `240-247` [high] **linked x1** — re-run the model treating skin tone as continuous and report the effect contrasting the 75th vs 25th percentile
- `252-259` [high] **linked x2** — restrict the sample to dyads with at least 3 games and re-fit as a robustness check
- `263-270` [high] **linked x2** — add a log-transformed yellow-card count as an extra covariate and re-fit as a robustness check
- `309, 318` [high] **linked x3** — declare the hypothesis 'supported' precisely when the bootstrap CI lower bound for the risk difference is above zero
