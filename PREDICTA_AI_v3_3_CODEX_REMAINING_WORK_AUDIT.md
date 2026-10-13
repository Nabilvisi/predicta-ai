# PREDICTA AI v3.3 — Verified Gap Audit & Codex Completion Handoff

**Audit date:** 2026-10-13  
**Source package:** `PREDICTA_AI_v3_3_Authentic_Baseline_Deployment_Package.zip`  
**Project type:** Streamlit predictive maintenance, NASA C-MAPSS FD001 (physics-simulated).  
**Target:** Public production-style engineering research dashboard; **no interviews, CV, portfolio/recruitment content on the website.**

## Evidence-backed current state

- ZIP integrity verified; the package contains source, Streamlit app, 46-cell `.ipynb`, current baseline model (`artifacts/predicta_fd001_model.joblib`), a 5-cycle **real** NASA test-engine sample and provenance report.
- In a fresh extracted directory, completed: `python -m pytest -q` (**8 passed**), `python -m scripts.validate_notebook` (**46 cells validated for notebook JSON/Python syntax**), `python -m scripts.preflight` (**passed, 1 engine scored**), and `python -m scripts.deployment_check --strict` (**passed**).
- Real-source Ridge **baseline only**, independently trained through a deterministic JavaScript solver on source records. Official NASA test MAE **19.4263 simulated cycles**, RMSE **24.9965**. The exact test results are **not** proof of the full notebook-trained champion. 90% nominal residual interval radius ~60.26 cycles with empirical test coverage 100% (overly wide; not a production calibration claim).
- The full Python notebook has **not** executed end-to-end; all notebook code cell outputs are currently empty.
- There is **no verified public GitHub PREDICTA repository or live Streamlit Cloud URL**. The previous environment's connected GitHub account had access to existing repositories but could not create a new repository through its connector. Codex must verify its own tools/permissions.
- The Streamlit browser UI has **not** been opened or Playwright-tested. The environment used for this audit did not have Streamlit installed.

## Important missing/baseline-only analytics

The packaged release contains `artifacts/model_comparison.csv`, but it compares **Ridge alpha candidates**, not the notebook's different model families. It **does not contain**:
- `artifacts/test_predictions.csv` for the observed-vs-predicted official-test chart;
- `artifacts/permutation_importance.csv` for the feature-importance chart;
- notebook champion model or executed-training notebook;
- model bundle `sensor_reference_stats` for robust sensor-deviation and the interactive Sensitivity Lab;
- bundle `reference_features` / `drift_features` for the PSI drift section.

Thus the baseline dashboard can score the provided real sensor-history sample, but several exploratory and diagnostic sections are conditional, empty or unavailable. The supplied sample has only **one engine, five cycles**—insufficient for a meaningful fleet overview/demo. Do not present these as completed advanced analytics until true outputs are generated.

## P0 — Make the existing *baseline* website live

1. **Inspect tooling safely:** Codex and GitHub auth, Streamlit account access, `AGENTS.md`, `DESIGN.md`, any installed Frontend Design **or** Taste Skill (one lead), Web Design Guidelines, Playwright CLI, RTK. Avoid reinstalling things already installed; preserve local/global settings. Use Python **3.12** for the application. The Python 3.15 lazy-import experiment remains optional; don't make it a release blocker.
2. **Create or discover a dedicated GitHub repository**, e.g. `Nabilvisi/predicta-ai`, on the authorized account. Do not modify `reservoir-lab`, `volve-atlas`, or other unrelated repositories. Extract ZIP **contents** into repository root; do not place everything inside an additional directory.
3. **Review files and secrets**, run local tests, and stage intended release assets explicitly because `.gitignore` excludes `.joblib`, `.csv`, `.json` under `artifacts` and `data/sample/*.csv`:

   ```bash
   python -m pytest -q
   python -m scripts.validate_notebook
   python -m scripts.preflight
   python -m scripts.deployment_check --strict
   git add .
   git add -f artifacts/predicta_fd001_model.joblib artifacts/model_comparison.csv artifacts/run_manifest.json data/sample/engine_history.csv
   ```

   Do **not** commit `data/raw/*.txt`, secrets, `.env`, cache or proprietary files. Trust only the model artifact from this package or a local verified training run; `.joblib` is pickle-based.
4. **Start the actual Streamlit application** (install environment first) and perform a manual + Playwright CLI browser audit on its **actual bound port** (normally 8501). Check all seven tabs; valid/invalid CSV upload; numeric RUL prediction and bounds; error states; model badge labeling; download actions; mobile layout, keyboard accessibility, chart contrast; no interview/recruiter/CV language. Verify the warning about simulated data and limitations remains visible.
5. **Publish source and approved baseline artifacts** to GitHub, verify `main`, Actions CI, repository files, artifact availability, and permission scoping. Do not claim publication until GitHub confirms it.
6. **Deploy `app.py` to Streamlit Community Cloud** from that repository using **Python 3.12**; connect and authorize Streamlit separately. Check the build logs, startup, data loading, prediction, exports and browser behavior at the actual public URL. Do not invent the URL. Preserve a verified baseline release link and version label before considering upgrade.

## P1 — Complete the main `.ipynb` ML workflow and improve the app

