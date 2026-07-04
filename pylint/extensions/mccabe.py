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


def _is_irrefutable(pattern: nodes.Pattern) -> bool:
    """Return True if the pattern always matches (wildcard or capture name).

    Mirrors the grammar: an as-pattern is irrefutable if it has no
    sub-pattern (wildcard ``_`` or bare capture name) or its sub-pattern is
    irrefutable; an or-pattern is irrefutable if its last alternative is.
    """
    if isinstance(pattern, nodes.MatchAs):
        return pattern.pattern is None or _is_irrefutable(pattern.pattern)
    if isinstance(pattern, nodes.MatchOr):
        return _is_irrefutable(pattern.patterns[-1])
    return False


class PathGraphingAstVisitor:
    """Compute McCabe cyclomatic complexity via control flow graph on astroid AST.

    Builds a simplified CFG tracking only compound statements (if, for, while,
    try, with, match, function/class definitions).  Simple statements are
    omitted since collapsing a linear chain of nodes does not change E - N + 2.

    Reproduces the same complexity scores as the ``mccabe`` library, but
    operates directly on astroid trees (no re-parsing) and uses a dict-based
    dispatch table instead of getattr, skipping expression sub-trees entirely.

    Intentional divergences from the previous ``mccabe``-based checker:

    - Results are keyed by node instead of by name, so same-named siblings
      (e.g. property getter/setter/deleter) no longer overwrite each other
      and are all reported (the old checker only kept the last one).
    - An exhaustive ``match`` (last case is an unguarded wildcard or capture
      name) no longer counts a fall-through path, mirroring how ``else``
      is counted for ``if``/``elif`` chains.
    - Straight-line functions are always rated 1: the old checker rated
      functions whose body holds no statement it tracked (docstring only,
      annotated assignments only, ...) at 2 because their graph stayed empty.
    - ``try``/``except*`` counts like ``try``/``except``; the ``mccabe``
      library predates ``except*`` and ignored it.

    Edge and node counts are kept as visitor instance variables to avoid
    per-increment method-call overhead (~1 M calls eliminated on
    repositories with ~2000 files).
    """

    __slots__ = ("_active", "_num_edges", "_num_nodes", "_tail", "graphs")

    # Dispatch table mapping node types to unbound visitor methods.
    # Created once at class level to avoid rebuilding per instance.
    _VISITORS: dict[type, Any] = {}

    def __init__(self) -> None:
        # Maps each scope node to its computed complexity (int).
        self.graphs: dict[nodes.NodeNG, int] = {}
        # Graph counters - modified in-place, saved when a scope closes.
        self._num_nodes = 0
        self._num_edges = 0
        self._active = False  # True while inside a graph scope
        self._tail = 0

    def _walk_body(self, body: list[nodes.NodeNG]) -> None:
        visitors = _VISITORS
        for child in body:
            handler = visitors.get(type(child))
            if handler is not None:
                handler(self, child)

    # -- Visitors ------------------------------------------------------------

    def _visit_function(self, node: nodes.FunctionDef) -> None:
        if self._active:
            # Closure: modeled as a decision point (enter body or skip).
            n = self._num_nodes
            self._num_nodes = n + 1
            self._num_edges += 1
            self._tail = n
            self._walk_body(node.body)
            # Merge node: body-end -> merge + path-node -> merge (skip edge).
            merge = n + 1 if self._num_nodes == n + 1 else self._num_nodes
            self._num_nodes = merge + 1
            self._num_edges += 2
            self._tail = merge
            return
        # Top-level function/method: save state, start fresh graph.
        old_n, old_e, old_tail = self._num_nodes, self._num_edges, self._tail
        self._num_nodes = 1  # entry node (id 0)
        self._num_edges = 0
        self._active = True
        self._tail = 0
        self._walk_body(node.body)
        self.graphs[node] = self._num_edges - self._num_nodes + 2
        self._num_nodes, self._num_edges, self._tail = old_n, old_e, old_tail
        self._active = False

    def _visit_body(self, node: nodes.NodeNG) -> None:
        # ClassDef and With both just recurse into the body.
        # ClassDef: don't reset the graph -- methods inside a nested class
        # (within a function) are treated as closures of the enclosing function.
        # With: no complexity added, but body may contain compound statements.
        self._walk_body(node.body)

    def _visit_subgraph(self, node: nodes.NodeNG) -> None:
        """Handle if / for / while as branching subgraphs."""
        is_toplevel = not self._active
        if is_toplevel:
            old_n, old_e, old_tail = (
                self._num_nodes,
                self._num_edges,
                self._tail,
            )
            self._num_nodes = 1  # path-node (id 0)
            self._num_edges = 0
            self._active = True
            pathnode = 0
        else:
            pathnode = self._num_nodes
            self._num_nodes = pathnode + 1
            self._num_edges += 1

        # -- inline sub-graph parse (no extra_blocks for if/for/while) --
        walk = self._walk_body
        self._tail = pathnode
        walk(node.body)
        if node.orelse:
            self._tail = pathnode
            walk(node.orelse)
        # Always 2 loose ends: body + (orelse or fall-through path-node).
        merge = self._num_nodes
        self._num_nodes = merge + 1
        self._num_edges += 2
        self._tail = merge

        if is_toplevel:
            self.graphs[node] = self._num_edges - self._num_nodes + 2
            self._num_nodes, self._num_edges, self._tail = (
                old_n,
                old_e,
                old_tail,
            )
            self._active = False

    def _visit_try(self, node: nodes.Try) -> None:
        """Handle try/except as branching subgraphs with except handlers."""
        is_toplevel = not self._active
        if is_toplevel:
            old_n, old_e, old_tail = (
                self._num_nodes,
                self._num_edges,
                self._tail,
            )
            self._num_nodes = 1
            self._num_edges = 0
            self._active = True
            pathnode = 0
        else:
            pathnode = self._num_nodes
            self._num_nodes = pathnode + 1
            self._num_edges += 1

        # -- inline sub-graph parse with extra_blocks = node.handlers --
        walk = self._walk_body
        num_loose_ends = 1  # main body
        self._tail = pathnode
        walk(node.body)
        for handler in node.handlers:
            self._tail = pathnode
            walk(handler.body)
            num_loose_ends += 1
        if node.orelse:
            self._tail = pathnode
            walk(node.orelse)
            num_loose_ends += 1
        else:
            num_loose_ends += 1  # fall-through
        merge = self._num_nodes
        self._num_nodes = merge + 1
        self._num_edges += num_loose_ends
        self._tail = merge

        if is_toplevel:
            self.graphs[node] = self._num_edges - self._num_nodes + 2
            self._num_nodes, self._num_edges, self._tail = (
                old_n,
                old_e,
                old_tail,
            )
            self._active = False

    def _visit_match(self, node: nodes.Match) -> None:
        is_toplevel = not self._active
        if is_toplevel:
            old_n, old_e, old_tail = (
                self._num_nodes,
                self._num_edges,
                self._tail,
            )
            self._num_nodes = 1
            self._num_edges = 0
            self._active = True
            pathnode = 0
        else:
            pathnode = self._num_nodes
            self._num_nodes = pathnode + 1
            self._num_edges += 1

        self._tail = pathnode
        walk = self._walk_body
        num_loose_ends = 0
        for case in node.cases:
            self._tail = pathnode
            walk(case.body)
            num_loose_ends += 1
        last_case = node.cases[-1]
        if last_case.guard is not None or not _is_irrefutable(last_case.pattern):
            # Non-exhaustive match: no case may apply, count the
            # fall-through path (equivalent to an if/elif without else).
            num_loose_ends += 1
        merge = self._num_nodes
        self._num_nodes = merge + 1
        self._num_edges += num_loose_ends
        self._tail = merge

        if is_toplevel:
            self.graphs[node] = self._num_edges - self._num_nodes + 2
            self._num_nodes, self._num_edges, self._tail = (
                old_n,
                old_e,
                old_tail,
            )
            self._active = False


