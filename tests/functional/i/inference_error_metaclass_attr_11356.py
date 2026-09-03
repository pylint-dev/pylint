# pylint: disable=missing-class-docstring,too-few-public-methods,undefined-variable
"""Regression test for https://github.com/pylint-dev/pylint/issues/11356."""
from collections.abc import GenericAlias


class C:
    pass


x = C.a

for GenericAlias.a in _:
    pass
