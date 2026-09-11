# 2025-11-22T00-10-57+0000  (ai)

- code: 311 lines, 25% exon (78 lines in 17 decisions)
- intron: print 103, comment 71, plot 48, import 8, config 2, glue 1
- prose: 304 lines, 77 claims (31 action, 46 result)
- links: 37 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 8
- result_claims_deferred: 46

## Silent decisions — executed, never disclosed

- **48** [high] encode dark skin tone as the positive class of a binary indicator (dark=1, light=0)

## Misaligned — code and prose disagree

- code: bin the continuous skin-tone score into three ordinal categories (light/medium/dark) using cutpoints at 0.375 and 0.625
  - prose: players were classified as light skin (mean rating 0.00-0.375) or dark skin (0.75-1.00) for the primary analysis, with medium-skin players (0.375-0.625) excluded to maximize contrast
  - why: code classifies dark as skinTone>0.625, but claim states the dark range is 0.75-1.00
- code: bucket free-text playing positions into five keyword-matched categories (Goalkeeper/Defender/Midfielder/Forward/Other)
  - prose: player position was simplified from 12 detailed positions into 4 broad categories
  - why: code buckets positions into five categories (Goalkeeper/Defender/Midfielder/Forward/Other); claim states four broad categories

## All decisions

- `25` [high] **linked x2** — load the full player-referee dyad dataset from a fixed CSV path as the analysis population
- `31` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `34` [high] **linked x3** — collapse red-card counts into a binary any-red-card outcome (redCards>0)
- `40-42` [high] **linked x2** — bin the continuous skin-tone score into three ordinal categories (light/medium/dark) using cutpoints at 0.375 and 0.625
- `45, 108` [high] **linked x2** — drop medium-toned players from the primary comparison by mapping them to missing and then filtering rows on that missingness
- `48` [high] **SILENT** — encode dark skin tone as the positive class of a binary indicator (dark=1, light=0)
- `51-52` [medium] **linked x1** — derive age as the fixed season year 2012 minus birth year, coercing unparseable birthdates to missing
- `55-70` [high] **linked x1** — bucket free-text playing positions into five keyword-matched categories (Goalkeeper/Defender/Midfielder/Forward/Other)
- `96-97` [low] **linked x2** — compute the crude, unadjusted red-card rate difference between light- and dark-skinned groups as a supplementary comparison
- `111-112` [high] **linked x2** — restrict to complete cases by dropping rows missing any of a chosen covariate set (position, height, weight, age, implicit/explicit bias)
- `133-136` [high] **linked x4** — specify and fit the primary logistic regression of any red card on dark skin adjusted for games, age, height, weight, position, league, and implicit/explicit bias measures
- `142-150` [medium] **linked x4** — convert the logistic coefficient and its confidence interval onto an odds-ratio scale for reporting
- `160-161, 167-172` [high] **linked x6** — compute the average marginal effect (risk-difference scale) of dark skin via dydx at overall covariate means
- `179, 288` [low] **linked x2** — fix the significance threshold at alpha=0.05, two-sided, for interpreting p-values
- `190-193, 194-196` [high] **linked x1** — re-estimate the primary model after dropping the implicit/explicit bias covariates, as a robustness check
- `205-213, 214-216` [high] **linked x3** — run a sensitivity analysis that reoperationalizes skin tone as a continuous exposure and re-includes the medium-toned players excluded from the primary comparison
- `307-311` [low] **linked x1** — declare the hypothesis supported based on the adjusted results
