# PREDICTA AI — execution and deployment runbook

## Local release gates
Recommended runtime: **Python 3.12**. Create a virtual environment first; do not install packages into the global interpreter unnecessarily.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install 'nbclient>=0.10,<1' 'ipykernel>=6.29,<8'
python -m pytest -q
python -m scripts.validate_notebook
python -m scripts.deployment_check
python -m scripts.train_release
python -m scripts.preflight
python -m scripts.deployment_check --strict
streamlit run app.py --server.port 8501
```

**macOS/Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install 'nbclient>=0.10,<1' 'ipykernel>=6.29,<8'
python -m pytest -q
python -m scripts.validate_notebook
python -m scripts.deployment_check
python -m scripts.train_release
python -m scripts.preflight
python -m scripts.deployment_check --strict
streamlit run app.py --server.port 8501
```

The training command needs network access for the **authentic** GitHub NASA C-MAPSS files unless they are already placed in `data/raw/`. The following are **outputs**, not included in the ZIP:
- `artifacts/predicta_fd001_model.joblib`
- `artifacts/run_manifest.json`
- `data/sample/engine_history.csv`

The notebook creates additional measured artifacts during execution. If required artifacts are missing, the strict deployment check fails by design.

## CI release option
1. Push source to an authorized GitHub repo (no secrets and no fake trained model).
2. On GitHub Actions, manually dispatch `Train NASA model release`. This trains with real data, uploads an artifact for review, and **does not commit it back to GitHub**.
3. Download and inspect the release artifact and evaluation reports. Explicitly include only the validated serving artifacts on the deploy branch (respect `.gitignore` and size limits).
4. In Streamlit Community Cloud, **Create app → existing app → select repository, branch, `app.py` → Advanced settings → Python 3.12 → Deploy**. Authentication may be needed, and the UI may change.
5. Smoke-test the actual live URL for real predictions, uploads, planner, metrics, error handling, desktop/mobile. Only then mark deployed.

## Public website requirements
Analytics-only interface. No portfolio, interview, recruiter or CV text. NASA data are physics simulations; no aircraft safety decisions. Python 3.15 lazy imports remain an experimental module, not production.

## Failure and uncertainty
If data download, CI authorization, trained model release, Streamlit Cloud access, or Playwright is blocked, record *which gate failed*, actual commands and logs, and what remains. Never replace artifacts with dummy data or claim a fake public URL.
