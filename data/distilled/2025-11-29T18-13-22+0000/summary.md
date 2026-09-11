# 2025-11-29T18-13-22+0000  (ai)

- code: 374 lines, 34% exon (127 lines in 16 decisions)
- intron: print 169, comment 58, glue 8, import 7, config 5
- prose: 214 lines, 104 claims (55 action, 49 result)
- links: 83 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 5
- result_claims_deferred: 49

## All decisions

- `38-39` [medium] **linked x1** — pull the raw player-referee dyad table from a specific CSV file using latin-1 encoding
- `52-54, 296` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skin-tone measure
- `68-69, 71, 83` [high] **linked x8** — keep only extreme-contrast dyads (skin_avg <=0.25 or >=0.75) and dichotomize skin tone into a very-dark exposure flag at that same cutoff
- `75-76, 78, 295` [high] **linked x5** — drop dyads with fewer than 2 shared games as too unstable to use
- `84-85, 298` [high] **linked x4** — collapse the red-card count into a binary any-red-card outcome
- `86-87, 89-90, 299` [high] **linked x3** — restrict to complete cases on the chosen covariate set before modeling
- `116-118, 120-126` [high] **linked x1** — compute an unadjusted (crude) risk difference and two-proportion z-test as a baseline comparison to the adjusted result
- `152-157, 300-305` [high] **linked x1** — z-standardize the continuous covariates before entering them in the model
- `158-161, 306-307` [medium] **linked x1** — cast position and league country to categorical types for dummy-coding in the model
- `162-164, 167` [high] **linked x11** — choose the model's adjustment set and fit a logistic regression of any red card on the dark-skin flag plus games/yellowCards/height/weight/position/league/implicit-bias/explicit-bias
- `198-208` [high] **linked x11** — estimate the primary effect as a standardized/counterfactual average risk difference rather than reading off the raw logit coefficient
- `225-227, 232-234, 236-237, 238-241, 242-245, 246-247, 250-251, 254-258, 262-265` [high] **linked x15** — quantify uncertainty for the risk difference via a 500-replicate nonparametric bootstrap with a percentile CI and a normal-approximation p-value
- `277-280` [high] **linked x14** — convert the logit coefficient to an odds ratio with a Wald-based 95% CI as a secondary effect measure
- `292, 297, 308-310, 311-315` [high] **linked x1** — re-run the analysis with an alternative dichotomization threshold (dark >=0.5) on the full, non-extreme-restricted sample as a sensitivity check
- `321, 323-324, 325-329` [high] **linked x1** — re-fit the primary model dropping yellowCards from the adjustment set as a sensitivity check
- `359-369` [high] **linked x5** — classify the overall finding into SUPPORTED/BORDERLINE/SUGGESTIVE/NOT SUPPORTED tiers using p<0.05, CI-excludes-zero, and p<0.10 cutoffs
