"""Regression test for https://github.com/pylint-dev/pylint/issues/11169.

PEP 695 type parameters are scoped to their declaration. Reusing a
type-parameter name from an outer scope (e.g. a type alias) is a common
idiom and must not trigger ``redefined-outer-name``.
"""
# pylint: disable=missing-function-docstring,invalid-name,unused-argument

from collections.abc import Callable

type S[T] = list[T]


def f[T](s: S[T]) -> T | None:
    return None


type A[**P] = Callable[P, int]


def g[**P](cb: A[P]) -> None:
    return None


# Genuine shadowing of an outer type-parameter name is still reported.
def h():
    T = 1  # [redefined-outer-name]
    return T
