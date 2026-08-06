# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/4554

'os.path.join(*a)' where 'a' is a populated list should not trigger no-value-for-parameter.

Fix landed in pylint 3.0.0.
"""

# pylint: disable=missing-docstring
import os.path


def bad():
    a = []
    a.extend(["a", "b"])
    return os.path.join(*a)
