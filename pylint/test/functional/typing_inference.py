"""Docstring"""
from __future__ import (
    absolute_import,
    division,
    print_function,
)

from typing import (
    Callable,
    List,
    NamedTuple,
    NewType,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

# With the plugin enabled none of these should complain anymore.

# Subscripts
MyUnion = Union[bytes, str]
MyTuple = Tuple[bytes]
MyList = List[str]
MyOptionalList = Optional[List[str]]
AnyCallable = Callable[..., None]

# Call
MyTypeVar = TypeVar("MyTypeVar")
MyNewType = NewType("MyNewType", str)
Employee = NamedTuple('Employee', [('name', str), ('id', int)])
