# PREDICTA AI v3 — Quick Start

## Local setup (Windows PowerShell)

```powershell
cd PREDICTA_AI_v3_Release
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python -m scripts.validate_notebook
jupyter lab
```

Execute `notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb` using **Run All** from repository root. With internet access it retrieves NASA FD001; offline, place official `train_FD001.txt`, `test_FD001.txt` and `RUL_FD001.txt` in `data/raw/`.

```powershell
python -m scripts.preflight
streamlit run app.py
```

## Linux/macOS

```bash
cd PREDICTA_AI_v3_Release
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m scripts.validate_notebook
jupyter lab
# Run notebook on real FD001, then:
python -m scripts.preflight
streamlit run app.py
```

## Python 3.15 compatibility experiment

Python 3.15.0 stable (2026-10-09) supports PEP 810, but ML package wheels and hosting compatibility need verification. Read `docs/PYTHON_315_LAZY_IMPORTS.md` and run `experiments/python315_explicit_lazy.py` **only** with Python 3.15+. The `.python-version` file keeps stable default execution on 3.12.

## Assistant implementation prompt

Copy `PROMPT_FOR_CLAUDE_OR_CODEX.md` to Claude Code or Codex with this full folder accessible. Nothing in the public app should show CV/interview/recruiter-related text.

**Status:** Source package and automated tests are available. Genuine model training and live cloud deployment must be performed in an environment with access to the actual dataset and deployment services. The app cannot score until a trusted `.joblib` model is produced by the notebook.
