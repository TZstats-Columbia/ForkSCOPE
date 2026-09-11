# 2025-11-22T09-56-46+0000  (ai)

- code: 325 lines, 39% exon (126 lines in 17 decisions)
- intron: print 139, comment 50, import 9, config 1
- prose: 280 lines, 114 claims (46 action, 68 result)
- links: 41 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 3
- result_claims_deferred: 68

## Silent decisions — executed, never disclosed

- **168-173, 250-255** [high] construct 95% confidence intervals and p-values using a normal (z) approximation with a fixed 1.96 critical value, applied to both the coefficient and the risk difference

## Misaligned — code and prose disagree

- code: bin the continuous skin-tone average into light/medium/dark categories using cutpoints at -0.01, 0.25, 0.625, 1.01
  - prose: players were categorized as light skin (avg rating ≤0.25) or dark skin (avg rating ≥0.75)
  - why: claim sets the dark threshold at avg rating >=0.75; code bins dark as skin_tone_avg > 0.625
- code: bin the continuous skin-tone average into light/medium/dark categories using cutpoints at -0.01, 0.25, 0.625, 1.01
  - prose: medium skin tone (0.25<rating<0.75) was excluded from the primary analysis to create a clearer contrast
  - why: claim defines medium as 0.25<rating<0.75; code's medium bin is (0.25, 0.625]

## All decisions

- `32` [high] **linked x3** — load the full player-referee dyad dataset from CSV as the analysis universe
- `44-49` [low] **linked x2** — assess inter-rater reliability between the two skin-tone raters via Pearson correlation computed on dyads where both ratings are present
- `50-51` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous measure
- `52-58` [high] **linked x2** — bin the continuous skin-tone average into light/medium/dark categories using cutpoints at -0.01, 0.25, 0.625, 1.01
- `69-70` [high] **linked x1** — define a binary outcome for whether any red card was given (redCards > 0)
- `81-82` [high] **linked x2** — restrict the sample to light and dark skin-tone categories only, dropping the medium category
- `85-86` [high] **linked x1** — recode the skin category into a binary dark_skin exposure indicator
- `87-91` [high] **linked x3** — choose the covariate set to retain (outcome, exposure, position, league, games, height, weight, player and referee identifiers) and drop any dyad with a missing value among them
- `108-111, 117-122` [medium] **linked x1** — compute crude (unadjusted) red-card rate difference and odds ratio between dark- and light-skin players as a comparison baseline
- `133-135` [high] **linked x2** — log-transform games played (plus one) to use as a nonlinear exposure-opportunity control
- `136-137` [high] **linked x6** — specify the adjustment covariate set and functional form for the outcome model (dark_skin plus categorical position, categorical league country, log games, linear height and weight)
- `138-140` [high] **linked x2** — choose logistic regression as the model family for the binary outcome
- `141-161, 243-247` [high] **linked x5** — estimate standard errors via two-way clustering, combining player-clustered, referee-clustered, and heteroskedasticity-robust covariance estimates with the Cameron-Gelbach-Miller subtraction formula, applied both to the coefficient SE and to the full covariance matrix
- `168-173, 250-255` [high] **SILENT** — construct 95% confidence intervals and p-values using a normal (z) approximation with a fixed 1.96 critical value, applied to both the coefficient and the risk difference
- `186-188` [high] **linked x3** — exponentiate the logistic coefficient and its confidence bounds to report an adjusted odds ratio
- `202-216` [high] **linked x6** — estimate the adjusted risk difference via standardization/average marginal effects: predict outcomes under counterfactual all-dark and all-light exposure using the player-clustered model and average the difference
- `220-242, 248-249` [high] **linked x1** — derive the standard error of the nonlinear risk-difference estimate via the delta method, using a numerically approximated gradient of the average-marginal-effect function combined with the two-way clustered covariance matrix
