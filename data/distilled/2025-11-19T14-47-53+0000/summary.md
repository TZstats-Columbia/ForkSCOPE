# 2025-11-19T14-47-53+0000  (ai)

- code: 368 lines, 43% exon (158 lines in 14 decisions)
- intron: print 106, comment 46, plot 46, import 8, config 3, glue 1
- prose: 214 lines, 89 claims (50 action, 39 result)
- links: 43 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 18
- R_only_consistent_negative: 12
- result_claims_deferred: 39

## Silent decisions — executed, never disclosed

- **26-28** [high] load the raw player-referee dyad dataset from a fixed file path

## Misaligned — code and prose disagree

- code: cut continuous skin tone into light/dark groups at 0.25/0.75, drop the ambiguous middle band, and recode the surviving rows into a binary dark-skin exposure
  - prose: medium skin tone (0.375-0.625) was excluded to maximize contrast between the light and dark groups
  - why: code excludes the whole band between the 0.25 and 0.75 cutoffs; claim states the excluded medium band is 0.375-0.625
- code: cut continuous skin tone into light/dark groups at 0.25/0.75, drop the ambiguous middle band, and recode the surviving rows into a binary dark-skin exposure
  - prose: 17,015 dyads (11.7%) were excluded for medium skin tone (0.375-0.625)
  - why: code excludes the band between 0.25 and 0.75; claim states the excluded medium band is 0.375-0.625

## All decisions

- `26-28` [high] **SILENT** — load the raw player-referee dyad dataset from a fixed file path
- `36-38` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `39-41` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `42-50` [high] **linked x8** — cut continuous skin tone into light/dark groups at 0.25/0.75, drop the ambiguous middle band, and recode the surviving rows into a binary dark-skin exposure
- `55-73` [high] **linked x1** — bucket free-text player positions into a coarser set of categories (Forward/Goalkeeper/Defender/Midfielder/Winger/Other/Unknown)
- `82-85, 90-91` [medium] **linked x1** — compute the raw (unadjusted) red-card rate within each skin-tone group and take their difference as a naive risk difference
- `97-104` [high] **linked x4** — choose which covariates enter the model and drop any dyad missing one of them (listwise deletion)
- `116-123` [high] **linked x4** — specify the adjusted logistic regression model (dark skin plus covariate set) and fit it by maximum likelihood
- `128-133, 138-141` [medium] **linked x4** — summarize the adjusted dark-skin effect as an odds ratio with a confidence interval, exponentiating the logit coefficient
- `154-166` [high] **linked x4** — estimate the adjusted risk difference by g-computation: predict outcome probability for every dyad under a forced-dark and forced-light counterfactual and average the difference
- `177-211, 213-216, 219` [high] **linked x3** — quantify uncertainty on the standardized risk difference via a parametric bootstrap: draw model coefficients from their asymptotic multivariate-normal distribution, recompute the counterfactual risk difference each draw, and silently discard draws that error out
- `221-229` [high] **linked x5** — summarize the bootstrap draws into a mean/SD and a percentile-based 95% interval, and construct a two-sided p-value from the share of draws at or below zero doubled
- `244-259, 264-273` [high] **linked x4** — re-run the exposure-outcome model treating skin tone as continuous rather than dichotomized, restricting to complete cases on this variable set, then predict outcome probability at the two extreme skin-tone values and take their difference as a sensitivity-check risk difference
- `306` [high] **linked x2** — declare the hypothesis outcome as 'SUPPORTED' as a fixed reporting label rather than one derived programmatically from a pre-specified significance rule
