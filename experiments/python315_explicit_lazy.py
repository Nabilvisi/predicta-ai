"""Python 3.15 ONLY: demonstration of PEP 810 explicit module-level lazy imports.

Run with: python3.15 experiments/python315_explicit_lazy.py
Not imported by application or notebook, so Python 3.11–3.14 remain supported.
"""
lazy import json
lazy from pathlib import Path
lazy import plotly.express as px


def main() -> None:
    # Modules are imported when their names are accessed for the first time.
    sample = {"component": "rul-inference", "mode": "demo"}
    print(json.dumps(sample))
    print('Repo directory:', Path(__file__).resolve().parents[1])
    # Plotly becomes necessary only for explicitly requested plotting.
    import sys
    if '--plotly' in sys.argv:
        chart = px.line(x=[1, 2, 3], y=[3, 2, 1], title='Lazy-import plotly demonstration')
        print('Chart object type:', type(chart).__name__)


if __name__ == '__main__':
    main()
