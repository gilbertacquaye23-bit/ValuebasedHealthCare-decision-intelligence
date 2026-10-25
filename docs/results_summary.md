# Resource allocation policy evaluation

## Business decision

Evaluate adaptive allocation across preventive care, chronic disease management, care coordination, and readmission prevention within a fixed total resource share. Public CMS measures calibrate starting conditions; modeled allocation responses generate simulated trajectories.

## Reference run

The completed run used **2,412 hospitals**, **81 states**, and **six allocation actions**. It screened **108 hyperparameter configurations**, confirmed eight candidates across three seeds (24 confirmation runs), and trained the final selected policy for **3,000 episodes**. Final evaluation used **500 episodes per policy**.

The highest-ranked configuration used **Q-Learning**: alpha **0.10**, gamma **0.90**, epsilon decay **0.995**, and **zero planning steps**. Dyna-Q was evaluated in the same framework; the selected configuration did not use planning.

## Final policy comparison

| Measure | Tuned Q-Learning | Equal allocation |
|---|---:|---:|
| Average episode reward | 0.26846 | -0.03698 |
| Average discounted return | 0.17176 | -0.02263 |
| Final MSPB score | 0.98597 | 0.99125 |
| Final excess readmission ratio | 0.99965 | 1.00157 |
| Final normalized HVBP MSPB measure score | 0.38406 | 0.15463 |

Higher reward, discounted return, and normalized HVBP MSPB measure score are preferred; lower MSPB and excess readmission ratio are preferred. The tuned policy outperformed equal allocation on each reported metric in this simulated evaluation. The absolute reward difference was **0.30543**. Ratios of reward improvement are inappropriate here because the baseline reward is negative.

## Selection uncertainty

The selected configuration's mean confirmation reward was **0.264146**, with a seed-level standard deviation of **0.002112**. The runner-up achieved **0.264134**. Their difference is approximately **0.000013**, much smaller than observed variation across the three seeds. Selection identifies the highest-ranked tested setting; it does not establish a decisive advantage over the runner-up.

Discounted return depends on gamma. Comparisons across configurations using different gamma values do not share an identical discounting objective. The final policy and equal-allocation baseline use the same gamma of 0.90.

## Engagement relevance

The workflow demonstrates public-data integration, explicit decision modeling, repeatable policy experiments, parameter selection, and interpretation of competing business objectives. Adapting it to an organization requires operational data, intervention-response estimates, dollar costs, practical capacity limits, and an independent validation design.

## Evidence boundaries

CMS supplies observations, not internal budget allocation histories. Action responses remain simulation assumptions. The normalized HVBP MSPB measure score overlaps with spending performance and does not independently establish clinical quality improvement. Reward improvements are not measured cost savings. Three-seed confirmation is not a clinical confidence interval or a test of future-year generalization. The comparison covers equal allocation and the tested RL candidates, not every feasible operational policy.

## Supporting exports

The CSVs under `results/reference_run/` are copied unchanged from the supplied completed run. `manifest.json` records their hashes and scope. These aggregate reference exports are included for portfolio review; live input snapshots and the complete executed notebook remain local run artifacts. Subsequent runs write to `artifacts/` and do not replace this reference evidence automatically.
