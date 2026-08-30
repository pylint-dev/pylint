# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/7381

Chained Flag | Flag | Flag should not trigger unsupported-binary-operation.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring
from enum import Flag


class MosaicFlags(Flag):
    NONE = 0
    SUPPLY_MUTABLE = 1
    TRANSFERABLE = 2
    RESTRICTABLE = 4
    REVOKABLE = 8


value = MosaicFlags.SUPPLY_MUTABLE | MosaicFlags.RESTRICTABLE | MosaicFlags.REVOKABLE
print(value)
