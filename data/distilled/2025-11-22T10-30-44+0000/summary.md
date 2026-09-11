# 2025-11-22T10-30-44+0000  (ai)

- code: 318 lines, 47% exon (148 lines in 19 decisions)
- intron: print 118, comment 44, import 7, config 1
- prose: 168 lines, 75 claims (35 action, 40 result)
- links: 43 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 7
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **117-127** [high] estimate the unadjusted risk difference between skin-tone groups using a normal-approximation SE, Wald CI, and two-sided z-test

## Misaligned — code and prose disagree

- code: collapse detailed player positions into four broader categories to limit position-covariate levels
  - prose: this raises the possibility that the main effect is driven by confounding related to position subtypes or playing styles not captured by the 3-category position variable
  - why: code collapses positions into four categories; claim refers to a 3-category position variable

## All decisions

- `29-31` [high] **linked x1** — load the full soccer dataset from CSV with no sampling or filtering applied
- `35-37` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `38-40` [low] **linked x1** — restrict to dyads with both ratings present before computing the inter-rater correlation diagnostic
- `42-45` [high] **linked x1** — binarize skin tone into light/dark groups using a >0.25 cutoff as the primary exposure definition
- `46-48` [high] **linked x1** — collapse any nonzero red-card count into a binary any-red-card outcome
- `49-64` [high] **linked x1** — collapse detailed player positions into four broader categories to limit position-covariate levels
- `69-74` [high] **linked x5** — select the analysis variable set and drop any dyad missing a value on those variables (complete-case restriction)
- `90-97` [low] **linked x1** — choose which outcome/covariate summaries to compute and report broken out by skin-tone group
- `117-127` [high] **SILENT** — estimate the unadjusted risk difference between skin-tone groups using a normal-approximation SE, Wald CI, and two-sided z-test
- `142-145` [high] **linked x1** — log-transform games and yellow cards (with a +1 offset) before using them as covariates
- `146-151` [high] **linked x1** — standardize height, weight, and the log-transformed covariates to zero mean/unit scale before modeling
- `152-157, 163` [high] **linked x3** — specify and fit the primary logistic regression of any_redcard on skin tone, adjusting for position, league, games, yellow cards, height, and weight
- `172-175, 180-186` [high] **linked x4** — use the average marginal effect of skin tone from the fitted model as the primary adjusted risk-difference estimand
- `187-198` [high] **linked x3** — compute adjusted risks by setting every dyad's skin tone to light or dark and averaging model-predicted probabilities (counterfactual standardization)
- `214-216` [high] **linked x3** — exponentiate the adjusted skin-tone coefficient and its CI to report an odds ratio as a secondary effect measure
- `229-230, 232-242` [high] **linked x2** — redefine the exposure with a more stringent dark-skin threshold (>=0.5) and refit the same adjusted model as a sensitivity check
- `248-249, 251-261` [high] **linked x4** — restrict the sample to Defender/Goalkeeper dyads only and refit the adjusted model without the position covariate
- `267-268, 270-283` [high] **linked x2** — fit the adjusted model separately within each of four leagues to check effect heterogeneity across leagues
- `308-313` [medium] **linked x8** — frame the final interpretive conclusion (small effect size, cross-league heterogeneity, non-significance among defenders, possible residual confounding) rather than reporting bare statistics
