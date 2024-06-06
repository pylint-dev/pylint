"""Test pylint.extension.typing - deprecated-typing-alias

'py-version' needs to be set to >= '3.9'.
"""
# pylint: disable=missing-docstring,invalid-name,unused-argument,line-too-long,unsubscriptable-object,unnecessary-direct-lambda-call,wrong-import-position
import collections
import collections.abc
import typing
from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Dict, List, Set, Union, TypedDict, Callable, Tuple, Type

var1: typing.Dict[str, int]  # [deprecated-typing-alias]
var2: List[int]  # [deprecated-typing-alias]
var3: collections.abc.Iterable[int]
var4: typing.OrderedDict[str, int]  # [deprecated-typing-alias]
var5: typing.Awaitable[None]  # [deprecated-typing-alias]
var6: typing.Iterable[int]  # [deprecated-typing-alias]
var7: typing.Hashable  # [deprecated-typing-alias]
var8: typing.ContextManager[str]  # only deprecated with 3.13
var9: typing.Pattern[str]  # [deprecated-typing-alias]
var10: typing.re.Match[str]  # [deprecated-typing-alias]
var11: list[int]
var12: collections.abc
var13: Awaitable[None]
var14: collections.defaultdict[str, str]

Alias1 = Set[int]  # [deprecated-typing-alias]
Alias2 = Dict[int, List[int]]  # [deprecated-typing-alias,deprecated-typing-alias]
Alias3 = Union[int, typing.List[str]]  # [deprecated-typing-alias]
Alias4 = List  # [deprecated-typing-alias]

var21: Type[object]  # [deprecated-typing-alias]
var22: Tuple[str]  # [deprecated-typing-alias]
var23: Callable[..., str]  # [deprecated-typing-alias]
var31: type[object]
var32: tuple[str]
var33: collections.abc.Callable[..., str]


def func1(arg1: List[int], /, *args: List[int], arg2: set[int], **kwargs: Dict[str, int]) -> typing.Tuple[int]:
    # -1:[deprecated-typing-alias,deprecated-typing-alias,deprecated-typing-alias,deprecated-typing-alias]
    pass

def func2(arg1: list[int]) -> tuple[int, int]:
    pass

class CustomIntList(typing.List[int]):  # [deprecated-typing-alias]
    pass

cast_variable = [1, 2, 3]
cast_variable = typing.cast(List[int], cast_variable)  # [deprecated-typing-alias]

(lambda x: 2)(List[int])  # [deprecated-typing-alias]

class CustomNamedTuple(typing.NamedTuple):
    my_var: List[int]  # [deprecated-typing-alias]

CustomTypedDict1 = TypedDict("CustomTypedDict1", my_var=List[int])  # [deprecated-typing-alias]

class CustomTypedDict2(TypedDict):
    my_var: List[int]  # [deprecated-typing-alias]

@dataclass
class CustomDataClass:
    my_var: List[int]  # [deprecated-typing-alias]


import typing_extensions

var40: typing_extensions.AsyncContextManager[int]
var41: typing_extensions.ContextManager[str]
var42: typing_extensions.AsyncGenerator[int]
var43: typing_extensions.Generator[str]
