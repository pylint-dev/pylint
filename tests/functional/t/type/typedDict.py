"""Test typing.TypedDict"""
# pylint: disable=invalid-name,missing-class-docstring,pointless-statement
import typing
from typing import TypedDict


class CustomTD(TypedDict):
    var: int


class CustomTD2(typing.TypedDict, total=False):
    var2: str


class CustomTD3(CustomTD2):
    var3: int


CustomTD4 = TypedDict("CustomTD4", var4=bool)

CustomTD5 = TypedDict("CustomTD5", {"var5": bool})

my_dict = CustomTD(var=1)
my_dict["var"]
my_dict["var"] = 2


# https://github.com/pylint-dev/pylint/issues/4715
# Instance of TypedDict should be callable
Link = TypedDict("Link", {"href": str})
Link(href="foo")
