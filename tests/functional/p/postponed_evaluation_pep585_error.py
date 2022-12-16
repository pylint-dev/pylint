"""Test PEP 585 without postponed evaluation. Everything should fail.

This check requires Python 3.7 or Python 3.8!
Testing with 3.8 only, to support TypedDict.
"""

# pylint: disable=missing-docstring,unused-argument,unused-import,too-few-public-methods
# pylint: disable=invalid-name,inherit-non-class,unsupported-binary-operation
# pylint: disable=unused-variable,line-too-long,unnecessary-direct-lambda-call

# Disabled because of a bug with pypy 3.8 see
# https://github.com/PyCQA/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

import collections
import dataclasses
import typing
from dataclasses import dataclass
from typing import Any, Dict, NamedTuple, TypedDict, Union


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
var3: dict[str, list[int]]  # [unsubscriptable-object,unsubscriptable-object]
var4: Dict[str, list[int]]  # [unsubscriptable-object]
var5: dict[tuple[int, int], str]  # [unsubscriptable-object,unsubscriptable-object]
var6: Dict[tuple[int, int], str]  # [unsubscriptable-object]
var7: list[list[int]]  # [unsubscriptable-object,unsubscriptable-object]
var8: tuple[list[int]]  # [unsubscriptable-object,unsubscriptable-object]
var9: int | list[str | int]   # [unsubscriptable-object]
var10: Union[list[str], None]   # [unsubscriptable-object]
var11: Union[Union[list[int], int]]   # [unsubscriptable-object]

def func(arg: list[int]):  # [unsubscriptable-object]
    pass

def func2() -> list[int]:  # [unsubscriptable-object]
    pass

Alias2 = Union[list[str], None]  # [unsubscriptable-object]
Alias3 = Union[Union[list[int], int]]  # [unsubscriptable-object]
Alias5 = Dict[str, list[int]]  # [unsubscriptable-object]
Alias6 = int | list[int]  # [unsubscriptable-object]
Alias7 = list[list[int]]  # [unsubscriptable-object,unsubscriptable-object]


def func3():
    AliasInvalid2 = list[int]  # [unsubscriptable-object]
    cast_variable2 = [1, 2, 3]
    cast_variable2 = typing.cast(list[int], cast_variable2)  # [unsubscriptable-object]
    var12: list[int]  # [unsubscriptable-object]

def func4(var=list[int]):  # [unsubscriptable-object]
    pass

def func5(arg1: list[int], arg2=set[int]):  # [unsubscriptable-object,unsubscriptable-object]
    pass

def func6(arg1: list[int], /, *args: tuple[str], arg2: set[int], **kwargs: dict[str, Any]):
    # -1:[unsubscriptable-object,unsubscriptable-object,unsubscriptable-object,unsubscriptable-object]
    pass
