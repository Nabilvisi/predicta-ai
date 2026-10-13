# MASTER PROMPT — Codex: PREDICTA AI final training, QA, GitHub and Streamlit deployment

Paste this into **Codex running in the extracted repository root**. Also provide the local `CODEX_USAGE_OPTIMIZATION_UPDATED.md` if useful. Execute the task rather than merely outlining it, while obeying authorization and access boundaries.

## Objective
Deliver a **working PREDICTA AI engineering analytics site** from this existing project, with empirical model artifacts trained on authentic NASA C-MAPSS FD001 and reproducible notebook results. Deploy via GitHub → Streamlit Community Cloud if authenticated access is supported; otherwise deliver verified sources, release artifacts, and exact remaining user actions. **No CV/interview/recruiter/portfolio content in the public UI.**

## 0. Discover installed Codex tools and protect the current setup
- Read `AGENTS.md`, `DESIGN.md`, `docs/CODEX_SKILL_PLUGIN_PLAYBOOK.md`, `docs/DEPLOYMENT_STREAMLIT_CLOUD.md`, `README.md`, and the existing notebook overview. Respect existing instructions and previous work.
- Inspect current Codex version, workspace instructions, installed skills, plugin/MCP list and CLI tools (`rtk`, `playwright-cli`, `gh`, Python). **Installation handoff is not proof that a tool is installed.**
- Use installed skills and plugins selectively. Do **not** reinstall them, change global Codex files, run arbitrary remote installation scripts, or stack token-rewriting hooks. If a needed tool is absent, use standard safe alternatives and note the gap.
- Use RTK for condensed noisy output only if operational. Obtain raw logs to diagnose errors. Optional `ccusage` can report local estimates, **not** official quota.

## 1. Baseline source and dataset validation
- Stay on the existing **Streamlit + Python** stack. Do not introduce a Next.js migration in this release.
- Inspect `app.py`, `predicta/core.py`, tests, `.github/workflows`, `.streamlit/config.toml`, requirements, and notebook. Read scope-specific contents; avoid dumping all files.
- Record Python version and baseline dependencies. Use Python **3.12** for the trusted run and deployment. Check package compatibility; only test 3.15 lazy imports in its experiment file, never deploy it as a blanket substitution.
- Run `python -m pytest -q`, `python -m scripts.validate_notebook`, `python -m scripts.deployment_check` (source-only), and review failures. Make minimal fixes, add targeted tests.
- Use only the **authentic NASA FD001 train, test, RUL files** from the documented GitHub dataset, record file hashes/source URL. Clearly label C-MAPSS **physics-simulated**.

## 2. Train + evaluate with documented leakage controls
- Run `python -m scripts.train_release` in a Python 3.12 environment with network access, or the corresponding manual documented download if necessary.
- Keep the whole modeling methodology in the existing `.ipynb`: narrative Markdown + Python, cleaning, EDA, grouped splits, feature engineering, baselines, dimensionality reduction/feature selection, hyperparameter tuning, independent held-out evaluation, interpretability, and deployment serialization.
- Verify engine-wise separation, official test labels, training/inference feature parity, meaningful metrics (MAE, RMSE, calibration coverage), failed-case analysis, and reproducible seeds. Be vigilant about look-ahead and training-data leakage.
- Never invent model metrics, train on dummy data for production artifacts, or show deterministic confidence claims beyond observed empirical coverage.
- Run `python -m scripts.preflight` and `python -m scripts.deployment_check --strict`; publish only if these pass.

## 3. Build a polished science-first UI using available skills
- Read `DESIGN.md`. Select exactly **one** available design lead: `frontend-design` OR `design-taste-frontend`. When neither is present, follow `DESIGN.md` directly.
- Preserve current Streamlit structure, and make meaningful changes only: analytical hierarchy, clear model readiness, datasets and units caveats, accessible colors and responsive plots, useful loading/errors, usable navigation and exports. Avoid gimmicky 3D or heavy animations unrelated to interpretation.
- Run `web-design-guidelines` on changed UI files if available, then resolve actionable findings.
- Use **Playwright CLI** when installed. Start `streamlit run app.py --server.headless true --server.port 8501`, inspect actual port; open `http://localhost:8501` (NOT the Next.js sample `localhost:3000`). Snapshot/screenshot desktop and mobile; navigate Overview, Sensor Explorer, RUL Prediction, Maintenance Planner, Sensitivity Lab, Model Diagnostics, Data Contract; inspect errors and prediction state. If CLI absent, use supported browser/HTTP smoke tests and identify missing coverage.
- Any source-only page must correctly show a model-not-trained state, never made-up inference.

## 4. Release and GitHub publish (when authorized)
- Run full verification: focused unit tests, notebook format/validation, preflight/strict source/artifact check, GitHub workflow syntax/source review, and Playwright smoke tests.
- Prefer already connected **GitHub plugin/MCP** for repository files, branches, commit/PR, and workflow run if actually available and permitted. Alternatively use authenticated `gh` or Git CLI. Do not assume the current machine or Codex has a connected GitHub plugin merely because the project docs mention it.
- Check remote identity and repository name before creating/updating anything. Avoid destructive force-push and overwriting user work. For existing repositories: create a reviewable branch/PR when appropriate. Do not embed credentials in repo/config/docs.
- `.gitignore` excludes validated model files and sample CSV by default. Package and publish **only trusted** release artifacts required at runtime; if using a git-ignored file use explicit reviewed inclusion or LFS/release storage and test Cloud availability. Do not publish raw unnecessary files or secrets.
- CI workflow `Train NASA model release` is manual and provides an artifact for review; do not claim it deploys automatically. For GitHub-bound tasks, report confirmed repo/commit/Actions run IDs and status, otherwise state pending.

## 5. Host on Streamlit Community Cloud
- When authenticated deployment access is available: configure repository, branch `main` (or verified target branch), entrypoint `app.py`, Python 3.12 in Advanced settings, and inspect build logs. Streamlit Community Cloud's official docs: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- If no approved Streamlit Cloud access/interface is available, **do not fake completion**. Give explicit authenticated UI steps at https://share.streamlit.io/ using known repo and branch values; do not fabricate a URL.
- Test actual public URL (when obtained) with Playwright CLI if available, including predicted RUL from **real** model, input uploads, planner exports, data provenance, warnings, mobile layout and console/browser failures. Return verified link.

## 6. Final acceptance report, concise and truthful
Report: (a) skills/plugins detected and actually used; (b) file changes; (c) test commands/results; (d) authentic dataset provenance; (e) official test metrics **only after actual training**; (f) checked model artifact names and hashes; (g) GitHub repository/commit/workflow link only if real; (h) Streamlit URL only if live; (i) outstanding access or deployment blockers. No placeholder artifacts or results presented as successful deployment. Do not finish with only a generic plan when executable next steps are available.

### Non-negotiables
- No interviewer, resume, CV, or recruiter-facing content anywhere in the deployed app.
- The real data are simulated engine sensor histories, not production-certified aviation maintenance data.
- Python 3.15 native lazy import is opt-in experimental, not a reason to break the production runtime.
- Skills improve process/quality; they do not guarantee fewer Codex quota units.
- Do not push/deploy to accounts without verified identity and authorization.
