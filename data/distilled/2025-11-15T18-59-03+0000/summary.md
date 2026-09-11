# 2025-11-15T18-59-03+0000  (ai)

- code: 344 lines, 23% exon (80 lines in 15 decisions)
- intron: print 105, comment 87, plot 54, import 10, glue 6, config 2
- prose: 283 lines, 117 claims (60 action, 57 result)
- links: 74 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 11
- result_claims_deferred: 57

## Silent decisions — executed, never disclosed

- **53** [medium] compute player age as a fixed reference year (2012) minus birth year rather than age at time of match

## All decisions

- `39` [high] **linked x2** — load the raw player-referee dyad dataset from CSV as the analysis source
- `43` [high] **linked x1** — average two independent raters' skin-tone scores into a single continuous skinTone score
- `46-47, 60` [high] **linked x5** — dichotomize continuous skin tone into a dark/light binary at the 0.5 cutoff, preserving missingness, then cast to an integer binary indicator for modeling
- `50` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome (any red card >0)
- `53` [medium] **SILENT** — compute player age as a fixed reference year (2012) minus birth year rather than age at time of match
- `56` [high] **linked x2** — restrict the analysis sample to dyads that have non-missing skin tone data
- `59` [high] **linked x4** — further restrict to complete cases by dropping dyads missing position, height, or weight (complete-case analysis)
- `84-85` [medium] **linked x4** — compute the unadjusted (crude) red-card rate separately for light- and dark-skin groups as a descriptive comparison
- `109-113` [high] **linked x17** — specify and fit a logistic regression of any red card on dark-skin indicator adjusting for position, league country, age, height, weight, games, and yellow cards
- `127-128` [medium] **linked x5** — exponentiate the dark-skin coefficient and its CI to report effect on the odds-ratio scale
- `149-160` [high] **linked x11** — estimate the adjusted risk difference by marginal standardization: predict outcome probabilities under counterfactual all-dark and all-light skin exposure and average the difference
- `173-209` [high] **linked x4** — propagate model uncertainty via a parametric bootstrap that draws 5000 coefficient vectors from the multivariate normal approximation to the fitted model and recomputes risk difference and odds ratio for each draw
- `210-215` [high] **linked x7** — derive percentile-based bootstrap confidence intervals and a two-sided empirical p-value from the bootstrap distribution
- `246` [high] **linked x7** — declare the hypothesis 'supported' using a specific significance rule: bootstrap CI lower bound above zero and p<0.05
- `264-269` [high] **linked x3** — redefine skin tone exposure using a stricter 0.75 threshold (very dark vs. rest) and refit the adjusted model as a sensitivity check
