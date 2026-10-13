"""Reproducible real-data notebook training for trusted model release.

Run at repository root: python -m scripts.train_release
Does not invent or include model metrics; requires GitHub network access.
"""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "PREDICTA_AI_Advanced_Machine_Learning.ipynb"
OUT = ROOT / "artifacts" / "executed_training_notebook.ipynb"

def main():
    nb = nbformat.read(NOTEBOOK, as_version=4)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        client = NotebookClient(nb, timeout=1800, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}})
        client.execute()
    except Exception:
        nbformat.write(nb, OUT)
        print(f"Notebook failed; inspect partial execution record: {OUT}")
        raise
    nbformat.write(nb, OUT)
    print(f"Notebook executed with authentic training data; saved to {OUT}")
    print("Run: python -m scripts.preflight")

if __name__ == "__main__":
    main()
