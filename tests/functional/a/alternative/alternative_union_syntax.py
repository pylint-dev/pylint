"""Test PEP 604 - Alternative Union syntax"""

# pylint: disable=missing-function-docstring,unused-argument,invalid-name,missing-class-docstring
# pylint: disable=inherit-non-class,too-few-public-methods,unnecessary-direct-lambda-call,superfluous-parens

import dataclasses
import typing
from dataclasses import dataclass
from typing import NamedTuple, TypedDict

Alias = str | list[int]
lst = [typing.Dict[str, int] | None,]

var1: typing.Dict[str, int | None]
var2: int | str | None
var3: int | list[str | int]
var4: typing.Dict[typing.Tuple[int, int] | int, None]

cast_var = 1
cast_var = typing.cast(str | int, cast_var)

T = typing.TypeVar("T", int | str, bool)

(lambda x: 2)(int | str)

var: str | int

def func(arg: int | str):
    pass

def func2() -> int | str:
    pass

class CustomCls(int):
    pass

Alias2 = CustomCls |  str

var2 = CustomCls(1) | int(2)


# Check typing.NamedTuple
CustomNamedTuple = typing.NamedTuple(
    "CustomNamedTuple", [("my_var", int | str)])

class CustomNamedTuple2(NamedTuple):
    my_var: int | str

class CustomNamedTuple3(typing.NamedTuple):
    my_var: int | str


# Check typing.TypedDict
CustomTypedDict = TypedDict("CustomTypedDict", my_var=(int | str))

CustomTypedDict2 = TypedDict("CustomTypedDict2", {"my_var": int | str})

class CustomTypedDict3(TypedDict):
    my_var: int | str

class CustomTypedDict4(typing.TypedDict):
    my_var: int | str


# Check dataclasses
def my_decorator(*args, **kwargs):
    def wraps(*args, **kwargs):
        pass
    return wraps

@dataclass
class CustomDataClass:
    my_var: int | str

@dataclasses.dataclass
class CustomDataClass2:
    my_var: int | str

@dataclass()
class CustomDataClass3:
    my_var: int | str

@my_decorator
@dataclasses.dataclass
class CustomDataClass4:
    my_var: int | str

class ForwardMetaclass(type):
    def __or__(cls, other):
        return True

class ReverseMetaclass(type):
    def __ror__(cls, other):
        return True

class WithForward(metaclass=ForwardMetaclass):
    pass

class WithReverse(metaclass=ReverseMetaclass):
    pass

class DefaultMetaclass:
    pass

class_list = [WithForward | DefaultMetaclass]
class_list_reversed = [WithReverse | DefaultMetaclass]
