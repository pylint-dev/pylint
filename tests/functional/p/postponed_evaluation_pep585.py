"""Test PEP 585 in combination with postponed evaluation PEP 563.

This check requires Python 3.7 or 3.8!
Testing with 3.8 only, to support TypedDict.
"""
# pylint: disable=missing-docstring,unused-argument,unused-import,too-few-public-methods,invalid-name,inherit-non-class
from __future__ import annotations
import collections
import dataclasses
import typing
from typing import NamedTuple, TypedDict
from dataclasses import dataclass


AliasInvalid = list[int]  # [unsubscriptable-object]

class CustomIntList(typing.List[int]):
    pass

class CustomIntListError(list[int]):  # [unsubscriptable-object]
    pass

cast_variable = [1, 2, 3]
cast_variable = typing.cast(list[int], cast_variable)  # [unsubscriptable-object]

T = typing.TypeVar("T", list[int], str)  # [unsubscriptable-object]

(lambda x: 2)(list[int])  # [unsubscriptable-object]


# Check typing.NamedTuple
CustomNamedTuple = typing.NamedTuple(
    "CustomNamedTuple", [("my_var", list[int])])  # [unsubscriptable-object]

class CustomNamedTuple2(NamedTuple):
    my_var: list[int]

class CustomNamedTuple3(typing.NamedTuple):
    my_var: list[int]


# Check typing.TypedDict
CustomTypedDict = TypedDict("CustomTypedDict", my_var=list[int])  # [unsubscriptable-object]

CustomTypedDict2 = TypedDict("CustomTypedDict2", {"my_var": list[int]})  # [unsubscriptable-object]

class CustomTypedDict3(TypedDict):
    my_var: list[int]

class CustomTypedDict4(typing.TypedDict):
    my_var: list[int]


# Check dataclasses
def my_decorator(*args, **kwargs):
    def wraps(*args, **kwargs):
        pass
    return wraps

@dataclass
class CustomDataClass:
    my_var: list[int]

@dataclasses.dataclass
class CustomDataClass2:
    my_var: list[int]

@dataclass()
class CustomDataClass3:
    my_var: list[int]

@my_decorator
@dataclasses.dataclass
class CustomDataClass4:
    my_var: list[int]


# Allowed use cases
var1: set[int]
var2: collections.OrderedDict[str, int]

def func(arg: list[int]):
    pass

def func2() -> list[int]:
    pass
