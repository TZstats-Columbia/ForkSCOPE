# 2025-11-21T02-39-07+0000  (ai)

- code: 332 lines, 26% exon (86 lines in 17 decisions)
- intron: print 121, comment 58, plot 54, import 7, config 3, glue 3
- prose: 244 lines, 70 claims (27 action, 43 result)
- links: 33 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 5
- result_claims_deferred: 43

## All decisions

- `30-31` [medium] **linked x1** — load the full soccer referee-player dyad dataset from a fixed CSV path with no filtering applied at read time
- `34-35` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skin_tone_avg measure
- `36-38` [high] **linked x2** — drop dyads that lack a skin-tone rating from either rater before further analysis
- `45-50, 53` [high] **linked x1** — collapse the continuous skin-tone average into two categories, Light vs Dark, split at the 0.5 midpoint of the 0-1 rating scale, then binarize it
- `51-52` [high] **linked x1** — define the outcome as any nonzero red card in the dyad rather than modeling card counts directly
- `54-64` [high] **linked x1** — collapse eleven granular playing positions down to four coarse groups (Goalkeeper/Defender/Midfielder/Forward)
- `70` [medium] **linked x1** — restrict the analytic sample to dyads whose position could be mapped to a coarse group, dropping unmapped positions
- `71` [high] **linked x2** — log-transform games played for use as the exposure-time covariate instead of the raw count
- `93-102` [medium] **linked x1** — compute and report the raw, unadjusted difference in red-card rates between light- and dark-skin groups before any covariate adjustment
- `112-117, 120-121` [high] **linked x5** — fit a logistic regression of any_red on dark_skin adjusting for log(games), position group, and league country as the primary specification
- `118-119` [high] **linked x2** — cluster the logistic model's standard errors by player instead of treating dyads as independent observations
- `142-143, 148-154` [high] **linked x4** — compute average marginal effects (risk differences) from the fitted logit model via numerical dy/dx averaged over the sample, then pull out the dark_skin row and its CI/SE/p-value for reporting
- `160-163` [high] **linked x3** — convert the dark_skin logistic coefficient to an odds ratio via exponentiation, alongside its CI and p-value, as a second effect-size metric
- `204-209` [high] **linked x1** — re-cut skin tone into a three-level extreme scheme (Very Light <=0.25, Very Dark >=0.75, Medium otherwise) and drop the Medium group to compare only the extremes
- `210-218` [high] **linked x1** — refit the same adjusted, clustered logistic specification using the extreme very_dark exposure in place of the binary dark_skin cut, and extract its marginal effect
- `230-237` [high] **linked x3** — add yellowCards as an extra covariate to the primary model as a robustness check on the dark_skin effect, and extract its marginal effect
- `318` [high] **linked x2** — declare the hypothesis 'supported' only if the adjusted effect is both statistically significant at p<0.05 and in the hypothesized direction (risk_diff positive)
