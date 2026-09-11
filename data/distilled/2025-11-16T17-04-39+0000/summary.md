# 2025-11-16T17-04-39+0000  (ai)

- code: 406 lines, 37% exon (150 lines in 19 decisions)
- intron: print 189, comment 52, import 10, config 5
- prose: 270 lines, 88 claims (48 action, 40 result)
- links: 55 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 7
- result_claims_deferred: 40

## All decisions

- `31-32` [high] **linked x1** — load the raw player-referee dyad dataset as the analysis input
- `38-39` [high] **linked x3** — average the two raters' scores into a single continuous skin_tone measure
- `54-56` [high] **linked x2** — drop dyads with no skin tone rating from the working sample
- `62-63` [high] **linked x1** — binarize the red-card count into a yes/no any_red outcome
- `73, 75-83` [medium] **linked x3** — scan several candidate cutoffs to see how the light/dark split shifts the crude risk difference before settling on one
- `87-90` [high] **linked x6** — fix 0.25 as the cutoff that splits players into light vs dark skin tone
- `104-123` [high] **linked x2** — bucket free-text position strings into six coarse position categories by keyword match
- `128-130` [high] **linked x2** — drop dyads missing height or weight before building the model dataset
- `138-140` [high] **linked x1** — one-hot encode position and league, dropping the first level of each as the reference category
- `141` [medium] **linked x1** — log-transform total games to serve as an exposure offset later
- `166-169` [medium] **linked x1** — compute the raw (unadjusted) risk difference and risk ratio between dark- and light-skin groups
- `183-189` [high] **linked x6** — fit a logistic regression of any red card on dark_skin, adjusting only for position category
- `194-197` [medium] **linked x4** — exponentiate the dark_skin coefficient into an adjusted odds ratio as the secondary estimand
- `214, 217-229` [high] **linked x4** — estimate the adjusted risk difference by predicting outcomes under all-light vs all-dark counterfactuals and averaging (g-computation)
- `244-256, 259-279` [high] **linked x3** — quantify uncertainty on the adjusted risk difference with a parametric bootstrap: draw 5000 coefficient vectors from the model's asymptotic normal distribution and recompute the risk difference each time
- `296, 301-312` [high] **linked x5** — refit as a Poisson count model of red cards with a log(games) offset, as an alternative to the binary/logistic specification
- `316, 318-324` [high] **linked x4** — refit using continuous skin_tone in place of the dichotomized dark_skin, to check sensitivity to the cutoff choice
- `329, 331-341` [high] **linked x3** — restrict to only the most extreme ratings (exactly 0 or 1) and compare those two groups directly
- `391-392, 401-402` [high] **linked x3** — declare the hypothesis supported or not based on whether the risk-difference CI's lower bound clears zero
