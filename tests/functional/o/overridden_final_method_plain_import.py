"""Regression test for a crash on a ``final`` decorator coming from a plain
``import final`` rather than ``from typing import final``.

https://github.com/pylint-dev/pylint/issues/11521
"""

# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods

import final  # [import-error]


@final
class Base:
    @final
    def method(self):
        pass


class Child(Base):
    def method(self):
        pass
