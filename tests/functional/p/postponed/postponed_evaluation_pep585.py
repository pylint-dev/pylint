"""Test PEP 585 in combination with postponed evaluation PEP 563.

This check requires Python 3.7 or 3.8!
Testing with 3.8 only, to support TypedDict.
"""

# pylint: disable=missing-docstring,unused-argument,unused-import,too-few-public-methods,invalid-name
# pylint: disable=inherit-non-class,unsupported-binary-operation,wrong-import-position,ungrouped-imports
# pylint: disable=unused-variable,unnecessary-direct-lambda-call

# Disabled because of a bug with pypy 3.8 see
# https://github.com/PyCQA/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from __future__ import annotations
import collections
import dataclasses
import typing
from dataclasses import dataclass
from typing import Any, Dict, NamedTuple, TypedDict, Union, Tuple


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


var1: set[int]
var2: collections.OrderedDict[str, int]
var3: dict[str, list[int]]
var4: Dict[str, list[int]]
var5: dict[tuple[int, int], str]
var6: Dict[tuple[int, int], str]
var7: list[list[int]]
var8: tuple[list[int]]
var9: int | list[str | int]
var10: Union[list[str], None]
var11: Union[Union[list[int], int]]

def func(arg: list[int]):
    pass

def func2() -> list[int]:
    pass

Alias2 = Union[list[str], None]  # [unsubscriptable-object]
Alias3 = Union[Union[list[int], int]]  # [unsubscriptable-object]
Alias4 = Tuple[list[int]]  # [unsubscriptable-object]
Alias5 = Dict[str, list[int]]  # [unsubscriptable-object]
Alias6 = int | list[int]  # [unsubscriptable-object]
Alias7 = list[list[int]]  # [unsubscriptable-object,unsubscriptable-object]


import collections.abc
import contextlib
import re

class OrderedDict:
    pass

var12: OrderedDict[str, int]  # string annotations aren't checked
var13: list[int]
var14: collections.OrderedDict[str, int]
var15: collections.Counter[int]
var16: collections.abc.Iterable[int]
var17: contextlib.AbstractContextManager[int]
var18: re.Pattern[str]


def func3():
    AliasInvalid2 = list[int]  # [unsubscriptable-object]
    cast_variable2 = [1, 2, 3]
    cast_variable2 = typing.cast(list[int], cast_variable2)  # [unsubscriptable-object]
    var19: list[int]

def func4(arg=list[int]):  # [unsubscriptable-object]
    pass

def func5(arg1: list[int], arg2=set[int]):  # [unsubscriptable-object]
    pass

def func6(arg1: list[int], /, *args: tuple[str], arg2: set[int], **kwargs: dict[str, Any]):
    pass
