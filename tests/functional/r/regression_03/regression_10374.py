# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10374

redefined-variable-type should not fire on dummy var assignment.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

import configparser

cfg_ = configparser.ConfigParser()
_ = cfg_.read("/tmp/x.cfg")
