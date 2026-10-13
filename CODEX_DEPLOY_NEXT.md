# Codex execution handoff — training evidence and publish

The attached ZIP contains a working, serialized **real-data NASA FD001 Ridge baseline**, along with a five-cycle real test-engine example. Read `AGENTS.md`, `DESIGN.md`, `docs/BASELINE_TRAINING_REPORT.md`, and `docs/RELEASE_EXECUTION_STATUS.md` first.

Your mission is to **finish** the deployment using currently installed Codex skills/plugins, not to remake the project:

1. Discover the installed GitHub connector/CLI, Frontend Design or Taste Skill (one visual lead), Web Design Guidelines, Playwright CLI and optional RTK. Do not reinstall what is already present, overwrite global instructions, or use competing design directions.
2. Ensure `python -m pytest -q`, `python -m scripts.validate_notebook`, `python -m scripts.preflight`, and `python -m scripts.deployment_check --strict` pass. Preserve the existing trusted model file. Do not fabricate model results or compare its metrics as though the whole Jupyter Notebook had run.
3. Inspect the `artifacts/run_manifest.json`. The real-data Ridge baseline's official test MAE is ~19.43 and RMSE ~25.00 simulated cycles. Preserve provenance and the distinction between this baseline and the notebook's future champion model.
4. Create a separate **public** PREDICTA GitHub repo in my authorized account, or reuse that repo only if it already exists. Do not change unrelated projects. Push all source, docs, notebook, and the explicitly approved baseline artifacts (the model and sample are intentionally gitignored and require force-add). Never commit secrets or raw FD001 datasets.
5. Deploy the actual `app.py` from that repo to Streamlit Community Cloud with Python 3.12 and verify the page with Playwright at the actual public URL. Do not invent a URL. Test an actual sensor CSV upload, model inference and download, all tabs, mobile layout and keyboard focus. Public site must not contain any interview, CV or recruiter-facing text.
6. On GitHub Actions run **Train NASA model release**, compare the advanced notebook's real test scores to the baseline and only promote a verified champion. Review GitHub Actions logs and downloadable release artifacts. Preserve the Jupyter Markdown narrative and code, the baseline release notes, and audit trail.
7. Return actual repository and verified live website URLs; list actions, tests and any blockers. No future-work claims without launching real operations.

Optimization: follow the supplied `CODEX_USAGE_OPTIMIZATION_UPDATED.md` minimally (RTK if already installed, focused output, no unnecessary MCP additions).
