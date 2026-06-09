# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10298

Iterable[X]|None narrowing should not trigger not-an-iterable.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring
from typing import Iterable


def gen(values: Iterable[int] | None) -> Iterable[int]:
    if values is None:
        return []
    return values


def use():
    for x in gen([1, 2, 3]):
        print(x)
