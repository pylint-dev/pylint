# pylint: disable=missing-docstring

from argparse import ArgumentParser # [unused-import]
from argparse import Namespace  # [unused-import]
import http  # [unused-import]
from http import HTTPStatus
import typing as t
from typing import Literal as Lit

# str inside Literal shouldn't be treated as names
example1: t.Literal["ArgumentParser", Lit["Namespace", "ArgumentParser"]]


def unused_variable_example():
    hello = "hello" # [unused-variable]
    world = "world" # [unused-variable]
    example2: Lit["hello", "world"] = "hello"
    return example2


# pylint shouldn't crash with the following strings in a type annotation context
example3: Lit["", " ", "?"] = "?"


# See https://peps.python.org/pep-0586/#literals-enums-and-forward-references
example4: t.Literal["http.HTTPStatus.OK", "http.HTTPStatus.NOT_FOUND"]
example5: "t.Literal[HTTPStatus.OK, HTTPStatus.NOT_FOUND]"
