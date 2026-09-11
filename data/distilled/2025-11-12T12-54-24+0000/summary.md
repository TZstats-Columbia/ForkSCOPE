# 2025-11-12T12-54-24+0000  (ai)

- code: 350 lines, 47% exon (163 lines in 22 decisions)
- intron: print 136, comment 37, import 10, config 4
- prose: 315 lines, 136 claims (41 action, 95 result)
- links: 74 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 4
- result_claims_deferred: 95

## Silent decisions — executed, never disclosed

- **56-72** [high] recode the detailed playing position into four coarse role groups, sending anything unmapped to Other

## All decisions

- `34-35` [high] **linked x2** — read in the raw player-referee dyad dataset as the analysis starting point
- `38-39` [high] **linked x1** — average the two raters' ratings into one continuous skin-tone score
- `40-43` [medium] **linked x2** — restrict to dyads rated by both raters and quantify agreement between them with a Pearson correlation
- `46-47` [high] **linked x2** — drop dyads with no skin-tone rating before proceeding
- `50-52` [high] **linked x2** — dichotomize the continuous skin-tone score at 0.5 into a dark/light exposure flag
- `53-55` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `56-72` [high] **SILENT** — recode the detailed playing position into four coarse role groups, sending anything unmapped to Other
- `73-78` [high] **linked x5** — select the covariate set for modeling and complete-case drop dyads missing any of them
- `86-89` [high] **linked x4** — z-standardize height, weight, and games before use as covariates
- `99-104, 116-118` [medium] **linked x5** — characterize the unadjusted skin-tone/red-card association with group counts, rates, a crude risk difference, and a crude odds ratio
- `132-134, 142-147` [high] **linked x7** — specify and fit the primary logistic model of any_red_card on skin_dark plus games/league/position/height/weight with SEs clustered by player
- `148-157` [high] **linked x5** — pull the skin_dark coefficient, SE, p-value, and CI from the fitted model and exponentiate to an odds ratio
- `163-166, 202-204` [low] **linked x2** — designate the adjusted risk difference as the primary estimand and the adjusted odds ratio as secondary in how results are structured
- `172-180` [high] **linked x4** — derive the adjusted risk difference as an average marginal effect via counterfactual predictions with skin_dark set to 1 vs 0
- `181-186` [medium] **linked x3** — approximate the marginal effect's standard error via the delta method, scaling the coefficient SE by the mean predicted-probability derivative
- `187-194` [medium] **linked x3** — build the 95% CI and two-sided p-value for the risk difference using a normal (z=1.96) approximation
- `223-228` [high] **linked x2** — for a stricter check, drop the middle skin-tone band and redefine exposure as very-dark vs very-light
- `234-246` [high] **linked x2** — refit the clustered logistic model on the restricted sample with the very-dark indicator replacing skin_dark
- `256-270` [high] **linked x4** — keep skin tone continuous (standardized) instead of binarizing and refit the clustered model with it
- `281-295` [high] **linked x3** — add standardized yellow-card count as an extra covariate and refit the clustered model to check robustness of the skin_dark effect
- `307-313` [high] **linked x5** — stratify the crude risk-difference comparison by league country
- `339-344` [high] **linked x10** — judge the hypothesis unsupported by checking whether the adjusted risk-difference CI crosses zero against a two-sided alpha=0.05 threshold
