"""Execute the complete CMS workflow; downloads require network access."""
import argparse
import json
import os
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=Path, help='Folder with hrrp.csv, mspb.csv, hvbp_eff.csv')
    parser.add_argument('--timeout', type=int, default=86400, help='Maximum seconds per cell')
    args = parser.parse_args()
    if args.data_dir:
        paths = {k: str((args.data_dir / f'{k}.csv').resolve()) for k in ['hrrp', 'mspb', 'hvbp_eff']}
        for path in paths.values():
            if not Path(path).is_file():
                raise FileNotFoundError(path)
        os.environ['VBHC_LOCAL_PATHS'] = json.dumps(paths)
    output = ROOT / 'artifacts'
    output.mkdir(exist_ok=True)
    notebook = nbformat.read(ROOT / 'notebooks/healthcare_policy_optimization.ipynb', as_version=4)
    total_cells = sum(c.cell_type == 'code' for c in notebook.cells)
    progress = {'completed': 0}
    def report_cell_start(cell, cell_index, **kwargs):
        if cell.cell_type == 'code':
            progress['completed'] += 1
            print(f"Running code cell {progress['completed']}/{total_cells} (notebook cell {cell_index + 1})", flush=True)

    print(f"Starting CMS ingestion and policy evaluation. Outputs: {output}", flush=True)
    client = NotebookClient(notebook, timeout=args.timeout, kernel_name='python3', resources={'metadata': {'path': str(output)}}, on_cell_start=report_cell_start)
    try:
        client.execute()
    finally:
        nbformat.write(notebook, output / 'executed.ipynb')
    print(f'Results: {output}')

if __name__ == '__main__':
    main()
