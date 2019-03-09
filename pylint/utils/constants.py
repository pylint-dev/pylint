# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import re

# Allow stopping after the first semicolon/hash encountered,
# so that an option can be continued with the reasons
# why it is active or disabled.
OPTION_RGX = re.compile(r"\s*#.*\bpylint:\s*([^;#]+)[;#]{0,1}")

PY_EXTS = (".py", ".pyc", ".pyo", ".pyw", ".so", ".dll")
