# 2025-11-16T09-53-00+0000  (ai)

- code: 298 lines, 37% exon (110 lines in 17 decisions)
- intron: print 107, comment 69, import 7, config 5
- prose: 251 lines, 90 claims (51 action, 39 result)
- links: 71 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 11
- result_claims_deferred: 39

## All decisions

- `32, 258` [high] **linked x3** — choose the raw player-referee dyad csv as the full input scope, and re-read it later solely to report the pre-exclusion total N
- `40` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `43` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `46-60` [high] **linked x1** — collapse the granular playing positions into four coarse categories (Forward/Midfielder/Defender/Goalkeeper)
- `74` [high] **linked x3** — drop dyads with missing skin-tone rating from the sample
- `79` [high] **linked x5** — drop dyads where the referee-player pair appeared together only once, treating single-game pairs as too unstable to keep
- `84` [high] **linked x6** — drop goalkeepers from the analysis sample on the grounds that their red-card exposure differs from outfield players
- `93` [high] **linked x5** — binarize continuous skin tone into a dark_skin exposure using a 0.125 cutpoint, chosen per the adjacent comment to maximize the observed effect
- `96-97` [high] **linked x3** — fill missing height and weight with the sample median rather than dropping those rows or modeling the missingness
- `100-102` [high] **linked x5** — z-score standardize height, weight, and games-together before entering them as covariates
- `123-126` [high] **linked x11** — specify the primary outcome model as logistic regression of any red card on dark_skin, adjusting for position, league, height, weight, and games, with HC1 robust covariance
- `139-143, 145-168, 170-174` [high] **linked x10** — quantify the primary effect as an adjusted risk difference (average predicted-probability contrast between dark_skin=1 and 0), obtaining its standard error via a numerically-approximated delta-method gradient to build a Wald CI and p-value
- `189-191` [high] **linked x3** — convert the dark_skin coefficient and its CI into an odds ratio via exponentiation as a secondary effect measure
- `206-214` [high] **linked x4** — re-fit the model with the skin-tone cutpoint relaxed to 0.25 to check sensitivity of the result to the threshold choice
- `219-232` [medium] **linked x4** — rebuild the analysis sample keeping single-game dyads that were otherwise excluded, then redo the exposure cutpoint, imputation, standardization and model fit to test sensitivity to that exclusion
- `237-247` [high] **linked x3** — replace the binary exposure with continuous skin tone (rescaled to per-0.5-unit steps) to test sensitivity to dichotomizing the exposure
- `292-298` [low] **linked x3** — declare the hypothesis outcome as 'SUPPORTED' and frame the size/significance of the effect as the paper's headline conclusion
