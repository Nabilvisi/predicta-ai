# Changelog

## v3.3 End-to-End ML Execution & Promoted Champion Release (2026-10-13)

- Executed all 46 cells of `PREDICTA_AI_Advanced_Machine_Learning.ipynb` end-to-end against authentic NASA C-MAPSS FD001 data.
- Evaluated 7 estimators on disjoint validation engines: Random Forest selected as champion (Val MAE: 18.080 vs Ridge 19.580).
- Evaluated champion on 100 official test engines: MAE 17.605 cycles (vs Ridge baseline 19.426 cycles), RMSE 22.653 cycles (vs 24.997 cycles), R² 0.7028.
- Preserved authentic Ridge baseline (`predicta_fd001_baseline_ridge.joblib`) and 5-cycle regression fixture (`baseline_engine_history.csv`).
- Populated all interactive diagnostics: official test predictions (100 engines), permutation importances (49 features), model comparison (7 models), sensor reference stats (21 sensors), and input drift features (PSI).
- Modernized Streamlit UI per `DESIGN.md`: dark palette, top context ribbon, tabular number metric formatting, reduced motion support.
- Added automated Playwright test suite (`scripts/ui_playwright_audit.py`) verifying all 7 tabs, mobile responsiveness, and zero-recruiter policy.
- Published dedicated GitHub repository: `https://github.com/Nabilvisi/predicta-ai`.

## v3 packaging + Python 3.15 readiness (2026-10-13)

- Retained the v2 notebook, analytical Streamlit UI, core features and CI tests.
- Extended the notebook with a runtime-report cell and release validation checklist.
- Added PEP 810-compatible `__lazy_modules__` opt-in for Plotly at app module scope.
- Added a **Python 3.15-only** native `lazy import` example, separate from baseline code.
- Added experimental Python 3.15 CI job and multi-version non-experimental CI matrix.
- Added automated weekly dependency-update pull requests (Dependabot).
- Added reproducible setup guide, interpreter deployment policy, assistant master prompt and packaged deliverable.
- Preserved public product UI without recruiter or interview material.

## v2 analytical upgrade

- Added FD001 data validation, grouped model selection, RUL regression and intervals.
- Added fleet priority, sensor history, statistical deviations, sensitivity simulation and app diagnostics.
- Added six original unit tests and release preflight.
