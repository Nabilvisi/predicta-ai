"""Real-source five-cycle model-serving contract regression tests."""
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from predicta.core import FEATURES, predict_assets

ROOT = Path(__file__).resolve().parents[1]

def test_real_fd001_baseline_can_score_trusted_sample():
    model_file = ROOT / 'artifacts/predicta_fd001_model.joblib'
    example = ROOT / 'data/sample/engine_history.csv'
    if not model_file.exists() or not example.exists():
        import pytest
        pytest.skip('Optional real-data baseline release not yet generated')
    bundle = joblib.load(model_file)
    assert bundle['feature_names'] == FEATURES
    scored, _ = predict_assets(pd.read_csv(example), bundle)
    assert len(scored) == 1
    assert scored.engine_id.iloc[0] == 1
    assert scored.cycle.iloc[0] == 31
    assert np.isclose(scored.rul_estimate.iloc[0], 149.29555560191, rtol=1e-8)
    assert np.isfinite(scored[['rul_lower', 'rul_upper']]).all().all()


def test_manifest_discloses_training_method_and_sources():
    file = ROOT / 'artifacts/run_manifest.json'
    if not file.exists():
        import pytest
        pytest.skip('Optional real-data baseline release not yet generated')
    m=json.loads(file.read_text())
    assert 'NOT executed Python notebook champion' in m['release_type']
    assert m['split']['official_test_engines']==100
    assert m['source_blob_sha1']['train_FD001.txt']
