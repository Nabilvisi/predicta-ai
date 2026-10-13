"""Local pre-deployment checks (requires a locally trained model artifact)."""
from pathlib import Path
import sys
import joblib
import numpy as np
import pandas as pd
from predicta.core import FEATURES, RAW_COLUMNS, predict_assets

root=Path(__file__).resolve().parents[1]
model_file=root/'artifacts'/'predicta_fd001_model.joblib'
example=root/'data'/'sample'/'engine_history.csv'
if not model_file.is_file():
    raise SystemExit('No trusted trained model artifact. Execute notebook with real FD001 data first.')
if not example.is_file():
    raise SystemExit('No real-data sample CSV found. Execute the notebook.')
bundle=joblib.load(model_file)
assert bundle['feature_names']==FEATURES
assert bundle['raw_columns']==RAW_COLUMNS
scores,_=predict_assets(pd.read_csv(example),bundle)
assert len(scores)>0 and np.isfinite(scores[['rul_estimate','rul_lower','rul_upper']]).all().all()
assert (scores.rul_lower<=scores.rul_estimate).all() and (scores.rul_estimate<=scores.rul_upper).all()
print('Release preflight passed. Engines scored:',len(scores))
