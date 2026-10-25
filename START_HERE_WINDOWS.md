# Windows setup and execution

## 1. Open the folder

Extract the ZIP. In VS Code choose **File → Open Folder** and open the extracted `vbhc-decision-intelligence` folder containing `README.md` and `requirements.txt`.

If working in a newly cloned GitHub repository, copy these contents into that repository folder first. Keep its `.git` directory. Open a terminal with **Terminal → New Terminal**. Run the commands below one at a time from the project folder.

## 2. Create the environment

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Python 3.11–3.12 is the reference environment. The corrected package was also reported to complete on the user's Windows Python 3.14 environment. This package has not been independently tested across every Python version. Activation is optional because all commands use the environment's Python executable directly.

## 3. Run offline checks

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

These checks include the CMS text-score conversion and hospital merge regression. They do not download live CMS data.

## 4. Execute the complete workflow

```powershell
.\.venv\Scripts\python.exe scripts/run_notebook.py
```

The runner prints code-cell progress. Hyperparameter search cells can take substantially longer than data preparation cells. Completion is indicated by `Results: ...\artifacts` and a returned terminal prompt. A traceback indicates failure; the partially executed notebook is retained for diagnosis.

No notebook editing or manual kernel selection is required for terminal execution.

## 5. Inspect outputs

Open `artifacts/executed.ipynb` to view saved outputs without rerunning cells. Open `artifacts/vbhc_policy_results/` for CSV results, including:

- `cms_merged_hospital_data.csv`
- `confirmation_summary.csv`
- `selected_hyperparameters.csv`
- `final_tuned_vs_baseline.csv`
- `final_tuned_training_episode_metrics.csv`
- `final_tuned_q_table.csv`

Exact source tables are retained under `artifacts/cms_snapshot/`.

To repeat the analysis using that saved snapshot:

```powershell
.\.venv\Scripts\python.exe scripts/run_notebook.py --data-dir artifacts/cms_snapshot
```

## 6. Publish source to your GitHub repository

If you deleted the local repository too, clone it again through VS Code using **Ctrl+Shift+P → Git: Clone** and your existing repository URL. Copy the extracted package contents into the cloned folder.

Review changes in Source Control, stage the implementation files, commit, and push. The supplied `.gitignore` excludes environments, data snapshots, and generated artifacts. Before publishing benchmark claims, inspect the new run's comparison and selected hyperparameters; this package contains no assumed winning configuration.
