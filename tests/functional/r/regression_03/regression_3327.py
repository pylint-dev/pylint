# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/3327

Module named 'builtins' (from-imported) should not trigger no-member 'dict has no...'.

Fix landed in pylint 2.15.0.
"""

# pylint: disable=missing-docstring,pointless-statement
from collections import abc as builtins_mod
print(builtins_mod.Mapping)
