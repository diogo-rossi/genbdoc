import genbdoc
from resources import cells


cells_indexes: list[int] = [cells.index(cell) for cell in cells if genbdoc.__is_shell_command_code_cell(cell)]

# %%          First cell
############# First cell #######################################################################################################

first_cell: str = """```
> python -c "print('hello')"

hello
```
"""

first_cell_output: str = "hello\n"

markdown_cell_text_after_1st_cell: str = """The above code renders as a shell command with output.

"""


def test_1st_shell_cell():
    assert first_cell == genbdoc.__format_shell_cell(cells[cells_indexes[0]], False)
    assert first_cell_output == genbdoc.__get_outputs(cells[cells_indexes[0]])
    assert markdown_cell_text_after_1st_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[0] + 1], False)


# %%          Second cell
############# Second cell ######################################################################################################

second_cell: str = """```
> python -c "print(-)"

File "<string>", line 1
    print(-)
           ^
SyntaxError: invalid syntax
```
"""

second_cell_output: str = """File "<string>", line 1
    print(-)
           ^
SyntaxError: invalid syntax
"""

markdown_cell_text_after_2nd_cell: str = """The above renders normally with output error.

"""


def test_2nd_shell_cell():
    assert second_cell == genbdoc.__format_shell_cell(cells[cells_indexes[1]], False)
    assert second_cell_output == genbdoc.__get_outputs(cells[cells_indexes[1]])
    assert markdown_cell_text_after_2nd_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[1] + 1], False)


# %%          Third cell
############# Third cell #######################################################################################################

third_cell: str = """```
> python script_argv_example.py 38

Printing the input as integer number:  38
```
"""

third_cell_output: str = """Printing the input as integer number:  38
"""

markdown_cell_text_after_3rd_cell: str = """The next shows the output error but removing the traceback.

"""


def test_3rd_shell_cell():
    assert third_cell == genbdoc.__format_shell_cell(cells[cells_indexes[2]], False)
    assert third_cell_output == genbdoc.__get_outputs(cells[cells_indexes[2]])
    assert markdown_cell_text_after_3rd_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[2] + 1], False)


# %%          Fourth cell
############# Fourth cell ######################################################################################################

fourth_cell: str = """```
> python script_argv_example.py -

ValueError: invalid literal for int() with base 10: '-'
```
"""

fourth_cell_output: str = """ValueError: invalid literal for int() with base 10: '-'
"""

markdown_cell_text_after_4th_cell: str = """Only the `ValueError` is shown.

"""


def test_4th_shell_cell():
    assert fourth_cell == genbdoc.__format_shell_cell(cells[cells_indexes[3]], False)
    assert fourth_cell_output == genbdoc.__get_outputs(cells[cells_indexes[3]])
    assert markdown_cell_text_after_4th_cell == genbdoc.__format_markdown_cell(cells[cells_indexes[3] + 1], False)
