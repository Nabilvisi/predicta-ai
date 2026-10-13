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


def test_champion_run_manifest_contract():
    manifest_file = ROOT / 'artifacts/run_manifest.json'
    if not manifest_file.exists():
        import pytest
        pytest.skip('run_manifest.json not found')
    m = json.loads(manifest_file.read_text())
    assert m['selected_model'] in ('Random forest', 'Random Forest')
    assert m['official_test_engines'] == 100
    assert 'test_metrics' in m
    metrics = m['test_metrics']
    assert 0 < metrics['MAE'] < 25
    assert 0 < metrics['RMSE'] < 30
    assert 0.5 < metrics['R2'] < 1.0
    for filename in ('train_FD001.txt', 'test_FD001.txt', 'RUL_FD001.txt'):
        assert filename in m['raw_dataset_hashes']
        assert len(m['raw_dataset_hashes'][filename]['sha256']) == 64


def test_diagnostic_artifacts_integrity():
    comp_file = ROOT / 'artifacts/model_comparison.csv'
    imp_file = ROOT / 'artifacts/permutation_importance.csv'
    preds_file = ROOT / 'artifacts/test_predictions.csv'

    if not (comp_file.exists() and imp_file.exists() and preds_file.exists()):
        import pytest
        pytest.skip('Diagnostic artifacts not found')

    comp = pd.read_csv(comp_file)
    assert {'Model', 'Validation_MAE', 'Validation_RMSE', 'Validation_R2'}.issubset(comp.columns)
    assert len(comp) >= 5
    assert (comp['Validation_MAE'] > 0).all()

    imp = pd.read_csv(imp_file)
    assert {'feature', 'mae_increase'}.issubset(imp.columns)
    assert len(imp) == len(FEATURES)
    assert set(imp['feature']) == set(FEATURES)

    preds = pd.read_csv(preds_file)
    assert {'engine_id', 'true_rul', 'predicted_rul', 'rul_lower', 'rul_upper', 'absolute_error'}.issubset(preds.columns)
    assert len(preds) == 100
    assert (preds['predicted_rul'] >= 0).all()
    assert (preds['rul_lower'] <= preds['predicted_rul']).all()
    assert (preds['predicted_rul'] <= preds['rul_upper']).all()
    assert np.allclose(preds['absolute_error'], np.abs(preds['true_rul'] - preds['predicted_rul']))


def test_cross_version_pipeline_serving_parity():
    model_file = ROOT / 'artifacts/predicta_fd001_model.joblib'
    example = ROOT / 'data/sample/engine_history.csv'
    if not model_file.exists() or not example.exists():
        import pytest
        pytest.skip('Active release model or sample not found')
    bundle = joblib.load(model_file)
    df = pd.read_csv(example)
    
    # Test that prediction succeeds with either or both imputer attribute variants
    model = bundle['model']
    if hasattr(model, 'named_steps'):
        for step in model.named_steps.values():
            if hasattr(step, '_fill_dtype'):
                delattr(step, '_fill_dtype')
    scored, _ = predict_assets(df, bundle)
    assert len(scored) == 20
    assert np.isfinite(scored['rul_estimate']).all()

