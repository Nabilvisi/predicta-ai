# PREDICTA AI v3 — Engine Health Intelligence

Predict remaining useful life (RUL) from the NASA C-MAPSS FD001 **physics-simulated** turbofan dataset, monitor sensor behavior and rank engines using transparent, adjustable engineering-review policies. Results are research demonstrations, not certified maintenance recommendations.

## Project structure

```text
PREDICTA_AI_v3_Release/
├── notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb  # Main narrative + all ML experiments
├── predicta/core.py            # Shared validated preprocessing and inference contract
├── app.py                      # Streamlit engineering analytics application
├── tests/test_core.py          # Automated tests
├── requirements.txt
├── data/raw/                   # Auto-downloaded original NASA text files (ignored by git)
├── data/sample/                # Real example histories written after training
└── artifacts/                  # Trained model and measured evaluation outputs
```

## Implemented analytics

- Publicly available FD001 ingestion with SHA-256 file provenance.
- Schema auditing: missing values, non-finite values, duplicate engine-cycle keys and constant sensors.
- Exploratory sensor analysis, distributions, correlations and degradation time series.
- Leakage-aware partitioning by engine: train/validation/calibration plus independent official NASA test.
- Causal moving mean, variability and recent-change features.
- Regression baselines, random forest, histogram gradient boosting, PCA and SelectKBest.
- GroupKFold hyperparameter search.
- Separate-engine conformal residual intervals; empirical official-test coverage reported.
- Permutation model interpretation, comparative evaluation and exploratory PSI drift assessment.
- Model persistence, real-data inference parity checks and policy-based fleet ranking.
- Statistical sensor-deviation screening and adjustable model sensitivity experiments.
- Streamlit application: Overview, Sensor Explorer, RUL Prediction, Maintenance Planner, Model Diagnostics and Data Contract.

## Setup

Python 3.12 recommended for deployment (3.11–3.14 covered by CI; 3.15 experimental). See `docs/PYTHON_315_LAZY_IMPORTS.md`.

```bash
python -m venv .venv
# Activate the virtual environment for your OS
pip install -r requirements.txt
python -m pytest -q
jupyter lab
```

Open `notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb` in Jupyter and choose **Run All**. Execute it from the **repository root**. The dataset downloads from [PunVas/nasa-c-mapss](https://github.com/PunVas/nasa-c-mapss) on GitHub; if networking is blocked, manually place `train_FD001.txt`, `test_FD001.txt`, `RUL_FD001.txt` in `data/raw/`.

Once model artifacts have been exported:

```bash
streamlit run app.py
```

## Important deployment note

The Streamlit application requires `artifacts/predicta_fd001_model.joblib` produced by the **trusted local notebook run**. It will show a controlled not-trained state until that artifact exists. No fabricated predictions or model evaluation numbers are bundled. For cloud deployment, include the validated model and derived reports from a trusted build pipeline; note the `.gitignore` ignores model and data artifacts by default.

## Evaluation protocol and limitations

FD001 has 100 simulated run-to-failure training engines and 100 truncated test engines. Official test targets come from `RUL_FD001.txt`; the program never substitutes the last observed cycle as the true test RUL. Model selection uses distinct validation engines, and calibration uses distinct calibration engines. The unmodified official test serves final evaluation only. All metrics are generated during notebook execution.

The 90% prediction interval is calibrated on internal training-engine snapshots; the snapshot distribution can differ from official test endpoints. It therefore carries **no unconditional 90% coverage guarantee** for external inputs. PSI is a descriptive stability check, not a formally calibrated alarm. Maintenance thresholds are illustrative and do not encode real operational safety policies.

**Dataset references:** [NASA C-MAPSS simulated jet engine data](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data) · [GitHub copy](https://github.com/PunVas/nasa-c-mapss).

### Additional analytical controls

The Sensor Explorer can rank robust per-sensor deviations from the training-only median/MAD distribution. The Sensitivity Lab changes a selected sensor over the latest five recorded cycles and measures the fitted model's numerical response. Neither control establishes fault causality, and channel measurements have no guaranteed physical units.

## Release checks and Continuous Integration

GitHub Actions checks unit tests and notebook syntax on pushes and pull requests. It intentionally does not claim to train on inaccessible data in CI. After running the full notebook against the real NASA dataset, verify the trusted model and its real-data example using:

```bash
python -m scripts.preflight
streamlit run app.py
```

For hosted use, only publish the trained `.joblib` produced by the trusted training process. Place it in `artifacts/` along with optional measured CSV reports, and put the example history in `data/sample/` if you want a populated interface on first visit. The no-model state avoids displaying fabricated predictions.

## v3 package additions

- `PROMPT_FOR_CLAUDE_OR_CODEX.md`: authoritative build/deployment prompt.
- `QUICK_START.md`: Windows and Linux/macOS commands.
- `docs/PYTHON_315_LAZY_IMPORTS.md`: Python 3.15 upgrade plan and practical cautions.
- `experiments/python315_explicit_lazy.py`: Python 3.15-only syntax demo.
- `.github/dependabot.yml`: reviewed dependency update PRs.
- `scripts/validate_notebook.py`: source notebook validation without inventing results.

The default runtime remains Python 3.12. Source ZIP does not ship a fake trained model.


## v3.1 deployment kit

- `docs/DEPLOYMENT_STREAMLIT_CLOUD.md` — verified GitHub → trained release → Streamlit deployment steps and release gates.
- `scripts/train_release.py` — execute entire notebook with authentic NASA FD001 on Python 3.12.
- `scripts/deployment_check.py` — source-only and strict trained-model release audits.
- `.github/workflows/train-model-release.yml` — manual GitHub Actions pipeline that trains, tests, and publishes a downloadable validated artifact **without auto-committing**.
- `PROMPT_DEPLOYMENT_CLAUDE_CODEX.md` — standalone deployment instruction prompt.

The source package **does not include the trained model**, so it is not a live operational deployment. Training and hosted deployment must be done in an authorized networked environment.


## v3.2 Codex skills/plugins deployment handoff

Start with [`CODEX_START_HERE.md`](CODEX_START_HERE.md) and [`CODEX_DEPLOYMENT_MASTER_PROMPT.md`](CODEX_DEPLOYMENT_MASTER_PROMPT.md). The project now includes scoped Codex `AGENTS.md`, engineering `DESIGN.md`, a non-mutating `scripts/codex_readiness.py`, and a skill/plugin usage playbook. This is a handoff for the user's **local Codex** installation, not proof the named skills are installed or used there. It does not produce a live model or deployment URL.


## Authentic baseline release (2026-10-13)

A separate **authentic-data Ridge baseline** was trained using the original NASA C-MAPSS FD001 GitHub blobs, then serialized as a small self-contained model (`artifacts/predicta_fd001_model.joblib`). See `docs/BASELINE_TRAINING_REPORT.md` for the exact split, model, metrics and limitations. This does **not** mean the full 46-cell notebook has executed. The Python notebook remains the authoritative route for advanced end-to-end retraining, comparison and promotion of a new model.

The source ZIP now includes a real-data baseline bundle and a five-cycle sample from NASA test engine 1, permitting functional inference without a new download. The sample is intentionally small; upload more authentic data for meaningful multi-engine comparisons.
