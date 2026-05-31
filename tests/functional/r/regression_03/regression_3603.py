# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/3603

Class differently defined in if/else branches should not trigger unexpected-keyword-arg.

Fix landed in pylint 3.3.0.
"""

# pylint: disable=missing-docstring,too-few-public-methods
if str is bytes:
    class C:
        def __init__(self, a):
            pass
else:
    class C:
        def __init__(self, a, b):
            pass


C(1, b=2)
