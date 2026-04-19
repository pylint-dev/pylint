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
    """Track control flow edges and nodes for McCabe complexity (E - N + 2).

    Instead of storing actual graph structure, we only need the counts:
    the complexity formula V = E - N + 2 depends only on the number of
    edges and nodes, not their identity.
    """

    __slots__ = ("_num_edges", "_num_nodes")

    def __init__(self) -> None:
        self._num_nodes = 0
        self._num_edges = 0

    def add_node(self) -> int:
        nid = self._num_nodes
        self._num_nodes += 1
        return nid

    def add_edge(self) -> None:
        self._num_edges += 1

    def complexity(self) -> int:
        return self._num_edges - self._num_nodes + 2


class PathGraphingAstVisitor:
    """Compute McCabe cyclomatic complexity via control flow graph on astroid AST.

    Builds a simplified CFG tracking only compound statements (if, for, while,
    try, with, match, function/class defs).  Simple statements are omitted since
    collapsing a linear chain of nodes does not change E - N + 2.

    Reproduces the same complexity scores as the ``mccabe`` library, but operates
    directly on astroid trees (no re-parsing) and uses a dict-based dispatch table
    instead of getattr, skipping expression subtrees entirely.
    """

    def __init__(self) -> None:
        self.graphs: dict[int, tuple[PathGraph, nodes.NodeNG]] = {}
        self._graph: PathGraph | None = None
        self._tail: int = -1
        self._visitors: dict[type, Any] = {
            nodes.FunctionDef: self._visit_function,
            nodes.AsyncFunctionDef: self._visit_function,
            nodes.ClassDef: self._visit_classdef,
            nodes.If: self._visit_branching,
            nodes.For: self._visit_branching,
            nodes.AsyncFor: self._visit_branching,
            nodes.While: self._visit_branching,
            nodes.Try: self._visit_try,
            nodes.TryStar: self._visit_try,
            nodes.With: self._visit_with,
            nodes.AsyncWith: self._visit_with,
            nodes.Match: self._visit_match,
        }

    def dispatch(self, node: nodes.NodeNG) -> None:
        handler = self._visitors.get(type(node))
        if handler is not None:
            handler(node)

    def _walk_body(self, body: list[nodes.NodeNG]) -> None:
        visitors = self._visitors
        for child in body:
            handler = visitors.get(type(child))
            if handler is not None:
                handler(child)

    def _append_node(self) -> int:
        """Create a new graph node, add an edge from tail, update tail."""
        graph = self._graph
        assert graph is not None
        nid = graph.add_node()
        graph.add_edge()
        self._tail = nid
        return nid

    # -- Visitors ------------------------------------------------------------

    def _visit_function(self, node: nodes.FunctionDef) -> None:
        if self._graph is not None:
            # Closure: modelled as a decision point (enter body or skip).
            self._append_node()
            self._walk_body(node.body)
            merge = self._graph.add_node()
            self._graph.add_edge()  # body end → merge
            self._graph.add_edge()  # pathnode → merge (skip edge)
            self._tail = merge
            return
        # Top-level function/method: start a new graph.
        graph = PathGraph()
        self._graph = graph
        self.graphs[id(node)] = (graph, node)
        self._tail = graph.add_node()
        self._walk_body(node.body)
        self._graph = None
        self._tail = -1

    def _visit_classdef(self, node: nodes.ClassDef) -> None:
        # Don't reset the graph: in the original mccabe, a class body is walked
        # with the enclosing graph still set. Methods inside a nested class
        # (within a function) are thus treated as closures of the enclosing
        # function, adding +1 each. At module level, graph is already None.
        self._walk_body(node.body)

    def _visit_branching(self, node: nodes.NodeNG) -> None:
        """Handle if / for / while — same subgraph logic, no extra blocks."""
        self._subgraph(node)

    def _visit_try(self, node: nodes.Try) -> None:
        """Handle try/except — except handlers are extra branching blocks."""
        self._subgraph(node, extra_blocks=node.handlers)

    def _subgraph(
        self,
        node: nodes.NodeNG,
        extra_blocks: tuple[()] | list[nodes.NodeNG] = (),
    ) -> None:
        if self._graph is None:
            # Top-level construct (module-level if/for/try): own graph.
            graph = PathGraph()
            self._graph = graph
            self.graphs[id(node)] = (graph, node)
            pathnode = graph.add_node()
            self._tail = pathnode
            self._subgraph_parse(node, pathnode, extra_blocks)
            self._graph = None
            self._tail = -1
        else:
            pathnode = self._append_node()
            self._subgraph_parse(node, pathnode, extra_blocks)

    def _subgraph_parse(
        self,
        node: nodes.NodeNG,
        pathnode: int,
        extra_blocks: tuple[()] | list[nodes.NodeNG],
    ) -> None:
        """Build the branching subgraph: body, extra blocks, orelse, merge."""
        graph = self._graph
        assert graph is not None
        num_loose_ends = 0

        # Main body
        self._tail = pathnode
        self._walk_body(node.body)
        num_loose_ends += 1

        # Extra blocks (except handlers for try)
        for extra in extra_blocks:
            self._tail = pathnode
            self._walk_body(extra.body)
            num_loose_ends += 1

        # Else branch
        if node.orelse:
            self._tail = pathnode
            self._walk_body(node.orelse)
            num_loose_ends += 1
        else:
            # No else: the pathnode itself is a loose end (fall-through path).
            num_loose_ends += 1

        # Merge all loose ends into a single bottom node.
        merge = graph.add_node()
        for _ in range(num_loose_ends):
            graph.add_edge()
        self._tail = merge

    def _visit_with(self, node: nodes.With) -> None:
        self._walk_body(node.body)

    def _visit_match(self, node: nodes.Match) -> None:
        if self._graph is None:
            return
        pathnode = self._append_node()
        num_cases = 0
        for case in node.cases:
            self._tail = pathnode
            self._walk_body(case.body)
            num_cases += 1
        merge = self._graph.add_node()
        for _ in range(num_cases):
            self._graph.add_edge()
        self._tail = merge


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
