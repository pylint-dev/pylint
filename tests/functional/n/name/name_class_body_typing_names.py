"""Test that typing constructs in a class body use their dedicated naming styles.

A ``TypeAlias``, ``TypeVar``, ``ParamSpec`` or ``TypeVarTuple`` defined in a class
scope is not a class attribute, so ``class-attribute-naming-style`` must not apply.
"""
# pylint: disable=missing-class-docstring,too-few-public-methods
from collections.abc import Callable
from typing import ParamSpec, TypeAlias, TypeVar, TypeVarTuple


class Valid:
    MyReturnType: TypeAlias = int
    MyCallVar = TypeVar("MyCallVar", bound=Callable[..., MyReturnType])
    MyParams = ParamSpec("MyParams")
    MyShape = TypeVarTuple("MyShape")
    class_attribute = 1


class Invalid:
    bad_alias: TypeAlias = int  # [invalid-name]
    bad_typevar = TypeVar("bad_typevar")  # [invalid-name]
    BadClassAttribute = 1  # [invalid-name]
    bad_params = ParamSpec("bad_params")  # [invalid-name]
    bad_shape = TypeVarTuple("bad_shape")  # [invalid-name]
    # Unpacking a TypeVar call is not a TypeVar definition.
    first, second = TypeVar("first")  # pylint: disable=unpacking-non-sequence
    annotated: int = 1
