# 2025-11-12T17-30-15+0000  (ai)

- code: 81 lines, 49% exon (40 lines in 16 decisions)
- intron: glue 18, comment 8, print 7, import 5, config 3
- prose: 256 lines, 91 claims (36 action, 55 result)
- links: 38 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 4
- result_claims_deferred: 55

## Silent decisions — executed, never disclosed

- **10** [high] load the full soccer dataset from a fixed file path as the analysis source
- **21** [high] encode the treatment indicator so that dark skin tone is coded 1 and light is the reference 0
- **42-43** [high] narrow the working data down to just the outcome, treatment, covariates, and identifiers that will enter the model

## All decisions

- `10` [high] **SILENT** — load the full soccer dataset from a fixed file path as the analysis source
- `13` [high] **linked x1** — average the two raters' ratings into a single continuous skin-tone score
- `14-16` [high] **linked x3** — bucket the continuous skin-tone score into light/dark categories using 0.25 and 0.75 cutoffs, leaving the middle range unlabeled
- `17` [high] **linked x1** — collapse red card counts into a binary outcome for having received any red card
- `20` [high] **linked x4** — drop players whose skin tone fell in the unlabeled middle band, restricting analysis to clearly light or dark cases
- `21` [high] **SILENT** — encode the treatment indicator so that dark skin tone is coded 1 and light is the reference 0
- `24-38` [high] **linked x2** — collapse the many free-text playing positions into a small set of coarse position groups (Forward/Winger, Midfielder, Defender, Goalkeeper, Other, Unknown) via keyword matching, then apply this mapping to every player
- `39` [high] **linked x1** — log-transform games played to use as a covariate instead of the raw count
- `42-43` [high] **SILENT** — narrow the working data down to just the outcome, treatment, covariates, and identifiers that will enter the model
- `44` [high] **linked x1** — one-hot encode position group and league country, dropping the first level of each as the reference category
- `50-51` [high] **linked x7** — choose the covariate/adjustment set for the regression (treatment, log games, position dummies, league dummies) and add an intercept term
- `52` [high] **linked x2** — choose to cluster standard errors by player rather than treat observations as independent
- `55-56` [high] **linked x2** — fit a logistic regression for the binary red-card outcome with cluster-robust standard errors and suppressed convergence output
- `59` [high] **linked x1** — compute average marginal effects (dy/dx at overall means) rather than reporting raw logit coefficients
- `63-66` [high] **linked x8** — designate the marginal-effect risk difference for darkSkin (with its CI and p-value) as the primary estimand to report
- `70-72` [high] **linked x5** — back out an adjusted odds ratio as a secondary estimand and build its confidence interval via a normal (1.96 SE) approximation on the log-odds scale
