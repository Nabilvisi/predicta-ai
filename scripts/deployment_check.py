"""Static/pretrained release audit. Run: python -m scripts.deployment_check --strict"""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SOURCE = [
    "app.py", "requirements.txt", ".streamlit/config.toml",
    "notebooks/PREDICTA_AI_Advanced_Machine_Learning.ipynb",
    "predicta/core.py", "tests/test_core.py",
]
REQUIRED_MODELS = [
    "artifacts/predicta_fd001_model.joblib",
    "artifacts/run_manifest.json",
    "data/sample/engine_history.csv",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Require a validated model release and run inference parity checks")
    args = parser.parse_args()
    missing_source = [p for p in REQUIRED_SOURCE if not (ROOT / p).is_file()]
    missing_model = [p for p in REQUIRED_MODELS if not (ROOT / p).is_file()]
    print("Source files:", "PASS" if not missing_source else "MISSING " + ", ".join(missing_source))
    print("Model release:", "PRESENT" if not missing_model else "NOT BUILT " + ", ".join(missing_model))
    if missing_source:
        return 2
    if args.strict:
        if missing_model:
            print("Execute the real-data notebook before publishing the cloud application.")
            return 3
        from scripts import preflight  # performs strict prediction assertions on trusted artifacts
        print("Deployment gate: PASS")
    else:
        print("Source-only audit passed; --strict checks trained release files.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
