"""Test PEP 585 without postponed evaluation. Everything should fail.

This check requires Python 3.7 or Python 3.8!
Testing with 3.8 only, to support TypedDict.
"""
# pylint: disable=missing-docstring,unused-argument,unused-import,too-few-public-methods,invalid-name,inherit-non-class
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
    my_var: list[int]  # [unsubscriptable-object]

class CustomNamedTuple3(typing.NamedTuple):
    my_var: list[int]  # [unsubscriptable-object]


# Check typing.TypedDict
CustomTypedDict = TypedDict("CustomTypedDict", my_var=list[int])  # [unsubscriptable-object]

CustomTypedDict2 = TypedDict("CustomTypedDict2", {"my_var": list[int]})  # [unsubscriptable-object]

class CustomTypedDict3(TypedDict):
    my_var: list[int]  # [unsubscriptable-object]

class CustomTypedDict4(typing.TypedDict):
    my_var: list[int]  # [unsubscriptable-object]


# Check dataclasses
def my_decorator(*args, **kwargs):
    def wraps(*args, **kwargs):
        pass
    return wraps

@dataclass
class CustomDataClass:
    my_var: list[int]  # [unsubscriptable-object]

@dataclasses.dataclass
class CustomDataClass2:
    my_var: list[int]  # [unsubscriptable-object]

@dataclass()
class CustomDataClass3:
    my_var: list[int]  # [unsubscriptable-object]

@my_decorator
@dataclasses.dataclass
class CustomDataClass4:
    my_var: list[int]  # [unsubscriptable-object]



var1: set[int]  # [unsubscriptable-object]
var2: collections.OrderedDict[str, int]  # [unsubscriptable-object]

def func(arg: list[int]):  # [unsubscriptable-object]
    pass

def func2() -> list[int]:  # [unsubscriptable-object]
    pass
