import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyRegressor

from predicta.core import (
    RAW_COLUMNS, FEATURES, validate_raw, engineer_features, latest_snapshot,
    conformal_radius, predict_assets, assign_priority, population_stability_index,
)


def observations():
    rows=[]
    for engine in (1,2):
        for cyc in (1,2,3,4,5,6):
            row=dict.fromkeys(RAW_COLUMNS,0.0)
            row.update(engine_id=engine,cycle=cyc)
            for i in range(1,22):
                row[f'sensor_{i}']=float(i+cyc+(engine*0.1))
            rows.append(row)
    return pd.DataFrame(rows)


def test_validation_and_features():
    raw=validate_raw(observations())
    fe=engineer_features(raw)
    assert set(FEATURES).issubset(fe.columns)
    assert not fe[FEATURES].isna().any().any()
    assert len(latest_snapshot(fe))==2
    assert fe.loc[0,'sensor_2_mean5']==3.1
    assert fe.loc[0,'sensor_2_std5']==0
    assert fe.loc[5,'sensor_2_delta5']==4.0


def test_no_future_leakage():
    raw=observations()
    first=engineer_features(raw)
    raw.loc[(raw.engine_id==1)&(raw.cycle==6),'sensor_2']=99999
    modified=engineer_features(raw)
    assert first.loc[:4,'sensor_2_mean5'].equals(modified.loc[:4,'sensor_2_mean5'])


def test_validation_rejects_duplicate_or_missing():
    with pytest.raises(ValueError,match='Duplicate'):
        validate_raw(pd.concat([observations(),observations().iloc[[0]]],ignore_index=True))
    raw=observations()
    raw.loc[0,'sensor_2']=np.nan
    with pytest.raises(ValueError,match='Missing'):
        validate_raw(raw)


def test_conformal_and_priority():
    assert conformal_radius([1,2,3],[2,4,6],alpha=.1)==3
    x=pd.DataFrame({'engine_id':[1,2], 'cycle':[30,100], 'rul_estimate':[10.,90.], 'rul_lower':[0.,70.], 'rul_upper':[20.,110.]})
    prioritized=assign_priority(x)
    assert prioritized.priority.tolist()==['Review now','Routine']


def test_inference_model_contract():
    fe=engineer_features(observations())
    model=DummyRegressor(strategy='constant',constant=35.0).fit(fe[FEATURES],np.ones(len(fe)))
    bundle={'feature_names':FEATURES,'model':model,'conformal_radius':7.0}
    scores,_=predict_assets(observations(),bundle)
    assert np.all(scores.rul_estimate==35)
    assert np.all(scores.rul_lower==28)
    assert np.all(scores.rul_upper==42)


def test_psi_symmetric_identity():
    z=np.linspace(0,10,101)
    assert abs(population_stability_index(z,z))<1e-12


def test_validation_rejects_malformed_inputs():
    with pytest.raises(ValueError, match="At least one observation"):
        validate_raw(pd.DataFrame(columns=RAW_COLUMNS))
    
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_raw(pd.DataFrame({"engine_id": [1], "cycle": [1]}))
        
    raw = observations()
    raw["sensor_1"] = raw["sensor_1"].astype(object)
    raw.loc[0, "sensor_1"] = "invalid_string"
    with pytest.raises(ValueError):
        validate_raw(raw)
        
    raw = observations()
    raw.loc[0, "sensor_3"] = np.inf
    with pytest.raises(ValueError, match="infinite or non-finite"):
        validate_raw(raw)

    raw = observations()
    raw["engine_id"] = raw["engine_id"].astype(float)
    raw.loc[0, "engine_id"] = 1.5
    with pytest.raises(ValueError, match="integer"):
        validate_raw(raw)

    raw = observations()
    raw.loc[0, "cycle"] = 0
    with pytest.raises(ValueError, match="positive"):
        validate_raw(raw)


def test_single_observation_engine():
    row = dict.fromkeys(RAW_COLUMNS, 2.0)
    row.update(engine_id=99, cycle=1)
    df = pd.DataFrame([row])
    fe = engineer_features(df)
    assert len(fe) == 1
    assert np.isfinite(fe[FEATURES].to_numpy(dtype=float)).all()
    assert fe.loc[0, "sensor_2_std5"] == 0.0
    assert fe.loc[0, "sensor_2_delta5"] == 0.0


def test_conformal_radius_boundaries():
    with pytest.raises(ValueError, match="alpha"):
        conformal_radius([1, 2], [1, 2], alpha=0.0)
    with pytest.raises(ValueError, match="alpha"):
        conformal_radius([1, 2], [1, 2], alpha=1.0)
    with pytest.raises(ValueError, match="finite and nonempty"):
        conformal_radius([], [])
    with pytest.raises(ValueError, match="finite and nonempty"):
        conformal_radius([1], [np.nan])


def test_priority_threshold_validation():
    scored = pd.DataFrame({"engine_id": [1], "cycle": [10], "rul_estimate": [50.0], "rul_lower": [40.0], "rul_upper": [60.0]})
    with pytest.raises(ValueError, match="greater"):
        assign_priority(scored, critical=30, watch=30)
    with pytest.raises(ValueError, match="greater"):
        assign_priority(scored, critical=30, watch=20)
    with pytest.raises(ValueError, match="greater"):
        assign_priority(scored, critical=-5, watch=20)


def test_psi_edge_cases():
    # Fewer than 5 observations
    assert np.isnan(population_stability_index([1, 2, 3], [1, 2, 3]))
    # Zero variance in base
    assert np.isnan(population_stability_index([5.0] * 10, [5.0, 5.1, 5.2, 5.3, 5.4]))
    # Non-finite values properly filtered
    base = np.array([1, 2, 3, 4, 5, 6, 7, 8, np.nan, np.inf])
    rec = np.array([1, 2, 3, 4, 5, 6, 7, 8, -np.inf])
    val = population_stability_index(base, rec)
    assert np.isfinite(val) and abs(val) < 1e-10

