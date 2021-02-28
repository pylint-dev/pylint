#!/usr/bin/env python

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os
import sys

import pylint

# Strip out the current working directory from sys.path.
# Having the working directory in `sys.path` means that `pylint` might
# inadvertently import user code from modules having the same name as
# stdlib or pylint's own modules.
# CPython issue: https://bugs.python.org/issue33053
sys.path = [p for p in sys.path if p not in ("", os.getcwd())]

pylint.run_pylint()
