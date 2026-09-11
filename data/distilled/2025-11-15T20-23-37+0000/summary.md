# 2025-11-15T20-23-37+0000  (ai)

- code: 419 lines, 25% exon (103 lines in 17 decisions)
- intron: print 172, comment 79, plot 50, import 10, config 4, glue 1
- prose: 323 lines, 75 claims (29 action, 46 result)
- links: 43 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 8
- result_claims_deferred: 46

## Silent decisions — executed, never disclosed

- **34** [high] point the analysis at a specific local CSV file as the full data source

## All decisions

- `34` [high] **SILENT** — point the analysis at a specific local CSV file as the full data source
- `40` [high] **linked x2** — average the two raters' skin-tone ratings into a single continuous skinTone score
- `43` [high] **linked x2** — collapse the red card count into a binary any-red-card outcome
- `46-47, 309` [high] **linked x3** — binarize the continuous skin-tone score into dark/light categories at a 0.5 cutoff (preserving missingness), and mark that same cutoff on the descriptive plot
- `50-65` [high] **linked x1** — bucket detailed position strings into a small set of position groups (Forward/Midfielder/Defender/Goalkeeper/Other/Unknown) via substring matching, then apply it to every row
- `68` [medium] **linked x2** — log-transform games played before using it as a model covariate
- `71` [high] **linked x3** — restrict the analysis sample to rows with non-missing skin tone, dropping the rest
- `102-105, 113-114` [high] **linked x2** — compute the crude (unadjusted) red-card-rate difference between skin-tone groups and test it with a chi-square test on the 2x2 table
- `144, 150` [high] **linked x5** — specify and fit the primary model as a logistic regression of any red card on skin tone adjusted for log games, position group, and league country
- `166-176` [high] **linked x5** — derive the primary effect as a standardized (g-computation) risk difference by predicting outcomes under counterfactual all-dark and all-light skin tone and averaging
- `183-192, 195-210, 213-214` [medium] **linked x2** — estimate the standard error of the standardized risk difference via the delta method using a numerically approximated gradient
- `219-221` [high] **linked x1** — build a 95% Wald confidence interval around the risk difference
- `227-228` [high] **linked x2** — test the risk difference with a two-sided z-test
- `231-235, 374` [high] **linked x3** — declare statistical significance (and later, whether the hypothesis is 'supported') using a 0.05 alpha threshold
- `244-247` [high] **linked x3** — report the secondary effect as an adjusted odds ratio by exponentiating the model's skin-tone coefficient and its CI
- `266-275` [high] **linked x3** — run a sensitivity analysis that redefines skin tone as extreme groups (<=0.25 vs >=0.75), discarding the middle range, and refits the same adjusted model on that subset
- `282-288` [high] **linked x4** — run a sensitivity analysis treating skin tone as a continuous predictor instead of binarized, refitting the same adjusted model
