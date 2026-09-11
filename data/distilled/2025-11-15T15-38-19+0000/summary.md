# 2025-11-15T15-38-19+0000  (ai)

- code: 327 lines, 50% exon (163 lines in 14 decisions)
- intron: print 104, comment 47, import 10, config 3
- prose: 299 lines, 122 claims (67 action, 55 result)
- links: 85 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 16
- result_claims_deferred: 55

## Silent decisions — executed, never disclosed

- **142-150** [high] fit an unadjusted logistic regression of red card receipt on dark_skin alone, with standard errors clustered by player

## All decisions

- `29-30` [high] **linked x3** — load the raw soccer referee dataset and treat it as the full analysis scope
- `34-36` [high] **linked x4** — average the two raters' skin-tone scores into a single skin_tone measure, dropping dyads missing either rating
- `39-42` [low] **linked x2** — check agreement between the two raters by computing their correlation
- `51-60, 65-67` [high] **linked x10** — bin continuous skin_tone into light (<=0.25) vs dark (>=0.50) groups, drop the middle band, and recode the group as a binary dark_skin indicator
- `68-70, 261` [high] **linked x8** — define the outcome as a binary indicator for whether any red card was received
- `79-96` [low] **linked x3** — compute and report the raw (unadjusted) red-card rate difference between skin-tone groups as a descriptive benchmark
- `105-122, 262-263` [high] **linked x2** — collapse free-text position strings into a small set of position categories (Forward/Defender/Midfielder/Goalkeeper/Other/Unknown)
- `123-128, 264-268` [high] **linked x7** — impute missing height and weight with the sample median and missing implicit-bias scores (meanIAT/meanExp) with zero
- `142-150` [high] **SILENT** — fit an unadjusted logistic regression of red card receipt on dark_skin alone, with standard errors clustered by player
- `153-154, 191-193` [high] **linked x7** — convert the logit coefficient on dark_skin into an odds ratio by exponentiating it and its confidence interval
- `165-188` [high] **linked x26** — specify the adjusted model's covariate set (games, height, weight, leagueCountry, position_cat, meanIAT, meanExp), dummy-encode the categoricals, and fit a logistic regression clustered by player
- `204-213` [high] **linked x10** — treat the average marginal effect (risk difference) of dark_skin from the adjusted model as the primary estimand
- `228-246` [medium] **linked x1** — compute predicted red-card probabilities for light vs dark skin holding all other covariates at their sample means
- `259-260, 269-285, 289-290` [high] **linked x2** — run a sensitivity analysis that keeps skin_tone continuous and uses the full rated sample (no dark/light exclusion), refitting the adjusted-style model
