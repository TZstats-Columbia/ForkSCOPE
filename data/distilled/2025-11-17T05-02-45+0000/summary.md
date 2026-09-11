# 2025-11-17T05-02-45+0000  (ai)

- code: 434 lines, 45% exon (194 lines in 21 decisions)
- intron: print 185, comment 44, import 6, config 5
- prose: 209 lines, 94 claims (44 action, 50 result)
- links: 66 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 7
- result_claims_deferred: 50

## Silent decisions — executed, never disclosed

- **39-43** [high] derive player age by subtracting birth year from a fixed 2012 season-reference year, coercing bad dates to missing
- **172, 175-179** [medium] choose which covariates (age, height, weight, games) to inspect for balance across skin-tone groups

## Misaligned — code and prose disagree

- code: restrict the working sample to only the extreme light/dark groups, discarding every dyad in the middle skin-tone range
  - prose: asserts no other exclusions were applied beyond the two listed
  - why: code restricts the sample to extreme light/dark groups, discarding all middle-range skin-tone dyads, an exclusion beyond the two the claim lists

## All decisions

- `28-29` [high] **linked x2** — read the player-referee dyad file from a fixed local path as the entire analysis universe
- `32-35` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `36-38` [high] **linked x1** — collapse red-card counts into a binary any-red-card-in-dyad outcome
- `39-43` [high] **SILENT** — derive player age by subtracting birth year from a fixed 2012 season-reference year, coercing bad dates to missing
- `44-60` [high] **linked x1** — fold the many free-text position labels into five coarse role buckets by keyword matching
- `73-75` [high] **linked x2** — drop every dyad lacking a skin-tone rating from the working data
- `85-115` [high] **linked x5** — grid-search light/dark skin-tone cutpoint pairs (with a 1000-per-group minimum) and rank them by unadjusted red-card-rate gap to surface a winning threshold pair
- `127-130` [high] **linked x4** — apply the chosen cutpoints (≤0.125 light, ≥0.75 dark) to flag each dyad's skin-tone group
- `131-134` [high] **linked x2** — restrict the working sample to only the extreme light/dark groups, discarding every dyad in the middle skin-tone range
- `143-147` [high] **linked x2** — complete-case restriction: drop dyads missing height or weight
- `162-166` [medium] **linked x2** — compute the crude (unadjusted) red-card rate gap between skin-tone groups as a baseline comparison prior to modeling
- `172, 175-179` [medium] **SILENT** — choose which covariates (age, height, weight, games) to inspect for balance across skin-tone groups
- `182, 184` [medium] **linked x1** — check position-category distribution across skin-tone groups via a normalized crosstab
- `205-208` [high] **linked x3** — fit a logistic regression of any_red on dark_skin adjusted for position category and games played (model family and adjustment set)
- `209-219` [high] **linked x6** — derive the odds ratio, Wald confidence interval, and two-sided p-value for dark_skin from the fitted model as the secondary estimand
- `237-251` [high] **linked x5** — estimate the adjusted risk difference by g-computation: set every dyad's dark_skin to 1 then to 0, predict, and average the counterfactual risks
- `256-264, 268-271` [high] **linked x5** — get the risk difference's SE/CI/p-value from a simple two-proportion variance formula that treats the two group risks as independent, ignoring model-based uncertainty
- `285, 289-298, 302-311` [high] **linked x6** — robustness check: refit with an expanded adjustment set (league country, age, height, weight) and recompute its odds ratio and g-computation risk difference
- `314, 318-320, 321-327, 332-341` [high] **linked x7** — robustness check: redefine the skin-tone groups with a wider cutpoint pair (light ≤0.25, dark ≥0.5) and rerun the same model plus g-computation RD on this alternate sample
- `344, 348-355` [high] **linked x6** — robustness check: replace the binary skin-tone grouping with the continuous skin_avg score as predictor, refit on the fuller (non-extremes-only) complete-case sample
- `362, 365-372` [high] **linked x5** — robustness check: add a dark_skin × meanIAT interaction term to test whether referee-country implicit bias moderates the skin-tone effect
