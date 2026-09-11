# 2025-11-29T08-36-37+0000  (ai)

- code: 407 lines, 32% exon (131 lines in 16 decisions)
- intron: print 166, comment 55, glue 39, import 11, config 5
- prose: 253 lines, 89 claims (43 action, 46 result)
- links: 46 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 7
- result_claims_deferred: 46

## Silent decisions — executed, never disclosed

- **112-114** [medium] derive player age relative to a fixed 2012 reference year from birthday

## All decisions

- `35-37` [high] **linked x1** — read the raw player-referee dyad table from a fixed local CSV path as the analysis universe
- `41-43` [high] **linked x1** — average the two independent raters' skin-tone scores into one continuous exposure measure
- `56-58` [high] **linked x1** — drop dyads with no skin-tone rating (missing photo) before analysis
- `62-64` [high] **linked x1** — collapse red-card counts per dyad into a binary any-red-card outcome
- `65-66, 71` [high] **linked x1** — restrict the analysis sample to complete cases on height and weight covariates
- `83-86` [high] **linked x4** — dichotomize skin tone at the 0.5 midpoint into dark-skin vs light-skin exposure groups
- `94-109` [high] **linked x1** — collapse detailed playing positions into four broad position categories via a custom mapping function
- `112-114` [medium] **SILENT** — derive player age relative to a fixed 2012 reference year from birthday
- `115-120` [high] **linked x2** — z-standardize age, height, weight, games, and yellow cards before using them as model covariates
- `158-166` [high] **linked x8** — fit the primary logistic regression of any-red-card on dark-skin exposure adjusted for position, league, age, height, weight, games and yellow cards, clustering standard errors by referee
- `187-199` [high] **linked x7** — compute the average marginal effect (adjusted risk difference) for dark_skin and its two-sided p-value via a normal-approximation z-test
- `217-223` [high] **linked x3** — exponentiate the dark_skin log-odds coefficient and its confidence interval into an odds ratio
- `248-249, 250-254, 255-257, 258-261, 262-264` [high] **linked x5** — rescale skin tone into 0.25-unit steps and refit the adjusted logistic model with continuous exposure to test a dose-response relationship
- `276-279, 280-281, 282-286, 287-289, 290-293, 294-296` [high] **linked x5** — restrict the sample to extreme skin tones (>=0.75 or <=0.25) and refit the adjusted model contrasting very-dark vs very-light players
- `305-306, 307-311, 312-314, 315-318, 319-321` [high] **linked x5** — restrict the sample to dyads with at least two games together and refit the adjusted model
- `401-403` [low] **linked x1** — assume a 1.2% baseline red-card rate to convert the risk difference into a relative percentage increase for interpretation
