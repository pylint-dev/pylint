# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Checker for functions used that are not supported by all python versions
indicated by the py-version setting.
"""

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker
from pylint.utils import get_global_option


class UnsupportedVersionChecker(BaseChecker):
    """Checker for functions that are not supported by all python versions
    indicated by the py-version setting.
    """

    __implements__ = (IAstroidChecker,)
    name = "unsupported_version"
    msgs = {
        "W1601": (
            "F-strings are not supported by all versions included in the py-version setting",
            "using-f-string-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.6 and pylint encounters "
            "a f-string.",
        ),
    }

    def open(self):
        """initialize visit variables and statistics"""
        py_version = get_global_option(self, "py-version")
        self._py35_plus = py_version >= (3, 5)
        self._py36_plus = py_version >= (3, 6)
        self._py37_plus = py_version >= (3, 7)
        self._py37_plus = py_version >= (3, 8)
        self._py39_plus = py_version >= (3, 9)
        self._py310_plus = py_version >= (3, 10)

    @check_messages("using-f-string-in-unsupported-version")
    def visit_joinedstr(self, node: nodes.JoinedStr) -> None:
        """Check f-strings"""
        self._check_unsupported_version(node)

    def _check_unsupported_version(self, node: nodes.JoinedStr) -> None:
        """Check if f-strings are used while < 3.6 is supported"""
        if not self._py36_plus:
            self.add_message("using-f-string-in-unsupported-version", node=node)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(UnsupportedVersionChecker(linter))