# Module-level dispatch table - built once, shared by all visitor instances.
# Uses unbound methods; callers pass ``self`` explicitly.
_VISITORS: dict[type, Any] = {
    nodes.FunctionDef: PathGraphingAstVisitor._visit_function,
    nodes.AsyncFunctionDef: PathGraphingAstVisitor._visit_function,
    nodes.ClassDef: PathGraphingAstVisitor._visit_body,
    nodes.If: PathGraphingAstVisitor._visit_subgraph,
    nodes.For: PathGraphingAstVisitor._visit_subgraph,
    nodes.AsyncFor: PathGraphingAstVisitor._visit_subgraph,
    nodes.While: PathGraphingAstVisitor._visit_subgraph,
    nodes.Try: PathGraphingAstVisitor._visit_try,
    nodes.TryStar: PathGraphingAstVisitor._visit_try,
    nodes.With: PathGraphingAstVisitor._visit_body,
    nodes.AsyncWith: PathGraphingAstVisitor._visit_body,
    nodes.Match: PathGraphingAstVisitor._visit_match,
}
PathGraphingAstVisitor._VISITORS = _VISITORS


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
    def visit_module(self, node: nodes.Module) -> None:
        """Visit an nodes.Module node to check too complex rating and
        add message if is greater than max_complexity stored from options.
        """
        visitor = PathGraphingAstVisitor()
        visitor._walk_body(node.body)
        max_complexity = self.linter.config.max_complexity
        for checked_node, complexity in visitor.graphs.items():
            if complexity <= max_complexity:
                continue
            if hasattr(checked_node, "name"):
                node_name = f"'{checked_node.name}'"
            else:
                node_name = f"This '{checked_node.__class__.__name__.lower()}'"
            self.add_message(
                "too-complex",
                node=checked_node,
                confidence=HIGH,
                args=(node_name, complexity),
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(McCabeMethodChecker(linter))
