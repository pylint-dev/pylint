# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/8050

pylint should check a file named exactly like its containing directory.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring,unused-import
import unittest  # type: ignore
