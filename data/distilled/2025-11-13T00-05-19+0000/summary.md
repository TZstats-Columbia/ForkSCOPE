# 2025-11-13T00-05-19+0000  (ai)

- code: 367 lines, 36% exon (131 lines in 20 decisions)
- intron: print 98, comment 53, plot 46, glue 25, import 9, config 5
- prose: 293 lines, 66 claims (35 action, 31 result)
- links: 43 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 9
- result_claims_deferred: 31

## Silent decisions — executed, never disclosed

- **78-79** [medium] encode dark skin tone as the exposure indicator (1) versus light (0)

## Misaligned — code and prose disagree

- code: bin the continuous skin-tone score into light/medium/dark categories using fixed cutpoints (0.375, 0.625)
  - prose: skin tone was dichotomized using thresholds of ≤0.375 for light skin (n=89,107) and ≥0.75 for dark skin (n=15,990)
  - why: code bins dark skin above the 0.625 cutpoint; claim states the dark threshold is ≥0.75
- code: bin the continuous skin-tone score into light/medium/dark categories using fixed cutpoints (0.375, 0.625)
  - prose: players with medium skin tone ratings (0.375–0.75) were excluded to create a clearer contrast between groups
  - why: code sets the medium band upper bound at 0.625; claim states medium spans 0.375–0.75

## All decisions

- `31` [high] **linked x1** — load the full soccer dyad dataset from a fixed csv path as the analysis population
- `34-35` [high] **linked x2** — average the two independent raters' scores into one continuous skin-tone measure
- `37-41` [high] **linked x2** — bin the continuous skin-tone score into light/medium/dark categories using fixed cutpoints (0.375, 0.625)
- `43-44` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome indicator
- `46-61` [high] **linked x1** — map free-text position strings into a small set of position categories (Forward/Midfielder/Defender/Goalkeeper/Other) via keyword matching, then apply it to every row
- `63-66` [high] **linked x1** — derive player age by subtracting birthdate from a chosen fixed mid-season reference date (2013-01-01)
- `74-75` [high] **linked x4** — drop medium skin-tone dyads and restrict the analytic sample to the light-vs-dark comparison
- `78-79` [medium] **SILENT** — encode dark skin tone as the exposure indicator (1) versus light (0)
- `81-84` [high] **linked x1** — drop dyads with missing position, age, height, or weight to form a complete-case analytic sample
- `98-105` [low] **linked x1** — select which variables and summary statistics (sum/mean) to tabulate by exposure group for the descriptive table
- `108-111` [medium] **linked x2** — compute the crude, unadjusted risk difference and implicit risk ratio between exposure groups before covariate adjustment
- `122-127` [high] **linked x2** — z-score standardize the continuous covariates (games, age, height, weight) before entering them in the model
- `129-139` [high] **linked x1** — dummy-code position category into indicator variables, leaving Midfielder as the implicit reference level
- `149-155` [high] **linked x7** — choose logistic regression as the model family and pick the adjustment set of covariates (darkSkin, standardized games/age/height/weight, position dummies, league country, referee bias scores) for the outcome model
- `168-183` [high] **linked x4** — estimate the adjusted risk difference via g-computation, setting exposure to all-dark and all-light counterfactual scenarios and averaging the model's predicted probabilities
- `197-198` [medium] **linked x3** — choose the number of bootstrap resamples (200) used to characterize sampling variability
- `203-209, 211-226, 230` [high] **linked x1** — resample dyads with replacement, refit the same logistic model and g-computation procedure on each resample to build a bootstrap distribution of the risk difference
- `232-234` [high] **linked x2** — construct the 95% confidence interval from the 2.5th/97.5th percentiles of the bootstrap distribution
- `236-237` [high] **linked x3** — define a two-sided bootstrap p-value as twice the proportion of bootstrap estimates at or below zero
- `252-261` [medium] **linked x4** — extract the exposure coefficient and use its Wald-based standard error/CI to report an exponentiated odds ratio as the secondary estimand
