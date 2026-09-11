# 2025-11-29T08-52-24+0000  (ai)

- code: 258 lines, 48% exon (125 lines in 18 decisions)
- intron: print 110, comment 12, import 6, config 5
- prose: 207 lines, 100 claims (56 action, 44 result)
- links: 70 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 12
- result_claims_deferred: 44

## All decisions

- `28-29` [high] **linked x2** — pull in the full raw dyad-level CSV as the starting dataset with no row filtering
- `32-34` [high] **linked x1** — collapse the two raters' scores into a single continuous skin-tone measure by averaging
- `35-37, 73` [high] **linked x1** — collapse red-card counts into a yes/no outcome using a >0 cutoff, applied both at the dyad level and again after aggregation
- `38-39` [high] **linked x3** — drop rows lacking a skin-tone rating rather than imputing them
- `43-53` [high] **linked x1** — regroup granular playing positions into four coarse buckets via a hand-built lookup table
- `54-57` [high] **linked x2** — backfill missing height and weight with the sample median rather than dropping those rows
- `62-72` [high] **linked x4** — change the unit of analysis from dyad to player, summing exposure/outcome counts and taking the first value for everything else
- `74` [high] **linked x2** — log-transform total games so exposure enters the model on a log scale
- `79-80` [high] **linked x5** — drop goalkeepers from the analytic sample entirely
- `89, 91-95, 98-115, 118-119, 122-123` [high] **linked x14** — scan a grid of candidate skin-tone cutoffs, refit at each, and keep whichever cutoff produces the largest estimated effect
- `96, 140, 210, 222` [high] **linked x7** — fix the same covariate set (exposure, position, league, height, weight) to adjust for across every model specification
- `97, 139, 141, 211, 223` [medium] **linked x2** — commit to a logistic regression as the estimator for the binary outcome across the search, primary, and two robustness fits
- `146-148, 153-159` [high] **linked x11** — use average marginal effects (at='overall') on the dark_skin term as the headline risk-difference estimate, pulling out its SE, CI, and p-value
- `168-173` [medium] **linked x3** — re-express the fitted coefficient as an odds ratio with a Wald-style CI as a secondary estimand
- `185-196` [high] **linked x5** — additionally report a crude, unadjusted risk difference between groups with its own normal-approximation CI and z-test
- `207-209, 212-213` [high] **linked x2** — rerun the primary model swapping in a fixed alternative cutoff (0.375) to check sensitivity of the effect to threshold choice
- `218-221, 224-225` [high] **linked x3** — rerun the model on the player set that still includes goalkeepers, using a fixed 0.25 cutoff, to check sensitivity to the goalkeeper exclusion
- `230-238` [high] **linked x2** — swap the whole modeling approach to a Poisson rate model on raw red-card counts with log(games) as an offset, reporting a rate ratio instead of a risk difference
