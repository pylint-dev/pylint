# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from itertools import zip_longest
from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH

# PEP 572 forbids an assignment expression inside a comprehension whose
# containing scope is a class body, and every comprehension form is covered.
COMPREHENSION_NODES = (
    nodes.DictComp,
    nodes.GeneratorExp,
    nodes.ListComp,
    nodes.SetComp,
)

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class LambdaExpressionChecker(BaseChecker):
    """Check for unnecessary usage of lambda expressions."""

    name = "lambda-expressions"
    msgs = {
        "C3001": (
            "Lambda expression assigned to a variable. "
            'Define a function using the "def" keyword instead.',
            "unnecessary-lambda-assignment",
            "Used when a lambda expression is assigned to variable "
            'rather than defining a standard function with the "def" keyword.',
        ),
        "C3002": (
            "Lambda expression called directly. Execute the expression inline instead.",
            "unnecessary-direct-lambda-call",
            "Used when a lambda expression is directly called "
            "rather than executing its contents inline.",
        ),
    }
    options = ()

    def visit_assign(self, node: nodes.Assign) -> None:
        """Check if lambda expression is assigned to a variable."""
        match node:
            case nodes.Assign(
                targets=[nodes.AssignName(), *_], value=nodes.Lambda() as value
            ):
                self.add_message(
                    "unnecessary-lambda-assignment",
                    node=value,
                    confidence=HIGH,
                )
            case nodes.Assign(
                targets=[nodes.Tuple() as target, *_],
                value=nodes.Tuple() | nodes.List() as value,
            ):
                # Iterate over tuple unpacking assignment elements and
                # see if any lambdas are assigned to a variable.
                # N.B. We may encounter W0632 (unbalanced-tuple-unpacking)
                # and still need to flag the lambdas that are being assigned.
                for lhs_elem, rhs_elem in zip_longest(target.elts, value.elts):
                    if lhs_elem is None or rhs_elem is None:
                        # unbalanced tuple unpacking. stop checking.
                        break
                    if isinstance(lhs_elem, nodes.AssignName) and isinstance(
                        rhs_elem, nodes.Lambda
                    ):
                        self.add_message(
                            "unnecessary-lambda-assignment",
                            node=rhs_elem,
                            confidence=HIGH,
                        )

    def visit_namedexpr(self, node: nodes.NamedExpr) -> None:
        match node:
            case nodes.NamedExpr(
                target=nodes.AssignName(), value=nodes.Lambda() as value
            ):
                self.add_message(
                    "unnecessary-lambda-assignment",
                    node=value,
                    confidence=HIGH,
                )

    def visit_call(self, node: nodes.Call) -> None:
        """Check if lambda expression is called directly."""
        if isinstance(node.func, nodes.Lambda) and not _lambda_scope_is_required(node):
            self.add_message(
                "unnecessary-direct-lambda-call",
                node=node,
                confidence=HIGH,
            )


def _lambda_scope_is_required(node: nodes.Call) -> bool:
    """Whether inlining this directly called lambda would not compile.

    A comprehension carrying an assignment expression is a SyntaxError when its
    containing scope is a class body (PEP 572). The lambda supplies a function
    scope in between, so removing it, which is exactly what the message advises,
    turns working code into code that does not parse.

    Only a comprehension that would land in the class body itself counts. One
    nested inside a further lambda or function keeps a scope of its own after
    the inlining, so the call around it is still reported.
    """
    if not isinstance(node.frame(), nodes.ClassDef):
        return False
    for comprehension in node.func.body.nodes_of_class(COMPREHENSION_NODES):
        if not any(True for _ in comprehension.nodes_of_class(nodes.NamedExpr)):
            continue
        enclosing_scope = comprehension.parent
        while enclosing_scope is not None and not isinstance(
            enclosing_scope, (nodes.Lambda, nodes.FunctionDef)
        ):
            enclosing_scope = enclosing_scope.parent
        if enclosing_scope is node.func:
            return True
    return False


def register(linter: PyLinter) -> None:
    linter.register_checker(LambdaExpressionChecker(linter))
