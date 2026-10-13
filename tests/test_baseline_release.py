"""Real-source five-cycle model-serving contract regression tests."""
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from predicta.core import FEATURES, predict_assets

ROOT = Path(__file__).resolve().parents[1]

def test_real_fd001_baseline_can_score_trusted_sample():
    baseline_model = ROOT / 'artifacts/predicta_fd001_baseline_ridge.joblib'
    model_file = baseline_model if baseline_model.exists() else ROOT / 'artifacts/predicta_fd001_model.joblib'
    baseline_example = ROOT / 'data/sample/baseline_engine_history.csv'
    example = baseline_example if baseline_example.exists() else ROOT / 'data/sample/engine_history.csv'
    if not model_file.exists() or not example.exists():
        import pytest
        pytest.skip('Optional real-data baseline release not yet generated')
    bundle = joblib.load(model_file)
    assert bundle['feature_names'] == FEATURES
    scored, _ = predict_assets(pd.read_csv(example), bundle)
    engine1 = scored[scored.engine_id == 1]
    assert len(engine1) == 1
    assert engine1.cycle.iloc[0] == 31
    assert np.isclose(engine1.rul_estimate.iloc[0], 149.29555560191, rtol=1e-8)
    assert np.isfinite(engine1[['rul_lower', 'rul_upper']]).all().all()


def test_manifest_discloses_training_method_and_sources():
    baseline_manifest = ROOT / 'artifacts/baseline_run_manifest.json'
    file = baseline_manifest if baseline_manifest.exists() else ROOT / 'artifacts/run_manifest.json'
    if not file.exists():
        import pytest
        pytest.skip('Optional real-data baseline release not yet generated')
    m = json.loads(file.read_text())
    assert 'NOT executed Python notebook champion' in m.get('release_type', '')
    assert m['split']['official_test_engines'] == 100
    assert m['source_blob_sha1']['train_FD001.txt']


def test_active_release_model_contract():
    model_file = ROOT / 'artifacts/predicta_fd001_model.joblib'
    example = ROOT / 'data/sample/engine_history.csv'
    if not model_file.exists() or not example.exists():
        import pytest
        pytest.skip('Active release model or sample not found')
    bundle = joblib.load(model_file)
    assert bundle['feature_names'] == FEATURES
    scored, _ = predict_assets(pd.read_csv(example), bundle)
    assert len(scored) > 0
    assert np.isfinite(scored[['rul_estimate', 'rul_lower', 'rul_upper']]).all().all()
    assert (scored.rul_lower <= scored.rul_estimate).all()
    assert (scored.rul_estimate <= scored.rul_upper).all()
