# 2025-11-26T22-40-16+0000  (ai)

- code: 377 lines, 55% exon (207 lines in 14 decisions)
- intron: print 105, comment 55, import 5, config 5
- prose: 181 lines, 73 claims (38 action, 35 result)
- links: 48 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 11
- result_claims_deferred: 35

## All decisions

- `31-32` [high] **linked x2** — load the raw player-referee dyad dataset from CSV with no filtering applied at read time
- `35-37` [high] **linked x2** — average the two raters' skin-tone scores into one continuous skintone measure
- `38-40` [high] **linked x1** — collapse the red card count into a yes/no indicator for whether the dyad had any red card
- `41-43` [high] **linked x1** — drop dyads with no recorded skin-tone rating
- `54-58, 241, 267, 289, 291-292` [high] **linked x4** — restrict to dyads with at least 3 shared games, then re-run the pipeline at 2- and 4-game cutoffs to check sensitivity
- `60-77, 244, 270, 295` [high] **linked x1** — map detailed position strings into five coarse role buckets (Forward/Defender/Midfielder/Goalkeeper/Other)
- `78-83, 245, 265, 296` [high] **linked x5** — remove goalkeeper dyads from the main sample, then re-run once with goalkeepers left in to see if it matters
- `90-94, 238, 240, 242, 268, 293, 316, 318-319` [high] **linked x11** — cut the continuous skin-tone score at 0.25 (a value chosen by scanning several candidate cutoffs) into a dark/light indicator, and separately refit treating skin tone as continuous instead
- `109-110, 243, 269, 294` [high] **linked x2** — log-transform games played for use as a covariate
- `124-126, 246-248, 271-273, 297-299` [high] **linked x7** — fit a logistic regression of any red card on the dark indicator, adjusting for log(games), position category, and league country
- `139-160, 249-258, 274-282, 300-309, 324-334` [high] **linked x4** — estimate the effect by marginal standardization: predict outcomes with the whole sample set to all-light and all-dark, then difference the mean predicted probabilities
- `170-205` [high] **linked x4** — derive the standard error of the marginal risk difference analytically via the delta method and build a normal-approximation 95% CI and two-sided p-value
- `219-224, 259-261, 283-285, 310-312, 320-323` [high] **linked x2** — convert the dark (or continuous skin-tone) coefficient into an odds ratio with a Wald-based CI and p-value
- `366-374` [high] **linked x2** — declare the hypothesis supported if the CI-consistent risk difference is significant, but fall back to declaring it supported on the p-value alone if that first check fails, only rejecting support when p is non-significant
