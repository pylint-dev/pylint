"""Test PEP 604 - Alternative Union syntax with postponed evaluation of
annotations enabled.

For Python 3.7 - 3.9: Everything should fail.
Testing only 3.8/3.9 to support TypedDict.
"""

# pylint: disable=missing-function-docstring,unused-argument,invalid-name,missing-class-docstring
# pylint: disable=inherit-non-class,too-few-public-methods,line-too-long,unnecessary-direct-lambda-call
# pylint: disable=unnecessary-lambda-assignment

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

import dataclasses
import typing
from dataclasses import dataclass
from typing import NamedTuple, TypedDict


Alias = str | typing.List[int]  # [unsupported-binary-operation]
lst = [typing.Dict[str, int] | None,]  # [unsupported-binary-operation]

var1: typing.Dict[str, int | None]  # [unsupported-binary-operation]
var2: int | str | None  # [unsupported-binary-operation, unsupported-binary-operation]
var3: int | typing.List[str | int]  # [unsupported-binary-operation]
var4: typing.Dict[typing.Tuple[int, int] | int, None]  # [unsupported-binary-operation]

cast_var = 1
cast_var = typing.cast(str | int, cast_var)  # [unsupported-binary-operation]

T = typing.TypeVar("T", int | str, bool)  # [unsupported-binary-operation]

(lambda x: 2)(int | str)  # [unsupported-binary-operation]

var: str | int  # [unsupported-binary-operation]

def func(arg: int | str):  # [unsupported-binary-operation]
    pass

def func2() -> int | str:  # [unsupported-binary-operation]
    pass

class CustomCls(int):
    pass

Alias2 = CustomCls |  str  # [unsupported-binary-operation]

var2 = CustomCls(1) | int(2)


# Check typing.NamedTuple
CustomNamedTuple = typing.NamedTuple(
    "CustomNamedTuple", [("my_var", int | str)])  # [unsupported-binary-operation]

class CustomNamedTuple2(NamedTuple):
    my_var: int | str  # [unsupported-binary-operation]

class CustomNamedTuple3(typing.NamedTuple):
    my_var: int | str  # [unsupported-binary-operation]


# Check typing.TypedDict
CustomTypedDict = TypedDict("CustomTypedDict", my_var=int | str)  # [unsupported-binary-operation]

CustomTypedDict2 = TypedDict("CustomTypedDict2", {"my_var": int | str})  # [unsupported-binary-operation]

class CustomTypedDict3(TypedDict):
    my_var: int | str  # [unsupported-binary-operation]

class CustomTypedDict4(typing.TypedDict):
    my_var: int | str  # [unsupported-binary-operation]


# Check dataclasses
def my_decorator(*args, **kwargs):
    def wraps(*args, **kwargs):
        pass
    return wraps

@dataclass
class CustomDataClass:
    my_var: int | str  # [unsupported-binary-operation]

@dataclasses.dataclass
class CustomDataClass2:
    my_var: int | str  # [unsupported-binary-operation]

@dataclass()
class CustomDataClass3:
    my_var: int | str  # [unsupported-binary-operation]

@my_decorator
@dataclasses.dataclass
class CustomDataClass4:
    my_var: int | str  # [unsupported-binary-operation]

# Not an error if the metaclass implements __or__

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
class_list_reversed_invalid = [WithReverse | DefaultMetaclass] # [unsupported-binary-operation]
class_list_reversed_valid = [DefaultMetaclass | WithReverse]


# Pathological cases
class HorribleMetaclass(type):
    __or__ = lambda x: x

class WithHorrible(metaclass=HorribleMetaclass):
    pass

class_list = [WithHorrible | DefaultMetaclass]

class SecondLevelMetaclass(ForwardMetaclass):
    pass

class WithSecondLevel(metaclass=SecondLevelMetaclass):
    pass

class_list_with_second_level = [WithSecondLevel | DefaultMetaclass]
