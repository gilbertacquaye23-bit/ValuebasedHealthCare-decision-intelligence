# Methodology and evaluation boundaries

The pipeline joins CMS HRRP, MSPB, and HVBP efficiency measures by facility ID. It creates empirical tertiles and calibrates baseline variability from the merged hospital population. Condition-level readmission aggregation and cross-release compatibility require review for each data snapshot.

Budget actions redistribute shares of a fixed total. The environment does not currently model dollar expenditures, intervention costs, capacity constraints, or measured causal intervention responses. HVBP efficiency must not be described as a direct patient outcome measure; it also overlaps conceptually with spending, so the reward components are not independent.

Action effects, mean reversion, noise scaling, and clipping bounds determine the simulated transitions. Higher policy reward means better performance under these assumptions. It does not establish that real allocation changes would improve care.

The tuning validation episodes share the CMS calibration population. Final evaluation uses different simulation seeds; there is no documented chronological hospital-data holdout. Cross-seed variation is not a clinical confidence interval. Threshold-based learning speed is measured from exploratory training reward and is not necessarily greedy-policy sample efficiency.

The agent uses one random stream for action selection and planning. Common seed values improve repeatability but do not hold action exploration random draws constant across planning counts. A more rigorous algorithm comparison should separate these random streams and use additional training seeds.

The 12-period horizon is not included in the state, which can cause finite-horizon state aliasing. This limits interpretation of the current model. Further validation should compare time-aware states, fixed-policy competitors for all six actions, structural sensitivity of action-effect coefficients, and an untouched temporal or hospital-level holdout.

For each new run, retain the exact CSV releases, download dates, measurement windows, row counts before/after joins, missingness, checksums, dependency versions, seed sets, and all candidate scores. Do not replace the original evidence with rounded README results.

## CMS score ingestion

The HVBP input prefers `mspb1_measure_score`. Values such as `1 out of 10` are parsed as 0.1 using the fraction-aware converter retained from the supplied working implementation. The internal `hvbp_efficiency_score` variable therefore represents the normalized HVBP MSPB measure score for this schema, not an overall domain score or a clinical quality measure. This reward overlaps with MSPB spending performance.

API loading continues until an empty page, with guards against repeated pages and a page limit. Local CSVs are read as strings to preserve leading zeros in identifiers. Empty prepared tables or an empty merge stop execution before training. Full live ingestion and tuning must be rerun on the target computer; offline fixture checks do not establish live API compatibility.
