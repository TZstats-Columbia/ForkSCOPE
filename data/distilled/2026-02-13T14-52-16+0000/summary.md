# 2026-02-13T14-52-16+0000  (ai)

- code: 236 lines, 36% exon (84 lines in 15 decisions)
- intron: print 86, comment 47, glue 11, import 6, config 2
- prose: 189 lines, 80 claims (31 action, 49 result)
- links: 43 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 9
- result_claims_deferred: 49

## Silent decisions — executed, never disclosed

- **65-71** [medium] compute and report the crude (unadjusted) difference in red-card rates between dark- and light-skin-toned groups before any covariate adjustment

## All decisions

- `23-24` [high] **linked x1** — load the raw soccer referee/player dataset from CSV as the analysis universe
- `26-28` [high] **linked x2** — average the two independent raters' skin-tone scores into a single continuous skin_tone_avg measure
- `29-31` [high] **linked x2** — drop players/dyads with no skin-tone rating before any further analysis
- `33-35` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome
- `36-39` [high] **linked x5** — dichotomize the continuous skin-tone score into dark vs light using a 0.5 cutpoint
- `44-47, 82-83` [high] **linked x3** — choose which player/match covariates (games, position, league country, height, weight, yellow cards) enter the adjustment set and regression formulas
- `48` [medium] **linked x6** — restrict the main regression sample to complete cases via listwise deletion
- `65-71` [medium] **SILENT** — compute and report the crude (unadjusted) difference in red-card rates between dark- and light-skin-toned groups before any covariate adjustment
- `80-81, 84-85` [high] **linked x2** — fit the exposure-outcome relationship as a logistic regression rather than another model family, with default optimizer settings
- `97-106` [high] **linked x5** — summarize the exposure effect as an average marginal effect (risk difference in percentage points) rather than only a coefficient/odds ratio
- `111, 134, 205-206, 225-226` [high] **linked x2** — declare statistical significance using a two-sided α=0.05 cutoff, and for the final conclusion additionally require the marginal-effect CI to exclude zero
- `120-129` [high] **linked x5** — compute a secondary effect measure, the adjusted odds ratio, with a Wald-type 95% CI built from a 1.96 z-multiplier on the log-odds scale
- `146-153` [medium] **linked x4** — re-express the absolute risk difference as a percentage relative to the baseline red-card rate
- `162-166` [high] **linked x2** — re-estimate the same model with heteroskedasticity-robust (HC1) standard errors as a robustness check
- `171-172, 177-186` [high] **linked x2** — re-run the model using the untransformed continuous skin-tone score instead of the binarized exposure, as a sensitivity check on the thresholding choice
