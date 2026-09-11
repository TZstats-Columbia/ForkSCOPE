# 2025-11-22T14-03-14+0000  (ai)

- code: 424 lines, 40% exon (171 lines in 21 decisions)
- intron: print 190, comment 53, import 9, config 1
- prose: 248 lines, 122 claims (43 action, 79 result)
- links: 52 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 6
- result_claims_deferred: 79

## Silent decisions — executed, never disclosed

- **31-32** [high] load the raw player-referee dyad dataset from a fixed CSV path

## All decisions

- `31-32` [high] **SILENT** — load the raw player-referee dyad dataset from a fixed CSV path
- `38-39` [high] **linked x1** — average the two independent raters' skin-tone scores into one continuous score
- `40-42` [high] **linked x1** — drop dyads that have no skin-tone rating at all before any further analysis
- `55-65, 72` [high] **linked x1** — bucket continuous skin tone into light/medium/dark using 0.25 and 0.75 cutpoints, and derive a binary dark_skin flag from the category
- `70-71` [high] **linked x3** — restrict the primary analytic sample to only light and dark categories, discarding medium-toned players
- `73, 281, 311` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome rather than modeling card counts
- `85-99, 282-288, 312-318` [high] **linked x1** — collapse 12 granular position labels into 4 broad position groups
- `100-102, 289, 319` [high] **linked x1** — drop dyads missing height, weight, position, or league country
- `110-113, 290-292, 320-322` [high] **linked x4** — z-standardize height, weight, and games-played before using them as covariates
- `123-124, 139` [medium] **linked x2** — compute the crude/unadjusted comparison of red-card rates between light and dark groups with no covariate adjustment
- `149-150` [high] **linked x4** — choose the covariate adjustment set and outcome/exposure specification for the primary model
- `163-168, 293-297, 325-327, 343-345` [high] **linked x3** — fit the adjustment model as logistic regression by maximum likelihood with standard errors clustered at the player level
- `183-199` [high] **linked x6** — estimate the adjusted risk difference by g-computation: predict outcome probabilities setting everyone to light then everyone to dark and averaging
- `206-242` [high] **linked x4** — derive the SE, 95% CI, and p-value for the g-computed risk difference via the delta method using the model's parameter covariance
- `257-258, 298-299, 328-330` [high] **linked x5** — report the exposure effect as an odds ratio by exponentiating the model coefficient, with the model's Wald confidence interval
- `276-280` [high] **linked x3** — re-derive the light/dark grouping using more extreme cutoffs (≤0.375 / ≥0.625) as a robustness check on the threshold choice
- `310, 323-324` [high] **linked x4** — re-run the analysis treating skin tone as a continuous exposure over the full sample (including medium-toned players) instead of the binary indicator
- `342` [high] **linked x2** — add a multiplicative interaction between dark_skin and league country to test effect modification
- `351-355` [high] **linked x3** — test the interaction terms jointly via a likelihood-ratio test against the no-interaction model
- `360-364` [high] **linked x2** — back out league-specific odds ratios by summing the main effect and each interaction coefficient before exponentiating
- `397` [low] **linked x1** — report the count of dyads excluded for missing covariates by subtracting from a hardcoded constant (100527) rather than a stored pre-exclusion count
