# 2025-11-22T08-00-17+0000  (ai)

- code: 439 lines, 48% exon (210 lines in 20 decisions)
- intron: print 92, plot 69, comment 47, import 10, other 6, config 5
- prose: 357 lines, 168 claims (64 action, 104 result)
- links: 74 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 15
- result_claims_deferred: 104

## Silent decisions — executed, never disclosed

- **100-108** [high] computes the raw, unadjusted difference in red-card rates between dark- and light-skin groups with no covariate control
- **177-180** [medium] discards any bootstrap replicate with fewer than 5 red-card events before fitting it

## All decisions

- `37-38` [high] **linked x1** — loads the raw player-referee dyad dataset from the soccer CSV file as the full analysis universe
- `41-43` [high] **linked x1** — builds a continuous skin-tone score by averaging the two independent raters' ratings
- `50-52` [high] **linked x3** — collapses the red-card count into a binary outcome flagging any red card at all
- `53-58, 77-78, 86-88` [high] **linked x3** — splits the continuous skin-tone score into light vs dark groups using 0.25/0.75 cutoffs, drops the excluded middle range from the sample, and encodes the result as a 0/1 indicator for modeling
- `59-76` [high] **linked x1** — collapses the many free-text playing-position labels into five coarse role buckets
- `79-85` [high] **linked x4** — restricts the analysis sample to dyads with non-missing height, weight, and referee bias scores, discarding the rest
- `100-108` [high] **SILENT** — computes the raw, unadjusted difference in red-card rates between dark- and light-skin groups with no covariate control
- `119-122` [high] **linked x12** — chooses which covariates enter the regression alongside skin tone (games, cards, goals, anthropometrics, position, league, referee bias scores)
- `123-129` [high] **linked x6** — fits a logistic regression for the model with standard errors clustered by referee rather than assumed independent
- `139-154` [high] **linked x9** — estimates the adjusted risk difference by g-computation: setting every dyad's skin tone to dark, then to light, and averaging the model's predicted probabilities under each counterfactual
- `165-169, 173-176, 181-203` [high] **linked x1** — builds a nonparametric bootstrap of the adjusted risk difference by resampling dyads with replacement, refitting the logistic model, and recomputing the standardized risk difference on each of 500 replicates
- `177-180` [medium] **SILENT** — discards any bootstrap replicate with fewer than 5 red-card events before fitting it
- `204-207` [high] **linked x5** — derives the 95% CI for the adjusted risk difference from the 2.5th/97.5th percentiles of the bootstrap distribution
- `208-213` [high] **linked x4** — computes a bootstrap p-value by doubling the one-sided tail proportion of replicates crossing zero, picking the tail from the sign of the point estimate
- `224-231` [high] **linked x10** — reports the skin-tone effect as an adjusted odds ratio by exponentiating the logistic coefficient and its confidence interval
- `242, 244-261` [high] **linked x1** — reruns the whole pipeline with a stricter light/dark cutoff (0.375/0.625) as a robustness check on the skin-tone threshold
- `264, 266-276` [high] **linked x3** — refits the outcome model treating skin tone as a continuous predictor instead of the binary light/dark split
- `277-278` [medium] **linked x1** — rescales the continuous skin-tone coefficient to express the effect per 0.5-unit increase before exponentiating
- `281, 283-291` [high] **linked x6** — reruns the model separately within each of four leagues, only reporting a league if it clears 1000 dyads and more than 10 red-card events
- `322-328, 402-427` [medium] **linked x3** — frames the statistical result as confirming the discrimination hypothesis, declaring it 'SUPPORTED', and restates that framing in the figure's summary text box
