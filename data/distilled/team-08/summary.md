# team-08  (human)

- code: 192 lines, 78% exon (150 lines in 25 decisions)
- intron: comment 15, print 12, glue 7, config 6, plot 2
- prose: 239 lines, 75 claims (33 action, 42 result)
- links: 29 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 8
- R_only_unbacked_action_claim: 17
- R_only_consistent_negative: 0
- result_claims_deferred: 42

## Silent decisions — executed, never disclosed

- **16-17, 62-64, 88-93** [high] recode RateAve into a 3-level scenario S6 (exactly 1 / under 3 / otherwise), test mean redCards across the groups, and follow up with SNK, Tukey and LSD pairwise comparisons at alpha .05
- **22-34** [high] pull in the full coded, missing-deleted crowdstorming sheet as the analysis dataset, reading the full cell range with the header row as variable names
- **96-98, 99-107** [high] build a per-game red-card rate by dividing summed red cards by summed games plus one, then test it against the S1 and S2 splits only
- **171-172** [medium] set variable-entry/removal significance thresholds and CI width for the regression procedure
- **173-174** [low] keep the regression intercept rather than forcing the line through the origin
- **187-188** [medium] request a Durbin-Watson statistic to check residual autocorrelation
- **189-190** [high] flag cases as outliers when their standardized residual exceeds 3 SD
- **191-192** [medium] save Mahalanobis distance and covariance/influence diagnostics as case-level variables

## All decisions

- `5-6` [high] **linked x1** — drop every case with a missing rater1 or rater2 score before any analysis
- `8-9, 114-116` [high] **linked x2** — average the two raters into a single continuous skin-tone score, computed once in Excel and recomputed identically in SPSS
- `11, 52-53, 68-71` [high] **linked x4** — binarize RateAve at the lowest possible cut (only a perfect 1 counts as 0) into scenario S1, then test mean redCards across this split
- `12, 54-55, 72-75` [high] **linked x2** — binarize RateAve at a <2 cutoff into scenario S2 and test mean redCards across the split
- `13, 56-57, 76-79` [high] **linked x1** — binarize RateAve at a <3 cutoff into scenario S3 and test mean redCards across the split
- `14, 58-59, 80-83` [high] **linked x1** — binarize RateAve at a <4 cutoff into scenario S4 and test mean redCards across the split
- `15, 60-61, 84-87` [high] **linked x1** — binarize RateAve at a <5 cutoff into scenario S5 and test mean redCards across the split
- `16-17, 62-64, 88-93` [high] **SILENT** — recode RateAve into a 3-level scenario S6 (exactly 1 / under 3 / otherwise), test mean redCards across the groups, and follow up with SNK, Tukey and LSD pairwise comparisons at alpha .05
- `22-34` [high] **SILENT** — pull in the full coded, missing-deleted crowdstorming sheet as the analysis dataset, reading the full cell range with the header row as variable names
- `38-51` [high] **linked x1** — collapse the row-level data to one record per player, summing games and red cards and averaging RateAve within player
- `96-98, 99-107` [high] **SILENT** — build a per-game red-card rate by dividing summed red cards by summed games plus one, then test it against the S1 and S2 splits only
- `124-147` [high] **linked x1** — mean-center each predictor by subtracting a fixed constant (the sample mean computed earlier) rather than centering dynamically
- `148-150, 151-153` [high] **linked x1** — form two centered interaction terms (implicit bias x rater score, explicit bias x rater score) to test moderation
- `163-164, 175-176` [high] **linked x2** — fit an OLS regression with raw redCards (not the aggregated or rate version) as the outcome
- `165-166, 169-170` [medium] **linked x2** — choose which regression output to report: means/SDs/correlation matrix with significance plus coefficients, 95% CIs, R, ANOVA table, collinearity diagnostics and R-squared change
- `167-168` [high] **linked x2** — exclude any case with missing data on any regression variable (listwise) rather than pairwise or imputed
- `171-172` [medium] **SILENT** — set variable-entry/removal significance thresholds and CI width for the regression procedure
- `173-174` [low] **SILENT** — keep the regression intercept rather than forcing the line through the origin
- `177-178` [high] **linked x2** — enter game-count, win-count and playing-position dummies as the first control block before any bias measures
- `179-180` [high] **linked x1** — add referee rater score as its own block, isolating its main effect from the controls
- `181-182` [high] **linked x2** — add implicit and explicit bias measures as a third block after the controls and main rater effect
- `183-184` [high] **linked x3** — add the two bias-by-rater interaction terms last to test moderation over and above the main effects
- `187-188` [medium] **SILENT** — request a Durbin-Watson statistic to check residual autocorrelation
- `189-190` [high] **SILENT** — flag cases as outliers when their standardized residual exceeds 3 SD
- `191-192` [medium] **SILENT** — save Mahalanobis distance and covariance/influence diagnostics as case-level variables
