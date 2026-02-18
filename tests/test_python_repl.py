import genbdoc
from resources import cells


cells_indexes: list[int] = [cells.index(cell) for cell in cells if genbdoc.__is_python_repl_code_cell(cell)]

# %%          First REPL cell
############# First REPL cell ##################################################################################################

first_cell: str = """```python
>>> import sys
... 
>>> print("Hello code")
Hello code
"""

first_cell_output: str = "Hello code\n"

markdown_cell_text_after_1st_cell: str = """```
The snippet above should return an output cell.

"""


def test_1st_repl_cell():
    assert first_cell_output == genbdoc.__get_outputs(cells[cells_indexes[0]])
    assert first_cell == genbdoc.__format_python_repl_snippet_cell(cells[cells_indexes[0]], False)
    assert markdown_cell_text_after_1st_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[0] + 1], True)


# %%          Second REPL cell
############# Second REPL cell #################################################################################################

second_cell: str = """```python
>>> import os
... 
>>> cwd = os.getcwd()
"""

second_cell_output: str = ""

markdown_cell_text_after_2nd_cell: str = """```
The snippet above does not return output cells.

"""


def test_2nd_repl_cell():
    assert second_cell_output == genbdoc.__get_outputs(cells[cells_indexes[1]])
    assert second_cell == genbdoc.__format_python_repl_snippet_cell(cells[cells_indexes[1]], False)
    assert markdown_cell_text_after_2nd_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[1] + 1], True)
