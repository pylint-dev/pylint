"""Tests for used-before-assignment with Python 3.12 generic typing syntax (PEP 695)"""
# pylint: disable = invalid-name,missing-docstring,too-few-public-methods,unused-argument

from typing import TYPE_CHECKING, Callable

type Point[T] = tuple[T, ...]
type Alias[*Ts] = tuple[*Ts]
type Alias2[**P] = Callable[P, None]

type AliasType = int | X | Y

class X:
    pass

if TYPE_CHECKING:
    class Y: ...

class Good[T: Y]: ...
type OtherAlias[T: Y] = T | None

# https://github.com/pylint-dev/pylint/issues/9884
def func[T: Y](x: T) -> None:  # [redefined-outer-name]  FALSE POSITIVE
    ...
