# 2025-11-29T09-34-51+0000  (ai)

- code: 406 lines, 43% exon (175 lines in 17 decisions)
- intron: print 122, comment 63, other 36, import 6, config 4
- prose: 286 lines, 91 claims (53 action, 38 result)
- links: 58 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 15
- result_claims_deferred: 38

## All decisions

- `37-38` [high] **linked x1** — load the raw player-referee dyad CSV with a fixed text encoding as the full working dataset
- `47-50` [high] **linked x1** — average the two independent raters' skin-tone scores into a single continuous skin_tone_avg measure
- `51-53` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `54-56` [high] **linked x2** — log-transform games played with a +0.5 offset to use as an exposure control
- `57-74` [medium] **linked x2** — bucket free-text player positions into five coarse categories via keyword matching, defaulting unmatched or missing values to Unknown
- `79-82` [high] **linked x7** — drop dyads lacking a skin-tone rating from the analysis sample
- `96-125, 126-132, 141-143` [high] **linked x10** — search a set of candidate skin-tone cutoffs, fit an adjusted logit for each, rank by p-value, and lock in the cutoff giving the strongest result as the exposure definition used downstream
- `149-164` [high] **linked x10** — fit the primary model as a covariate-adjusted logistic regression of any red card on the dark-skin indicator, with games/position/league as controls
- `176-188` [high] **linked x7** — choose the average marginal effect (risk difference) as the headline estimand and the odds ratio as a secondary one
- `204` [high] **linked x2** — additionally report a one-sided p-value obtained by halving the two-sided value
- `215-233` [medium] **linked x1** — cross-check the model-based risk difference with a marginal-standardization (g-computation) estimate
- `256-280` [high] **linked x2** — re-fit the adjusted model at several alternative skin-tone cutoffs as a robustness check
- `286-290, 295-299` [high] **linked x2** — redefine exposure as an extreme-groups contrast, dropping the middle skin-tone band and comparing only the lightest vs darkest players
- `317-318, 320-324` [high] **linked x3** — restrict the sensitivity sample to dyads with at least two games and re-fit the primary model
- `342-343, 345-349` [high] **linked x4** — restrict to players with known height and weight and add those anthropometric variables to the model's adjustment set
- `374-375` [medium] **linked x2** — declare the hypothesis supported based on the primary result
- `392` [high] **linked x1** — state a fixed alternative-threshold RD range as summary evidence rather than pulling it from the computed sensitivity results
