# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/4608

'-x if x is not None else None' should not trigger invalid-unary-operand-type.

Fix landed in pylint 4.0.0.
"""

# pylint: disable=missing-docstring,invalid-name
import random

if random.choice([0, 1]):
    x = None
else:
    x = 15

y = (-x if x is not None else None)
