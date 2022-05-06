"""Test pylint.extension.typing - consider-alternative-union-syntax

'py-version' needs to be set to >= '3.10'.
"""
# pylint: disable=missing-docstring,invalid-name,unused-argument,line-too-long
# pylint: disable=deprecated-typing-alias,unnecessary-direct-lambda-call
from dataclasses import dataclass
import typing
from typing import Dict, List, Optional, Union, TypedDict

var1: Union[int, str]  # [consider-alternative-union-syntax]
var2: List[Union[int, None]]  # [consider-alternative-union-syntax]
var3: Dict[str, typing.Union[int, str]]  # [consider-alternative-union-syntax]
var4: Optional[int]  # [consider-alternative-union-syntax]

Alias1 = Union[int, str]  # [consider-alternative-union-syntax]
Alias2 = List[Union[int, None]]  # [consider-alternative-union-syntax]
Alias3 = Dict[str, typing.Union[int, str]]  # [consider-alternative-union-syntax]
Alias4 = Optional[int]  # [consider-alternative-union-syntax]

def func1(
    arg1: Optional[int],  # [consider-alternative-union-syntax]
    **kwargs: Dict[str, Union[int, str]]  # [consider-alternative-union-syntax]
) -> Union[str, None]:  # [consider-alternative-union-syntax]
    pass

class Custom1(List[Union[str, int]]):  # [consider-alternative-union-syntax]
    pass

cast_variable = [1, 2, 3]
cast_variable = typing.cast(Union[List[int], None], cast_variable)  # [consider-alternative-union-syntax]

(lambda x: 2)(Optional[int])  # [consider-alternative-union-syntax]

class CustomNamedTuple(typing.NamedTuple):
    my_var: Union[int, str]  # [consider-alternative-union-syntax]

CustomTypedDict1 = TypedDict("CustomTypedDict1", my_var=Optional[int])  # [consider-alternative-union-syntax]

class CustomTypedDict2(TypedDict):
    my_var: Dict[str, List[Union[str, int]]]  # [consider-alternative-union-syntax]

@dataclass
class CustomDataClass:
    my_var: Optional[int]  # [consider-alternative-union-syntax]
