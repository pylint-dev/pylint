"""Test pylint.extension.typing - consider-alternative-union-syntax

'py-version' needs to be set to >= '3.7' and 'runtime-typing=no'.
"""
# pylint: disable=missing-docstring,invalid-name,unused-argument,line-too-long
# pylint: disable=consider-using-alias
from dataclasses import dataclass
import typing
from typing import Dict, List, Optional, Union, TypedDict

var1: Union[int, str]  # [consider-alternative-union-syntax]
var2: List[Union[int, None]]  # [consider-alternative-union-syntax]
var3: Dict[str, typing.Union[int, str]]  # [consider-alternative-union-syntax]
var4: Optional[int]  # [consider-alternative-union-syntax]

Alias1 = Union[int, str]
Alias2 = List[Union[int, None]]
Alias3 = Dict[str, typing.Union[int, str]]
Alias4 = Optional[int]

def func1(
    arg1: Optional[int],  # [consider-alternative-union-syntax]
    **kwargs: Dict[str, Union[int, str]]  # [consider-alternative-union-syntax]
) -> Union[str, None]:  # [consider-alternative-union-syntax]
    pass

class Custom1(List[Union[str, int]]):
    pass

cast_variable = [1, 2, 3]
cast_variable = typing.cast(Union[List[int], None], cast_variable)

(lambda x: 2)(Optional[int])

class CustomNamedTuple(typing.NamedTuple):
    my_var: Union[int, str]  # [consider-alternative-union-syntax]

CustomTypedDict1 = TypedDict("CustomTypedDict1", my_var=Optional[int])

class CustomTypedDict2(TypedDict):
    my_var: Dict[str, List[Union[str, int]]]  # [consider-alternative-union-syntax]

@dataclass
class CustomDataClass:
    my_var: Optional[int]  # [consider-alternative-union-syntax]
