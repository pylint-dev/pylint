# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/8179

consider-using-augmented-assign should not fire for string %% formatting.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring
s = "text %s"
s = s % 5
print(s)
