# Authentic NASA FD001 Ridge baseline — 2026-10-13

## Training execution performed

This is a **real-data baseline training run** that accessed the original `train_FD001.txt`, `test_FD001.txt` and `RUL_FD001.txt` files through the connected GitHub service, using blob SHAs recorded in `artifacts/run_manifest.json`. It is **not** the execution of `notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb`. The complete notebook still requires a Python environment with access to the original dataset for its advanced model comparison and retraining.

### Procedure

- NASA C-MAPSS FD001: 100 full training trajectories and 100 truncated official test trajectories; all physics-simulated rather than field observations.
- Independent shuffled engine partitions (seed=42): 70 train, 15 validation, 15 calibration. Official test engines were never used for model selection or scaling.
- Features: operational cycle, 3 settings, 21 sensors and causal 5-cycle rolling mean, sample standard deviation and delta for 8 selected sensors (49 features). Current/past cycles only.
- Training examples: 9 snapshot fractions per training engine; validation: 3 snapshots per validation engine; calibration: one snapshot at 65% trajectory length per calibration engine.
- Baseline estimator: closed-form standardized Ridge regression, trained with a deterministic JavaScript implementation; scanned regularization alpha in `[1, 10, 100, 300, 1000, 3000, 10000]`. Chose alpha=1 using validation MAE; refit using training+validation snapshots.
- Calibration: separate 15-engine split, absolute residual conformal radius at nominal 90% level. Distinct snapshot fractions and test-endpoint distribution can affect coverage.
- Official test: exactly one last-cycle prediction for each of 100 test engines, evaluated once after selection. Negative predicted RUL values clipped at zero.

### Authentic observed results

| Metric | Value |
|---|---:|
| Internal validation MAE (alpha=1) | 22.5584 cycles |
| Internal validation RMSE (alpha=1) | 26.8740 cycles |
| Official test MAE | **19.4263 cycles** |
| Official test RMSE | **24.9965 cycles** |
| Conformal radius | 60.2616 cycles |
| Empirical official-test interval coverage | 100% (100/100 engines) |

The test interval is extremely wide. Its 100% coverage **is not evidence** of narrow or well-calibrated intervals. Model comparisons with the advanced Jupyter notebook are still pending.

### Serving artifact

`scripts/create_verified_baseline.py` recreates the frozen estimator and `artifacts/predicta_fd001_model.joblib` from the authenticated real-data fit's coefficients. `predicta.baseline.FrozenStandardizedRidge` provides strict feature-order inference. The stored sample contains five actual rows (cycles 27–31) from the *test* engine 1, with **no test RUL labels**; it is only for interface smoke testing, not model training. The model is deliberately labeled **Ridge baseline**, not notebook-selected champion.

The serialized joblib model should only be loaded from this trusted project. As with all pickle-based serialization, do not load model files from untrusted uploaders.

### Outstanding work

- Run all 46 notebook cells against the authenticated FD001 source under Python 3.12.
- Compare baseline against the notebook's ensemble, feature-selection, PCA and tuning experiments and promote a validated champion only if appropriate.
- Publish the repository, connect it to Streamlit Community Cloud and verify the live deployment. No public URL has been produced in this environment.
