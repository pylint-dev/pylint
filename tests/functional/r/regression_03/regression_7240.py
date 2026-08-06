# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/7240

List/set comprehension after sys.platform guard should not trigger no-member.

Fix landed in pylint 2.15.0.
"""

# pylint: disable=missing-docstring,unnecessary-comprehension,invalid-name
import sys

if sys.platform == "linux":
    import os
    print(os.getgroups())
    print([group for group in os.getgroups()])
    print({group for group in os.getgroups()})
