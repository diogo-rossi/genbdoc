# %%          IMPORTS
############# IMPORTS ##########################################################################################################

from typing import TypedDict, Literal
from pathlib import Path
from collections.abc import Iterable
import json
import os

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


def __end_snippet(previous_was_snippet: bool):
    return "```\n" if previous_was_snippet else ""


def __get_outputs(cell: Cell) -> str:

    if __is_python_file_code_cell(cell):
        return ""

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


def __format_markdown_cell(cell: Cell, previous_was_snippet: bool) -> str:
    out = __end_snippet(previous_was_snippet) + "".join(cell["source"])
    return out.strip() + "\n\n"


def __format_python_file_cell(cell: Cell, previous_was_snippet: bool):
    return __end_snippet(previous_was_snippet) + "```python\n" + "".join(cell["source"][1:]) + "\n```\n"


def __format_shell_cell(cell: Cell, previous_was_snippet: bool):
    return (
        (__end_snippet(previous_was_snippet))
        + ("```\n>" + cell["source"][0].lstrip("!"))
        + "\n\n"
        + __get_outputs(cell)
        + "```\n"
    )


def __format_python_repl_snippet_cell(cell: Cell, previous_was_snippet: bool):
    lines: list[str] = []
    for line in cell["source"]:
        lines.append(f"... {line}" if (line.startswith(" ") or len(line.strip()) == 0) else f">>> {line}")
    lines = [line for line in lines if ">>> pass" not in line]
    content = ("" if previous_was_snippet else "```python\n") + "".join(lines)
    return content.strip() + "\n" + __get_outputs(cell)


def __is_code_cell_with_source_content(cell: Cell) -> bool:
    return cell["cell_type"] == "code" and len(cell["source"]) > 0


def __is_code_cell_starting_with(cell: Cell, char: str) -> bool:
    return __is_code_cell_with_source_content(cell) and cell["source"][0].startswith(char)


def __is_shell_command_code_cell(cell: Cell) -> bool:
    return __is_code_cell_starting_with(cell, "!")


def __is_python_file_code_cell(cell: Cell) -> bool:
    return __is_code_cell_starting_with(cell, "%%") and cell["source"][1].startswith("#")


def __is_python_repl_code_cell(cell: Cell) -> bool:
    return __is_code_cell_with_source_content(cell) and not any(
        [__is_shell_command_code_cell(cell), __is_python_file_code_cell(cell)]
    )


# %%          MAIN FUNCTION
############# MAIN FUNCTION ####################################################################################################


def nbtomd(
    filepath: list[Path] | Path,
    kind: Literal["tutorial", "function", "class"] = "tutorial",
    prettier: bool = True,
):

    if not isinstance(filepath, Iterable):
        filepath = [filepath]

    for path in filepath:

        with open(path.resolve(), "r", encoding="utf-8") as file:
            notebook: Notebook = json.load(file)

        lines: list[str] = []

        previous_was_simple_python_repl_snippet: bool = False
        for cell in notebook["cells"]:

            if cell["metadata"] and "to_hide" in cell["metadata"]["tags"]:
                continue

            if cell["cell_type"] == "markdown":
                lines.append(__format_markdown_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = False

            if __is_shell_command_code_cell(cell):
                lines.append(__format_shell_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = False

            if __is_python_file_code_cell(cell):
                lines.append(__format_python_file_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = False

            if __is_python_repl_code_cell(cell):
                lines.append(__format_python_repl_snippet_cell(cell, previous_was_simple_python_repl_snippet))
                previous_was_simple_python_repl_snippet = True

        text: str = "".join(lines)

        markdown_filepath: Path = path.with_suffix(".md")

        with open(markdown_filepath, "w", encoding="utf-8") as file:
            file.write(text)

        if prettier:
            os.system(f"prettier --write {markdown_filepath}")


def __get_notebook_example_prefix(cells: list[Cell]) -> str:
    for cell in reversed(cells):
        if cell["metadata"]:
            for tag in cell["metadata"]["tags"]:
                if tag.startswith("ex_"):
                    return tag.removeprefix("ex_")
    return "example"


from clig import Arg, data


def genex(
    filepath: Arg[list[Path] | Path, data(nargs="*")],
    change_shell_cells: bool = False,
    output_suffix: str = "",
):

    if not filepath:
        filepath = list(Path.cwd().glob("*.ipynb"))

    if not isinstance(filepath, Iterable):
        filepath = [filepath]

    for path in filepath:

        with open(path.resolve(), "r", encoding="utf-8") as file:
            notebook: Notebook = json.load(file)

        cells: list[Cell] = notebook["cells"]

        example_number: int = 0
        previous_example_prefix: str = __get_notebook_example_prefix(cells[:1])
        example_prefix = previous_example_prefix

        for i, cell in enumerate(cells):

            source: list[str] | None = cell.get("source")

            if __is_python_file_code_cell(cell):
                example_prefix: str = __get_notebook_example_prefix(cells[: i + 1])
                if example_prefix == previous_example_prefix:
                    example_number += 1
                else:
                    example_number = 1
                    previous_example_prefix = example_prefix

                example_filename: str = f"{example_prefix}{example_number:02d}.py"
                source[1] = f"# {example_filename}\n"

                with open(example_filename, "w", encoding="utf-8") as file:
                    file.write("".join(source[1:]))

            if change_shell_cells:
                if __is_shell_command_code_cell(cell):
                    if source[0].startswith("! python") and any([s.endswith(".py") for s in source[0].split()]):
                        parts: list[str] = source[0].split(".py")
                        parts[0] = f"! python {example_prefix}{example_number:02d}.py"
                        source[0] = "".join(parts)

            if source:
                cell["source"] = source  # update source
                cells[i] = cell  # update cell

        notebook["cells"] = cells
        if output_suffix:
            path: Path = path.with_suffix(f".{output_suffix}.ipynb")

        with open(path, "w", encoding="utf-8") as file:
            json.dump(notebook, file, indent=4)
