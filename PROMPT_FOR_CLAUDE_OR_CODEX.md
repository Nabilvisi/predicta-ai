    # MASTER BUILD PROMPT — PREDICTA AI v3

    Use the following as the main instruction to **Claude Code or OpenAI Codex**. Provide the whole extracted project folder as working directory.

    ---

    You are the lead machine-learning engineer, scientific Python developer, and product UI engineer responsible for completing **PREDICTA AI: Engine Health Intelligence** from this repository.

    ## Non-negotiable delivery requirements

    1. **Start by inspecting the entire repository**—especially `notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb`, `predicta/core.py`, `app.py`, `tests/`, and `docs/PYTHON_315_LAZY_IMPORTS.md`. Preserve the existing working architecture and fix deficiencies rather than replacing it with unrelated boilerplate.
    2. The authoritative end-to-end ML workflow must live in the **executable Jupyter Notebook (.ipynb)**, using professional **Markdown narration followed by Python code cells**. Include problem definition, GitHub data provenance, cleaning and validation, visualization and EDA, engine-group splitting and causal feature engineering, baseline and advanced ML models, feature selection/PCA, grouped hyperparameter tuning, evaluation, calibration/uncertainty, explanation, persistence and deployment. Explain why each method is used and interpret every resulting figure/table.
    3. Work with **authentic NASA C-MAPSS FD001 original files**, retrieved from the dataset source documented in the notebook, without inventing sensor values, RUL labels, accuracy metrics, charts or asset records. FD001 is a **physics-simulated engineering benchmark**; never call it real field-operation measurements. When internet access is unavailable, provide honest instructions for obtaining the original files; do not silently substitute mock data. Test fixtures in `tests/` are allowed but must never be presented as portfolio results.
    4. Keep model validation **engine-disjoint**; all preprocessing, feature selection and tuning must be fit only within the training partitions and their group-aware cross-validation. Use internal validation for model selection, separate calibration engines for residual intervals, and the official NASA test labels exclusively for final performance assessment. Describe mismatch between train snapshots and test endpoints and report actual interval coverage.
    5. Do not create target leakage. Ensure deployed scoring uses the exact same feature definitions, ordering, and fitted transformations as the notebook. Validate the model bundle format, raw 26-field input schema and temporal ordering. Create tests for malformed files, leakage, feature parity, prediction shape and runtime checks.
    6. The **deployed public website is exclusively an industrial decision-support tool**. It MUST NOT display interview guides, CV, job-application messages, recruiter language, portfolio promotion, coding instructions, or audience-facing personal information. Use a clean responsive dark industrial interface with accessible, meaningful animation. Pages: Overview, Sensor Explorer, RUL Prediction, Maintenance Planner, Sensitivity Lab, Model Diagnostics, Data Contract. Distinguish statistical sensor shifts, hypothetical sensitivity inputs, and demonstrated model predictions from validated physical failure causality.
    7. Do **not** start by redesigning the whole frontend. First get real FD001 acquisition, notebook execution, model artifact saving and inference parity passing. Then refine the Streamlit UI with analytical value: filtering engines, historical sensor trends, RUL intervals, downloadable scores, configurable review thresholds, model error charts, feature importance, drift diagnostics and clear warnings. 3D is optional and only warranted if it supports analysis rather than animation for its own sake.
    8. **Python 3.15 / PEP 810:** Python 3.15.0 stable was released on 2026-10-09. Preserve the pinned Python 3.12 deployment baseline until all dependencies and Streamlit hosting support 3.15. Keep the cross-version `__lazy_modules__` bridge for Plotly in `app.py`; native `lazy import` syntax belongs only in `experiments/python315_explicit_lazy.py` or other files expressly requiring Python >=3.15. Run both eager/lazy behavior tests. Do not blanket-enable global lazy imports or claim that laziness upgrades packages or speeds numerical computation. Benchmark startup differences before reporting them.
    9. **CI and maintainability:** Validate tests and notebook code, retain Dependabot updates, support vetted Python runtimes, reject failing smoke tests and document all limitations. Do not commit secrets or executable artifacts from untrusted sources. `joblib.load` is unsafe for untrusted files; load only locally trained and verified artifacts.
    10. If GitHub and cloud deployment integrations are authorized, create or update a repository and deploy the project. Otherwise leave exact reproducible terminal commands and never claim a push or live deployment happened. Verify deployment with real artifacts before declaring it complete.

    ## Execution order

    A. Audit repo, dependencies, data-source URLs and notebook order. Produce a short issue list.
B. Run unit tests and notebook syntax validation.
C. Acquire real FD001 and execute the complete notebook.
D. Confirm model comparisons, test MAE/RMSE/R², interval coverage and model-bundle compatibility.
E. Run preflight and a real-data end-to-end app smoke test.
F. Improve UI/UX without adding recruiting content.
G. Review Python 3.15 experimental support and selected import performance.
H. Update README, test status, deployment instructions and changelog; produce a final packaged ZIP.

    ## Definition of done

    - Notebook is self-explanatory and runs **top to bottom** on authentic dataset inputs.
    - Artifacts are reproducible and separate from temporary unit-test fixtures.
    - Trained model and deployed UI use the same feature transformations.
    - Core unit tests, notebook syntax, trusted release preflight and app validation pass.
    - Real held-out metrics, limitations and dataset provenance are documented.
    - Python 3.15 features do not break supported older runtimes.
    - The website is production-oriented, analytical, and free of CV/interview content.

    Report precisely what was tested, what was not tested, every outstanding dependency or network blocker, and the location of generated files. Do not invent validation outcomes.
