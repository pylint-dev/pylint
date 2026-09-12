# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/9470

``random.choices`` should not trigger no-member.

Clean on every pylint from 2.13 on, the oldest version that runs on Python 3.12.
"""

# pylint: disable=missing-module-docstring,invalid-name
import random
import string

local_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
print(local_part)
