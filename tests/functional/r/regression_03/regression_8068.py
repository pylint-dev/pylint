# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/8068

del self._m[:] after conditional None init should not trigger unsupported-delete-operation.

Fix landed in pylint 4.0.0.
"""

# pylint: disable=missing-docstring,too-few-public-methods
class A:
    def __init__(self, b=False):
        self._m = [] if b else None

    def reset(self):
        if self._m:
            del self._m[:]
