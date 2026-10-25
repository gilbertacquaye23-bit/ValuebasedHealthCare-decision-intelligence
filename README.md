# Value-Based Healthcare Decision Intelligence

A decision-support workflow for evaluating healthcare resource-allocation policies using public CMS hospital benchmarks and a transparent reinforcement learning simulation.

**Business question:** How can a fixed resource envelope be distributed among preventive care, chronic disease management, care coordination, and readmission prevention while balancing spending, readmission performance, and an efficiency-related payment measure?

## Reference results

A completed run used **2,412 CMS hospitals**, screened **108 configurations**, and evaluated the final policy over **500 episodes**. The highest-ranked confirmed configuration was **Q-Learning** (alpha 0.10, gamma 0.90, epsilon decay 0.995, zero planning steps).

| Measure | Tuned Q-Learning | Equal allocation |
|---|---:|---:|
| Average episode reward | 0.26846 | -0.03698 |
| Average discounted return | 0.17176 | -0.02263 |
| Final MSPB score | 0.98597 | 0.99125 |
| Final excess readmission ratio | 0.99965 | 1.00157 |
| Final normalized HVBP MSPB measure score | 0.38406 | 0.15463 |

These are **simulation results**, not realized savings or demonstrated clinical effects. The top two confirmed configurations were nearly tied. See the [results summary](docs/results_summary.md) for selection uncertainty and [supporting CSVs](results/reference_run/) for the exported evidence.

## Start here

Windows and VS Code instructions: [START_HERE_WINDOWS.md](START_HERE_WINDOWS.md).

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/run_notebook.py
```

On macOS/Linux, create the environment with `python3 -m venv .venv` and use `.venv/bin/python` for the remaining commands.

## Workflow

1. Load HRRP, MSPB, and HVBP CMS measures from the API or archived CSV exports.
2. Parse reported scores, prepare hospital tables, validate usable records, and merge facility identifiers.
3. Derive 81 discrete states from MSPB, discharge volume, normalized HVBP MSPB measure score, and excess readmissions.
4. Train Q-Learning and Dyna-Q policies over six allocation actions summing to 100%.
5. Evaluate planning sensitivity and search 108 hyperparameter configurations.
6. Confirm shortlisted configurations across three seeds and train the selected policy.
7. Compare with equal allocation using a common discount factor and evaluation seed.
8. Export diagnostics, selected parameters, Q-values, policy comparisons, and input snapshots.

The data preparation retains the fraction-aware converter from the supplied working implementation, including `1 out of 10 → 0.1`. Empty inputs stop before training. The 81-state formulation and tuning workflow are consolidated in one executable notebook.

## Business application

This implementation demonstrates how to structure allocation decisions, combine public benchmarks with explicit assumptions, compare policy alternatives, and communicate trade-offs. An organization-specific engagement would validate input definitions, estimate intervention responses, add operational constraints and costs, and establish monitoring before adoption.

## Outputs

`artifacts/executed.ipynb` contains executed results. CSV exports are written to `artifacts/vbhc_policy_results/`. Exact downloaded inputs are retained in `artifacts/cms_snapshot/` for local replay. The executed notebook is saved even if a run fails.

Each new run generates its own selected parameters and metrics. The versioned reference evidence under `results/reference_run/` records the completed run reviewed on October 25, 2026; subsequent runs do not overwrite it.

## Implementation

- `notebooks/healthcare_policy_optimization.ipynb`: complete ingestion, modeling, tuning, evaluation, and export workflow.
- `scripts/run_notebook.py`: command-line execution with progress and output persistence.
- `tests/test_core.py`: offline behavior and data parsing regressions.
- `.github/workflows/ci.yml`: automated dependency installation and checks.
- [Methodology](docs/methodology.md): assumptions and evaluation limits.

For archived data, supply CSVs named `hrrp.csv`, `mspb.csv`, and `hvbp_eff.csv`:

```powershell
.\.venv\Scripts\python.exe scripts/run_notebook.py --data-dir data
```

## Interpretation

CMS observations establish starting conditions and empirical variability. Allocation effects and future trajectories are simulated, not estimated causal intervention effects. The HVBP MSPB measure score overlaps with spending performance and is not an overall clinical quality score. New simulation seeds are not a temporal or hospital-level holdout. Reward changes are not dollar savings or proven patient benefits.

This is a decision-support prototype, not a live budget allocation service. See methodology for finite-horizon and planning-comparison limitations. No open-source license has been assigned; select one before authorizing reuse.
