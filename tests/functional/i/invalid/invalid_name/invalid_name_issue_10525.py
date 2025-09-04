"""Regression test for https://github.com/pylint-dev/pylint/issues/10525."""

# pylint: disable=too-few-public-methods

from typing import ClassVar

import attrs


class X:
    """Class without attrs decorator"""

    A: ClassVar[int] = 1

    def __init__(self) -> None:
        self.b: int = 2


@attrs.define
class Y:
    """Class with attrs decorator"""

    A: ClassVar[int] = 1  # should not trigger `invalid-name`
    b: int = 2
