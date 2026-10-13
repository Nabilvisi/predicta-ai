"""PREDICTA AI | Industrial engine health intelligence."""
# PEP 810 compatibility bridge: in Python 3.15+, defer Plotly until used.
# Earlier Python versions ignore this declaration and import normally.
# Keep before the corresponding module-level import statements.
__lazy_modules__ = ["plotly.express", "plotly.graph_objects"]

from pathlib import Path
import json
import sys
import hashlib

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from predicta.ui import setup_style, context_ribbon, engine_scene, methodology

from predicta.core import (
    RAW_COLUMNS, SENSORS, FEATURES, engineer_features, predict_assets,
    assign_priority, population_stability_index,
)

ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "predicta_fd001_model.joblib"
SAMPLE = ROOT / "data" / "sample" / "engine_history.csv"
TEST_PREDS = ROOT / "artifacts" / "test_predictions.csv"
IMPORTANCES = ROOT / "artifacts" / "permutation_importance.csv"
COMPARISON = ROOT / "artifacts" / "model_comparison.csv"

st.set_page_config(page_title="PREDICTA AI · Predictive Maintenance", page_icon="⚙️", layout="wide")
setup_style()

@st.cache_resource
def load_bundle():
    if not ARTIFACT.exists():
        return None
    # Load only the model artifact produced locally by the trusted training notebook.
    return joblib.load(ARTIFACT)

@st.cache_data
def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def read_optional(path: Path) -> pd.DataFrame:
    try:
        return read_csv(str(path)) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()

PRIORITY_COLORS = {
    "Review now": "#B42318",
    "Review soon": "#965400",
    "Watchlist": "#234FCC",
    "Routine": "#587975",
}

def bars(df: pd.DataFrame, x: str, y: str, title: str, color: str | None = None, color_map: dict | None = None):
    fig = px.bar(
        df, x=x, y=y, color=color, title=title,
        color_discrete_map=color_map,
        color_discrete_sequence=["#234FCC", "#965400", "#587975", "#768BCB"]
    )
    fig.update_layout(template="paper_atlas", height=350)
    st.plotly_chart(fig, use_container_width=True)

bundle = load_bundle()
model_release_id = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()[:12] if ARTIFACT.exists() else None
st.title("PREDICTA AI")
st.caption("NASA C-MAPSS FD001 · Physics-simulated data · Research use only")

if bundle is None:
    st.error("Trained model artifact unavailable.")
    st.markdown("Prediction services are temporarily unavailable because a validated model release has not been provisioned. Contact the system administrator.")
    st.markdown("**Data source:** [NASA C-MAPSS FD001](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data) · [GitHub mirror](https://github.com/PunVas/nasa-c-mapss)")
    st.stop()

with st.sidebar:
    st.header("Workspace")
    uploaded = st.file_uploader("Upload sensor history CSV", type=["csv"], help="26 fields: engine_id, cycle, 3 settings and 21 sensor channels.")
    if SAMPLE.exists():
        st.download_button("Download example engine history", SAMPLE.read_bytes(), file_name="engine_history.csv", mime="text/csv", on_click="ignore")
    st.divider()
    critical = st.slider("Immediate review threshold (cycles)", 5, 90, 30, 5)
    warning = st.slider("Watchlist threshold (cycles)", critical + 5, 200, max(60,critical+5), 5)
    capacity = st.slider("Planning capacity (engines)", 1, 50, 10)
    st.divider()
    methodology(bundle)

try:
    if uploaded is not None:
        input_df = pd.read_csv(uploaded)
        source = "Uploaded data"
    elif SAMPLE.exists():
        input_df = read_csv(str(SAMPLE))
        source = "NASA FD001 engine-history example"
    else:
        st.info("Upload a sensor-history CSV to enable sensor analytics and asset-level predictions. Run the notebook to generate a real example CSV.")
        input_df = None
        source = "No input selected"
    if input_df is not None:
        predictions, observations = predict_assets(input_df, bundle)
        ranked = assign_priority(predictions, critical=critical, watch=warning)
        display_preds = predictions.merge(ranked[["engine_id","priority"]],on="engine_id",how="left")
    else:
        predictions = observations = ranked = display_preds = None
except (ValueError, KeyError, TypeError) as exc:
    st.error("Input failed data-contract validation: " + str(exc))
    st.stop()

model_name = bundle.get("model_name", "Random forest")
conformal_alpha = 100 * (1 - float(bundle.get("alpha", 0.1)))
context_ribbon(source, model_release_id, conformal_alpha)

tabs = st.tabs(["Overview", "Sensor Explorer", "RUL Prediction", "Maintenance Planner", "Sensitivity Lab", "Model Diagnostics", "Data Contract"])

