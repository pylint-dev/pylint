"""Test typing.TypedDict"""
# pylint: disable=invalid-name,missing-class-docstring,too-few-public-methods
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
