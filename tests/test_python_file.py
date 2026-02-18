import genbdoc
from resources import cells


cells_indexes: list[int] = [cells.index(cell) for cell in cells if genbdoc.__is_python_file_code_cell(cell)]

# %%          First file cell
############# First file cell ##################################################################################################

first_cell: str = """```python
# script.py
from pathlib import Path
cwd = Path().cwd()
```
"""

first_cell_output: str = ""

markdown_cell_text_after_1st_cell: str = """The script above would not return an output. However, even if it would, the
output should not be rendered.

"""


def test_1st_file_cell():
    assert first_cell_output == genbdoc.__get_outputs(cells[cells_indexes[0]])
    assert first_cell == genbdoc.__format_python_file_cell(cells[cells_indexes[0]], False)
    assert markdown_cell_text_after_1st_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[0] + 1], False)


# %%          Second file cell
############# Second file cell #################################################################################################

second_cell: str = """```python
# example.py
from pathlib import Path
cwd = Path().cwd()
print(cwd)
```
"""

second_cell_output: str = ""

markdown_cell_text_after_2nd_cell: str = """The output above should not be rendered

"""


def test_2nst_file_cell():
    assert second_cell == genbdoc.__format_python_file_cell(cells[cells_indexes[1]], False)
    assert second_cell_output == genbdoc.__get_outputs(cells[cells_indexes[1]])
    assert markdown_cell_text_after_2nd_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[1] + 1], False)