with tabs[0]:
    hero, visual = st.columns([1, 1.4], vertical_alignment="center")
    with hero:
        median = "—" if predictions is None else f"{predictions.rul_estimate.median():.1f}"
        st.markdown(f'<div class="pa-hero-copy"><h2 class="pa-deck">Read the life<br>of an engine.</h2><div class="pa-intro">An experimental view of remaining useful life.</div><div class="pa-number">{median} <small>cycles</small></div><div class="pa-number-label">Median predicted RUL</div></div>', unsafe_allow_html=True)
    with visual:
        engine_scene()
    cols = st.columns(3)
    cols[0].metric("Analyzed engines", "—" if predictions is None else f"{len(predictions):,}")
    cols[1].metric("Review now / soon", "—" if predictions is None else int(ranked.priority.isin(["Review now","Review soon"]).sum()))
    metric = bundle.get("test_metrics", {})
    cols[2].metric("Official test MAE", f"{metric['MAE']:.2f} cycles" if "MAE" in metric else "Not available", help="Measured on the separate official NASA FD001 test set, not the current input.")
    if predictions is not None:
        left, right = st.columns([2,1])
        with left:
            fig = px.scatter(display_preds, x="cycle", y="rul_estimate", hover_data=["engine_id","rul_lower","rul_upper"], color="priority", color_discrete_map=PRIORITY_COLORS,
                             title="Where each engine stands", labels={"cycle":"Operating cycle", "rul_estimate":"Estimated RUL (cycles)","priority":"Review"})
            fig.update_layout(template="paper_atlas", height=365, legend={"orientation":"h", "y":1.1,"title_text":""})
            st.plotly_chart(fig, use_container_width=True)
        with right:
            counts = ranked.priority.value_counts().reindex(["Review now","Review soon","Watchlist","Routine"],fill_value=0).reset_index()
            counts.columns = ["Priority","Engines"]
            fig = px.pie(counts[counts.Engines.gt(0)], names="Priority", values="Engines", hole=.76, color="Priority", color_discrete_map=PRIORITY_COLORS, title="Review distribution")
            fig.update_traces(textinfo="value", textposition="outside", hovertemplate="%{label}: %{value} engines<extra></extra>")
            fig.update_layout(template="paper_atlas", height=365, legend={"orientation":"h","y":-.1,"title_text":""}, annotations=[{"text":str(len(ranked)),"x":.5,"y":.5,"showarrow":False,"font":{"size":38,"color":"#17292D"}}])
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("Engine values"):
            st.dataframe(display_preds.round(2), use_container_width=True, hide_index=True)
            st.download_button("Download fleet report", display_preds.to_csv(index=False).encode(), "predicta_fleet_report.csv", "text/csv", on_click="ignore")
    else:
        st.info("Load engine sensor observations to display fleet analytics.")

with tabs[1]:
    st.subheader("Historical sensor behavior")
    if observations is None:
        st.info("Sensor history requires a CSV input.")
    else:
        c1,c2,c3 = st.columns(3)
        engine = c1.selectbox("Engine", options=sorted(observations.engine_id.unique().tolist()), key="sensor_engine")
        signal = c2.selectbox("Sensor", options=SENSORS, index=1)
        normalize = c3.toggle("Standardize within engine", value=False)
        subset = observations[observations.engine_id.eq(engine)].sort_values("cycle")
        values = subset[signal]
        if normalize:
            sd = values.std(ddof=0)
            values = (values - values.mean()) / sd if sd > 0 else values * 0.0
        fig = go.Figure()
        fig.add_scatter(x=subset.cycle, y=values, name=signal, mode="lines+markers", line={"color":"#234FCC"}, marker={"size": 4})
        fig.update_layout(title=f"Engine {engine} · {signal}", xaxis_title="Operating cycle", yaxis_title="Standardized value" if normalize else "Sensor value", template="paper_atlas", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=390)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Simulator signals · physical channel meanings and units are not guaranteed.")
        with st.expander("Sensor values"):
            st.dataframe(subset[["engine_id","cycle",signal,f"{signal}_mean5"]] if signal in bundle.get("rolling_sensors",[]) else subset[["engine_id","cycle",signal]], use_container_width=True, hide_index=True)
        stats = bundle.get("sensor_reference_stats", {})
        if stats:
            last = subset.iloc[-1]
            deviations = []
            for col in SENSORS:
                base = stats.get(col, {})
                scale = 1.4826 * float(base.get("mad", 0))
                if scale > 1e-10:
                    deviations.append({"sensor": col, "robust_deviation":
                                       abs(float(last[col]) - float(base["median"])) / scale})
            if deviations:
                st.markdown("#### Statistical sensor deviations")
                dframe = pd.DataFrame(deviations).nlargest(10, "robust_deviation")
                bars(dframe.sort_values("robust_deviation"), "robust_deviation", "sensor",
                     "Top deviations from training reference (median/MAD)")
                st.caption("A large numerical deviation does not imply a verified fault. Channels with negligible reference MAD are excluded.")