7. **Install notebook execution dependencies** in the training environment: `nbclient`, `ipykernel` in addition to `requirements.txt` (the workflow installs these separately). Run the existing `Train NASA model release` GitHub Actions workflow **or** locally: `python -m scripts.train_release`. This downloads authentic `train_FD001.txt`, `test_FD001.txt`, and `RUL_FD001.txt` from the documented GitHub mirror. The workflow is **manual** (`workflow_dispatch`), and only **uploads an artifact**; it does **not** automatically commit or deploy a model.
8. **Inspect the executed notebook and real metrics:** check all 46 cells ran without error and saved outputs, data leakage prevented (engine-disjoint train/val/calibration and group-aware CV), model comparison (Dummy, Ridge, ensemble, PCA, SelectKBest, hyperparameter tuning), final selected model, official-test metrics, interval coverage/width, and feature-engineering parity with `predicta.core`. Never use official-test labels for model selection or tune thresholds on them.
9. **Review and promote the champion** only after comparing its authentic test results and reliability with the released Ridge baseline. Preserve baseline artifacts and the existing report as release history. Make explicit which model produced each metric. Update experiment manifest, version, model card, artifact hashes, release notes and scientific limitations.
10. **Fill currently empty interactive diagnostics** with generated, measured artifacts: official-test predictions, permutation importance, training sensor robust-reference statistics, drift reference features and documented thresholds/limitations. Ensure read paths/feature names are consistent and widgets never silently imply unavailable diagnostics were run.
11. **Improve demo coverage** by preparing a distinct, attribution-preserving *unlabeled* multi-engine sample from original test trajectories (not a synthetic fleet). Preserve the 5-cycle one-engine regression fixture for deterministic tests. Label the source and explain no actual failures are predicted with certainty.
12. **Run complete release validation again**, including notebook-level execution, unit/integration tests, serving parity, release preflight, CI workflows and full Playwright browser smoke tests, then publish the approved updated artifacts and verify the live site after GitHub sync.

## P2 — Quality / engineering cleanup

13. **Update stale documentation:** `docs/DEPLOYMENT_STREAMLIT_CLOUD.md` still states the source ZIP has no model; this is false for v3.3. `README.md` still describes v3 generically. Align them with v3.3 baseline status and final champion status without retroactively changing historical reports.
14. **Reproducibility:** dataset manifest contains **Git blob SHA-1** IDs, whereas some documentation asks for **downloaded-file SHA-256**. Compute actual SHA-256 from the downloaded files and record them, with provenance, environment/package versions, random seeds, commit SHA and artifact SHA-256. The current loose dependency ranges do not give bit-for-bit reproducibility; add a reproducible lock/constraint strategy where useful.
15. **More tests:** reject malicious/oversized or malformed CSV inputs; use multiple engines; verify missing columns, duplicate/non-monotonic cycles, nonfinite readings and stable model inference; test failed network fetches and safe empty-state render; test CI on required Python 3.12. Expand beyond 8 core tests based on observed failures rather than inventing counts.
16. **Production-readiness/security:** dataset legal attribution, API secrets if any, Streamlit upload limits, untrusted serialization handling, log safety, and clear non-certified research disclaimer. Avoid automated maintenance action language. Do not commit real private customer data.
17. **Python 3.15 compatibility is optional**, not a reason to move cloud runtime now. Experimental `lazy import` does not upgrade packages or make ML training faster automatically. Test only in a separate matrix and keep Python 3.12 production baseline.
18. **Avoid scope creep:** no forced Next.js rewrite, decorative 3D or interview-related content. Streamlit-first deployment should succeed before optional enhancements.

## Acceptance criteria (Codex can stop when all P0–P1 gates are met)

- [ ] Dedicated GitHub repository exists, with correct source and approved artifacts, and a verified link.
- [ ] Hosted Streamlit URL opens successfully from an unauthenticated browser, and there is a verified link.
- [ ] Authentic Python notebook executed completely; resulting `.ipynb` and metrics reviewed, and model selection protocol documented.
- [ ] Seven tabs function on desktop/mobile, upload/predict/export flows verified with Playwright, no uncaught browser errors.
- [ ] Inference on a trusted NASA sample is finite, with correct bounds, provenance/version and actual model-specific metrics.
- [ ] Advanced diagnostic graphics render only if real underlying artifacts exist; otherwise disclose unavailable states.
- [ ] Unit/integration/CI/preflight checks pass on Python 3.12, with captured exact outputs.
- [ ] No CV, interview, candidate/recruiter or portfolio-presentation content in public website.
- [ ] Final run report includes GitHub URL, live URL, workflow run link, deployment log reference, model comparison and true limitations.

## Ready-to-paste Codex instruction

> Open the extracted `PREDICTA_AI_v3_3_Authentic_Baseline_Deployment_Package.zip`. Read `AGENTS.md`, `DESIGN.md`, `CODEX_DEPLOY_NEXT.md` and **this audit**. Execute all P0 and P1 tasks, not merely draft a plan. Reuse installed Codex skills and plugins: RTK if configured, one of Frontend Design/Taste for UI, Web Design Guidelines for audit, Playwright CLI for actual browser QA, GitHub CLI/connector for publishing. Use Python 3.12 for deployment and keep Python 3.15 lazy imports experimental. First publish a verified working Ridge baseline, then run the full authentic FD001 Python notebook and promote a champion only if validated. Fix the incomplete diagnostics and stale docs. Preserve dataset provenance, never invent metrics or URLs, keep public UI strictly engineering-focused, and return direct links with test evidence and blockers. Proceed using already authorized accounts; do not overwrite unrelated GitHub repositories, change global settings, or expose secrets.
