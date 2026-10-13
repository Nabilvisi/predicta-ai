# PREDICTA AI — Deployment execution prompt for Claude Code / Codex

You are acting as a release engineer and ML engineer for the PREDICTA AI Streamlit application in this repository. Work from the checked-out repository root. Do not replace real results with synthetic metrics. Do not add CV, recruiter, or interview content to the public website.

## Objective

Turn this existing source-only project into a validated, cloud-deployable application. Deploy to GitHub + Streamlit Community Cloud **only when account access and authorization are available**. If access is unavailable, stop before publication and provide exact UI steps and pending blockers. Do not claim deployment is complete until you have a confirmed live URL and successful public smoke test.

## Tasks

1. Read `README.md`, `docs/DEPLOYMENT_STREAMLIT_CLOUD.md`, `requirements.txt`, `scripts/preflight.py`, `predicta/core.py`, and the full `.ipynb` before editing. Preserve the notebook as the authoritative ML development workflow.
2. Use Python 3.12 for model training and cloud deployment. Treat Python 3.15 `lazy import` as opt-in experimental only; verify third-party compatibility before considering a switch.
3. Run `python -m pytest -q` and `python -m scripts.validate_notebook`.
4. Train on **authentic NASA FD001 files** fetched from the documented GitHub source, via `python -m scripts.train_release`. Preserve provenance/SHA-256 manifest and independent test results. Do not use simulated fixtures for reported ML results.
5. Review real MAE/RMSE and coverage with meaningful statistical interpretation. Investigate suspicious values and train/serve mismatch; do not fabricate accuracy claims.
6. Run `python -m scripts.preflight` and `python -m scripts.deployment_check --strict`. Exercise sensor visualizations, RUL predictions, maintenance planner, sensitivity and diagnostics. Fix genuine defects and add tests.
7. Confirm correct cloud files: `app.py`, `requirements.txt`, `.streamlit/config.toml`, `artifacts/predicta_fd001_model.joblib`, `data/sample/engine_history.csv` and optional measured reports.
8. If explicitly authorized and authenticated, publish source and trusted release artifacts to the designated GitHub repository. Respect `.gitignore` and use `git add -f` only for the validated intended release artifacts. Never commit secrets or raw data unnecessarily.
9. If available, create the Streamlit Community Cloud app with branch `main`, entrypoint `app.py`, Python 3.12. If the platform cannot be automated, provide exact Streamlit UI instructions; do not imply cloud deployment occurred.
10. Smoke-test the actual public URL and record environment versions, trained model provenance, hosted URL and unresolved issues in a release report.

## Acceptance criteria

- One coherent `.ipynb` with narrative and executable ML work, no leakage.
- App displays real FD001 sample predictions, diagnostics and metrics.
- No model train-on-request in Streamlit serving process.
- No false maintenance safety claims: data are NASA physics simulations.
- No portfolio/interview/CV presentation anywhere in deployed interface.
- No fake URL or fabricated test score.
- GitHub CI and Streamlit Cloud deploy are functional when authorized.
