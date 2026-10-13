# PREDICTA AI — Codex project instructions

## Mission
Finish and deploy the existing **Streamlit + Python** predictive-maintenance analytics project. The authoritative ML workflow is `notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb`. Do not rebuild it as a generic website, do not replace empirical results with synthetic numbers, and do not put CV, interview, recruiter, or portfolio text in the public app.

## Engineering boundaries
- Real NASA C-MAPSS FD001 data only for reported experiments. It is **physics-simulated**, not actual equipment telemetry.
- Use engine-disjoint train/validation/calibration and official test data for final evaluation. Never fit preprocessing or feature selection on held-out engines.
- Ensure shared `predicta/core.py` transformations are identical between notebook and serving, and retain strict inference checks.
- Preserve current `app.py`, tests, and GitHub Actions workflows unless a verified defect requires targeted changes.
- Python **3.12** is the deployment baseline. Keep Python 3.15 `lazy import` inside `experiments/` until its dependencies and hosting runtime are demonstrated compatible.
- Training must be separate from the Streamlit serving path. No trained artifact means no numerical predictions; never show mock scores as real measurements.
- Use descriptive, scientific UI copy with appropriate uncertainty and simulation disclaimers.

## Skill / plugin routing (verify local availability; do not presume installation)
- Use RTK for verbose supported shell commands **if found**; raw output for accurate errors and stack traces. `ccusage` is observability only.
- For design, use `frontend-design` **or** `design-taste-frontend` as the lead, never both simultaneously; read `DESIGN.md` first. Apply useful guidance to **Streamlit**, do not introduce Next.js merely to use a skill.
- After changes, invoke `web-design-guidelines` if available, scoped to modified UI files.
- Use `playwright-cli` if available to test real local URL (normally `http://localhost:8501`) and eventual public app. Inspect the actual bound port.
- Use connected GitHub plugin/MCP if available and authorized, else `gh`/Git only where authenticated. Streamlit Cloud requires explicit account access; no fabricated deployment URL.
- Do not install third-party skills, duplicate hook systems, or modify global Codex configuration without a specific need and approval.

## Efficient implementation
1. Read `CODEX_DEPLOYMENT_MASTER_PROMPT.md` and `docs/CODEX_SKILL_PLUGIN_PLAYBOOK.md`.
2. Make a minimal evidence-based plan; inspect relevant files only.
3. Run focused unit tests, then notebook validation, then real-data training and strict preflight.
4. Validate critical Streamlit interactions with Playwright when available. Fix observed failures.
5. Publish only after source, model and deployment gates pass; report links only when verified.
6. Report changed files, exact commands, tests, true metrics, provenance, deployment URL (if live), and blockers. Concise output; correctness wins over token savings.
