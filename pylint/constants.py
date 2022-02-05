# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
import platform
import sys
from typing import Dict

import astroid
import platformdirs

from pylint.__pkginfo__ import __version__
from pylint.typing import MessageTypesFullName

PY37_PLUS = sys.version_info[:2] >= (3, 7)
PY38_PLUS = sys.version_info[:2] >= (3, 8)
PY39_PLUS = sys.version_info[:2] >= (3, 9)

IS_PYPY = platform.python_implementation() == "PyPy"

PY_EXTS = (".py", ".pyc", ".pyo", ".pyw", ".so", ".dll")

MSG_STATE_CONFIDENCE = 2
_MSG_ORDER = "EWRCIF"
MSG_STATE_SCOPE_CONFIG = 0
MSG_STATE_SCOPE_MODULE = 1

# The line/node distinction does not apply to fatal errors and reports.
_SCOPE_EXEMPT = "FR"

MSG_TYPES: Dict[str, MessageTypesFullName] = {
    "I": "info",
    "C": "convention",
    "R": "refactor",
    "W": "warning",
    "E": "error",
    "F": "fatal",
}
MSG_TYPES_LONG: Dict[str, str] = {v: k for k, v in MSG_TYPES.items()}

MSG_TYPES_STATUS = {"I": 0, "C": 16, "R": 8, "W": 4, "E": 2, "F": 1}

# You probably don't want to change the MAIN_CHECKER_NAME
# This would affect rcfile generation and retro-compatibility
# on all project using [MASTER] in their rcfile.
MAIN_CHECKER_NAME = "master"

# pylint: disable-next=fixme
# TODO Remove in 3.0 with all the surrounding code
OLD_DEFAULT_PYLINT_HOME = ".pylint.d"
DEFAULT_PYLINT_HOME = platformdirs.user_cache_dir("pylint")


class WarningScope:
    LINE = "line-based-msg"
    NODE = "node-based-msg"


full_version = f"""pylint {__version__}
astroid {astroid.__version__}
Python {sys.version}"""

HUMAN_READABLE_TYPES = {
    "file": "file",
    "module": "module",
    "const": "constant",
    "class": "class",
    "function": "function",
    "method": "method",
    "attr": "attribute",
    "argument": "argument",
    "variable": "variable",
    "class_attribute": "class attribute",
    "class_const": "class constant",
    "inlinevar": "inline iteration",
}
