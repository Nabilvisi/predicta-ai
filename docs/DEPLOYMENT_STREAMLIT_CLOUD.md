# PREDICTA AI — GitHub + Streamlit Community Cloud deployment

## Current release gate (Updated 2026-10-13)

This package contains the fully validated NASA C-MAPSS FD001 Random Forest champion model (`artifacts/predicta_fd001_model.joblib`), the preserved Ridge baseline (`artifacts/predicta_fd001_baseline_ridge.joblib`), full model comparison records, permutation importance metrics, test predictions, and a 20-engine evaluation sample.

**Recommended baseline:** Python 3.12 (Python 3.15 lazy imports remain experimental). Deploy the Streamlit application (`app.py`), connected to the `main` branch of repository `Nabilvisi/predicta-ai`.

## Route A — train locally and publish

1. Create and activate a Python 3.12 virtual environment at the repository root. Install `requirements.txt`.
2. Run `python -m pytest -q` and `python -m scripts.validate_notebook`.
3. Execute the full notebook on authentic NASA FD001 records from GitHub: `python -m scripts.train_release`. This needs public internet access, and may take substantial compute time.
4. Examine the notebook's authentic NASA official-test metrics and training manifest. Check the model before promoting it; the automated tests alone do not establish model quality.
5. Run `python -m scripts.preflight` and `python -m scripts.deployment_check --strict`. Then check the UI with `streamlit run app.py` using its real test-engine sample, test a CSV upload, and test error handling.
6. Create a **public GitHub repository** and push the source files. **The model is ignored by `.gitignore` intentionally**: only after validating/trusting the artifact, explicitly include these files, for example:

```bash
git add .
git add -f artifacts/predicta_fd001_model.joblib artifacts/model_comparison.csv artifacts/permutation_importance.csv artifacts/test_predictions.csv artifacts/run_manifest.json data/sample/engine_history.csv
git commit -m "Release validated NASA FD001 inference model"
git push origin main
```

Review repository size and GitHub binary-file limits before pushing. Do not push raw datasets or secrets. Git LFS may be needed for large models; Streamlit Cloud supports LFS.

## Route B — train in GitHub Actions

1. Push the **source ZIP contents** to the GitHub repository root (not an extra nested folder).
2. In GitHub Actions, manually run **Train NASA model release** (`workflow_dispatch`). This runs the notebook on the real FD001 dataset, tests, and preflight checks, then uploads the result as a workflow artifact. It does **not** automatically publish or commit any files.
3. Inspect the run logs, model metrics and manifest. Download the generated `predicta-model-release` artifact from the run.
4. Extract its `artifacts/` and `data/sample/` paths into the repository root and add these validated files using the explicit `git add -f ...` commands above; commit and push.
5. Run the local deployment audit if possible before cloud promotion. Only execute `joblib.load` for self-generated trusted artifacts: serialized pickle/joblib files are unsafe from untrusted sources.

## Deploy the application

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and connect GitHub.
2. Choose **Create app → Yup, I have an app**.
3. Choose your repository, `main` branch and **main file path `app.py`**.
4. Under Advanced settings choose **Python 3.12**. The repository contains `requirements.txt` and `.streamlit/config.toml`.
5. Choose a public subdomain, for example `predicta-engine-health` if available; deploy.
6. Check that the real test-engine example is loaded, predicted RULs are finite, the official test metrics display correctly, CSV export works, and all analytics tabs render.
7. Check application logs and fix any missing dependency or file path problems before sharing. Never claim a public URL until the cloud platform confirms it.

Streamlit Cloud syncs with GitHub pushes. Note: To change the Python runtime of an already deployed Community Cloud app, follow the official recreate/redeploy process.

## Release gates

- Source is committed without secrets or private datasets.
- Real FD001 source recorded with SHA-256 hashes in `artifacts/run_manifest.json`.
- Trained model present and created by the trusted notebook.
- Actual model quality and calibration coverage reviewed; no placeholder metrics.
- Test data and calibration data are not used to select the final model.
- `python -m pytest -q` passes; `python -m scripts.preflight` passes.
- Streamlit app tested on a real example input and at least one invalid input.
- User-facing interface contains only engineering analytics; no CV/interview/recruitment material.
- Python 3.15 lazy imports remain opt-in until third-party package compatibility is verified.

## Official references

- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization
