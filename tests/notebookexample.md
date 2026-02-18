# Example of tutorial documentation

This is an example of tutorial in the format of jupyter notebook. The cells in a
jupyter notebook can contain to types of information: markdown text or code.

## Markdown text

The cells in the format of markdown text is simply text that will be reproduced
in markdown files when processed.

## Code cells

The cells in the format of code cells can contain python code, in general, but
also other contents. These cells can appear in 3 possibly formats:

- Simple python snippets (REPL)
- Python code that would be written inside of a source code file
- Shell commands

### Python REPL snippets

The follwing cell has a simple python snippet that would be interpreted as code
inside of a REPL, i.e., code run in a command line starting with `>>>`:

```python
>>> import sys
...
>>> print("Hello code")
Hello code
```

The snippet above should return an output cell.

```python
>>> import os
...
>>> cwd = os.getcwd()
```

The snippet above does not return output cells.

### Python code in files

The follwing cell has a python code that would be written in a script file

```python
# script.py
from pathlib import Path
cwd = Path().cwd()
```

The script above would not return an output. However, even if it would, the
output should not be rendered.

```python
# example.py
from pathlib import Path
cwd = Path().cwd()
print(cwd)
```

The output above should not be rendered

### Shell commands

The follwing cell has a shell command, that has an output.

```
> python -c "print('hello')"

hello
```

The above code renders as a shell command with output.

```
> python -c "print(-)"

File "<string>", line 1
    print(-)
           ^
SyntaxError: invalid syntax
```

The above renders normally with output error.

The next is a file script, that is run as shell command after. The output must
be ignored. In this case, the cell start with `%%` to supres the output.

```python
# script_argv_example.py
import sys

print("Printing the input as integer number: ", int(sys.argv[1]))
```

```
> python script_argv_example.py 38

Printing the input as integer number:  38
```

The next shows the output error but removing the traceback.

```
> python script_argv_example.py -

ValueError: invalid literal for int() with base 10: '-'
```

Only the `ValueError` is shown.
