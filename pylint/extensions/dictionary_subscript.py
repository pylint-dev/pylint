# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check for dictionary read-access via subscript."""

from astroid import Assign, Dict, nodes

from pylint.checkers import BaseChecker, utils
from pylint.lint import PyLinter


class NoDictSubscriptChecker(BaseChecker):
    name = "no-dict-subscript"
    msgs = {
        "R5701": (
            "Using dict operator [], consider using get() instead",
            "dict-subscript",
            "Used to warn when subscripting a dictionary instead of using the get() function",
        ),
    }

    def visit_subscript(self, node: nodes.Subscript) -> None:
        if isinstance(utils.safe_infer(node.value), Dict) and not isinstance(
            node.parent, Assign
        ):
            self.add_message("dict-subscript", node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(NoDictSubscriptChecker(linter))
