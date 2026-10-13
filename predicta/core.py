"""Shared, deterministic C-MAPSS FD001 transformations for notebook and app.

No model training occurs here. Only features using current/past observations are
constructed. It is essential that deployment uses this exact module.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

SENSORS = [f"sensor_{j}" for j in range(1, 22)]
SETTINGS = [f"setting_{j}" for j in range(1, 4)]
RAW_COLUMNS = ["engine_id", "cycle", *SETTINGS, *SENSORS]
ROLLING_SENSORS = ["sensor_2", "sensor_3", "sensor_4", "sensor_7", "sensor_11", "sensor_12", "sensor_15", "sensor_20"]
WINDOW = 5
FEATURES = ["cycle", *SETTINGS, *SENSORS] + [
    f"{sensor}_{suffix}{WINDOW}" for sensor in ROLLING_SENSORS
    for suffix in ("mean", "std", "delta")
]


def load_trajectory(path: str | Path) -> pd.DataFrame:
    """Read original NASA whitespace-separated file with strict 26-column contract."""
    frame = pd.read_csv(path, sep=r"\s+", header=None)
    if frame.shape[1] != len(RAW_COLUMNS):
        raise ValueError(f"Expected {len(RAW_COLUMNS)} raw columns; got {frame.shape[1]}.")
    frame.columns = RAW_COLUMNS
    return validate_raw(frame)


def validate_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Fail loudly on structurally invalid records instead of silently filtering."""
    absent = sorted(set(RAW_COLUMNS) - set(df.columns))
    if absent:
        raise ValueError("Missing required columns: " + ", ".join(absent))
    if df.empty:
        raise ValueError("At least one observation is required.")
    out = df.loc[:, RAW_COLUMNS].copy()
    for col in RAW_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="raise")
    if out.isna().any().any():
        raise ValueError("Missing observations detected; investigate before inference.")
    if not np.isfinite(out.to_numpy(dtype=float)).all():
        raise ValueError("Data contains infinite or non-finite values.")
    for col in ("engine_id", "cycle"):
        if (out[col] != np.floor(out[col])).any():
            raise ValueError(f"{col} must contain integer values.")
        out[col] = out[col].astype(int)
        if (out[col] < 1).any():
            raise ValueError(f"{col} must be a positive integer.")
    if out.duplicated(["engine_id", "cycle"]).any():
        raise ValueError("Duplicate (engine_id, cycle) readings detected.")
    return out.sort_values(["engine_id", "cycle"]).reset_index(drop=True)


