# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Module to add McCabe checker class for pylint.

Based on:
http://nedbatchelder.com/blog/200803/python_code_complexity_microtool.html
Later integrated in pycqa/mccabe under the MIT License then vendored in pylint
under the GPL License.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from astroid import nodes

from pylint import checkers
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class PathGraph:
    def __init__(self) -> None:
        self.nodes: dict[Any, list[Any]] = {}

    def connect(self, n1: Any, n2: Any) -> None:
        if n1 not in self.nodes:
            self.nodes[n1] = []
        self.nodes[n1].append(n2)
        # Ensure that the destination node is always counted.
        if n2 not in self.nodes:
            self.nodes[n2] = []

    def complexity(self) -> int:
        """Return the McCabe complexity for the graph.

        V-E+2
        """
        num_edges = sum(len(n) for n in self.nodes.values())
        num_nodes = len(self.nodes)
        return num_edges - num_nodes + 2


class PathGraphingAstVisitor:
    """A visitor for a parsed Abstract Syntax Tree which finds executable
    statements.
    """

    def __init__(self) -> None:
        self.graphs: dict[str, tuple[PathGraph, nodes.NodeNG]] = {}
        self._bottom_counter = 0
        self.graph: PathGraph | None = None
        self.tail: Any = None

    def dispatch(self, node: nodes.NodeNG) -> None:
        meth = getattr(self, "visit" + node.__class__.__name__, self.default)
        meth(node)

    def default(self, node: nodes.NodeNG) -> None:
        for child in node.get_children():
            self.dispatch(child)

    def visitFunctionDef(self, node: nodes.FunctionDef) -> None:
        if self.graph is not None:
            # closure
            self.graph.connect(self.tail, node)
            self.tail = node
            for child in node.body:
                self.dispatch(child)
            bottom = f"{self._bottom_counter}"
            self._bottom_counter += 1
            self.graph.connect(self.tail, bottom)
            self.graph.connect(node, bottom)
            self.tail = bottom
        else:
            self.graph = PathGraph()
            self.tail = node
            for child in node.body:
                self.dispatch(child)
            self.graphs[node.name] = (self.graph, node)
            self.graph = None
            self.tail = None

    visitAsyncFunctionDef = visitFunctionDef

    def visitAssert(self, node: nodes.NodeNG) -> None:
        if self.tail and self.graph:
            self.graph.connect(self.tail, node)
            self.tail = node

    visitAssign = visitAugAssign = visitDelete = visitRaise = visitYield = (
        visitImport
    ) = visitCall = visitSubscript = visitPass = visitContinue = visitBreak = (
        visitGlobal
    ) = visitReturn = visitExpr = visitAwait = visitAssert

    def visitWith(self, node: nodes.With) -> None:
        if self.tail and self.graph:
            self.graph.connect(self.tail, node)
            self.tail = node
        for child in node.body:
            self.dispatch(child)

    visitAsyncWith = visitWith

    def visitFor(self, node: nodes.For | nodes.While) -> None:
        self._subgraph(node, node.handlers if isinstance(node, nodes.Try) else [])

    visitAsyncFor = visitWhile = visitIf = visitFor

    def visitTry(self, node: nodes.Try) -> None:
        self._subgraph(node, node.handlers)

    def visitMatch(self, node: nodes.Match) -> None:
        self._subgraph(node, node.cases)

    def _subgraph(
        self, node: nodes.NodeNG, extra_blocks: list[nodes.NodeNG] | None = None
    ) -> None:
        if extra_blocks is None:
            extra_blocks = []
        if self.graph is None:
            self.graph = PathGraph()
            self._parse(node, extra_blocks)
            self.graphs[f"loop_{id(node)}"] = (self.graph, node)
            self.graph = None
            self.tail = None
        else:
            if self.tail:
                self.graph.connect(self.tail, node)
                self.tail = node
            self._parse(node, extra_blocks)

    def _parse(self, node: nodes.NodeNG, extra_blocks: list[nodes.NodeNG]) -> None:
        loose_ends = []
        if isinstance(node, nodes.Match):
            for case in extra_blocks:
                if isinstance(case, nodes.MatchCase):
                    self.tail = node
                    for child in case.body:
                        self.dispatch(child)
                    loose_ends.append(self.tail)
            loose_ends.append(node)
        else:
            self.tail = node
            for child in node.body:
                self.dispatch(child)
            loose_ends.append(self.tail)
            for extra in extra_blocks:
                self.tail = node
                for child in extra.body:
                    self.dispatch(child)
                loose_ends.append(self.tail)
            if hasattr(node, "orelse") and node.orelse:
                self.tail = node
                for child in node.orelse:
                    self.dispatch(child)
                loose_ends.append(self.tail)
            else:
                loose_ends.append(node)

        if self.graph:
            bottom = f"{self._bottom_counter}"
            self._bottom_counter += 1
            for end in loose_ends:
                self.graph.connect(end, bottom)
            self.tail = bottom


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
        """Visit an astroid.Module node to check too complex rating and
        add message if is greater than max_complexity stored from options.
        """
        visitor = PathGraphingAstVisitor()
        for child in module.body:
            visitor.dispatch(child)
        for graph, node in visitor.graphs.values():
            complexity = graph.complexity()
            if hasattr(node, "name"):
                node_name = f"'{node.name}'"
            else:
                node_name = f"This '{node.__class__.__name__.lower()}'"
            if complexity <= self.linter.config.max_complexity:
                continue
            self.add_message(
                "too-complex", node=node, confidence=HIGH, args=(node_name, complexity)
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(McCabeMethodChecker(linter))
