# 2025-11-12T13-46-32+0000  (ai)

- code: 519 lines, 35% exon (180 lines in 18 decisions)
- intron: print 131, plot 129, comment 62, import 9, config 5, glue 3
- prose: 278 lines, 160 claims (68 action, 92 result)
- links: 62 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 21
- result_claims_deferred: 92

## Silent decisions — executed, never disclosed

- **79-82** [high] choose which columns define a complete case for modeling (outcome, exposure, covariates, id fields)
- **324** [medium] require at least 100 dyads in the extreme-comparison sample before fitting a model

## All decisions

- `37-38` [high] **linked x2** — load the player-referee dyad dataset from a specific CSV file as the analytic input
- `41-43` [high] **linked x1** — average the two raters' skin-tone scores into one continuous skin-tone measure
- `44-53` [high] **linked x3** — bin continuous skin tone into Light/Medium/Dark categories using ≤0.25 / 0.25-0.75 / ≥0.75 cutpoints
- `54-56` [high] **linked x3** — define a binary any-red-card outcome from the red card count
- `57-59` [high] **linked x3** — exclude medium skin-tone dyads, restricting the comparison to light vs dark only
- `60` [high] **linked x3** — recode skin category into a binary dark_skin exposure indicator
- `62-78, 317` [high] **linked x2** — collapse detailed player positions into four broad groups (Goalkeeper/Defender/Midfielder/Forward)
- `79-82` [high] **SILENT** — choose which columns define a complete case for modeling (outcome, exposure, covariates, id fields)
- `83, 318` [high] **linked x2** — drop rows with any missing value in the selected variables instead of imputing
- `133-135, 140-144` [high] **linked x11** — fit a logistic regression of red card on dark skin adjusted for position, league and games, and report the exposure effect as an odds ratio with a 95% CI
- `158-171, 250-259, 285-295, 330-338` [high] **linked x8** — estimate the adjusted risk difference via marginal standardization: predict outcomes with everyone set to dark vs light skin and average the predicted probabilities
- `186-222` [high] **linked x2** — quantify uncertainty via parametric bootstrap: draw 5000 parameter vectors from the model's asymptotic multivariate-normal distribution and recompute RD/OR for each draw
- `223-228` [high] **linked x2** — form 95% CIs by taking the 2.5th/97.5th percentiles of the bootstrap distributions
- `244-249, 260-261` [high] **linked x4** — add height, weight and yellow cards to the adjustment set as a sensitivity check
- `277-284, 296-300` [high] **linked x9** — stratify the analysis by league, refitting the adjusted model separately within each of four selected leagues
- `315-316, 325-329, 339-340` [high] **linked x4** — restrict to the most extreme skin-tone ratings (0.0 vs 1.0) and refit the same adjusted model as a sensitivity check
- `324` [medium] **SILENT** — require at least 100 dyads in the extreme-comparison sample before fitting a model
- `507-514` [high] **linked x3** — characterize the hypothesis as 'supported with caveats' despite a small effect size, borderline significance, cross-league heterogeneity, and unaddressed clustering
