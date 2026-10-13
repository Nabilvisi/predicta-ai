"""Frozen, auditably exported linear inference for a real FD001 Ridge baseline.

This is a separate real-data baseline, not the notebook-selected final model.
The sklearn notebook can later replace this bundle after full training.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

class FrozenStandardizedRidge:
    def __init__(self, feature_names, mean, scale, coef, intercept):
        self.feature_names = list(feature_names)
        self.mean = np.asarray(mean, dtype=float)
        self.scale = np.asarray(scale, dtype=float)
        self.coef = np.asarray(coef, dtype=float)
        self.intercept = float(intercept)
        n = len(self.feature_names)
        if any(len(v) != n for v in (self.mean, self.scale, self.coef)):
            raise ValueError('Baseline coefficient and feature dimensions differ.')
        if not np.isfinite(self.mean).all() or not np.isfinite(self.coef).all() or not np.isfinite(self.scale).all() or (self.scale <= 0).any():
            raise ValueError('Invalid coefficients.')

    def predict(self, X):
        if not isinstance(X, pd.DataFrame):
            raise TypeError('Expected pandas DataFrame with named features.')
        if X.columns.tolist() != self.feature_names:
            raise ValueError('Feature order differs from the trained baseline.')
        values = X.to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError('Nonfinite inference features.')
        return self.intercept + ((values - self.mean) / self.scale) @ self.coef
