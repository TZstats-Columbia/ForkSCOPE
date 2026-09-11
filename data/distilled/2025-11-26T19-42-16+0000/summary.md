# 2025-11-26T19-42-16+0000  (ai)

- code: 306 lines, 44% exon (135 lines in 13 decisions)
- intron: print 114, comment 46, import 6, config 5
- prose: 238 lines, 70 claims (44 action, 26 result)
- links: 36 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 12
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 11
- result_claims_deferred: 26

## Silent decisions — executed, never disclosed

- **49-66** [high] buckets free-text position strings into Goalkeeper/Defender/Midfielder/Forward/Unknown via keyword matching

## All decisions

- `31-33` [high] **linked x1** — reads the full player-referee dyad CSV as the analysis universe before any filtering
- `39-42` [high] **linked x2** — averages the two independent raters' scores into one continuous skin-tone measure
- `43-45` [high] **linked x1** — collapses the red-card count into a binary any-red-card indicator
- `46-48` [high] **linked x2** — log-transforms total games played to serve as an exposure-adjustment term
- `49-66` [high] **SILENT** — buckets free-text position strings into Goalkeeper/Defender/Midfielder/Forward/Unknown via keyword matching
- `67-70` [high] **linked x2** — drops dyads with no skin-tone rating, defining the complete-case analysis sample
- `99-103` [high] **linked x5** — picks the outcome/exposure/covariate columns for the primary model and drops any dyad missing one of them
- `104-106` [high] **linked x1** — rescales cumulative yellow cards into a per-game disciplinary-history rate
- `113-129` [high] **linked x9** — specifies the primary logistic model of any-red-card on continuous skin tone adjusted for exposure, position, league, physical size and disciplinary rate, fit with heteroskedasticity-robust (HC1) errors
- `136, 144-191` [high] **linked x6** — defines and applies the adjusted risk-difference and odds-ratio estimands via counterfactual predictions at skinTone=0 vs 1, with a delta-method SE for the risk difference and a 95%-CI (alpha=0.05) normal approximation
- `218, 221, 224-225` [high] **linked x2** — excludes goalkeepers and refits the primary specification on field players only
- `232, 235-236, 239-252, 255` [high] **linked x3** — dichotomizes skin tone at the 0.5 midpoint, refits the model with the binary indicator in place of continuous skin tone, and derives its risk difference and a 1.96-multiplier odds-ratio CI
- `258, 261, 264-265` [high] **linked x2** — restricts to dyads with at least 3 games and refits the primary specification on that stable-dyad subsample
