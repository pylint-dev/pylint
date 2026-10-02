"""Test for no crash when a ``@final`` decorator is imported via ``import final``.

https://github.com/pylint-dev/pylint/issues/11521
"""

# pylint: disable=import-error,missing-class-docstring,missing-function-docstring,too-few-public-methods

import final


class Base:
    @final
    def my_method(self):
        pass


class Subclass(Base):
    def my_method(self):
        pass
