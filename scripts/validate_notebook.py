"""Validate notebook content without downloading datasets or claiming ML scores."""
from pathlib import Path
import nbformat

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    notebook_file = root / "notebooks" / "PREDICTA_AI_Advanced_Machine_Learning.ipynb"
    notebook = nbformat.read(notebook_file, as_version=4)
    nbformat.validate(notebook)
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == 'code':
            compile(cell.source, f'{notebook_file.name}:cell_{index}', 'exec')
    print(f'Notebook validated: {len(notebook.cells)} cells')

if __name__ == '__main__':
    main()
