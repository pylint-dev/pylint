"""Test pylint.extension.typing - consider-using-alias

'py-version' needs to be set to '3.7' or '3.8' and 'runtime-typing=no'.
"""
# pylint: disable=missing-docstring,invalid-name,unused-argument,line-too-long,unsubscriptable-object
import collections
import collections.abc
import typing
from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Dict, List, Set, Union, TypedDict, Callable, Tuple, Type

var1: typing.Dict[str, int]  # [consider-using-alias]
var2: List[int]  # [consider-using-alias]
var3: collections.abc.Iterable[int]
var4: typing.OrderedDict[str, int]  # [consider-using-alias]
var5: typing.Awaitable[None]  # [consider-using-alias]
var6: typing.Iterable[int]  # [consider-using-alias]
var7: typing.Hashable  # [consider-using-alias]
var8: typing.ContextManager[str]  # [consider-using-alias]
var9: typing.Pattern[str]  # [consider-using-alias]
var10: typing.re.Match[str]  # [consider-using-alias]
var11: list[int]
var12: collections.abc
var13: Awaitable[None]
var14: collections.defaultdict[str, str]

Alias1 = Set[int]
Alias2 = Dict[int, List[int]]
Alias3 = Union[int, typing.List[str]]
Alias4 = List  # [consider-using-alias]

var21: Type[object]  # [consider-using-alias]
var22: Tuple[str]  # [consider-using-alias]
var23: Callable[..., str]  # [consider-using-alias]
var31: type[object]
var32: tuple[str]
var33: collections.abc.Callable[..., str]


def func1(arg1: List[int], /, *args: List[int], arg2: set[int], **kwargs: Dict[str, int]) -> typing.Tuple[int]:
    # -1:[consider-using-alias,consider-using-alias,consider-using-alias,consider-using-alias]
    pass

def func2(arg1: list[int]) -> tuple[int, int]:
    pass

class CustomIntList(typing.List[int]):
    pass

cast_variable = [1, 2, 3]
cast_variable = typing.cast(List[int], cast_variable)

(lambda x: 2)(List[int])

class CustomNamedTuple(typing.NamedTuple):
    my_var: List[int]  # [consider-using-alias]

CustomTypedDict1 = TypedDict("CustomTypedDict1", my_var=List[int])

class CustomTypedDict2(TypedDict):
    my_var: List[int]  # [consider-using-alias]

@dataclass
class CustomDataClass:
    my_var: List[int]  # [consider-using-alias]
