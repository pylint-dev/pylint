# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import os
import pathlib
import platform
import sys
from datetime import datetime

import astroid
import platformdirs

from pylint.__pkginfo__ import __version__
from pylint.typing import MessageTypesFullName

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

MSG_TYPES: dict[str, MessageTypesFullName] = {
    "I": "info",
    "C": "convention",
    "R": "refactor",
    "W": "warning",
    "E": "error",
    "F": "fatal",
}
MSG_TYPES_LONG: dict[str, str] = {v: k for k, v in MSG_TYPES.items()}

MSG_TYPES_STATUS = {"I": 0, "C": 16, "R": 8, "W": 4, "E": 2, "F": 1}

# You probably don't want to change the MAIN_CHECKER_NAME
# This would affect rcfile generation and retro-compatibility
# on all project using [MAIN] in their rcfile.
MAIN_CHECKER_NAME = "main"

USER_HOME = os.path.expanduser("~")
# TODO: 3.0: Remove in 3.0 with all the surrounding code
OLD_DEFAULT_PYLINT_HOME = ".pylint.d"
DEFAULT_PYLINT_HOME = platformdirs.user_cache_dir("pylint")

DEFAULT_IGNORE_LIST = ("CVS",)


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
    "typevar": "type variable",
}

# ignore some messages when emitting useless-suppression:
# - cyclic-import: can show false positives due to incomplete context
# - deprecated-{module, argument, class, method, decorator}:
#   can cause false positives for multi-interpreter projects
#   when linting with an interpreter on a lower python version
INCOMPATIBLE_WITH_USELESS_SUPPRESSION = frozenset(
    [
        "R0401",  # cyclic-import
        "W0402",  # deprecated-module
        "W1505",  # deprecated-method
        "W1511",  # deprecated-argument
        "W1512",  # deprecated-class
        "W1513",  # deprecated-decorator
        "R0801",  # duplicate-code
    ]
)


TYPING_TYPE_CHECKS_GUARDS = frozenset({"typing.TYPE_CHECKING", "TYPE_CHECKING"})


def _warn_about_old_home(pylint_home: pathlib.Path) -> None:
    """Warn users about the old pylint home being deprecated.

    The spam prevention mechanism is due to pylint being used in parallel by
    pre-commit, and the message being spammy in this context
    Also if you work with an old version of pylint that recreates the
    old pylint home, you can get the old message for a long time.
    """
    prefix_spam_prevention = "pylint_warned_about_old_cache_already"
    spam_prevention_file = pathlib.Path(pylint_home) / datetime.now().strftime(
        prefix_spam_prevention + "_%Y-%m-%d.temp"
    )
    old_home = pathlib.Path(USER_HOME) / OLD_DEFAULT_PYLINT_HOME

    if old_home.exists() and not spam_prevention_file.exists():
        print(
            f"PYLINTHOME is now '{pylint_home}' but obsolescent '{old_home}' is found; "
            "you can safely remove the latter",
            file=sys.stderr,
        )

        # Remove old spam prevention file
        if pylint_home.exists():
            for filename in pylint_home.iterdir():
                if prefix_spam_prevention in str(filename):
                    try:
                        os.remove(pylint_home / filename)
                    except OSError:  # pragma: no cover
                        pass

        # Create spam prevention file for today
        try:
            pylint_home.mkdir(parents=True, exist_ok=True)
            with open(spam_prevention_file, "w", encoding="utf8") as f:
                f.write("")
        except Exception as exc:  # pragma: no cover  # pylint: disable=broad-except
            print(
                "Can't write the file that was supposed to "
                f"prevent 'pylint.d' deprecation spam in {pylint_home} because of {exc}."
            )


def _get_pylint_home() -> str:
    """Return the pylint home."""
    if "PYLINTHOME" in os.environ:
        return os.environ["PYLINTHOME"]

    _warn_about_old_home(pathlib.Path(DEFAULT_PYLINT_HOME))

    return DEFAULT_PYLINT_HOME


PYLINT_HOME = _get_pylint_home()

TYPING_NORETURN = frozenset(
    (
        "typing.NoReturn",
        "typing_extensions.NoReturn",
    )
)
TYPING_NEVER = frozenset(
    (
        "typing.Never",
        "typing_extensions.Never",
    )
)
