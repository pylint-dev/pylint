# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/9722

Multi-level property subclass should not trigger comparison-with-callable.

Fix landed in pylint 3.3.0.
"""

# pylint: disable=missing-docstring,too-few-public-methods,invalid-name
class my_prop(property):
    pass


class my_prop2(my_prop):
    pass


class Test:
    def __init__(self) -> None:
        self._prop = None
        self._prop2 = None

    @my_prop
    def prop(self) -> str:
        return self._prop

    @my_prop2
    def prop2(self) -> str:
        return self._prop2


c = Test()

if c.prop == "test":
    pass

if c.prop2 == "test":
    pass
