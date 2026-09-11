# team-03  (human)

- code: 235 lines, 84% exon (198 lines in 7 decisions)
- intron: glue 33, comment 4
- prose: 393 lines, 67 claims (37 action, 30 result)
- links: 18 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 7
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 24
- R_only_consistent_negative: 1
- result_claims_deferred: 30

## All decisions

- `5-10, 59, 95-96, 123-127, 182, 213-214` [high] **linked x5** — define the outcome as a binomial count of red cards out of games played, linked to a linear predictor p via binomial_logit
- `11-14, 27-35, 55, 60-63, 68, 73-76, 81-85, 87, 99-104` [high] **linked x4** — treat the raters' mean skin-tone score as an ordinal 1-5 exposure, giving each category its own effect shrunk toward a fitted linear trend across categories, via non-centered parameterization
- `15-20, 36-45, 56-57, 64-65, 69-70, 77-78, 88, 105-112, 128-134, 147-156, 174-175, 183-184, 188-189, 193-194, 206, 217-224` [high] **linked x2** — adjust for player position and dyad league/country as confounders, each given its own random effect with non-centered parameterization
- `24-26, 97-98, 144-146, 215-216` [high] **linked x1** — give the model a single intercept for baseline red-card probability with a normal(0,10) prior
- `46-50, 58, 66-67, 71-72, 79-80, 89, 113-115, 165-169, 181, 186-187, 191-192, 196-197, 207, 232-234` [high] **linked x2** — add a per-dyad random effect to the linear predictor to absorb overdispersion beyond the binomial model
- `122` [low] **linked x1** — restrict the second model's sample to dyads involving dark-skin-toned players only
- `135-140, 157-164, 176-180, 185, 190, 195, 198-199, 200-203, 205, 225-231` [high] **linked x3** — model referee-country bias as a random country effect whose mean is regressed on that country's average implicit (IAT) and explicit bias scores
