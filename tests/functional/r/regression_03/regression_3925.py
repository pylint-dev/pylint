# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/3925

Destructuring 'a, b = f or (None, None)' should not trigger not-callable.

Fix landed in pylint 4.0.0.
"""

# pylint: disable=missing-docstring
class X:
    def __init__(self, f=None):
        self.f1, self.f2 = f or (None, None)

    def g(self, x):
        if self.f1:
            return self.f1(x)
        return x

    def h(self, y):
        return self.f2(y) if self.f2 else y
