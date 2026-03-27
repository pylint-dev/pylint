# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Looks for unassigned function/method calls that have non-nullable return type."""

from __future__ import annotations

from typing import TYPE_CHECKING

import astroid
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.typecheck import TypeChecker
from pylint.checkers.utils import only_required_for_messages, safe_infer

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class FunctionReturnNotAssignedChecker(BaseChecker):
    name = "function_return_not_assigned"
    msgs = {
        "W5486": (
            "Function returned value which is never used",
            "function-return-not-assigned",
            "Function returns non-nullable value which is never used. "
            "Use explicit `_ = func_call()` if you are not interested in returned value",
        )
    }

    @only_required_for_messages("function-return-not-assigned")
    def visit_call(self, node: nodes.Call) -> None:
        result_is_used = not isinstance(node.parent, nodes.Expr)

        if result_is_used:
            return

        function_node = safe_infer(node.func)
        funcs = (nodes.FunctionDef, astroid.UnboundMethod, astroid.BoundMethod)

        # FIXME: more elegant solution probably exists
        # methods called on instances returned by functions in some libraries
        # are having function_node None and needs to be handled here
        # for example:
        #   attrs.evolve returned instances
        #   instances returned by any pyrsistent method (pmap.set, pvector.append, ...)
        if function_node is None:
            try:
                for n in node.func.infer():
                    if not isinstance(n, astroid.BoundMethod):
                        continue
                    function_node = n
                    break
            except Exception:  # pylint:disable=broad-exception-caught
                pass

        if not isinstance(function_node, funcs):
            return

        # Unwrap to get the actual function node object
        if isinstance(function_node, astroid.BoundMethod) and isinstance(
            function_node._proxied, astroid.UnboundMethod
        ):
            function_node = function_node._proxied._proxied

        # Make sure that it's a valid function that we can analyze.
        # Ordered from less expensive to more expensive checks.
        if (
            not function_node.is_function
            or function_node.decorators
            or TypeChecker._is_ignored_function(function_node)
        ):
            return

        return_nodes = list(
            function_node.nodes_of_class(nodes.Return, skip_klass=nodes.FunctionDef)
        )
        for ret_node in return_nodes:
            if not (
                isinstance(ret_node.value, nodes.Const)
                and ret_node.value.value is None
                or ret_node.value is None
            ):
                self.add_message("function-return-not-assigned", node=node)
                return


def register(linter: PyLinter) -> None:
    linter.register_checker(FunctionReturnNotAssignedChecker(linter))
