# 2025-11-22T07-51-01+0000  (ai)

- code: 330 lines, 43% exon (141 lines in 19 decisions)
- intron: print 119, comment 44, glue 14, import 11, config 1
- prose: 268 lines, 132 claims (56 action, 76 result)
- links: 66 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 19
- R_only_consistent_negative: 6
- result_claims_deferred: 76

## Silent decisions — executed, never disclosed

- **173-176** [high] strip the referee fixed effects out of the covariate set for the logit model so it doesn't hit a singularity

## All decisions

- `20-22` [high] **linked x1** — pull in the raw soccer dyad dataset from a fixed CSV path as the full universe for everything downstream
- `27-29` [high] **linked x2** — collapse the two raters' scores into a single continuous skin-tone measure by averaging them
- `30-33` [medium] **linked x4** — keep only rows where both raters supplied a score before checking how well the two raters agree
- `34-36` [high] **linked x4** — reduce the red-card count to a yes/no flag for whether a player was carded at all
- `37-46, 88-90` [high] **linked x9** — split the continuous skin-tone scale into light vs. dark groups at the 0.375/0.625 cutoffs, throw out everyone in between, and code dark as the 1-indicator
- `55-71` [high] **linked x1** — bucket free-text position strings into a fixed taxonomy of playing positions
- `76-82` [high] **linked x4** — drop anyone missing a resolvable position, height, or weight to form the complete-case analysis set
- `91-100` [high] **linked x3** — rescale height and weight onto a z-score scale for use as model covariates
- `114-120` [high] **linked x3** — characterize the raw group gap with a simple unadjusted risk difference and relative risk between dark and light groups
- `129-132` [high] **linked x10** — settle on the covariate set for the main model: position, league, games played, height, weight, plus referee fixed effects
- `139-144, 264-268` [high] **linked x4** — fit the adjusted association with ordinary least squares (linear probability model) and cluster the standard errors by player
- `150-154, 185-189, 273-277` [high] **linked x5** — translate raw model coefficients into percentage points or odds ratios and build 95% intervals with the ±1.96 normal-approximation rule
- `173-176` [high] **SILENT** — strip the referee fixed effects out of the covariate set for the logit model so it doesn't hit a singularity
- `177-179` [high] **linked x4** — swap model families and fit a logistic regression for the odds-ratio side analysis
- `208-214` [medium] **linked x1** — screen a chosen subset of predictors for multicollinearity via variance inflation factors
- `217-223` [medium] **linked x1** — flag what fraction of the linear model's fitted probabilities fall outside the valid 0-1 range as a diagnostic on the LPM choice
- `232-237, 239-246` [high] **linked x4** — run a minimum-detectable-effect calculation at 80% power and 0.05 alpha off the observed group sizes and event rate
- `247-252` [high] **linked x2** — compute Cohen's h as a standardized effect size and sort it into negligible/small/medium buckets at fixed cutoffs
- `261-263` [high] **linked x4** — rebuild the adjustment set for a sensitivity check that swaps in continuous skin tone for the binary exposure
