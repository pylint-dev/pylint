"""Regression test for https://github.com/pylint-dev/pylint/issues/7978

On the right of ``x is None or``, ``x`` is not None, so a membership test
on it is valid.
"""

# pylint: disable=missing-docstring,too-few-public-methods

from typing import TypedDict


class Point(TypedDict):
    x: int


def check() -> None:
    point: Point | None = None
    while point is None or "x" in point:
        print("checking")
