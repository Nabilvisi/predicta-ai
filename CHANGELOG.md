# Changelog

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
