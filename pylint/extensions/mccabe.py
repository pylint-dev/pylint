# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# mypy: ignore-errors
# pylint: disable=unused-argument,consider-using-generator

"""Module to add McCabe checker class for pylint.

Based on:
http://nedbatchelder.com/blog/200803/python_code_complexity_microtool.html
Later integrated in pycqa/mccabe under the MIT License then vendored in pylint
under the GPL License.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, TypeAlias, TypeVar

from astroid import nodes

from pylint import checkers
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


_StatementNodes: TypeAlias = (
    nodes.Assert
    | nodes.Assign
    | nodes.AugAssign
    | nodes.Delete
    | nodes.Raise
    | nodes.Yield
    | nodes.Import
    | nodes.Call
    | nodes.Subscript
    | nodes.Pass
    | nodes.Continue
    | nodes.Break
    | nodes.Global
    | nodes.Return
    | nodes.Expr
    | nodes.Await
)

_SubGraphNodes: TypeAlias = nodes.If | nodes.Try | nodes.For | nodes.While | nodes.Match
_AppendableNodeT = TypeVar(
    "_AppendableNodeT", bound=_StatementNodes | nodes.While | nodes.FunctionDef
)


class PathGraph:
    def __init__(self, node: _SubGraphNodes | nodes.FunctionDef):
        self.name = ""
        self.root = node
        self.nodes = {}

    def connect(self, n1, n2):
        if n1 not in self.nodes:
            self.nodes[n1] = []
        self.nodes[n1].append(n2)
        # Ensure that the destination node is always counted.
        if n2 not in self.nodes:
            self.nodes[n2] = []

    def complexity(self):
        """Return the McCabe complexity for the graph.

        V-E+2
        """
        num_edges = sum([len(n) for n in self.nodes.values()])
        num_nodes = len(self.nodes)
        return num_edges - num_nodes + 2


class PathGraphingAstVisitor:
    """A visitor for a parsed Abstract Syntax Tree which finds executable
    statements.
    """

    def __init__(self) -> None:
        self.classname = ""
        self.graphs = {}
        self._cache = {}
        self._bottom_counter = 0
        self.graph: PathGraph | None = None
        self.tail = None

    def reset(self):
        self.graph = None
        self.tail = None

    def default(self, node: nodes.NodeNG, *args: Any) -> None:
        for child in node.get_children():
            self.dispatch(child, *args)

    def dispatch(self, node: nodes.NodeNG, *args: Any) -> Any:
        klass = node.__class__
        meth = self._cache.get(klass)
        if meth is None:
            class_name = klass.__name__
            meth = getattr(self, "visit" + class_name, self.default)
            self._cache[klass] = meth
        return meth(node, *args)

    def preorder(self, tree, visitor):
        """Do preorder walk of tree using visitor."""
        self.dispatch(tree)

    def dispatch_list(self, node_list):
        for node in node_list:
            self.dispatch(node)

    def visitFunctionDef(self, node: nodes.FunctionDef) -> None:
        if self.graph is not None:
            # closure
            pathnode = self._append_node(node)
            self.tail = pathnode
            self.dispatch_list(node.body)
            bottom = f"{self._bottom_counter}"
            self._bottom_counter += 1
            self.graph.connect(self.tail, bottom)
            self.graph.connect(node, bottom)
            self.tail = bottom
        else:
            self.graph = PathGraph(node)
            self.tail = node
            self.dispatch_list(node.body)
            self.graphs[f"{self.classname}{node.name}"] = self.graph
            self.reset()

    visitAsyncFunctionDef = visitFunctionDef

    def visitClassDef(self, node: nodes.ClassDef) -> None:
        old_classname = self.classname
        self.classname += node.name + "."
        self.dispatch_list(node.body)
        self.classname = old_classname

    def visitSimpleStatement(self, node: _StatementNodes) -> None:
        self._append_node(node)

    visitAssert = visitAssign = visitAugAssign = visitDelete = visitRaise = (
        visitYield
    ) = visitImport = visitCall = visitSubscript = visitPass = visitContinue = (
        visitBreak
    ) = visitGlobal = visitReturn = visitExpr = visitAwait = visitSimpleStatement

    def visitWith(self, node: nodes.With) -> None:
        self._append_node(node)
        self.dispatch_list(node.body)

    visitAsyncWith = visitWith

    def visitLoop(self, node: nodes.For | nodes.While) -> None:
        name = f"loop_{id(node)}"
        self._subgraph(node, name)

    visitAsyncFor = visitFor = visitWhile = visitLoop

    def visitIf(self, node: nodes.If) -> None:
        name = f"if_{id(node)}"
        self._subgraph(node, name)

    def visitTryExcept(self, node: nodes.Try) -> None:
        name = f"try_{id(node)}"
        self._subgraph(node, name, extra_blocks=node.handlers)

    visitTry = visitTryExcept

    def visitMatch(self, node: nodes.Match) -> None:
        self._subgraph(node, f"match_{id(node)}", node.cases)

    def _append_node(self, node: _AppendableNodeT) -> _AppendableNodeT | None:
        if not self.tail or not self.graph:
            return None
        self.graph.connect(self.tail, node)
        self.tail = node
        return node

    def _subgraph(
        self,
        node: _SubGraphNodes,
        name: str,
        extra_blocks: Sequence[nodes.ExceptHandler | nodes.MatchCase] = (),
    ) -> None:
        """Create the subgraphs representing any `if`, `for` or `match` statements."""
        if self.graph is None:
            # global loop
            self.graph = PathGraph(node)
            self._subgraph_parse(node, node, extra_blocks)
            self.graphs[f"{self.classname}{name}"] = self.graph
            self.reset()
        else:
            self._append_node(node)
            self._subgraph_parse(node, node, extra_blocks)

    def _subgraph_parse(
        self,
        node: _SubGraphNodes,
        pathnode: _SubGraphNodes,
        extra_blocks: Sequence[nodes.ExceptHandler | nodes.MatchCase],
    ) -> None:
        """Parse `match`/`case` blocks, or the body and `else` block of `if`/`for`
        statements.
        """
        loose_ends = []
        if isinstance(node, nodes.Match):
            for case in extra_blocks:
                if isinstance(case, nodes.MatchCase):
                    self.tail = node
                    self.dispatch_list(case.body)
                    loose_ends.append(self.tail)
            loose_ends.append(node)
        else:
            self.tail = node
            self.dispatch_list(node.body)
            loose_ends.append(self.tail)
            for extra in extra_blocks:
                self.tail = node
                self.dispatch_list(extra.body)
                loose_ends.append(self.tail)
            if node.orelse:
                self.tail = node
                self.dispatch_list(node.orelse)
                loose_ends.append(self.tail)
            else:
                loose_ends.append(node)

        if node and self.graph:
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
    def visit_module(self, node: nodes.Module) -> None:
        """Visit an astroid.Module node to check too complex rating and
        add message if is greater than max_complexity stored from options.
        """
        visitor = PathGraphingAstVisitor()
        for child in node.body:
            visitor.preorder(child, visitor)
        for graph in visitor.graphs.values():
            complexity = graph.complexity()
            node = graph.root
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
