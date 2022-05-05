# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import os
import pathlib
import platform
import sys
from datetime import datetime
from typing import NamedTuple

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
# on all project using [MASTER] in their rcfile.
MAIN_CHECKER_NAME = "master"

USER_HOME = os.path.expanduser("~")
# TODO: 3.0: Remove in 3.0 with all the surrounding code
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
    "typevar": "type variable",
}


class DeletedMessage(NamedTuple):
    msgid: str
    symbol: str
    old_names: list[tuple[str, str]] = []


DELETED_MSGID_PREFIXES: list[int] = []

DELETED_MESSAGES = [
    # Everything until the next comment is from the
    # PY3K+ checker, see https://github.com/PyCQA/pylint/pull/4942
    DeletedMessage("W1601", "apply-builtin"),
    DeletedMessage("E1601", "print-statement"),
    DeletedMessage("E1602", "parameter-unpacking"),
    DeletedMessage(
        "E1603", "unpacking-in-except", [("W0712", "old-unpacking-in-except")]
    ),
    DeletedMessage("E1604", "old-raise-syntax", [("W0121", "old-old-raise-syntax")]),
    DeletedMessage("E1605", "backtick", [("W0333", "old-backtick")]),
    DeletedMessage("E1609", "import-star-module-level"),
    DeletedMessage("W1601", "apply-builtin"),
    DeletedMessage("W1602", "basestring-builtin"),
    DeletedMessage("W1603", "buffer-builtin"),
    DeletedMessage("W1604", "cmp-builtin"),
    DeletedMessage("W1605", "coerce-builtin"),
    DeletedMessage("W1606", "execfile-builtin"),
    DeletedMessage("W1607", "file-builtin"),
    DeletedMessage("W1608", "long-builtin"),
    DeletedMessage("W1609", "raw_input-builtin"),
    DeletedMessage("W1610", "reduce-builtin"),
    DeletedMessage("W1611", "standarderror-builtin"),
    DeletedMessage("W1612", "unicode-builtin"),
    DeletedMessage("W1613", "xrange-builtin"),
    DeletedMessage("W1614", "coerce-method"),
    DeletedMessage("W1615", "delslice-method"),
    DeletedMessage("W1616", "getslice-method"),
    DeletedMessage("W1617", "setslice-method"),
    DeletedMessage("W1618", "no-absolute-import"),
    DeletedMessage("W1619", "old-division"),
    DeletedMessage("W1620", "dict-iter-method"),
    DeletedMessage("W1621", "dict-view-method"),
    DeletedMessage("W1622", "next-method-called"),
    DeletedMessage("W1623", "metaclass-assignment"),
    DeletedMessage(
        "W1624", "indexing-exception", [("W0713", "old-indexing-exception")]
    ),
    DeletedMessage("W1625", "raising-string", [("W0701", "old-raising-string")]),
    DeletedMessage("W1626", "reload-builtin"),
    DeletedMessage("W1627", "oct-method"),
    DeletedMessage("W1628", "hex-method"),
    DeletedMessage("W1629", "nonzero-method"),
    DeletedMessage("W1630", "cmp-method"),
    DeletedMessage("W1632", "input-builtin"),
    DeletedMessage("W1633", "round-builtin"),
    DeletedMessage("W1634", "intern-builtin"),
    DeletedMessage("W1635", "unichr-builtin"),
    DeletedMessage(
        "W1636", "map-builtin-not-iterating", [("W1631", "implicit-map-evaluation")]
    ),
    DeletedMessage("W1637", "zip-builtin-not-iterating"),
    DeletedMessage("W1638", "range-builtin-not-iterating"),
    DeletedMessage("W1639", "filter-builtin-not-iterating"),
    DeletedMessage("W1640", "using-cmp-argument"),
    DeletedMessage("W1642", "div-method"),
    DeletedMessage("W1643", "idiv-method"),
    DeletedMessage("W1644", "rdiv-method"),
    DeletedMessage("W1645", "exception-message-attribute"),
    DeletedMessage("W1646", "invalid-str-codec"),
    DeletedMessage("W1647", "sys-max-int"),
    DeletedMessage("W1648", "bad-python3-import"),
    DeletedMessage("W1649", "deprecated-string-function"),
    DeletedMessage("W1650", "deprecated-str-translate-call"),
    DeletedMessage("W1651", "deprecated-itertools-function"),
    DeletedMessage("W1652", "deprecated-types-field"),
    DeletedMessage("W1653", "next-method-defined"),
    DeletedMessage("W1654", "dict-items-not-iterating"),
    DeletedMessage("W1655", "dict-keys-not-iterating"),
    DeletedMessage("W1656", "dict-values-not-iterating"),
    DeletedMessage("W1657", "deprecated-operator-function"),
    DeletedMessage("W1658", "deprecated-urllib-function"),
    DeletedMessage("W1659", "xreadlines-attribute"),
    DeletedMessage("W1660", "deprecated-sys-function"),
    DeletedMessage("W1661", "exception-escape"),
    DeletedMessage("W1662", "comprehension-escape"),
    # https://github.com/PyCQA/pylint/pull/3578
    DeletedMessage("W0312", "mixed-indentation"),
    # https://github.com/PyCQA/pylint/pull/3577
    DeletedMessage(
        "C0326",
        "bad-whitespace",
        [
            ("C0323", "no-space-after-operator"),
            ("C0324", "no-space-after-comma"),
            ("C0322", "no-space-before-operator"),
        ],
    ),
    # https://github.com/PyCQA/pylint/pull/3571
    DeletedMessage("C0330", "bad-continuation"),
    # No PR
    DeletedMessage("R0921", "abstract-class-not-used"),
    # https://github.com/PyCQA/pylint/pull/3577
    DeletedMessage("C0326", "bad-whitespace"),
    # Pylint 1.4.3
    DeletedMessage("W0142", "star-args"),
    # https://github.com/PyCQA/pylint/issues/2409
    DeletedMessage("W0232", "no-init"),
    # https://github.com/PyCQA/pylint/pull/6421
    DeletedMessage("W0111", "assign-to-new-keyword"),
]


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
