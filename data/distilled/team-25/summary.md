# team-25  (human)

- code: 59 lines, 61% exon (36 lines in 16 decisions)
- intron: glue 12, print 6, comment 3, dead 1, import 1
- prose: 206 lines, 54 claims (24 action, 30 result)
- links: 34 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 6
- C_only_silent_decision: 10
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 2
- result_claims_deferred: 30

## Silent decisions — executed, never disclosed

- **1** [high] load the raw crowdstorming dataset from CSV as the analysis source
- **3** [high] drop every row with any missing value before building the working sample
- **4, 6-7** [high] restrict analysis to a random draw of 250 referees rather than the full referee pool
- **10-15** [high] z-score every model covariate (skin tone, height, weight, goals, IAT, experience) before fitting
- **37-38** [high] fit an alternate red-card model on the full unsampled data using rater1's raw rating treated as a categorical factor, with a player random intercept
- **40-41** [high] refit the same rater1 model but treat the rating as a continuous linear predictor instead of a factor
- **45-46** [high] swap in rater2's categorical rating in place of rater1 for the same model structure
- **49-50** [high] build two alternate skin-tone measures by taking the elementwise min (lower) and max (higher) of the two raters' scores
- **52-53** [high] fit the red-card model using the min-of-two-raters score as the skin-tone predictor
- **56-57** [high] fit the red-card model using the max-of-two-raters score as the skin-tone predictor

## Misaligned — code and prose disagree

- code: fit a poisson GLMM for red cards on height, weight, goals and position with a referee random intercept, holding skin tone out entirely
  - prose: a multilevel logistic regression model was used to analyze data on male soccer players in top European divisions
  - why: claim states a multilevel logistic regression was used, but decision 8 fits a Poisson GLMM

## All decisions

- `1` [high] **SILENT** — load the raw crowdstorming dataset from CSV as the analysis source
- `3` [high] **SILENT** — drop every row with any missing value before building the working sample
- `4, 6-7` [high] **SILENT** — restrict analysis to a random draw of 250 referees rather than the full referee pool
- `9` [high] **linked x1** — collapse the two raters' skin-tone judgments into one averaged score per player
- `10-15` [high] **SILENT** — z-score every model covariate (skin tone, height, weight, goals, IAT, experience) before fitting
- `18-20` [high] **linked x6** — fit a poisson GLMM for red cards on height, weight, goals and position with a referee random intercept, holding skin tone out entirely
- `22-23` [high] **linked x6** — add the standardized skin-tone score as a fixed effect on top of the baseline covariates, keeping the referee term as a plain random intercept
- `24-25` [high] **linked x1** — let the skin-tone effect vary by referee via a random slope instead of forcing it constant across referees
- `27-29` [high] **linked x11** — test whether the skin-tone effect is moderated by referees' implicit-bias (IAT) score via an interaction term
- `31-32` [high] **linked x9** — test whether the skin-tone effect is moderated by referee experience instead, dropping back to a simple random intercept
- `37-38` [high] **SILENT** — fit an alternate red-card model on the full unsampled data using rater1's raw rating treated as a categorical factor, with a player random intercept
- `40-41` [high] **SILENT** — refit the same rater1 model but treat the rating as a continuous linear predictor instead of a factor
- `45-46` [high] **SILENT** — swap in rater2's categorical rating in place of rater1 for the same model structure
- `49-50` [high] **SILENT** — build two alternate skin-tone measures by taking the elementwise min (lower) and max (higher) of the two raters' scores
- `52-53` [high] **SILENT** — fit the red-card model using the min-of-two-raters score as the skin-tone predictor
- `56-57` [high] **SILENT** — fit the red-card model using the max-of-two-raters score as the skin-tone predictor
