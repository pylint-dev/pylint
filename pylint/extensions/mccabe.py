# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from astroid import nodes

from pylint import checkers
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class PathGraph:
    """Represent a linear control flow subgraph for complexity calculation."""

    __slots__ = ("complexity_score",)

    def __init__(self) -> None:
        self.complexity_score = 1

    def complexity(self) -> int:
        return self.complexity_score


class PathGraphingAstVisitor:
    """Compute McCabe cyclomatic complexity by walking astroid AST nodes.

    For each function, method, or top-level loop/with, a PathGraph is created.
    Decision points (if, for, while, except, case, etc.) each add +1.

    Only compound statements (if, for, while, try, with, match, function/class
    defs) can contain nested statements. Simple statements and expressions never
    do. We provide explicit handlers for every compound statement type so that
    ``dispatch`` can skip non-compound nodes entirely — avoiding millions of
    useless ``get_children()`` + recursive calls into expression trees.
    """

    def __init__(self) -> None:
        self.graphs: dict[int, tuple[PathGraph, nodes.NodeNG]] = {}
        self._current_graph: PathGraph | None = None
        # Build dispatch table: node type → bound method.
        # Only compound statements need handlers; all others are no-ops.
        self._visitors: dict[type, Any] = {
            nodes.FunctionDef: self._visit_function,
            nodes.AsyncFunctionDef: self._visit_function,
            nodes.ClassDef: self._visit_classdef,
            nodes.If: self._visit_if,
            nodes.For: self._visit_loop,
            nodes.AsyncFor: self._visit_loop,
            nodes.While: self._visit_loop,
            nodes.Try: self._visit_try,
            nodes.TryStar: self._visit_try,
            nodes.With: self._visit_with,
            nodes.AsyncWith: self._visit_with,
            nodes.Match: self._visit_match,
        }

    def dispatch(self, node: nodes.NodeNG) -> None:
        """Dispatch to the appropriate visitor method for a node.

        Nodes without a handler are simple statements or expressions that
        cannot contain nested compound statements, so they are skipped.
        """
        handler = self._visitors.get(type(node))
        if handler is not None:
            handler(node)

    def _walk_body(self, body: list[nodes.NodeNG]) -> None:
        visitors = self._visitors
        for child in body:
            handler = visitors.get(type(child))
            if handler is not None:
                handler(child)

    def _visit_function(self, node: nodes.FunctionDef) -> None:
        graph = self._current_graph
        if graph is not None:
            # Inner function definition: adds +1 to enclosing scope
            # and its body is walked as part of the enclosing graph.
            graph.complexity_score += 1
            self._walk_body(node.body)
            return
        # Top-level function/method: create a new graph
        graph = PathGraph()
        self.graphs[id(node)] = (graph, node)
        self._current_graph = graph
        self._walk_body(node.body)
        self._current_graph = None

    def _visit_classdef(self, node: nodes.ClassDef) -> None:
        # Classes don't get their own complexity graph.
        # Recurse into the class body to discover methods.
        old_graph = self._current_graph
        self._current_graph = None
        self._walk_body(node.body)
        self._current_graph = old_graph

    def _visit_if(self, node: nodes.If) -> None:
        graph = self._current_graph
        if graph is not None:
            graph.complexity_score += 1
        self._walk_body(node.body)
        orelse = node.orelse
        if orelse:
            self._walk_body(orelse)

    def _visit_loop(self, node: nodes.For | nodes.While) -> None:
        graph = self._current_graph
        if graph is None:
            # Top-level loop: create its own graph
            graph = PathGraph()
            self.graphs[id(node)] = (graph, node)
            self._current_graph = graph
            graph.complexity_score += 1
            self._walk_body(node.body)
            orelse = node.orelse
            if orelse:
                self._walk_body(orelse)
            self._current_graph = None
            return
        graph.complexity_score += 1
        self._walk_body(node.body)
        orelse = node.orelse
        if orelse:
            self._walk_body(orelse)

    def _visit_try(self, node: nodes.Try) -> None:
        graph = self._current_graph
        if graph is None:
            return
        # Walk the try body
        self._walk_body(node.body)
        # Each except handler: +1
        for handler in node.handlers:
            graph.complexity_score += 1
            self._walk_body(handler.body)
        # try-else: +1
        if node.orelse:
            graph.complexity_score += 1
            self._walk_body(node.orelse)
        # finally: +1 for the exceptional path, but the finally body
        # is NOT included in complexity analysis
        if node.finalbody:
            graph.complexity_score += 1

    def _visit_with(self, node: nodes.With) -> None:
        # ``with`` does not add complexity, but its body may contain
        # compound statements that do.
        self._walk_body(node.body)

    def _visit_match(self, node: nodes.Match) -> None:
        graph = self._current_graph
        if graph is None:
            return
        for case in node.cases:
            graph.complexity_score += 1
            self._walk_body(case.body)


class McCabeMethodChecker(checkers.BaseChecker):
    """Checks McCabe complexity cyclomatic threshold in methods and functions
    to validate a too complex code.
    """

    name = "design"

    msgs = {
        "R1260": (
            "%s is too complex. The McCabe rating is %d",
            "too-complex",
            "Used when a method or function is too complex based on "
            "McCabe Complexity Cyclomatic",
        )
    }
    options = (
        (
            "max-complexity",
            {
                "default": 10,
                "type": "int",
                "metavar": "<int>",
                "help": "McCabe complexity cyclomatic threshold",
            },
        ),
    )

    @only_required_for_messages("too-complex")
    def visit_module(self, module: nodes.Module) -> None:
        """Visit a module node to check too complex rating and
        add message if is greater than max_complexity stored from options.
        """
        visitor = PathGraphingAstVisitor()
        for child in module.body:
            visitor.dispatch(child)
        for graph, node in visitor.graphs.values():
            complexity = graph.complexity()
            if complexity <= self.linter.config.max_complexity:
                continue
            if hasattr(node, "name"):
                node_name = f"'{node.name}'"
            else:
                node_name = f"This '{node.__class__.__name__.lower()}'"
            self.add_message(
                "too-complex", node=node, confidence=HIGH, args=(node_name, complexity)
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(McCabeMethodChecker(linter))
