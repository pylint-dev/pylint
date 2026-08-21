# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/1934

Single-iteration for-loop lambda capture should not trigger cell-var-from-loop.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring
def f():
    for i in [1]:
        return lambda: i
