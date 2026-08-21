# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/7350

Nested try with exhaustive raise should not trigger used-before-assignment.

Fix landed in pylint 3.0.0.
"""

# pylint: disable=missing-docstring,bare-except
def test():
    try:
        try:
            x = None
        except:
            x = None
            raise
    finally:
        print("x", x)
