# 2025-11-12T10-05-42+0000  (ai)

- code: 379 lines, 26% exon (97 lines in 18 decisions)
- intron: print 149, plot 65, comment 40, glue 14, import 9, config 5
- prose: 281 lines, 82 claims (41 action, 41 result)
- links: 53 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 8
- result_claims_deferred: 41

## Silent decisions — executed, never disclosed

- **31-32** [high] loads the raw player-referee dyad dataset from CSV as the analysis input

## Misaligned — code and prose disagree

- code: specifies and fits a logistic regression of any-red-card on darkSkin plus covariates, with standard errors clustered by player
  - prose: the analysis adjusted for position and yellow cards to address behavioral confounding, though could not fully rule out residual behavioral differences
  - why: claim says the model adjusted for yellow cards, but the fitted logistic covariates are only darkSkin, log_games, position, leagueCountry, height, weight — yellow cards is not in the model

## All decisions

- `31-32` [high] **SILENT** — loads the raw player-referee dyad dataset from CSV as the analysis input
- `35-36` [high] **linked x1** — averages the two raters' scores into one continuous skin-tone measure
- `37-39` [high] **linked x2** — drops rows lacking a skin-tone rating from the working dataset
- `42-49` [high] **linked x4** — cuts continuous skin tone into Light/Medium/Dark categories using 0.25/0.75 cutpoints
- `50-52` [high] **linked x3** — restricts the analysis sample to the Light and Dark extremes, dropping Medium skin tone
- `55-56` [medium] **linked x1** — recodes the Dark/Light category into a 0/1 darkSkin indicator
- `57` [high] **linked x3** — defines the outcome as receiving any red card (count>0) rather than using the red card count
- `58-60` [high] **linked x1** — log-transforms games played for use as a model covariate
- `61-64` [high] **linked x2** — drops rows missing height, weight, position, leagueCountry, or games covariates
- `89-90` [medium] **linked x1** — computes the raw unadjusted risk difference between dark- and light-skinned groups
- `93-95` [medium] **linked x1** — assesses inter-rater agreement via correlation between the two raters' skin-tone scores
- `106-107, 110-115` [high] **linked x14** — specifies and fits a logistic regression of any-red-card on darkSkin plus covariates, with standard errors clustered by player
- `144-148, 149-154, 155-157, 195-208` [high] **linked x6** — estimates the adjusted risk difference by g-computation: predicting outcomes under counterfactual all-dark vs all-light skin tone and averaging, including within each bootstrap refit
- `171-172` [high] **linked x1** — chooses a nonparametric bootstrap with 1000 resamples to quantify uncertainty in the risk difference
- `182, 186-194, 209-214` [high] **linked x2** — resamples dyads with replacement, refits the logistic model on each resample, and accumulates the per-resample risk difference, skipping failed fits
- `217-220` [high] **linked x4** — derives a 95% CI for the risk difference from the 2.5th/97.5th percentiles of the bootstrap distribution
- `221-223` [high] **linked x3** — computes a two-sided bootstrap p-value by doubling the smaller tail proportion of the distribution relative to zero
- `238-240` [high] **linked x4** — converts the darkSkin logistic coefficient and CI into an odds ratio via exponentiation as the secondary estimand
