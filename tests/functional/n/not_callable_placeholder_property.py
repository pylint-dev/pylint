"""A property whose body is only ``...`` is a placeholder, like ``pass``.

Its return value is unknown, so calling or iterating it is not reported.
This is how sqlalchemy declares its ``func`` helpers for type checkers.
Regression test for https://github.com/pylint-dev/pylint/issues/8138.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods
# pylint: disable=invalid-name,unnecessary-ellipsis,useless-return

from typing import TYPE_CHECKING, Any, Callable, Iterator, Type


class Function:
    def __init__(self, *args: Any) -> None:
        self.args = args


class FunctionGenerator:
    def __getattr__(self, name: str) -> "FunctionGenerator":
        return FunctionGenerator()

    def __call__(self, *args: Any) -> Function:
        return Function(*args)

    if TYPE_CHECKING:

        @property
        def count(self) -> Type[Function]: ...

        @property
        def now(self) -> "Type[Function]": ...


func = FunctionGenerator()
func.count(1)
func.now()


class Stubs:
    @property
    def builtin_type(self) -> type[Function]: ...

    @property
    def callback(self) -> Callable[[int], None]: ...

    @property
    def with_docstring(self) -> Type[Function]:
        """Only a docstring and ``...``."""
        ...

    @property
    def values(self) -> Iterator[int]: ...


stubs = Stubs()
stubs.builtin_type()
stubs.callback(1)
stubs.with_docstring()
for value in stubs.values:
    print(value)


class Parent:
    @property
    def method(self) -> Type[Function]: ...


class ChildReturnsNone(Parent):
    @property
    def method(self) -> Type[Function]:
        return None


class ChildAttribute(Parent):
    method = None


ChildReturnsNone().method()  # [not-callable]
ChildAttribute().method()  # [not-callable]


class NotOnlyEllipsis:
    @property
    def method(self) -> Type[Function]:
        ...
        return None


NotOnlyEllipsis().method()  # [not-callable]
