# 2025-11-29T02-07-25+0000  (ai)

- code: 314 lines, 61% exon (193 lines in 20 decisions)
- intron: print 75, comment 33, import 8, config 4, glue 1
- prose: 262 lines, 106 claims (63 action, 43 result)
- links: 79 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 12
- result_claims_deferred: 43

## Silent decisions — executed, never disclosed

- **257-264** [high] restrict the sample to dyads with at least 3 games together and refit the model
- **270-277** [high] refit the model separately within each league, dropping the league covariate, to check cross-league consistency
- **292-301** [low] frame the risk difference as the primary estimand and the odds ratio as the secondary one in the reported results

## Misaligned — code and prose disagree

- code: collapse red card counts into a single any-red-card binary outcome per dyad
  - prose: no transformation was applied to the already-binary outcome
  - why: code collapses red-card counts into an any-red-card binary (a transformation), contradicting the claim that the outcome was already binary and no transformation was applied

## All decisions

- `30-32` [high] **linked x4** — read the full player-referee dyad dataset from CSV as the analytic universe
- `38-41` [high] **linked x5** — drop dyads missing either skin-tone rating before deriving the exposure
- `47-50` [high] **linked x3** — average the two raters' skin-tone scores into one continuous exposure variable
- `51-54, 244` [high] **linked x8** — binarize skin tone at a 0.25 cutoff into dark vs light skin, chosen explicitly to maximize the observed effect
- `55-57` [high] **linked x2** — collapse red card counts into a single any-red-card binary outcome per dyad
- `58-61` [medium] **linked x1** — fill missing height and weight values with the sample median
- `62-79` [high] **linked x1** — regroup granular playing positions into four broad categories, bucketing anything unmapped as Other
- `80-84` [high] **linked x4** — drop goalkeepers from the modeling sample as a subgroup restriction
- `100-106` [high] **linked x12** — specify the primary outcome model as logistic regression of red-card occurrence on dark skin, adjusting for position, league, and games played
- `107-111` [high] **linked x7** — report the darkSkin effect from the primary model on the odds-ratio scale with its Wald CI and p-value
- `116-129, 231-238` [high] **linked x2** — convert the fitted model's coefficient into an absolute risk difference by predicting every observation under counterfactual dark-skin=1 and dark-skin=0 and differencing the averaged predictions
- `133-172` [high] **linked x11** — derive the risk difference's sampling uncertainty via a numerical-gradient delta method, then build a two-sided 95% Wald interval and z-test around it
- `189-197` [high] **linked x3** — re-estimate the model under two alternative dark-skin cutoffs (0.125 and 0.375) to probe sensitivity of the threshold choice
- `202-210, 212-220` [high] **linked x6** — recompute the primary model's standard errors clustering first on referee, then on player, instead of treating dyads as independent
- `225-228` [high] **linked x2** — re-estimate the exposure-outcome relationship with a probit link in place of logit
- `245-252` [high] **linked x2** — refit the model on the full sample with goalkeepers reinstated to check sensitivity of their exclusion
- `257-264` [high] **SILENT** — restrict the sample to dyads with at least 3 games together and refit the model
- `270-277` [high] **SILENT** — refit the model separately within each league, dropping the league covariate, to check cross-league consistency
- `292-301` [low] **SILENT** — frame the risk difference as the primary estimand and the odds ratio as the secondary one in the reported results
- `302-309` [medium] **linked x6** — declare the hypothesis 'supported' and characterize the effect as statistically significant and robust across the sensitivity analyses
