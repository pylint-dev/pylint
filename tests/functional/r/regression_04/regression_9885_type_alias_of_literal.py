"""Regression test for https://github.com/pylint-dev/pylint/issues/9885

The name of a ``type`` statement is a ``TypeAliasType``, which has a
``__value__``, even when the alias is a ``Literal``.
"""

from typing import Literal

type Mode = Literal["a"]

print(Mode.__value__)
