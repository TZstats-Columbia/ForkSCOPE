# 2025-11-26T23-31-05+0000  (ai)

- code: 355 lines, 44% exon (157 lines in 18 decisions)
- intron: print 135, comment 52, import 7, config 4
- prose: 326 lines, 130 claims (64 action, 66 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 23
- R_only_consistent_negative: 15
- result_claims_deferred: 66

## All decisions

- `34` [high] **linked x1** — pull the raw player-referee dyad table in from a fixed CSV path rather than any other source or vintage of the data
- `38` [high] **linked x1** — collapse the two raters' scores into one continuous skin-tone score by simple averaging
- `40-55` [high] **linked x1** — derive age from a hand-rolled birthday parser pinned to a Jan-1-2013 reference date, silently returning missing on any parse failure
- `56-58` [high] **linked x1** — collapse the red-card count into a yes/no outcome at the any-red-card-at-all threshold
- `59-75` [high] **linked x1** — roll free-text playing positions up into a small fixed set of position buckets via keyword matching, with a leftover Unknown bucket
- `84-93` [high] **linked x6** — restrict the working sample to dyads with complete data on skin tone plus five covariates, dropping everything else
- `108-111, 115-120, 124-126` [high] **linked x5** — define light/dark skin as the bottom vs. top tertile of the skin-tone score and recode the comparison as a single binary contrast, discarding the middle third
- `121-123` [high] **linked x1** — drop players whose position fell into the Unknown bucket from the primary comparison sample
- `144-147` [high] **linked x11** — pick the adjustment set for the primary model: exposure, position, age, height, weight, league, yellow cards, and both referee-country bias measures
- `165` [medium] **linked x2** — commit to a logistic regression as the model family for the binary red-card outcome
- `175-186` [high] **linked x7** — designate the average marginal effect of dark_skin, evaluated overall via dy/dx, as the primary effect measure (a risk difference) rather than the raw coefficient
- `201-208` [high] **linked x5** — additionally report an adjusted odds ratio by exponentiating the dark_skin logit coefficient as a secondary effect measure
- `209-210, 246-247, 267-268, 287-288, 309-310` [medium] **linked x2** — build every odds-ratio confidence interval with a Wald normal approximation (coef +/- 1.96*SE) instead of profile-likelihood or bootstrap intervals
- `225-226, 229-245` [high] **linked x2** — rerun the whole tertile comparison with wider bottom-25%/top-25% cutoffs as a robustness check on the threshold choice
- `254-255, 258-266` [high] **linked x1** — refit the primary model with yellowCards dropped from the adjustment set to check sensitivity to that covariate
- `275-276, 279-286` [high] **linked x1** — strip the adjustment set down to just exposure and position as a minimally-adjusted comparison model
- `295-296, 299-308` [high] **linked x2** — swap the binary dark/light contrast for the raw continuous skin-tone score (full non-tertile-restricted sample) and rescale the resulting effect to a per-0.1-unit increment
- `347-352` [high] **linked x3** — declare the hypothesis 'SUPPORTED' and frame the risk difference as statistically significant and robust in the final narrative conclusion
