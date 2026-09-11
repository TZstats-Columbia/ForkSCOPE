# 2025-11-21T02-18-05+0000  (ai)

- code: 428 lines, 50% exon (213 lines in 20 decisions)
- intron: print 108, comment 44, plot 42, import 9, glue 7, config 5
- prose: 268 lines, 126 claims (53 action, 73 result)
- links: 67 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 18
- R_only_consistent_negative: 7
- result_claims_deferred: 73

## Silent decisions — executed, never disclosed

- **123-126** [high] one-hot encode position and league without dropping a reference column at the get_dummies step

## All decisions

- `34-35` [high] **linked x3** — pick the source CSV and load the full raw dyad-level dataset with no row filtering
- `38-39` [high] **linked x1** — collapse the two raters' skin-tone scores into a single measure by averaging them
- `40-55` [high] **linked x1** — bucket the continuous skin-tone score into Light/Medium/Dark using cutpoints 0.25 and 0.625
- `56-58` [high] **linked x1** — collapse the red-card count into a yes/no indicator for whether any red card occurred in the dyad
- `59-74` [high] **linked x1** — fold the many raw position labels into four buckets (Goalkeeper/Defender/Forward/Midfielder) via keyword matching
- `75-77, 79-80` [low] **linked x3** — quantify how well the two raters agree, via Pearson correlation and exact-match rate, on the non-missing subset
- `91-98` [high] **linked x4** — restrict the working sample to dyads with complete data on skin tone category, position, height and weight, dropping everything else
- `123-126` [high] **SILENT** — one-hot encode position and league without dropping a reference column at the get_dummies step
- `127-129` [medium] **linked x3** — z-score height and weight before putting them in the model
- `130` [medium] **linked x3** — log-transform the games-played count instead of using it raw
- `131-149` [high] **linked x4** — assemble the regression design matrix: encode skin tone as Dark/Medium indicators with Light left as reference, pick which position and league dummies enter (Defender and one league omitted as reference), and choose the final covariate set alongside the binary outcome
- `150-154` [high] **linked x7** — fit a logistic regression as the outcome model, with standard errors clustered on player rather than left unclustered
- `166-204` [high] **linked x7** — define the primary effect as a covariate-adjusted risk difference: hold every other covariate at its sample mean (0 for the standardized ones) and contrast predicted P(red card) for Dark vs Light skin tone
- `210-230, 347-360` [high] **linked x5** — quantify uncertainty on the predicted probabilities via a parametric bootstrap (10,000 draws from the coefficient sampling distribution), using the percentile method for the CI and a two-sided proportion-based p-value
- `243-248` [high] **linked x3** — report a secondary effect as an adjusted odds ratio, with its CI built from a Wald normal-approximation around the log-odds coefficient rather than the bootstrap
- `262-264, 270-289` [high] **linked x4** — re-estimate the same model clustering standard errors by referee instead of player, and recompute the bootstrap risk-difference CI/p-value under that alternative clustering
- `325-332` [low] **linked x1** — add error bars to the unadjusted rate chart using a normal-approximation (Wald) standard error for a proportion
- `333-339` [low] **linked x1** — narrow the position-by-skin-tone crosstab down to four hand-picked position labels for the panel 3 display
- `413-416` [low] **linked x2** — state exclusion counts as fixed literal numbers (21407; 124621 minus final N) rather than values computed from the actual filtering steps applied earlier
- `417-423` [high] **linked x13** — declare the hypothesis supported or not by thresholding the bootstrap p-value at 0.05, and characterize the risk difference's size in the accompanying text
