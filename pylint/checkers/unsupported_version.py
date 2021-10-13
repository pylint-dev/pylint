# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Checker for features used that are not supported by all python versions
indicated by the py-version setting.
"""

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter
from pylint.utils import get_global_option


class UnsupportedVersionChecker(BaseChecker):
    """Checker for features that are not supported by all python versions
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

    def open(self) -> None:
        """Initialize visit variables and statistics."""
        py_version = get_global_option(self, "py-version")
        self._py36_plus = py_version >= (3, 6)

    @check_messages("using-f-string-in-unsupported-version")
    def visit_joinedstr(self, node: nodes.JoinedStr) -> None:
        """Check f-strings"""
        if not self._py36_plus:
            self.add_message("using-f-string-in-unsupported-version", node=node)


def register(linter: PyLinter) -> None:
    """Required method to auto register this checker"""
    linter.register_checker(UnsupportedVersionChecker(linter))
