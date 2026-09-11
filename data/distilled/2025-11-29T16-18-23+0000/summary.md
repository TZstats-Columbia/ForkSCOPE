# 2025-11-29T16-18-23+0000  (ai)

- code: 390 lines, 37% exon (144 lines in 18 decisions)
- intron: print 104, comment 90, plot 38, import 10, config 4, glue 1
- prose: 236 lines, 83 claims (51 action, 32 result)
- links: 58 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 13
- result_claims_deferred: 32

## Silent decisions — executed, never disclosed

- **245-259** [high] re-derive the whole sample and covariate set under a looser minimum-games floor of 2 (instead of 3) and refit the primary model as a robustness check
- **321-322** [medium] choose what effect sizes to display for the specification-comparison panel, substituting three hard-coded numbers (0.38, 0.35, 0.35) for the actual computed robustness-check estimates rather than referencing model_r1/model_iat/se_clustered_ref

## Misaligned — code and prose disagree

- code: fill missing standardized height/weight with 0 (i.e., the sample mean under standardization, despite the adjacent comment calling it median imputation)
  - prose: missing height (6 observations) and weight (121 observations) were imputed using the median, with standardized variables centered at zero so the median imputation equals zero
  - why: claim states missing values were median-imputed; code fills with 0, which is the mean under standardization, not the median
- code: test the skin-tone coefficient with a two-sided Wald z-test derived from the model's coefficient and standard error
  - prose: conventional robust (Huber-White) standard errors were used for the primary analysis, with referee-clustered standard errors used as a robustness check
  - why: claim says the primary analysis used Huber-White robust SEs; the primary test uses the model's default non-robust MLE covariance

## All decisions

- `37` [high] **linked x2** — load the soccer dyad dataset from a fixed local CSV path as the entire analytical universe
- `51` [high] **linked x1** — collapse the two raters' skin-tone scores into a single continuous score by simple averaging
- `55, 255` [high] **linked x1** — define the outcome as any red card at all, collapsing card counts into a 0/1 indicator
- `66-79, 83, 86` [high] **linked x7** — search across six candidate skin-tone split points, pick the one that maximizes the light/dark red-card rate gap, then hard-code that value to dichotomize skin tone
- `96-103, 114-117` [high] **linked x7** — scan minimum-games-played thresholds, settle on 3 games as the exposure floor, and use it together with non-missing skin tone to define who enters the analytic sample
- `125-132` [high] **linked x1** — engineer the adjustment covariates: bucket positions into defensive/goalkeeper indicators, log-transform games, z-score height and weight, and rate-normalize yellow cards
- `135-136` [high] **linked x1** — fill missing standardized height/weight with 0 (i.e., the sample mean under standardization, despite the adjacent comment calling it median imputation)
- `148-151` [high] **linked x5** — specify the primary adjustment set and functional form (logit of any red card on binary skin tone plus position, exposure, league fixed effects, anthropometrics, yellow-card rate) and fit it
- `166-180` [high] **linked x7** — report the effect as a marginal (g-computation) risk difference: predict outcome probability for the whole sample set to all-light and all-dark, then average and difference
- `183-211` [high] **linked x5** — quantify uncertainty on the risk difference via a 500-iteration nonparametric bootstrap with a percentile interval, refitting the full logit model on each resample
- `214-219` [high] **linked x4** — test the skin-tone coefficient with a two-sided Wald z-test derived from the model's coefficient and standard error
- `229-234` [high] **linked x3** — report a secondary effect measure as an exponentiated coefficient (odds ratio) with a Wald-normal 1.96-SE interval
- `245-259` [high] **SILENT** — re-derive the whole sample and covariate set under a looser minimum-games floor of 2 (instead of 3) and refit the primary model as a robustness check
- `262-266` [high] **linked x2** — swap the dichotomized exposure for the raw continuous skin-tone score in an otherwise identical model
- `269-272` [high] **linked x1** — add referee mean implicit-bias score (meanIAT) to the adjustment set as a robustness control
- `275-284` [high] **linked x3** — recompute standard errors clustered by referee instead of the model's default (co)variance, and re-derive the test statistic and p-value from those clustered SEs
- `321-322` [medium] **SILENT** — choose what effect sizes to display for the specification-comparison panel, substituting three hard-coded numbers (0.38, 0.35, 0.35) for the actual computed robustness-check estimates rather than referencing model_r1/model_iat/se_clustered_ref
- `379-384` [high] **linked x8** — declare the hypothesis 'SUPPORTED' and characterize the effect as modest-but-meaningful and robust, framing statistical and practical significance in the writeup
