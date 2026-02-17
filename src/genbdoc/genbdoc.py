# %%          IMPORTS
############# IMPORTS ##########################################################################################################

from typing import TypedDict, Literal
from pathlib import Path
import json

# %%          CLASSES
############# CLASSES ##########################################################################################################

Data = TypedDict("Data", {"text/plain": list[str]})


class Output(TypedDict):
    name: str
    output_type: Literal["stream", "execute_result"]
    text: list[str]
    data: Data


class MetaData(TypedDict):
    tags: list[str]


class Cell(TypedDict):
    cell_type: Literal["markdown", "code"]
    source: list[str]
    metadata: MetaData
    outputs: list[Output]


class Notebook(TypedDict):
    cells: list[Cell]


# %%          AUX FUNCTIONS
############# AUX FUNCTIONS ####################################################################################################


def end_snippet(previous_was_snippet: bool):
    return "```\n" if previous_was_snippet else ""


def get_outputs(cell: Cell):
    lines = []
    for o in cell["outputs"]:
        if o["output_type"] == "stream":
            lines.append("".join(o["text"]))
        if o["output_type"] == "execute_result":
            lines.append("".join(o["data"]["text/plain"]))
    out = "".join(lines)
    if "Traceback " in out:
        out = cell["outputs"][-1]["text"][-1]

    return out.strip() + "\n" if out else ""


# %%          FORMAT FUNCTIONS
############# FORMAT FUNCTIONS #################################################################################################


def format_markdown_cell(cell: Cell, previous_was_snippet: bool) -> str:
    out = end_snippet(previous_was_snippet) + "".join(cell["source"])
    return out + ("\n" if not out.endswith("\n") else "")


def format_python_file_cell(cell: Cell, previous_was_snippet: bool):
    return end_snippet(previous_was_snippet) + "```python\n" + "".join(cell["source"][1:]) + "\n```\n"


def format_shell_cell(cell: Cell, previous_was_snippet: bool):
    return (
        (end_snippet(previous_was_snippet)) + ("```\n>" + cell["source"][0].lstrip("!")) + "\n\n" + get_outputs(cell) + "```\n"
    )


def format_python_snippet_cell(cell: Cell, previous_was_snippet: bool):
    lines: list[str] = []
    for line in cell["source"]:
        lines.append(f"... {line}" if (line.startswith(" ") or len(line.strip()) == 0) else f">>> {line}")
    lines = [line for line in lines if ">>> pass" not in line]
    content = ("" if previous_was_snippet else "```python\n") + "".join(lines)
    return content.strip() + "\n" + get_outputs(cell)


# %%          MAIN FUNCTION
############# MAIN FUNCTION ####################################################################################################


def genbdoc(filepath: Path | None = None, kind: Literal["tutorial", "function", "class"] = "tutorial"):

    if filepath is None:
        return

    with open(filepath.resolve(), "r", encoding="utf-8") as file:
        notebook: Notebook = json.load(file)

    lines: list[str] = []

    previous_was_simple_python_snippet_cell: bool = False
    for cell in notebook["cells"]:

        if cell["metadata"] and "to_hide" in cell["metadata"]["tags"]:
            continue

        if cell["cell_type"] == "markdown":
            lines.append(format_markdown_cell(cell, previous_was_simple_python_snippet_cell))
            previous_was_simple_python_snippet_cell = False

        if cell["cell_type"] == "code" and len(cell["source"]) > 0:
            if cell["source"][0].startswith("!"):
                lines.append(format_shell_cell(cell, previous_was_simple_python_snippet_cell))
                previous_was_simple_python_snippet_cell = False
            elif cell["source"][0].startswith("%%"):
                lines.append(format_python_file_cell(cell, previous_was_simple_python_snippet_cell))
                previous_was_simple_python_snippet_cell = False
            else:
                lines.append(format_python_snippet_cell(cell, previous_was_simple_python_snippet_cell))
                previous_was_simple_python_snippet_cell = True

    text: str = "".join(lines)
    
    with open(filepath.with_suffix(".md"), "w", encoding="utf-8") as file
        file.write(text)