import clig
from .genbdoc import genbdoc
from .init import init


def main():
    clig.Command(genbdoc, make_shorts=True).add_subcommand(init).run()
