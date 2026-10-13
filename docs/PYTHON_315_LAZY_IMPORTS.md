# Python 3.15 and PEP 810: scoped adoption plan

**Current status (2026-10-13):** Python 3.15.0 stable was released on **2026-10-09**.
Sources: <https://www.python.org/downloads/release/python-3150/> and <https://peps.python.org/pep-0810/>.

## Deployment policy

- **Recommended deployment runtime: Python 3.12** until the selected ML and hosting environment is tested end-to-end on 3.15. `.python-version` pins the baseline for tools honoring this file; for Streamlit Community Cloud select the appropriate Python version in deployment settings.
- Tests cover Python 3.11–3.14. An **experimental 3.15 CI job** is non-blocking because third-party binary wheels may lag a new language release.
- In `app.py`, the module-scoped `__lazy_modules__` bridge is defined before `import plotly.express as px` and `import plotly.graph_objects as go`. Python 3.15 treats those imports as lazy; older versions ignore the declaration. Most pages use Plotly, so benchmark before claiming a startup improvement.
- A standalone Python-3.15-only demonstration is in `experiments/python315_explicit_lazy.py` with explicit `lazy import` syntax. **Do not import this file in older Python environments.**

## Try Python 3.15

```bash
# Run inside a Python 3.15 environment with the dependencies installed.
python experiments/python315_explicit_lazy.py
python experiments/python315_explicit_lazy.py --plotly
python -m pytest -q
python -m scripts.preflight  # only AFTER training the real dataset
streamlit run app.py          # only AFTER producing model artifacts
```

Native Python 3.15 syntax:

```python
lazy import json
lazy from pathlib import Path
```

Cross-version bridge (eager on old Python, potentially lazy in 3.15+):

```python
__lazy_modules__ = ["plotly.express"]
import plotly.express as px
```

PEP 810 lazy imports can postpone `ImportError` until first use, so **run every app page** and run application-level checks. They do not make ML inference faster, automatically upgrade dependencies, or update the interpreter. A newer Python interpreter also requires compatible versions of NumPy, pandas, SciPy, scikit-learn and Streamlit. Update dependencies via reviewed Dependabot PRs, not unrestricted auto-upgrade in production.

## Profiling and rollout

1. Compare import overhead: `python -X importtime -c 'import plotly.express' 2> importtime_plotly.txt`.
2. Benchmark application cold starts and page navigation on the same machine, using controlled repeated runs. Do not claim performance gains without measurements.
3. Ensure `python -m pytest`, notebook output equivalence, `scripts.preflight` and complete Streamlit smoke tests pass with the validated real-trained model.
4. Promote 3.15 to `.python-version` only after dependency resolution and deployment platform support have been verified.

## Restrictions

`lazy import` is valid **only at module level** in Python 3.15; not inside functions, classes or `try` blocks. Do not use the global `PYTHON_LAZY_IMPORTS=all` mode as a blanket configuration for the project because it changes third-party import behavior and can delay failures.
