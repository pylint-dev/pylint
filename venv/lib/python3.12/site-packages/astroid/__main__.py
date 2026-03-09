# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/pylint-dev/astroid/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/astroid/blob/main/CONTRIBUTORS.txt

"""Command line interface for astroid."""

from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import cast

import astroid


class Arguments(Namespace):
    func: Callable[[Arguments], int]


class ASTParserArguments(Arguments):
    file: str


def parse_ast(args: ASTParserArguments) -> int:
    if not ((file := Path(args.file)).is_file() and file.suffix in {".py", ".pyi"}):
        print(f"error: '{file}' does not exist or isn't a Python file")
        return 1

    tree = astroid.parse(file.read_text(encoding="utf8"))
    print(tree.repr_tree())
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    parser = ArgumentParser(description="Command line interface for astroid")
    subparsers = parser.add_subparsers()

    ast_parser = subparsers.add_parser("ast", help="Print astroid AST")
    ast_parser.set_defaults(func=parse_ast)
    ast_parser.add_argument("file", metavar="FILE", help="File to parse")

    args = cast(Arguments, parser.parse_args(argv))
    if "func" not in args:
        parser.print_help()
        return 2

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
