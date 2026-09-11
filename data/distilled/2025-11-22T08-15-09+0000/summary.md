# 2025-11-22T08-15-09+0000  (ai)

- code: 284 lines, 36% exon (102 lines in 14 decisions)
- intron: print 119, comment 51, import 9, config 3
- prose: 190 lines, 97 claims (45 action, 52 result)
- links: 65 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 11
- result_claims_deferred: 52

## Silent decisions — executed, never disclosed

- **35-37** [high] load the raw player-referee dyad dataset from a fixed CSV path

## All decisions

- `35-37` [high] **SILENT** — load the raw player-referee dyad dataset from a fixed CSV path
- `39-41` [high] **linked x2** — average the two independent raters' skin-tone scores into a single continuous rating
- `42-44` [medium] **linked x5** — keep only dyads where both raters supplied a rating, as the basis for an inter-rater agreement check and later exclusion accounting
- `51-57, 61-63` [high] **linked x11** — collapse the continuous skin-tone score into a light/dark binary by thresholding at 0.25 and 0.625 and dropping the ambiguous middle band, then form the analysis sample from the non-dropped rows
- `58-60` [high] **linked x3** — collapse red-card counts into a yes/no indicator of ever receiving a red card in the dyad
- `64` [high] **linked x2** — recode missing player position values as an explicit 'Unknown' category rather than dropping them
- `79-80, 82, 84-85` [high] **linked x2** — tabulate raw red-card rates by skin-tone group and take their difference as a crude, unadjusted effect estimate
- `100-103, 104-110` [high] **linked x11** — fit a logistic regression of red-card receipt on skin tone, adjusting for games played, position and league country, with standard errors clustered by player
- `124-134` [high] **linked x10** — convert the logit coefficient into an average marginal effect to report the exposure effect on the risk-difference scale
- `150-154` [high] **linked x4** — exponentiate the logit coefficient into an odds ratio as a second, secondary effect-size scale
- `168-169, 171-176` [high] **linked x1** — refit the model using the continuous skin-tone score instead of the binary exposure, as a robustness check on the functional form of the exposure
- `181-182, 184-189, 190-192, 194-195, 197, 198-202` [high] **linked x4** — add a skin-tone-by-country interaction term, test it with a likelihood-ratio chi-square test against a 0.05 threshold, and if significant decompose it into country-specific odds ratios
- `250-265` [high] **linked x4** — translate the primary p-value, effect direction, and a near-null CI-lower-bound threshold (-0.002) into a categorical support/no-support verdict for the hypothesis
- `275-276, 278-279` [low] **linked x6** — report fixed, literal odds-ratio numbers for each country's heterogeneity effect in the final summary rather than the values computed earlier from the interaction model
