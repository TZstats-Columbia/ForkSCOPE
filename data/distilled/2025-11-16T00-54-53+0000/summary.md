# 2025-11-16T00-54-53+0000  (ai)

- code: 293 lines, 29% exon (84 lines in 19 decisions)
- intron: print 143, comment 43, glue 10, import 8, config 5
- prose: 256 lines, 107 claims (32 action, 75 result)
- links: 64 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 3
- R_only_consistent_negative: 2
- result_claims_deferred: 75

## All decisions

- `28-29` [high] **linked x2** — load the full player-referee dyad dataset from CSV with no row filtering applied
- `34-35` [high] **linked x1** — average the two raters' ratings into a single continuous skin_tone score
- `37-39` [medium] **linked x1** — assess inter-rater agreement by computing the Pearson correlation between the two raters on complete cases
- `42-43` [high] **linked x1** — collapse red card counts into a binary any-red-card outcome
- `45-50` [high] **linked x2** — bin the continuous skin_tone score into Light/Medium/Dark categories at cutoffs 0.25 and 0.75
- `55-57` [high] **linked x3** — drop Medium-skin dyads and recode the remaining Light/Dark categories into a binary dark_skin treatment indicator
- `72, 75-77` [high] **linked x3** — compare unadjusted red-card rates between dark- and light-skin groups as a simple difference of group means
- `85-88` [high] **linked x7** — drop dyads with missing outcome, treatment, or covariates to define the regression sample by complete-case analysis
- `90` [high] **linked x2** — log-transform games before entering it as a model covariate
- `105-113` [high] **linked x5** — specify the primary logistic model (dark_skin adjusted for position, league, and log games) and fit it with standard errors clustered by player
- `127-129` [high] **linked x5** — exponentiate the logit coefficient and its CI to report an odds ratio as the secondary estimand
- `141-151` [high] **linked x7** — estimate the primary risk-difference estimand as the average marginal effect of dark_skin (treated as a discrete dummy), rescaled to percentage points
- `180-185` [high] **linked x5** — refit the model with height and weight added as additional covariates as a robustness check
- `192-197` [high] **linked x3** — refit the model with yellowCards added as an additional covariate as a robustness check
- `204-206` [high] **linked x3** — refit the primary model clustering standard errors by referee instead of by player as a sensitivity check
- `222-225` [high] **linked x1** — fit an interaction model between dark_skin and leagueCountry to test whether the effect varies by league
- `227-230` [high] **linked x3** — test significance of the league interaction with a likelihood-ratio test against the primary model using 3 degrees of freedom
- `236, 238-241` [low] **linked x7** — derive each league's dark_skin coefficient by adding its interaction term to the reference-category (England) coefficient
- `277-282` [high] **linked x3** — declare the result 'supported' or 'not supported' using a p<0.05 significance threshold on the adjusted risk difference
