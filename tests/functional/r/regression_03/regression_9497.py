# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/9497

datetime.datetime non-existent member should be detected by no-member.

Fix landed in pylint 3.0.0.
"""

import datetime

print(datetime.datetime.not_a_member)  # [no-member]
