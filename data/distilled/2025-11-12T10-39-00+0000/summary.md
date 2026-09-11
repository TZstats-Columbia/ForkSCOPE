# 2025-11-12T10-39-00+0000  (ai)

- code: 301 lines, 35% exon (104 lines in 17 decisions)
- intron: print 87, glue 64, comment 38, import 8
- prose: 252 lines, 107 claims (38 action, 69 result)
- links: 33 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 11
- result_claims_deferred: 69

## Silent decisions — executed, never disclosed

- **105-110** [high] one-hot encode position and league with drop_first=True, fixing the omitted category as the implicit reference level
- **162-163** [medium] construct the odds-ratio confidence interval via a manual normal (Wald) approximation on the log-odds scale using a fixed 1.96 multiplier, rather than the model's own CI method

## All decisions

- `28-29` [high] **linked x2** — read the raw player-referee dyad dataset from a fixed CSV path as the analysis input
- `32-34` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `35-37` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `38-44` [high] **linked x2** — bucket the continuous skin tone score into Light/Medium/Dark categories using fixed cutpoints at 0.375 and 0.625
- `45-61, 226` [high] **linked x1** — collapse detailed playing positions into four broad position groups via a hand-built lookup table
- `62-65` [high] **linked x2** — restrict the analysis sample to Light and Dark players only, dropping Medium, and encode Dark as the treatment indicator
- `94-97, 111-116` [high] **linked x6** — choose which covariates enter the primary adjustment model (games, position group, league, height, weight) and build the corresponding design-matrix column list
- `98-99` [high] **linked x4** — handle missing covariate/outcome data by complete-case (listwise) deletion rather than imputation
- `105-110` [high] **SILENT** — one-hot encode position and league with drop_first=True, fixing the omitted category as the implicit reference level
- `121-124` [high] **linked x3** — fit the primary effect as a linear probability model (OLS on the binary outcome) with standard errors clustered by player rather than by referee or dyad
- `140-141` [medium] **linked x1** — declare statistical significance using a 0.05 two-sided alpha threshold
- `150-157` [high] **linked x1** — add a secondary logistic-regression specification to express the same contrast as an odds ratio
- `162-163` [medium] **SILENT** — construct the odds-ratio confidence interval via a manual normal (Wald) approximation on the log-odds scale using a fixed 1.96 multiplier, rather than the model's own CI method
- `185-188` [high] **linked x1** — add an unadjusted (no-covariate) sensitivity model regressing outcome on darkSkin alone
- `200-218` [high] **linked x4** — re-run the effect model using the continuous skinTone score instead of the dichotomized category, then rescale the per-unit coefficient by 0.5 to approximate the light-to-dark contrast
- `227-230` [high] **linked x2** — for the three-category sensitivity model, keep all rows with non-missing skin-tone category (including Medium) instead of excluding them
- `236-241` [high] **linked x2** — fit a three-level categorical model of skin tone with Light set as the reference category
