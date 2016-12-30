"""Docstring"""
from __future__ import (
    absolute_import,
    division,
    print_function,
)

from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    NewType,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

# pylint: disable=line-too-long

_T = TypeVar("_T")

MyUnion = Union[bytes, str]
MyTuple = Tuple[bytes]
MyList = List[str]
MyOptionalList = Optional[List[str]]
AnyCallable = Callable[..., None]
MyTypeVar = TypeVar("MyTypeVar")
MyNewType = NewType("MyNewType", str)
Employee = NamedTuple('Employee', [('name', str), ('id', int)])

def func_1(arg1, arg2):
    # type: (Dict[str, str], Tuple[int, ...]) -> Optional[Iterable[int]]
    """Docstring"""
    var = None  # type: Optional[Set[int]]
    assert arg2
    if arg1:
        var = {1, 2, 3}
    return var
