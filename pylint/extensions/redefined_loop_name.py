# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Optional checker to warn when loop variables are overwritten in the loop's body."""

from astroid import nodes

from pylint import checkers, interfaces
from pylint.checkers import utils
from pylint.checkers.variables import in_for_else_branch
from pylint.interfaces import HIGH
from pylint.lint import PyLinter
from pylint.utils import utils as pylint_utils


class RedefinedLoopName(checkers.BaseChecker):

    name = "redefined-loop-name"

    msgs = {
        "W2901": (
            "Redefining %r from loop (line %s)",
            "redefined-loop-name",
            "Used when a loop variable is overwritten in the loop body.",
        ),
    }

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self._loop_variables = []

    @utils.check_messages("redefined-loop-name")
    def visit_assignname(self, node: nodes.AssignName) -> None:
        assign_type = node.assign_type()
        if not isinstance(assign_type, (nodes.Assign, nodes.AugAssign)):
            return
        node_scope = node.scope()
        for outer_for, outer_variables in self._loop_variables:
            if node_scope is not outer_for.scope():
                continue
            if node.name in outer_variables and not in_for_else_branch(outer_for, node):
                self.add_message(
                    "redefined-loop-name",
                    args=(node.name, outer_for.fromlineno),
                    node=node,
                    confidence=HIGH,
                )
                break

    @utils.check_messages("redefined-loop-name")
    def visit_for(self, node: nodes.For) -> None:
        assigned_to = [a.name for a in node.target.nodes_of_class(nodes.AssignName)]
        # Only check variables that are used
        dummy_rgx = pylint_utils.get_global_option(
            self, "dummy-variables-rgx", default=None
        )
        assigned_to = [var for var in assigned_to if not dummy_rgx.match(var)]

        node_scope = node.scope()
        for variable in assigned_to:
            for outer_for, outer_variables in self._loop_variables:
                if node_scope is not outer_for.scope():
                    continue
                if variable in outer_variables and not in_for_else_branch(
                    outer_for, node
                ):
                    self.add_message(
                        "redefined-loop-name",
                        args=(variable, outer_for.fromlineno),
                        node=node,
                        confidence=HIGH,
                    )
                    break

        self._loop_variables.append((node, assigned_to))

    @utils.check_messages("redefined-loop-name")
    def leave_for(self, node: nodes.For) -> None:  # pylint: disable=unused-argument
        self._loop_variables.pop()


def register(linter: PyLinter) -> None:
    linter.register_checker(RedefinedLoopName(linter))
