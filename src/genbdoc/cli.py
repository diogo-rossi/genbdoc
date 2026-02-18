import clig
from genbdoc import nbtomd
import genbdoc.init


def pyproj():
    pass


def doc():
    pass


def init():
    pass


def genex():
    pass


def main():
    # fmt: off
    (
        clig.Command(pyproj, make_shorts=True)
        .add_subcommand(genbdoc.init.init)
        .new_subcommand(doc)
            .add_subcommand(init)
            .add_subcommand(nbtomd, make_shorts=True)
            .end_subcommand(genex)
    ).run()
