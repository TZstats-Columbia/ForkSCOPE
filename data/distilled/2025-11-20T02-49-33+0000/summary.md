# 2025-11-20T02-49-33+0000  (ai)

- code: 264 lines, 21% exon (55 lines in 17 decisions)
- intron: print 107, comment 75, other 14, import 10, config 3
- prose: 199 lines, 93 claims (43 action, 50 result)
- links: 66 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 4
- result_claims_deferred: 50

## Silent decisions — executed, never disclosed

- **67-68, 86-89** [medium] split the sample by dark_skin and compute crude (unadjusted) risk difference and odds ratio between groups

## All decisions

- `25` [high] **linked x3** — load the full raw player-referee dyad dataset from CSV with no pre-filtering
- `28` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skintone measure
- `31` [high] **linked x1** — restrict the sample to dyads that have a non-missing skin-tone rating
- `35` [high] **linked x4** — split continuous skin tone into a binary dark/light exposure at the 0.5 cutoff
- `38` [high] **linked x5** — drop dyads missing height, weight, or position to form the complete-case analysis set
- `41-42` [high] **linked x1** — z-standardize height and weight before entering them as covariates
- `45, 109` [high] **linked x3** — build a log(games) term and feed it in as the Poisson model's exposure offset
- `48` [high] **linked x1** — collapse red card count into a binary any-red-card outcome for the secondary model
- `67-68, 86-89` [medium] **SILENT** — split the sample by dark_skin and compute crude (unadjusted) risk difference and odds ratio between groups
- `105-108` [high] **linked x7** — specify the primary model as a Poisson GLM of red card count on skin tone adjusted for position, league, height and weight
- `110, 180-181` [high] **linked x2** — cluster the standard errors of both regression models at the player level
- `127-131, 134-135, 138-139, 142-144` [high] **linked x10** — estimate the adjusted risk difference by marginal standardization: predict counterfactual outcomes under dark_skin=0/1, convert Poisson rates to P(Y>=1) probabilities, and average
- `149-152` [high] **linked x2** — approximate the standard error of the standardized risk difference with a first-order delta-method formula instead of e.g. bootstrapping
- `155-158` [medium] **linked x8** — form a 95% CI and two-sided p-value for the risk difference using a normal-approximation (Wald) reference distribution
- `175` [high] **linked x3** — handle exposure to games in the logistic model as a log-transformed covariate rather than an offset, unlike the Poisson model
- `178-179` [high] **linked x9** — specify the secondary model as a logistic regression of any-red-card on skin tone with the same covariate set plus log games played
- `253-261` [medium] **linked x6** — declare the hypothesis unsupported by reading the small effect size, non-significant p-value, and CI spanning zero together as a null result