def engineer_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Causal rolling summaries; never inspect future cycles of an engine."""
    out = validate_raw(frame)
    group = out.groupby("engine_id", sort=False)
    for sensor in ROLLING_SENSORS:
        series = group[sensor]
        out[f"{sensor}_mean{WINDOW}"] = series.transform(
            lambda s: s.rolling(WINDOW, min_periods=1).mean()
        )
        out[f"{sensor}_std{WINDOW}"] = series.transform(
            lambda s: s.rolling(WINDOW, min_periods=2).std().fillna(0.0)
        )
        out[f"{sensor}_delta{WINDOW}"] = series.transform(
            lambda s: s - s.shift(WINDOW - 1).fillna(s.iloc[0])
        )
    if not np.isfinite(out[FEATURES].to_numpy(dtype=float)).all():
        raise ValueError("Engineered feature matrix is not finite.")
    return out


def latest_snapshot(frame: pd.DataFrame) -> pd.DataFrame:
    return (frame.sort_values(["engine_id", "cycle"])
            .groupby("engine_id", sort=True).tail(1)
            .sort_values("engine_id").reset_index(drop=True))


def snapshot_at_fractions(featured: pd.DataFrame, fractions: tuple[float, ...]) -> pd.DataFrame:
    """One snapshot per engine and specified trajectory fraction.

    Only use the full trajectories for constructing *train/validation/calibration*
    snapshots; never derive test RUL from test trajectory endpoints.
    """
    rows = []
    for _eid, group in featured.groupby("engine_id", sort=True):
        group = group.sort_values("cycle")
        for frac in fractions:
            if not 0 < frac <= 1:
                raise ValueError("Fractions must be in (0, 1].")
            pos = max(0, min(len(group)-1, math.ceil(frac * len(group))-1))
            rows.append(group.iloc[[pos]])
    return pd.concat(rows, ignore_index=True)


def regression_metrics(y_true, y_pred) -> dict[str, float]:
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    y = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    return {
        "MAE": float(mean_absolute_error(y, pred)),
        "RMSE": float(np.sqrt(mean_squared_error(y, pred))),
        "R2": float(r2_score(y, pred)),
    }


def conformal_radius(y_true, y_pred, alpha: float = 0.10) -> float:
    """Finite-sample split conformal absolute-error quantile.

    Requires an exchangeable, separate calibration set for nominal coverage.
    C-MAPSS test-endpoint distribution can differ from calibration snapshots.
    """
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    errors = np.abs(np.asarray(y_true, float) - np.asarray(y_pred, float))
    if not len(errors) or not np.isfinite(errors).all():
        raise ValueError("Calibration residuals must be finite and nonempty")
    n = len(errors)
    rank = min(n, math.ceil((n + 1) * (1 - alpha)))
    return float(np.partition(errors, rank - 1)[rank - 1])


def predict_assets(raw: pd.DataFrame, bundle: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Score each engine at its most recent uploaded cycle."""
    featured = engineer_features(raw)
    latest = latest_snapshot(featured)
    names = bundle["feature_names"]
    if names != FEATURES:
        raise ValueError("Model feature contract does not match deployment feature definition")
    estimate = np.maximum(0, bundle["model"].predict(latest[names]))
    radius = max(float(bundle.get("conformal_radius", 0)), 0)
    scored = latest[["engine_id", "cycle"]].copy()
    scored["rul_estimate"] = estimate
    scored["rul_lower"] = np.maximum(0, estimate - radius)
    scored["rul_upper"] = estimate + radius
    scored["interval_width"] = scored["rul_upper"] - scored["rul_lower"]
    return scored, featured


def assign_priority(scored: pd.DataFrame, critical: int = 30, watch: int = 60) -> pd.DataFrame:
    """User-adjustable illustrative triage, NOT a validated failure probability."""
    if critical < 0 or watch <= critical:
        raise ValueError("Watch threshold must be greater than the critical threshold.")
    out = scored.copy()
    out["priority"] = np.select(
        [out.rul_upper <= critical, out.rul_lower <= critical,
         out.rul_lower <= watch],
        ["Review now", "Review soon", "Watchlist"],
        default="Routine",
    )
    order = {"Review now": 0, "Review soon": 1, "Watchlist": 2, "Routine": 3}
    out["priority_rank"] = out["priority"].map(order)
    return out.sort_values(["priority_rank", "rul_lower", "engine_id"]).reset_index(drop=True)


def population_stability_index(reference, observed, bins: int = 8) -> float:
    """Descriptive PSI diagnostic, not a calibrated statistical test."""
    base = np.asarray(reference, dtype=float)
    recent = np.asarray(observed, dtype=float)
    base = base[np.isfinite(base)]
    recent = recent[np.isfinite(recent)]
    if len(base) < 5 or len(recent) < 5 or np.ptp(base) == 0:
        return float("nan")
    edges = np.unique(np.quantile(base, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return float("nan")
    edges[0], edges[-1] = -np.inf, np.inf
    base_counts = np.histogram(base, bins=edges)[0].astype(float)
    recent_counts = np.histogram(recent, bins=edges)[0].astype(float)
    eps = 1e-6
    p = np.clip(base_counts / base_counts.sum(), eps, None)
    q = np.clip(recent_counts / recent_counts.sum(), eps, None)
    p /= p.sum()
    q /= q.sum()
    return float(np.sum((q - p) * np.log(q / p)))
