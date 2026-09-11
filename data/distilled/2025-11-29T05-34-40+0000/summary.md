# 2025-11-29T05-34-40+0000  (ai)

- code: 375 lines, 34% exon (129 lines in 19 decisions)
- intron: print 153, comment 68, glue 16, import 5, config 4
- prose: 258 lines, 115 claims (73 action, 42 result)
- links: 76 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 22
- R_only_consistent_negative: 9
- result_claims_deferred: 42

## Silent decisions — executed, never disclosed

- **33** [high] pick the input file and dataset scope to analyze

## All decisions

- `33` [high] **SILENT** — pick the input file and dataset scope to analyze
- `37-38` [high] **linked x3** — average two raters' scores into one composite skin-tone measure
- `41` [high] **linked x4** — drop dyads with no measurable skin tone rather than impute or keep them
- `50` [high] **linked x1** — collapse red-card counts into a binary any-red-card outcome
- `55-57, 66-67` [high] **linked x8** — define the primary exposure as extreme skin-tone groups (>=0.75 dark, <=0.25 light) and restrict the analysis sample to only those dyads
- `59-61` [high] **linked x2** — construct alternate skin-tone thresholds (>=0.5 and >=0.375) for later robustness checks
- `63-64` [high] **linked x2** — log-transform games played to use as an exposure/covariate
- `93-96` [medium] **linked x2** — compute a simple unadjusted risk-difference contrast between the two exposure groups as a headline descriptive statistic
- `115-117` [high] **linked x7** — choose the primary adjustment set: position and league-country dummies plus the exposure and log(games)
- `118-120` [high] **linked x5** — fill missing referee implicit/explicit bias scores with the column median rather than dropping those rows
- `131-132` [high] **linked x2** — choose logistic regression as the primary model family for the binary red-card outcome
- `142-145` [medium] **linked x4** — report the exponentiated coefficient and its CI as an odds-ratio secondary estimand
- `162-170, 172-173` [high] **linked x13** — estimate the adjusted risk difference via marginal standardization: predict outcome probabilities setting exposure to all-dark vs all-light and take the mean difference
- `182-183, 184-191, 193-195, 196-207, 209-211` [high] **linked x5** — derive the standard error of the adjusted risk difference via the delta method using a numerically approximated gradient
- `213-217` [high] **linked x4** — build a 95% confidence interval and two-sided p-value using the normal approximation (1.96 multiplier) around the risk-difference estimate
- `238-241, 246-247, 248-256` [high] **linked x4** — run a robustness check dropping the referee-bias covariates from the adjustment set, refit logistic model and recompute the standardized risk difference
- `266-271, 278-279, 280-288` [high] **linked x4** — run a robustness check using a broader >=0.5 skin-tone threshold on the full (non-extreme-restricted) sample, refit and recompute standardized risk difference
- `298-301, 302-303` [high] **linked x4** — run a robustness check modeling skin tone as a continuous linear predictor instead of a dichotomized exposure
- `356-371` [high] **linked x2** — set the significance rule (two-sided p<0.05 and CI excluding zero) that labels the hypothesis as supported, marginally supported, or not supported
