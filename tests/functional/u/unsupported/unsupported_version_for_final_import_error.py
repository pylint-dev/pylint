"""Test for no crash when a ``@final`` decorator is imported via ``import final``.

https://github.com/pylint-dev/pylint/issues/11521
"""

# pylint: disable=import-error,missing-class-docstring,too-few-public-methods,missing-function-docstring

import final


@final
class MyClass1:
    @final
    def my_method(self):
        pass
