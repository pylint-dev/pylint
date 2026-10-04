"""Regression test for https://github.com/pylint-dev/pylint/issues/8138.

An ellipsis ``@property`` whose annotation is a class or callable is a stub for
type checkers. Calling it is not ``not-callable``. An implemented body, or an
annotation that is not itself a callable type, still is.
"""
# pylint: disable=invalid-name, missing-class-docstring, missing-function-docstring
# pylint: disable=missing-module-docstring, too-few-public-methods, unused-argument
# pylint: disable=invalid-overridden-method

from collections.abc import Callable as AbcCallable
from typing import TYPE_CHECKING, Any, Callable, Type


class myfunc:
    def __init__(self, *args: Any) -> None:
        pass


class _FunctionGenerator:
    def __getattr__(self, name: str) -> "_FunctionGenerator":
        return _FunctionGenerator()

    def __call__(self, *args: Any) -> None:
        pass

    if TYPE_CHECKING:

        @property
        def myfunc(self) -> Type[myfunc]:
            ...


func = _FunctionGenerator()
func.myfunc(1, 2, 3)


class SomeClass:
    pass


# A plain method of the same name must not hide the property annotation.
class _HasReturnsInt:
    def returns_int(self):
        return 1


class EllipsisProperties(_HasReturnsInt):
    @property
    def typed(self) -> Type[SomeClass]:
        ...

    @property
    def builtin_type(self) -> type[SomeClass]:
        ...

    @property
    def callback(self) -> Callable[[int], None]:
        ...

    @property
    def abc_callback(self) -> AbcCallable[[int], None]:
        ...

    @property
    def returns_int(self) -> int:
        ...

    @property
    def unannotated(self):
        ...

    @property
    def union(self) -> Type[SomeClass] | None:
        ...

    @property
    def implemented(self) -> Type[SomeClass]:
        return 1


props = EllipsisProperties()
props.typed()
props.builtin_type()
props.callback()
props.abc_callback()
props.returns_int()  # [not-callable]
props.unannotated()  # [not-callable]
props.union()  # [not-callable]
props.implemented()  # [not-callable]


# An attribute that is not a function is still not callable.
class _ConstAttr:
    value = None


_ConstAttr().value()  # [not-callable]
