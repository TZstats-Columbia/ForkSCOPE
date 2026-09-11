# 2025-11-28T18-46-03+0000  (ai)

- code: 164 lines, 46% exon (76 lines in 14 decisions)
- intron: print 61, glue 10, import 9, comment 5, config 3
- prose: 251 lines, 118 claims (57 action, 61 result)
- links: 43 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 23
- R_only_consistent_negative: 17
- result_claims_deferred: 61

## Silent decisions — executed, never disclosed

- **80** [high] additionally report a one-sided p-value by halving the two-sided p-value

## All decisions

- `22-24` [high] **linked x3** — load the raw player-referee dyad dataset from a fixed CSV path with no filtering
- `27-28` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `29-31` [high] **linked x2** — drop dyads with no skin-tone rating instead of imputing or otherwise handling them
- `34-35` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `36-38` [medium] **linked x1** — log-transform games played to use as an exposure-time covariate
- `39-41` [high] **linked x3** — dichotomize skin tone at a 0.75 cutoff into dark vs. light
- `45-49` [high] **linked x8** — restrict to the extreme skin-tone dyads (0.0 or >=0.75) to build a sharper exposure contrast sample
- `57-62` [high] **linked x5** — fit a logistic regression of any red card on the extreme-groups exposure, adjusted for exposure time/position/league, with HC1 robust SEs
- `68-74, 102-106, 128-132` [medium] **linked x3** — exponentiate the exposure coefficient (and its CI) to report effects as odds ratios rather than log-odds
- `80` [high] **SILENT** — additionally report a one-sided p-value by halving the two-sided p-value
- `81-88, 107-112, 133-138` [medium] **linked x6** — derive an absolute risk difference via average marginal effects rather than relying only on the odds ratio
- `97-101` [high] **linked x2** — re-fit the same model on the full (non-extreme) sample using the binary dark_skin exposure instead of the extreme contrast
- `123-127` [high] **linked x3** — re-fit the model using continuous skin_tone as the exposure instead of any binarized version
- `158` [low] **linked x3** — declare the research hypothesis 'SUPPORTED' as the stated conclusion