with tabs[2]:
    st.subheader("Remaining useful life estimates")
    if predictions is None:
        st.info("Upload valid engine history to score assets.")
    else:
        st.download_button("Export RUL predictions", display_preds.to_csv(index=False).encode(), "predicta_rul_predictions.csv", "text/csv", on_click="ignore")
        chosen = st.selectbox("Inspect engine", predictions.engine_id.tolist(), key="pred_engine")
        p = predictions.loc[predictions.engine_id.eq(chosen)].iloc[0]
        st.caption(f"Engine {chosen} · observation cycle {int(p.cycle)} · research estimate, not maintenance instructions")
        x,y,z=st.columns(3)
        x.metric("RUL estimate",f"{p.rul_estimate:.1f} cycles")
        y.metric("Lower interval",f"{p.rul_lower:.1f} cycles")
        z.metric("Upper interval",f"{p.rul_upper:.1f} cycles")
        fig=go.Figure()
        fig.add_trace(go.Bar(x=[float(p.rul_estimate)],y=[str(chosen)],orientation="h", name="Estimate", marker_color="#234FCC", error_x={"type":"data","symmetric":False,"array":[float(p.rul_upper-p.rul_estimate)],"arrayminus":[float(p.rul_estimate-p.rul_lower)]}))
        fig.update_layout(title="Point estimate and calibration-based interval",template="paper_atlas",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",height=250,xaxis_title="Remaining cycles")
        st.plotly_chart(fig,use_container_width=True)
        st.caption("The interval comes from independent calibration engines. Nominal coverage is not guaranteed on shifted deployment data.")
        with st.expander("All engine estimates"):
            st.dataframe(display_preds.sort_values("rul_estimate").round(2), use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Maintenance decision support")
    st.caption("Illustrative triage · user-selected thresholds · not repair recommendations.")
    if ranked is None:
        st.info("Prioritization becomes available after loading engine histories.")
    else:
        active = ranked.head(capacity).copy()
        top = st.columns(3)
        top[0].metric("Review now",int((ranked.priority=="Review now").sum()))
        top[1].metric("Review soon",int((ranked.priority=="Review soon").sum()))
        top[2].metric("Planning shortlist",len(active))
        st.download_button("Export prioritized worklist",ranked.to_csv(index=False).encode(),"predicta_maintenance_worklist.csv","text/csv", on_click="ignore")
        bars(active, "engine_id", "rul_estimate", f"Top {len(active)} engines by planning priority", "priority", color_map=PRIORITY_COLORS)
        with st.expander("Full worklist & policy"):
            st.dataframe(ranked[["engine_id","cycle","rul_estimate","rul_lower","rul_upper","priority"]].round(2),use_container_width=True,hide_index=True)
            st.caption("Thresholds have not been optimized using maintenance costs, failure probabilities or field histories.")

with tabs[4]:
    st.subheader("Controlled model sensitivity")
    st.caption("Change one sensor across its latest five cycles · model response, not physical causality.")
    stats = bundle.get("sensor_reference_stats", {})
    if predictions is None or not stats:
        st.info("Load engine-history data and a model with training sensor statistics to use this analysis.")
    else:
        perturbable_sensors = [k for k in SENSORS if float(stats.get(k, {}).get("std", 0)) > 1e-10]
        if not perturbable_sensors:
            st.info("No sensor channels with sufficient variance available for sensitivity analysis.")
        else:
            a, b, c = st.columns(3)
            eid = a.selectbox("Engine", sorted(predictions.engine_id.tolist()), key="sensitivity_engine")
            sensor = b.selectbox("Sensor to perturb", perturbable_sensors, key="sensitivity_sensor")
            shift = c.slider("Shift (training σ)", -2.0, 2.0, 0.5, 0.25)
            shifted = input_df.copy()
            mask = shifted.engine_id.eq(eid)
            idx = shifted.loc[mask].sort_values('cycle').tail(int(bundle.get('rolling_window',5))).index
            shifted.loc[idx,sensor] = (pd.to_numeric(shifted.loc[idx,sensor]) + shift * float(stats[sensor]['std']))
            try:
                altered,_ = predict_assets(shifted,bundle)
                base_value = float(predictions.loc[predictions.engine_id.eq(eid),'rul_estimate'].iloc[0])
                updated_value = float(altered.loc[altered.engine_id.eq(eid),'rul_estimate'].iloc[0])
                x,y,z=st.columns(3)
                x.metric("Baseline RUL", f"{base_value:.2f} cycles")
                y.metric("Perturbed RUL", f"{updated_value:.2f} cycles")
                z.metric("Model response",f"{updated_value-base_value:+.2f} cycles")
                comparison = pd.DataFrame({"Scenario": ["Baseline", "Perturbed"], "RUL (cycles)": [base_value, updated_value]})
                chart = px.bar(comparison, x="RUL (cycles)", y="Scenario", orientation="h", color="Scenario", color_discrete_sequence=["#587975", "#234FCC"], text_auto=".1f")
                chart.update_layout(template="paper_atlas", height=270, showlegend=False, title=f"Engine {eid} · {sensor} · {shift:+.2f} training σ")
                st.plotly_chart(chart, use_container_width=True)
                st.caption("Same fitted model · only the selected sensor was adjusted.")
            except ValueError as e:
                st.error(str(e))

with tabs[5]:
    st.subheader("Model validation and interpretability")
    metrics = bundle.get("test_metrics", {})
    m = st.columns(3)
    for idx,key in enumerate(("MAE","RMSE","R2")):
        if key in metrics:
            m[idx].metric("Official test " + key, f"{metrics[key]:.3f}")
    comparison = read_optional(COMPARISON)
    if len(comparison) and {"Model","Validation_MAE"}.issubset(comparison.columns):
        bars(comparison.sort_values("Validation_MAE"),"Model","Validation_MAE","Internal validation: model comparison")
    importance = read_optional(IMPORTANCES)
    if len(importance) and {"feature","mae_increase"}.issubset(importance.columns):
        imp = importance.nlargest(15,"mae_increase").sort_values("mae_increase")
        bars(imp,"mae_increase","feature","Permutation importance (internal validation)")
    testpred = read_optional(TEST_PREDS)
    if len(testpred) and {"true_rul","predicted_rul"}.issubset(testpred.columns):
        chart = px.scatter(
            testpred, x="true_rul", y="predicted_rul",
            labels={"true_rul": "Actual RUL (cycles)", "predicted_rul": "Predicted RUL (cycles)"},
            hover_data=[c for c in ["engine_id", "cycle", "rul_lower", "rul_upper", "absolute_error"] if c in testpred.columns],
            title="Official NASA test: actual vs predicted RUL",
            color_discrete_sequence=["#234FCC"]
        )
        maxv = float(max(testpred.true_rul.max(), testpred.predicted_rul.max()))
        chart.add_shape(type="line", x0=0, y0=0, x1=maxv, y1=maxv, line={"dash": "dash", "color": "#965400"})
        chart.update_layout(template="paper_atlas", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(chart, use_container_width=True)
    if observations is not None and "reference_features" in bundle:
        current = observations.sort_values(["engine_id","cycle"]).groupby("engine_id").tail(1)
        reference = bundle["reference_features"]
        checks = []
        for feature in bundle.get("drift_features", []):
            psi_val = population_stability_index(reference[feature], current[feature])
            checks.append({
                "feature": feature,
                "PSI": round(psi_val, 4) if np.isfinite(psi_val) else "N/A (< 5 assets)"
            })
        with st.expander("Exploratory input drift diagnostics"):
            st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
            st.caption("PSI is descriptive: alert thresholds are not calibrated. At least 5 assets are required for quantile estimation.")
    st.caption("Permutation importance describes sensitivity of fitted predictions to individual predictors, not causal contributions.")

with tabs[6]:
    st.subheader("Input schema and validation")
    a, b, c = st.columns(3)
    a.metric("Required fields", len(RAW_COLUMNS))
    b.metric("Sensor channels", len(SENSORS))
    c.metric("Rolling window", f"{int(bundle.get('rolling_window', 5))} cycles")
    st.caption("One row per engine and cycle · finite readings only · duplicate keys rejected.")
    with st.expander("CSV field contract"):
        st.code(", ".join(RAW_COLUMNS),language="text")
        st.write("All 26 fields are required. Observations are sorted within each engine; causal rolling features use recorded history. Only the latest cycle per engine is scored with the exact trained feature contract.")
    with st.expander("Training & uncertainty protocol"):
        st.write("Engine-disjoint training, validation and calibration, followed by official NASA test evaluation. Test labels never enter preprocessing, feature selection or model selection. Residual-quantile intervals use separate calibration engines; coverage can deteriorate under population shift.")
        st.write("NASA C-MAPSS FD001: physics-simulated turbofan degradation, one operating condition and one fault mode. Sensor deviations and perturbations are statistical checks, not physical fault identification.")
    st.markdown("[NASA dataset information](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data) | [Dataset mirror](https://github.com/PunVas/nasa-c-mapss)")
