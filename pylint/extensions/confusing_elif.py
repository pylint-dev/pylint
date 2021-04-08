# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import astroid

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker


class ConfusingConsecutiveElifChecker(BaseChecker):
    """Checks if "elif" is used right after an indented block that finishes with "if" or "elif" itself."""

    __implements__ = IAstroidChecker

    name = "confusing-elif-checker"
    priority = -1
    msgs = {
        "R5601": (
            "Consecutive elif with differing indentation level, consider creating a function to separate the inner elif",
            "confusing-consecutive-elif",
            "Used when an elif statement follows right after an indented block which itself ends with if or elif. "
            "It may not be ovious if the elif statement was willingly or mistakenly unindented. "
            "Extracting the indented if statement into a separate function might avoid confusion and prevent errors.",
        )
    }

    @check_messages("confusing-consecutive-elif")
    def visit_if(self, node):
        if node.has_elif_block() and self.__ends_with_if(node.body):
            self.add_message("confusing-consecutive-elif", node=node.orelse[0])

    def __ends_with_if(self, body):
        last_node = body[-1]
        return isinstance(last_node, astroid.If) and self.__has_no_else_clause(
            last_node
        )

    @staticmethod
    def __has_no_else_clause(node):
        orelse = node.orelse
        while orelse and isinstance(orelse[0], astroid.If):
            orelse = orelse[0].orelse
        if not orelse or isinstance(orelse[0], astroid.If):
            return True
        return False


def register(linter):
    """This required method auto registers the checker.

    :param linter: The linter to register the checker to.
    :type linter: pylint.lint.PyLinter
    """
    linter.register_checker(ConfusingConsecutiveElifChecker(linter))
