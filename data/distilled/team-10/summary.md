# team-10  (human)

- code: 352 lines, 31% exon (109 lines in 26 decisions)
- intron: comment 143, print 100
- prose: 538 lines, 83 claims (43 action, 40 result)
- links: 60 (9 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 7
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 4
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **9, 10, 11, 12, 13, 14, 15, 22** [high] z-score standardize continuous variables before modeling
- **133, 235, 277, 319** [high] estimate unadjusted skin-tone/outcome association controlling only for games, per outcome
- **156-168** [high] aggregate tone/scoring-rate/BMI to club level, binarize tone at the same >3 threshold to count black-coded players per club, merge back and standardize
- **171** [high] test unadjusted association of club-average skin tone with red cards alongside individual tone
- **183, 189, 259, 262** [high] test IAT/explicit-prejudice moderation of both individual and club-average tone effects
- **210** [high] add club-level count of African-appearing players as covariate alongside categorical tone
- **215, 218, 301, 304** [high] test IAT/explicit-prejudice moderation of both the categorical tone effect and club-level black-count effect

## Misaligned — code and prose disagree

- code: choose which player-level variables to correlate against skin tone as a confound screen
  - prose: player age was not included in any analyses because a player's age at each particular match/referee pairing could not be determined
  - why: code correlates daysold (player age) against skin tone in the confound screen, but claim says age was not included in any analysis
- code: test club's association with skin tone
  - prose: no analyses were possible using club/league membership variables because each player was linked to only one 2012-2013 club while red-card data spanned multiple years
  - why: decision tests club's association with skin tone, an analysis using the club variable the claim says was impossible
- code: fit models testing whether club and whether position predict the disciplinary outcome, repeated for every outcome
  - prose: no analyses were possible using club/league membership variables because each player was linked to only one 2012-2013 club while red-card data spanned multiple years
  - why: decision fits models testing whether club predicts the disciplinary outcomes, contradicting claim that no club analyses were possible
- code: choose club+position as the confound adjustment set for the skin-tone model, per outcome
  - prose: no analyses were possible using club/league membership variables because each player was linked to only one 2012-2013 club while red-card data spanned multiple years
  - why: decision uses club as a covariate in the primary adjusted models, contradicting claim that club could not be analyzed
- code: add club-average skin tone as covariate alongside individual tone and position, per outcome
  - prose: no analyses were possible using club/league membership variables because each player was linked to only one 2012-2013 club while red-card data spanned multiple years
  - why: decision adds club-average skin tone as a covariate, a club-membership analysis the claim says was impossible
- code: choose club+position as the confound adjustment set for the skin-tone model, per outcome
  - prose: the model predicted red cards from fixed effects of mean skin tone, controlling for games in dyad, win/draw percentage, and alphabetically dummy-coded position, with dyads nested in referees nested in referee country, and random intercepts at each level
  - why: code adjusts for club + position, but claim lists covariates as games, win/draw percentage, and position (no club)
- code: choose club+position as the confound adjustment set for the skin-tone model, per outcome
  - prose: win percentage, draw percentage, and position were used as covariates in all primary analyses, and loss percentage was also included since the three percentages are linearly dependent
  - why: claim lists covariates as win/draw/loss percentages and position; code's adjustment set is club and position
- code: choose club+position as the confound adjustment set for the skin-tone model, per outcome
  - prose: the same nesting structure and same covariates (position, win percentage, draw percentage, games per dyad) were supported for the yellow-card and total-bookings analyses
  - why: claim says yellow/bookings used covariates position, win%, draw%, games; code uses club and position
- code: add club-average skin tone as covariate alongside individual tone and position, per outcome
  - prose: other possible confounds, such as clubs having a more aggressive playing style and possibly more darker-skinned players, could not be adequately assessed in this data set
  - why: code adds club-average skin tone (and club black-count) as covariates, assessing the club confound the claim says could not be adequately assessed

## All decisions

- `4-5, 41, 44, 47, 50-51, 54-55, 58-61, 64, 67-68, 71, 74-75` [high] **linked x10** — set referee/country grouping factors and compare nested random-effects structures (fixed vs random intercept, referee vs country vs nested, with/without random tone slope) via LRTs to pick the specification used later
- `8` [high] **linked x1** — average two raters' ratings into one continuous skin-tone score
- `9, 10, 11, 12, 13, 14, 15, 22` [high] **SILENT** — z-score standardize continuous variables before modeling
- `18` [high] **linked x1** — compute BMI from weight and height via standard formula
- `21` [high] **linked x1** — combine card types into one bookings score, weighting yellow-red double
- `25` [high] **linked x2** — compute losing rate as defeats per game
- `28` [high] **linked x1** — compute scoring rate as goals per game
- `31-32` [high] **linked x3** — dichotomize skin tone into African-appearing vs. not via <3/>3 threshold, dropping the ambiguous middle category
- `86, 89-92, 95-97, 100-103, 106-107` [high] **linked x2** — build a player-level table aggregating match stats by player x club x position (with missing position recoded to 'unknown'), merge the aggregates, derive player-level rates
- `110` [medium] **linked x5** — choose which player-level variables to correlate against skin tone as a confound screen
- `113-114` [high] **linked x2** — test position's association with skin tone, excluding unknown-position players
- `117-118` [high] **linked x1** — test club's association with skin tone
- `122, 126, 226, 230, 268, 272, 310, 314` [high] **linked x3** — fit models testing whether club and whether position predict the disciplinary outcome, repeated for every outcome
- `133, 235, 277, 319` [high] **SILENT** — estimate unadjusted skin-tone/outcome association controlling only for games, per outcome
- `138, 239, 281, 323` [high] **linked x11** — choose club+position as the confound adjustment set for the skin-tone model, per outcome
- `144, 244, 286, 328` [high] **linked x5** — test IAT as a moderator of the skin-tone effect via interaction term
- `150, 249, 291, 333` [high] **linked x5** — test explicit prejudice as a moderator of the skin-tone effect via interaction term
- `156-168` [high] **SILENT** — aggregate tone/scoring-rate/BMI to club level, binarize tone at the same >3 threshold to count black-coded players per club, merge back and standardize
- `171` [high] **SILENT** — test unadjusted association of club-average skin tone with red cards alongside individual tone
- `177, 254, 296, 338` [high] **linked x2** — add club-average skin tone as covariate alongside individual tone and position, per outcome
- `183, 189, 259, 262` [high] **SILENT** — test IAT/explicit-prejudice moderation of both individual and club-average tone effects
- `195` [high] **linked x2** — rerun confound-adjusted red-card model swapping continuous tone for categorical tonecode
- `202, 205` [high] **linked x1** — test IAT/explicit-prejudice moderation of the categorical skin-tone effect on red cards
- `210` [high] **SILENT** — add club-level count of African-appearing players as covariate alongside categorical tone
- `215, 218, 301, 304` [high] **SILENT** — test IAT/explicit-prejudice moderation of both the categorical tone effect and club-level black-count effect
- `343, 346` [medium] **linked x2** — for total bookings, test moderation of a model mixing categorical tonecode with continuous club-average tone; object naming here doesn't match the following report calls, unlike every parallel block
