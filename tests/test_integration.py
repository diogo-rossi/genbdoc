from resources import notebook_filepath

import genbdoc


def test_write_md_file():
    genbdoc.genbdoc(notebook_filepath)
