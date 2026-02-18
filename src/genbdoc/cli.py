import clig
from genbdoc import nbtomd
import genbdoc.init


def pyprojdev():
    pass


def docs():
    pass


def init():
    pass


def genex():
    pass


def main():
    # fmt: off
    (
        clig.Command(pyprojdev, make_shorts=True)
        .add_subcommand(genbdoc.init.init)
        .new_subcommand(docs)
            .add_subcommand(init)
            .add_subcommand(nbtomd, make_shorts=True)
            .end_subcommand(genex)
    ).run()
