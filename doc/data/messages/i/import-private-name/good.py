"""Private import can be used as type annotations."""

from argparse import _SubParsersAction


def add_sub_parser(sub_parsers: _SubParsersAction):
    sub_parsers.add_parser("my_subparser")
    # ...
