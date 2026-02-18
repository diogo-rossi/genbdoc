import json
from pathlib import Path
from genbdoc import Notebook

THIS_DIR = Path(__file__).parent

notebook_filepath: Path = THIS_DIR / "notebookexample.ipynb"
with open(notebook_filepath, "r", encoding="utf-8") as file:
    notebook: Notebook = json.load(file)

cells = notebook["cells"]
