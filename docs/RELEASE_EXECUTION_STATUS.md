# PREDICTA AI — Release Execution Status (Updated 2026-10-13)

## Current release: PAPER ATLAS PUBLIC ACCEPTANCE PASSED

The user approved **02 Paper Atlas**, with more graphics, interactive 3D motion and less visible text. The approved UI is live at **[https://predicta-ai.streamlit.app](https://predicta-ai.streamlit.app)**. Final anonymous headless dashboard audit: **2026-10-13 19:12:40–19:13:56 WIB, 27/27 PASS**. Final rendered graphics audit: **19:12:55–19:14:04 WIB, 11/11 PASS**.

### Approved design and behavior

- Warm paper/ink/cobalt palette and bundled IBM Plex Sans / Instrument Serif fonts. DESIGN.md records the approved replacement of the original dark tokens.
- Procedural WebGL cutaway turbine with drag, keyboard/button turning, Rotate/Pause and animated Explode/Assemble. Clearly labeled illustration, not observed engine geometry, telemetry or health.
- Charts and actual metrics lead the overview; a review-distribution chart and actual baseline/perturbed sensitivity comparison add graphics. Full engine tables, raw schema and extended methods are expandable; cycle units, uncertainty and research/non-causal caveats remain visible.
- Rotation pauses offscreen/when hidden. Reduced motion prevents autoplay and makes explode/assemble immediate. Rendering is capped at DPR 1.5; WebGL loss/unavailability uses an accessible static SVG, with tested context recovery. GPU resources are released on page exit.
- Analytics downloads use on_click="ignore" to prevent unnecessary app reruns. An initial public run recorded a stale CSV media 404 during a rerun; the final run actually downloaded/parsed the reports with no application console errors. Initial diagnostic evidence remains locally available.

### Fresh release evidence

| Verification | Final result |
|---|---|
| Public functional audit | **27/27 PASS**: all seven desktop/mobile tabs; real normal CSV upload; missing-field, duplicate-key and nonfinite-sensor rejection; recovery; Champion inference; parsed RUL/worklist/example downloads; keyboard navigation; forbidden-copy scan; no Streamlit exceptions or uncaught JavaScript/application console errors. |
| Mobile design | **375x812 PASS**: no document horizontal overflow, computed ink/cobalt tokens match #17292D/#234FCC, reduced-motion preference honored. |
| 3D and typography | **11/11 PASS**: actual WebGL geometry, rotation/pause, explode/assemble, keyboard/focus/tap alternatives, offscreen pause/resume, context loss/recovery, loaded local fonts, mobile reduced motion, bounded canvas resolution/touch controls, static fallback, no uncaught illustration errors. |
| Source/model gates | **17 tests PASS**, all **46 notebook cells** structurally validated, strict preflight scored **20 engines**, Python compilation and whitespace checks passed. No retraining or inference transformation changes. |
| Prediction integrity | Default 20-engine and uploaded 2-engine report values match the trusted local artifact at rtol/atol 1e-8. Model SHA256 remains ec08e6117bc355c269ffce9ffa39f0e50ffe1e57e51ff500e2a146744faed297. |
| Provider console entries | Five recorded Cloud-wrapper errors: heap analytics 404, app-open telemetry 403 and three anonymous user-details 404s. These remain disclosed; **zero total browser errors is not claimed**. CSV media failures are not excluded from the application-error gate. |

Published machine-readable evidence: [functional report](audit/2026-10-13/paper-atlas-live-final/report.json), [motion report](audit/2026-10-13/paper-atlas-live-final/motion-report.json), [scoped design review](audit/2026-10-13/paper-atlas-design-review.md), [CI job snapshot](audit/2026-10-13/paper-atlas-ci-code-fix.json). Actual screenshots and downloaded CSVs are retained locally alongside the reports; PNGs remain ignored by repository policy. Earlier acceptance/recovery links below refer to historical local evidence, not all of which is published remotely.

UI publication: [be3512d](https://github.com/Nabilvisi/predicta-ai/commit/be3512d95da57cf048f84a1d53b21a260e55f794). Download fix: [2588992](https://github.com/Nabilvisi/predicta-ai/commit/2588992e8c71cfd2141e5674d322affab7d118ff). [Validation run 38395540512](https://github.com/Nabilvisi/predicta-ai/actions/runs/38395540512) passed all four required jobs (Python 3.11, 3.12, 3.13, 3.14). At this snapshot, experimental Python 3.15 is still in dependency installation; it is allowed to fail and is not a deployment compatibility claim. Streamlit deployment baseline remains Python 3.12. Documentation/evidence publication follows the validated serving revision; source-line ending normalization does not change behavior.

Reproduce the current public audits:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m scripts.public_acceptance_audit https://predicta-ai.streamlit.app --output docs/audit/2026-10-13/paper-atlas-live-final
python -m scripts.paper_atlas_motion_audit https://predicta-ai.streamlit.app --output docs/audit/2026-10-13/paper-atlas-live-final
python -m pytest -q
python -m scripts.validate_notebook
python -m scripts.deployment_check --strict
```

Scope: public software acceptance and scoped UI review, not full WCAG certification or operational maintenance qualification. NASA FD001 is physics-simulated data. Calibration coverage on shifted inputs is not guaranteed. Native Streamlit tab state is not URL-persisted; existing width/component APIs emit nonfatal deprecation warnings.

## Previous closure checkpoint: PUBLIC ACCEPTANCE PASSED (18:03 WIB)

Final anonymous headless audit: **2026-10-13 18:03:29–18:04:31 WIB**. Verified live URL: **[https://predicta-ai.streamlit.app](https://predicta-ai.streamlit.app)**. The public root returned **HTTP 200**, PREDICTA rendered inside its Cloud app frame, and the final audit passed **27/27 checks**. This result supersedes the historical blocked checkpoints below.

The user explicitly approved deployment. The app was deployed from `Nabilvisi/predicta-ai`, `main`, `app.py`, with **Python 3.12** selected in Advanced settings and no secrets entered. Chrome's authenticated workspace provided the recovery route; the earlier Edge browser was not authenticated. A targeted DESIGN.md fix added the actual model-artifact identity to the context ribbon and engine/cycle/source/model identity beside predictions. That fix was published as [`d9489a9cc20149b5f216f9e1b9d36a7a1c17920b`](https://github.com/Nabilvisi/predicta-ai/commit/d9489a9cc20149b5f216f9e1b9d36a7a1c17920b); local HEAD was fast-forwarded to the same commit without discarding the audit documentation.

### Final acceptance evidence

| Requirement | Verified result |
|---|---|
| Seven navigation tabs | **PASS** on desktop 1280×850 and mobile 375×812: Overview, Sensor Explorer, RUL Prediction, Maintenance Planner, Sensitivity Lab, Model Diagnostics, Data Contract. Each selected panel was checked and screenshotted. |
| Normal CSV upload | **PASS** using actual FD001 histories for two engines. Input source changed to Uploaded data; downloaded predictions contained two engines and matched trusted local inference. |
| Invalid data contract | **PASS** for missing required columns, duplicate engine-cycle keys, and an infinite sensor value. Each case waited for its specific rejection message; no Streamlit exception or stale prediction export remained. Valid upload recovery also passed. |
| Random Forest Champion inference | **PASS**. Default 20-engine and uploaded 2-engine predictions matched the trusted artifact's numerical outputs at rtol/atol 1e-8, including engine, cycle, RUL and interval bounds. |
| Analytics downloads | **PASS**. Prediction CSV, prioritized worklist CSV and example-history CSV were actually downloaded and parsed. Worklist policy matched local thresholds 30/60; example CSV matched source values/content after CRLF/LF normalization. |
| Mobile and DESIGN.md | **PASS within the documented scope**. All seven mobile tabs had no document horizontal overflow; computed foreground/accent tokens matched #ECF4FF/#4BD5CA, reduced-motion preference was active, keyboard ArrowRight/Enter navigation worked, and screenshots were captured after loading finished. Additional scrolled panel screenshots expose the analytic content. |
| Public copy | **PASS**. Visible app content on every desktop/mobile tab was scanned for CV, curriculum vitae, resume, recruiter, interview, portfolio, hire me and hiring manager. No matches. Simulation, cycle-unit and research/maintenance caveats remain visible. |
| Application errors | **PASS** for Streamlit exceptions, uncaught JavaScript errors and application console errors. Provider-owned heap analytics and `/api/v2/user/details` emitted four 404 console entries in the final run; these are explicitly retained as Cloud-wrapper issues, not described as zero total browser errors. |
| Public model identity | **PASS**. Displayed fingerprint `ec08e6117bc3` matches model SHA256 `ec08e6117bc355c269ffce9ffa39f0e50ffe1e57e51ff500e2a146744faed297`. This identifies the artifact; it is not an invented semantic version or independent source-commit attestation. |

The complete final machine-readable evidence is [`release-final/report.json`](audit/2026-10-13/release-final/report.json), with execution log [`release-final.log`](audit/2026-10-13/release-final.log). Actual report downloads: [`default-rul.csv`](audit/2026-10-13/release-final/default-rul.csv), [`default-worklist.csv`](audit/2026-10-13/release-final/default-worklist.csv), [`uploaded-rul.csv`](audit/2026-10-13/release-final/uploaded-rul.csv), and [`downloaded-engine-history.csv`](audit/2026-10-13/release-final/downloaded-engine-history.csv).

Screenshots and per-tab accessible snapshots are retained in [`release-final/`](audit/2026-10-13/release-final/). Representative views: [`overview-desktop.png`](audit/2026-10-13/release-final/overview-desktop.png), [`rul-prediction-mobile-panel.png`](audit/2026-10-13/release-final/rul-prediction-mobile-panel.png). PNGs are retained locally and ignored by repository policy. Scrolled mobile content evidence: [`mobile-panels.json`](audit/2026-10-13/release-final/mobile-panels.json). The scoped UI review is [`design-review.md`](audit/2026-10-13/design-review.md); this is not full WCAG certification.

Reproducible commands:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m scripts.public_acceptance_audit https://predicta-ai.streamlit.app --output docs/audit/2026-10-13/release-final
python -m pytest -q
python -m scripts.deployment_check --strict
python -m py_compile app.py scripts/public_acceptance_audit.py
```

Fresh local source checks passed **17 tests**, strict preflight scored **20 engines**, and compile/diff checks passed. The runner uses local Python 3.13.0; deployment was explicitly configured for Python 3.12. Prior diagnostic runs exposed audit-runner issues (case-sensitive model name, newline comparison, upload-rerun races and a NaN/infinity fixture mismatch); these were corrected, and those failed-run logs were retained rather than presented as successful acceptance.

### Previous GitHub and CI checkpoint

At the post-fix check, local HEAD and remote `main` matched **d9489a9cc20149b5f216f9e1b9d36a7a1c17920b**. The new validation workflow [38386518349](https://github.com/Nabilvisi/predicta-ai/actions/runs/38386518349) finished **completed / success**. All four required jobs (Python 3.11/3.12/3.13/3.14) passed. The experimental Python 3.15 job failed during dependency installation (SciPy/OpenBLAS build), with subsequent tests skipped; it uses continue-on-error and does not block Python 3.12 deployment. Evidence: [`final-github-ci.json`](audit/2026-10-13/final-github-ci.json), [`final-ci-python312-excerpt.log`](audit/2026-10-13/final-ci-python312-excerpt.log), and [`final-ci-python315-excerpt.log`](audit/2026-10-13/final-ci-python315-excerpt.log). Earlier successful validation/training runs remain documented below. Final audit script, status documentation and evidence are local additions unless explicitly published later; the runtime UI fix is already committed remotely.

Cloud Manage app logs independently confirmed **Python 3.12.15**, Streamlit 1.65.0, and successful dependency processing; see [`cloud-runtime-excerpt.txt`](audit/2026-10-13/cloud-runtime-excerpt.txt). Plotly lazily renders on viewport entry, so the final audit explicitly scrolls charts into view and waits for actual SVG content before recording panel screenshots. Runtime logs also contain a nonfatal Streamlit use_container_width deprecation warning, retained for future API maintenance.

**Release scope:** the requested Streamlit public-app acceptance is passed. NASA C-MAPSS FD001 is physics-simulated data, not field equipment telemetry. Passing this audit does not certify aviation maintenance decisions, guarantee calibration coverage on shifted populations, or establish Python 3.15 compatibility. Provider-wrapper 404 entries remain a disclosed platform limitation.

## Historical recovery and blocked checkpoints (superseded)

### Recovery solution prepared after user requested an alternative

The available **Chrome** browser is authenticated to Streamlit workspace **nabilvisi**. Its My apps dashboard showed five apps and **no PREDICTA entry**; the earlier Edge browser login state did not establish Chrome's account availability. GitHub repository metadata has no homepage URL, and the repository documentation does not identify another deployed PREDICTA URL. A public search did not find a verified alternative URL; absence from search is not proof of absence.

A new deployment form is prepared in Chrome, but **Deploy has not been submitted**:

| Setting | Verified draft value |
|---|---|
| Workspace | nabilvisi |
| Repository | Nabilvisi/predicta-ai |
| Branch | main |
| Entrypoint | app.py |
| Python | 3.12 (selected and rechecked in Advanced settings) |
| Requested subdomain | predicta-ai |
| Domain validation | Streamlit displayed **Domain is available** |
| Secrets | None entered |

The live GitHub tree confirms the champion model (`artifacts/predicta_fd001_model.joblib`, 2,364,737 bytes), manifest, three diagnostic CSVs, test predictions, and engine-history sample are present remotely. Details: [`deployment-source-files.json`](audit/2026-10-13/deployment-source-files.json). These findings make a new deployment a concrete recovery option rather than a guessed URL. They do not establish a running app.

User approval has been requested for publishing this **new public deployment**, because the initial request described an already deployed app and authorized an audit. Once approved: submit the prepared form, inspect launch/build results, verify anonymous access, then run the complete public acceptance tests before changing this verdict to passed. No replacement host or localhost result will be substituted for the requested Streamlit Community Cloud audit.

Fresh audit: **2026-10-13, 17:17 WIB (10:17 UTC)**. The supplied deployment URL is [https://predicta-ai.streamlit.app](https://predicta-ai.streamlit.app). **This URL is not verified live/public:** an anonymous headless Microsoft Edge session driven by Playwright CLI received HTTP **404** and navigated to `https://share.streamlit.io/errors/not_found`, displaying **“You do not have access to this app or it does not exist.”** The same result occurred on initial access and on repeat desktop/mobile navigation. This evidence cannot distinguish a missing deployment, an incorrect subdomain, or a private application. No application code failure is inferred from the Cloud error page.

### Fresh public browser acceptance evidence

| Requested check | Result | Evidence / limit |
|---|---|---|
| Anonymous public availability | **FAIL** | Target root returned 404; Cloud error page returned 200. A 200 on that error page does not prove a live app. |
| Overview, Sensor Explorer, RUL Prediction, Maintenance Planner, Sensitivity Lab, Model Diagnostics, Data Contract | **BLOCKED** | 0 application tabs rendered; application unavailable before navigation. |
| Normal CSV upload and invalid data-contract rejection | **BLOCKED** | No PREDICTA uploader was reachable. |
| Random Forest Champion inference | **BLOCKED** | No hosted prediction or model identity could be observed. Local preflight is separate evidence. |
| Analytics CSV/report downloads and downloaded-content validation | **BLOCKED** | No application download control was reachable; no hosted report was downloaded. |
| Mobile viewport 375×812 and DESIGN.md compliance | **BLOCKED** | Mobile browser navigation and screenshot completed, but only the Cloud error page rendered. PREDICTA layout, tokens, overflow, chart alternatives and keyboard accessibility could not be assessed publicly. |
| No CV, recruiter or portfolio presentation text in public application | **BLOCKED** | PREDICTA content did not render. Scanning the Cloud error page cannot establish this requirement. |
| Zero browser errors / Streamlit exceptions | **NOT PASSED** | Browser recorded 404/401 resource errors on the Cloud error page. There was no running PREDICTA page on which to assess Streamlit exceptions. |

**No passing public Playwright audit is claimed.** The successful execution of an availability probe is evidence of the access failure, not a passing application acceptance test. Historical local results below do not substitute for public acceptance.

Evidence retained under [`docs/audit/2026-10-13/`](audit/2026-10-13/):

- [`public-browser.json`](audit/2026-10-13/public-browser.json): timestamps, viewport dimensions, actual navigation URLs/statuses, console errors, visible error text, accessible snapshots, and tab counts.
- [`desktop-public.png`](audit/2026-10-13/desktop-public.png) and [`mobile-public.png`](audit/2026-10-13/mobile-public.png): actual hosted access-error screenshots (PNG files are ignored by repository policy; retained locally).
- [`public_probe.js`](audit/2026-10-13/public_probe.js): repeatable Playwright CLI function for reproducing this specific access failure, not a full acceptance suite.
- [`github-ci.json`](audit/2026-10-13/github-ci.json) and [`ci-python312.log`](audit/2026-10-13/ci-python312.log): live GitHub API run/job evidence and the deployment-baseline job log.
- [`local-tests.log`](audit/2026-10-13/local-tests.log), [`notebook-validation.log`](audit/2026-10-13/notebook-validation.log), [`local-preflight.log`](audit/2026-10-13/local-preflight.log): fresh local checks, run on **Python 3.13.0**, not proof of the Cloud runtime.

Commands executed:

```powershell
playwright-cli -s=predicta-public-closeout open https://predicta-ai.streamlit.app --browser=msedge
playwright-cli -s=predicta-public-closeout --raw run-code --filename=docs/audit/2026-10-13/public_probe.js | Set-Content -Encoding utf8 docs/audit/2026-10-13/public-browser.json
playwright-cli -s=predicta-public-closeout close
$env:PYTHONPATH = (Get-Location).Path
python -m pytest -q
python -m scripts.validate_notebook
python -m scripts.deployment_check --strict
```

The named browser ran headless and was closed afterward. Initial sandbox browser launch failed; the authorized launch outside the sandbox succeeded. Initial local pytest collection failed to resolve `predicta`; setting the workspace `PYTHONPATH` corrected the runner environment without changing source. The rerun passed **17 tests**, notebook validation passed **46 cells**, and strict preflight scored **20 engines** successfully. Notebook validation checks structure/cells; this audit did not retrain or reexecute the ML notebook.

### Fresh GitHub synchronization and CI

- Confirmed remote: [Nabilvisi/predicta-ai](https://github.com/Nabilvisi/predicta-ai). Local HEAD and live remote `main` both equal [`b7450c8a13168e80ff4945590a7cfb27bc479ce5`](https://github.com/Nabilvisi/predicta-ai/commit/b7450c8a13168e80ff4945590a7cfb27bc479ce5). Working tree was clean before this audit. Audit documentation/evidence are new local changes and have not been pushed.
- Latest validation run: [38375345959](https://github.com/Nabilvisi/predicta-ai/actions/runs/38375345959), `completed / success`, on the same SHA; created **2026-10-13 16:18:20 WIB**. Required Python **3.11, 3.12, 3.13 and 3.14** jobs all passed. Python 3.12 job log independently confirms **17 passed** and **Notebook validated: 46 cells**.
- Python **3.15 experimental** job **failed** in dependency installation: SciPy build could not find OpenBLAS; scikit-learn build dependencies failed. Its analytical tests/notebook checks were skipped. Overall workflow success is possible because this experimental job uses `continue-on-error`; it is not a five-version pass.
- Latest model-training run: [38375006784](https://github.com/Nabilvisi/predicta-ai/actions/runs/38375006784), `completed / success`, on `b82ebae27d429154f4a9d84c31c231236772ab7f`. Previous main validation [38374501401](https://github.com/Nabilvisi/predicta-ai/actions/runs/38374501401) also succeeded. Training success does not establish Streamlit deployment availability.
- GitHub connector reads succeeded. Local `gh auth status` reported an invalid token, so authenticated CLI was not used for remote evidence. No remote writes, workflow changes, application changes or deployment actions were performed.
- The inaccessible public page exposes no deployment SHA, runtime version or model hash. Matching repository HEAD cannot attest the Cloud deployment revision.

### Historical closure gate (resolved)

Third consecutive goal-turn check at **2026-10-13 17:22 WIB** again reached `https://share.streamlit.io/errors/not_found` in a fresh headless session. Snapshot: [`public-recheck-1722.txt`](audit/2026-10-13/public-recheck-1722.txt). The available Cloud browser remained on **Sign in**. All audit browser sessions were closed. The goal was **BLOCKED** at that checkpoint: no passing public acceptance evidence existed yet. This was resolved by the later authorized deployment and final audit above.

Continuation recheck at **2026-10-13 17:20 WIB** used a fresh named headless Edge session (`predicta-closeout-recheck`) and again reached the Cloud `errors/not_found` page. Snapshot: [`public-recheck-1720.txt`](audit/2026-10-13/public-recheck-1720.txt). A read-only check of `https://share.streamlit.io/` in the available Edge browser also showed the **Sign in** page rather than an authenticated dashboard; no deployment URL or settings could be retrieved. No account/login or visibility changes were made. The public acceptance blocker remains unchanged.

Verify the actual app URL and public visibility in the authenticated Streamlit Community Cloud dashboard for `Nabilvisi/predicta-ai`, branch `main`, entrypoint `app.py`, deployment baseline Python **3.12**. Once anonymous access renders PREDICTA AI, rerun all seven tabs, valid/invalid uploads, actual Random Forest inference, real CSV downloads with content checks, keyboard/mobile/design checks, and forbidden-copy checks. Preserve the current **BLOCKED** verdict until those public tests pass. NASA FD001 remains physics-simulated research data; release acceptance does not imply operational maintenance certification.

## Completed Milestones

### 1. End-to-End Authentic NASA FD001 Machine Learning Workflow
- Downloaded and validated authentic NASA C-MAPSS FD001 dataset from GitHub repository (`PunVas/nasa-c-mapss`):
  - `train_FD001.txt` (3,515,356 bytes, SHA-256: `963b5e22825b34d8b21c69e1aeb4af3e647050eb672ee8834ba4b5d91d2de0f8`)
  - `test_FD001.txt` (2,228,855 bytes, SHA-256: `3cda7109ce17bafb5443f2ac926cfcf88154b941b8c4cf95eb55d1ddd6f52851`)
  - `RUL_FD001.txt` (429 bytes, SHA-256: `a19c8ec94931949d0485bdc35118206e9c81c4547b422efb9cf86f4ceddbceca`)
- Executed all 46 cells of `notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb` with authentic physics-simulated data and zero cell failures.
- Saved executed notebook with all outputs, plots, and metrics to `artifacts/executed_training_notebook.ipynb` and `notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb`.

### 2. Model Comparison and Champion Promotion
- Partitioned engines using group-disjoint splits: 70 train, 15 validation, 15 calibration, and 100 official NASA test engines.
- Internal Validation Results across 7 estimators:
  1. **Random Forest (Champion)**: Validation MAE **18.080**, RMSE **23.763**, R² **0.613**
  2. **Tuned Gradient Boosting**: Validation MAE **19.041**, RMSE **25.055**, R² **0.570**
  3. **Ridge (alpha=20)**: Validation MAE **19.580**, RMSE **23.816**, R² **0.611**
  4. **Ridge + PCA (95%)**: Validation MAE **19.870**, RMSE **24.222**, R² **0.598**
  5. **Ridge + SelectKBest (16)**: Validation MAE **21.500**, RMSE **25.753**, R² **0.545**
  6. **Histogram Gradient Boosting**: Validation MAE **21.835**, RMSE **27.958**, R² **0.464**
  7. **Dummy Mean**: Validation MAE **33.600**, RMSE **39.439**, R² **-0.066**
- Promoted Model: **Random Forest** selected strictly using validation engines without peeking at official test labels.
- Preserved Baseline: Authentic standardized Ridge baseline preserved at `artifacts/predicta_fd001_baseline_ridge.joblib` and `artifacts/baseline_run_manifest.json` with 5-cycle regression fixture `data/sample/baseline_engine_history.csv`.
- Official NASA Test Set Performance (100 test engines):
  - **Random Forest Champion**: Official Test MAE **17.605 cycles**, RMSE **22.653 cycles**, R² **0.7028**, NASA Asymmetric Score **1629.67**, Conformal Interval Coverage **100% (1.0)**, Mean Interval Width **146.06 cycles**.
  - **Ridge Baseline**: Official Test MAE **19.426 cycles**, RMSE **24.997 cycles**, Conformal Interval Coverage **100% (1.0)**.
  - Improvement: MAE reduced by **1.82 cycles** (-9.4%), RMSE reduced by **2.34 cycles** (-9.4%).

### 3. Generated Diagnostic Artifacts
- `artifacts/predicta_fd001_model.joblib`: Serialized Random Forest bundle containing model, feature names, rolling configuration, training sensor reference stats (median/MAD/std for all 21 sensors), and drift features.
- `artifacts/test_predictions.csv`: Full official test predictions for all 100 engines with ground-truth RUL, predicted RUL, uncertainty intervals, and absolute errors.
- `artifacts/permutation_importance.csv`: Validation permutation feature importances for all 49 features.
- `artifacts/model_comparison.csv`: Validation metrics across all evaluated model families.
- `artifacts/run_manifest.json`: Full provenance with dataset SHA-256 hashes, splits, hyperparameters, and test metrics.
- `data/sample/engine_history.csv`: Real 20-engine multi-cycle trajectory sample for interactive dashboard exploration.

### 4. Streamlit Dashboard Improvements & Browser Verification
- Implemented `DESIGN.md` tokens: background `#081421`, panels `#13243A`, text `#ECF4FF`, teal accent `#4BD5CA`.
- Added top context ribbon displaying active model, calibration interval, dataset source, and benchmark target.
- Polished metric typography (`font-variant-numeric: tabular-nums`, no text truncation).
- Added reduced-motion CSS accessibility support.
- Previous local Playwright script (`scripts/ui_playwright_audit.py`) covers the following intended areas; these are historical claims, not fresh public acceptance results. Source review during this audit found that it checks download-button presence rather than downloading/validating reports, only checks for a mobile heading rather than layout compliance, and prints console errors without failing the audit. Therefore its success banner alone is insufficient evidence for closure:
  - All 7 tabs: Overview, Sensor Explorer, RUL Prediction, Maintenance Planner, Sensitivity Lab, Model Diagnostics, Data Contract.
  - Absence of any forbidden candidate/interview/portfolio text.
  - Valid and invalid CSV upload error flows and dynamic data contract alerts.
  - Download functionality for predictions, prioritized worklists, and sample data.
  - Keyboard focus navigation (Tab traversal).
  - Priority status color mapping per `DESIGN.md` (#ef4444, #f59e0b, #38bdf8, #4bd5ca).
  - Mobile viewport (375x812) layout responsiveness.
  - Zero console errors and zero Streamlit exceptions.

### 5. Repository Publication & CI Validation
- Dedicated GitHub Repository: `https://github.com/Nabilvisi/predicta-ai`
- GitHub Actions CI workflow: multi-version matrix (Python 3.11, 3.12, 3.13, 3.14 passing 17/17 tests; 3.15 experimental).
- Dedicated model-training workflow: `.github/workflows/train-model-release.yml` executed and verified green (`38375006784`), producing the downloadable `predicta-model-release` artifact.

