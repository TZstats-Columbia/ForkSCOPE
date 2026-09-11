# 2025-11-20T00-05-27+0000  (ai)

- code: 461 lines, 34% exon (156 lines in 19 decisions)
- intron: print 189, plot 50, comment 49, import 10, glue 5, config 2
- prose: 234 lines, 99 claims (39 action, 60 result)
- links: 58 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 8
- result_claims_deferred: 60

## Silent decisions — executed, never disclosed

- **127-134** [high] compute an unadjusted odds ratio for red cards by skin group with a log-scale normal-approximation CI
- **378** [high] hardcode the per-league odds ratios used in the plot as literal numbers instead of the values computed in the stratified-by-league loop above

## All decisions

- `29-30` [high] **linked x1** — load the full input CSV as the analysis dataset with no read-time filtering
- `39-40` [high] **linked x2** — average the two independent raters' scores into a single continuous skin-tone measure
- `41-44` [medium] **linked x2** — restrict to dyads rated by both raters and compute their correlation as an inter-rater reliability check
- `46-48` [high] **linked x2** — define the outcome as a binary indicator for any red card in the dyad, collapsing card counts
- `49-51` [high] **linked x2** — drop dyads that lack a skin-tone rating before further analysis
- `53-56` [high] **linked x3** — dichotomize the continuous skin-tone score at the 0.5 midpoint into dark vs light categories
- `57-61` [high] **linked x2** — drop dyads missing position, height, or weight, further narrowing the analysis sample
- `102-116` [high] **linked x2** — compute the unadjusted risk difference in red-card probability between dark and light skin groups with a normal-approximation SE/CI/z-test
- `127-134` [high] **SILENT** — compute an unadjusted odds ratio for red cards by skin group with a log-scale normal-approximation CI
- `155-167` [high] **linked x10** — fit a logistic regression of any_red_card on dark_skin adjusting for games, position, and league, with player-clustered standard errors, and extract the dark_skin coefficient
- `176-179` [high] **linked x4** — exponentiate the adjusted logistic coefficient and CI to report an odds ratio as the secondary estimand
- `186-195` [high] **linked x7** — compute average marginal effects from the logistic model to convert the exposure effect onto the risk-difference scale as the primary estimand
- `221-237` [high] **linked x2** — recode skin tone using stricter cutoffs (<=0.25 light, >=0.75 dark), drop the ambiguous middle group, and refit the adjusted model as a sensitivity check
- `247-262` [high] **linked x2** — re-specify the exposure as the continuous skin_tone score instead of the binarized variable and refit the adjusted model
- `272-284, 286` [high] **linked x5** — refit the adjusted model separately within each league, dropping the now-constant league covariate, and silently skip leagues whose model fails to converge
- `288-299` [high] **linked x3** — test for effect modification by league via a likelihood-ratio test comparing a dark_skin x leagueCountry interaction model to a main-effects-only model
- `314-325` [high] **linked x3** — compute the minimum detectable effect for the study's sample sizes assuming alpha=0.05 and 80% power
- `378` [high] **SILENT** — hardcode the per-league odds ratios used in the plot as literal numbers instead of the values computed in the stratified-by-league loop above
- `447-457` [high] **linked x6** — classify the study's conclusion as SUPPORTED vs NOT SUPPORTED using the combined criterion of p<0.05 and the CI lower bound exceeding zero
