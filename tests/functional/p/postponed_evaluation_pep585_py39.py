"""Test PEP 585 works as expected, starting with Python 3.9"""
# pylint: disable=missing-docstring,unused-argument,unused-import,too-few-public-methods,invalid-name,inherit-non-class,unsupported-binary-operation
import collections
import dataclasses
import typing
from dataclasses import dataclass
from typing import Dict, NamedTuple, TypedDict, Union, Tuple


AliasValid = list[int]

class CustomIntList(typing.List[int]):
    pass

class CustomIntListError(list[int]):
    pass

cast_variable = [1, 2, 3]
cast_variable = typing.cast(list[int], cast_variable)

T = typing.TypeVar("T", list[int], str)

(lambda x: 2)(list[int])


# Check typing.NamedTuple
CustomNamedTuple = typing.NamedTuple(
    "CustomNamedTuple", [("my_var", list[int])])

class CustomNamedTuple2(NamedTuple):
    my_var: list[int]

class CustomNamedTuple3(typing.NamedTuple):
    my_var: list[int]


# Check typing.TypedDict
CustomTypedDict = TypedDict("CustomTypedDict", my_var=list[int])

CustomTypedDict2 = TypedDict("CustomTypedDict2", {"my_var": list[int]})

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

Alias2 = Union[list[str], None]
Alias3 = Union[Union[list[int], int]]
Alias4 = Tuple[list[int]]
Alias5 = Dict[str, list[int]]
Alias6 = int | list[int]
Alias7 = list[list[int]]
