# 2025-11-21T03-54-46+0000  (ai)

- code: 429 lines, 28% exon (118 lines in 20 decisions)
- intron: print 126, plot 87, glue 75, comment 10, import 9, config 4
- prose: 215 lines, 102 claims (44 action, 58 result)
- links: 52 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 8
- result_claims_deferred: 58

## Silent decisions — executed, never disclosed

- **64-66** [high] derive player age as a fixed season year (2012) minus birth year

## All decisions

- `34` [high] **linked x3** — pull in the raw player-referee dyad dataset from a fixed file path as the entire analysis scope
- `40-41` [high] **linked x2** — average the two raters' skin-tone ratings into a single continuous skin_tone score
- `48-49` [high] **linked x2** — binarize red-card count into an any-red-card outcome using a >0 threshold
- `60-61` [high] **linked x2** — drop dyads with missing skin-tone rating to define the working sample
- `64-66` [high] **SILENT** — derive player age as a fixed season year (2012) minus birth year
- `67-84` [high] **linked x1** — collapse detailed position strings into coarse buckets (Forward/Midfielder/Defender/Goalkeeper/Other/Unknown)
- `87-90, 94, 322-323` [high] **linked x3** — cut continuous skin tone into light/medium/dark categories at 0.375/0.625 and derive a binary dark_skin indicator from it
- `92-93` [high] **linked x3** — drop the medium skin-tone category so the primary analysis compares only light vs dark
- `99-101, 220-221, 226` [high] **linked x2** — recode exposure as a median split of skin tone for a sensitivity specification
- `114-115, 222, 260` [high] **linked x1** — drop dyads whose position could not be classified (Unknown)
- `116-117, 223, 261` [high] **linked x1** — complete-case exclusion of dyads missing height or weight
- `118-119, 224, 262` [high] **linked x2** — log-transform games played to adjust for playing-time exposure
- `134-136` [medium] **linked x1** — compute the unadjusted (crude) risk difference between light and dark skin groups as a comparison point
- `150-151` [high] **linked x8** — choose the regression adjustment set (log_games, position, league, height, weight, age)
- `153-159, 228-233, 264-269` [high] **linked x5** — fit a logistic regression with standard errors clustered at the player level
- `170-173, 249-250, 275-276` [high] **linked x4** — exponentiate the logit coefficient to report an adjusted odds ratio as the secondary estimand
- `190-199, 235-242, 278-283` [high] **linked x2** — use average marginal effects (dydx, overall) as the primary risk-difference estimand
- `201-205` [medium] **linked x4** — rescale the marginal-effect risk difference from a proportion to percentage points for reporting
- `257` [high] **linked x2** — use continuous skin_tone as the exposure instead of a categorical cut, for a second sensitivity specification
- `421` [high] **linked x4** — declare the hypothesis 'supported' only if p<0.05 and the adjusted risk-difference CI lower bound exceeds zero
