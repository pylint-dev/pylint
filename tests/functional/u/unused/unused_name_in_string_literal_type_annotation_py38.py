# pylint: disable=missing-docstring
from argparse import ArgumentParser # [unused-import]
from argparse import Namespace  # [unused-import]
from typing import Literal as Lit
import typing as t

# str inside Literal shouldn't be treated as names
example1: t.Literal["ArgumentParser", Lit["Namespace", "ArgumentParser"]]


def unused_variable_example():
    hello = "hello" # [unused-variable]
    world = "world" # [unused-variable]
    example2: Lit["hello", "world"] = "hello"
    return example2
