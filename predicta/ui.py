"""Paper Atlas presentation helpers; no training or inference logic."""
from functools import lru_cache
from html import escape
from pathlib import Path

import plotly.io as pio
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
ACCENT = "#234FCC"
INK = "#17292D"


@lru_cache(maxsize=1)
def stylesheet() -> str:
    return (ROOT / "static" / "paper-atlas.css").read_text(encoding="utf-8")


def setup_style():
    st.markdown(f"<style>{stylesheet()}</style>", unsafe_allow_html=True)
    st.markdown('<a class="pa-skip" href="#analysis-start">Skip to analysis</a><span id="analysis-start" tabindex="-1"></span>', unsafe_allow_html=True)
    theme = pio.templates["plotly_white"].to_plotly_json()
    theme["layout"].update(
        font={"family": "IBM Plex Sans, sans-serif", "color": INK, "size": 13},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        colorway=[ACCENT, "#A76217", "#587975", "#768BCB"],
        xaxis={"gridcolor": "#DCE0D5", "zerolinecolor": "#DCE0D5", "automargin": True},
        yaxis={"gridcolor": "#DCE0D5", "zerolinecolor": "#DCE0D5", "automargin": True},
        margin={"l": 25, "r": 25, "t": 55, "b": 45},
    )
    pio.templates["paper_atlas"] = theme


def context_ribbon(source: str, release: str, calibration: float):
    st.markdown(
        '<div class="pa-context" aria-label="Analysis context">'
        f'<span class="pa-source">{escape(source)}</span>'
        '<span>Random Forest Champion</span>'
        f'<span>SHA256 {escape(release)}</span>'
        f'<span>{calibration:.0f}% nominal calibration</span></div>',
        unsafe_allow_html=True,
    )


def engine_scene():
    """Schematic illustration. Geometry and rotation do not encode sensor data."""
    components.html(
        (ROOT / "static" / "turbine.html").read_text(encoding="utf-8"),
        height=320, scrolling=False,
    )


def methodology(bundle: dict):
    with st.expander("Method & limitations"):
        st.markdown(
            "NASA C-MAPSS FD001 contains **physics-simulated turbofan histories**. "
            "It is not equipment telemetry. Predictions use the latest recorded cycle "
            "and are research estimates, not certified maintenance instructions."
        )
        st.markdown(
            "Training, validation and calibration use separate engine groups. "
            "Official test metrics come from the independent NASA test set. "
            "Residual-based intervals are calibrated on separate engines; nominal "
            "coverage can deteriorate on shifted inputs."
        )
        st.caption(
            f"Calibration radius: ±{bundle.get('conformal_radius', 0):.1f} cycles. "
            "Review categories use interval lower bounds and your thresholds. "
            "The 3D model is an illustration, not reconstructed engine geometry."
        )

