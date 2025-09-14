# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# mypy: ignore-errors
# pylint: disable=consider-using-f-string,inconsistent-return-statements,consider-using-generator,redefined-builtin
# pylint: disable=super-with-arguments,too-many-function-args,bad-super-call

"""Module to add McCabe checker class for pylint.

Based on:
http://nedbatchelder.com/blog/200803/python_code_complexity_microtool.html
Later integrated in pycqa/mccabe under the MIT License then vendored in pylint
under the GPL License.
"""

from __future__ import annotations

import ast
from ast import iter_child_nodes
from collections import defaultdict
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, TypeAlias, TypeVar

from astroid import nodes

from pylint import checkers
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class ASTVisitor:
    """Performs a depth-first walk of the AST."""

    def __init__(self):
        self.node = None
        self._cache = {}

    def default(self, node, *args):
        for child in iter_child_nodes(node):
            self.dispatch(child, *args)

    def dispatch(self, node, *args):
        self.node = node
        klass = node.__class__
        meth = self._cache.get(klass)
        if meth is None:
            className = klass.__name__
            meth = getattr(self.visitor, "visit" + className, self.default)
            self._cache[klass] = meth
        return meth(node, *args)

    def preorder(self, tree, visitor, *args):
        """Do preorder walk of tree using visitor."""
        self.visitor = visitor
        visitor.visit = self.dispatch
        self.dispatch(tree, *args)  # XXX *args make sense?


class PathNode:
    def __init__(self, name, look="circle"):
        self.name = name
        self.look = look

    def to_dot(self):
        print('node [shape=%s,label="%s"] %d;' % (self.look, self.name, self.dot_id()))

    def dot_id(self):
        return id(self)


class Mccabe_PathGraph:
    def __init__(self, name, entity, lineno, column=0):
        self.name = name
        self.entity = entity
        self.lineno = lineno
        self.column = column
        self.nodes = defaultdict(list)

    def connect(self, n1, n2):
        self.nodes[n1].append(n2)
        # Ensure that the destination node is always counted.
        self.nodes[n2] = []

    def to_dot(self):
        print("subgraph {")
        for node in self.nodes:
            node.to_dot()
        for node, nexts in self.nodes.items():
            for next in nexts:
                print("%s -- %s;" % (node.dot_id(), next.dot_id()))
        print("}")

    def complexity(self):
        """Return the McCabe complexity for the graph.

        V-E+2
        """
        num_edges = sum([len(n) for n in self.nodes.values()])
        num_nodes = len(self.nodes)
        return num_edges - num_nodes + 2


class Mccabe_PathGraphingAstVisitor(ASTVisitor):
    """A visitor for a parsed Abstract Syntax Tree which finds executable
    statements.
    """

    def __init__(self):
        super(Mccabe_PathGraphingAstVisitor, self).__init__()
        self.classname = ""
        self.graphs = {}
        self.reset()

    def reset(self):
        self.graph = None
        self.tail = None

    def dispatch_list(self, node_list):
        for node in node_list:
            self.dispatch(node)

    def visitFunctionDef(self, node):

        if self.classname:
            entity = "%s%s" % (self.classname, node.name)
        else:
            entity = node.name

        name = "%d:%d: %r" % (node.lineno, node.col_offset, entity)

        if self.graph is not None:
            # closure
            pathnode = self.appendPathNode(name)
            self.tail = pathnode
            self.dispatch_list(node.body)
            bottom = PathNode("", look="point")
            self.graph.connect(self.tail, bottom)
            self.graph.connect(pathnode, bottom)
            self.tail = bottom
        else:
            self.graph = PathGraph(name, entity, node.lineno, node.col_offset)
            pathnode = PathNode(name)
            self.tail = pathnode
            self.dispatch_list(node.body)
            self.graphs["%s%s" % (self.classname, node.name)] = self.graph
            self.reset()

    visitAsyncFunctionDef = visitFunctionDef

    def visitClassDef(self, node):
        old_classname = self.classname
        self.classname += node.name + "."
        self.dispatch_list(node.body)
        self.classname = old_classname

    def appendPathNode(self, name):
        if not self.tail:
            return
        pathnode = PathNode(name)
        self.graph.connect(self.tail, pathnode)
        self.tail = pathnode
        return pathnode

    def visitSimpleStatement(self, node):
        if node.lineno is None:
            lineno = 0
        else:
            lineno = node.lineno
        name = "Stmt %d" % lineno
        self.appendPathNode(name)

    def default(self, node, *args):
        if isinstance(node, ast.stmt):
            self.visitSimpleStatement(node)
        else:
            super(PathGraphingAstVisitor, self).default(node, *args)

    def visitLoop(self, node):
        name = "Loop %d" % node.lineno
        self._subgraph(node, name)

    visitAsyncFor = visitFor = visitWhile = visitLoop

    def visitIf(self, node):
        name = "If %d" % node.lineno
        self._subgraph(node, name)

    def _subgraph(self, node, name, extra_blocks=()):
        """Create the subgraphs representing any `if` and `for` statements."""
        if self.graph is None:
            # global loop
            self.graph = PathGraph(name, name, node.lineno, node.col_offset)
            pathnode = PathNode(name)
            self._subgraph_parse(node, pathnode, extra_blocks)
            self.graphs["%s%s" % (self.classname, name)] = self.graph
            self.reset()
        else:
            pathnode = self.appendPathNode(name)
            self._subgraph_parse(node, pathnode, extra_blocks)

    def _subgraph_parse(self, node, pathnode, extra_blocks):
        """Parse the body and any `else` block of `if` and `for` statements."""
        loose_ends = []
        self.tail = pathnode
        self.dispatch_list(node.body)
        loose_ends.append(self.tail)
        for extra in extra_blocks:
            self.tail = pathnode
            self.dispatch_list(extra.body)
            loose_ends.append(self.tail)
        if node.orelse:
            self.tail = pathnode
            self.dispatch_list(node.orelse)
            loose_ends.append(self.tail)
        else:
            loose_ends.append(pathnode)
        if pathnode:
            bottom = PathNode("", look="point")
            for le in loose_ends:
                self.graph.connect(le, bottom)
            self.tail = bottom

    def visitTryExcept(self, node):
        name = "TryExcept %d" % node.lineno
        self._subgraph(node, name, extra_blocks=node.handlers)

    visitTry = visitTryExcept

    def visitWith(self, node):
        name = "With %d" % node.lineno
        self.appendPathNode(name)
        self.dispatch_list(node.body)

    visitAsyncWith = visitWith


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


class PathGraph(Mccabe_PathGraph):  # type: ignore[misc]
    def __init__(self, node: _SubGraphNodes | nodes.FunctionDef):
        super().__init__(name="", entity="", lineno=1)
        self.root = node


class PathGraphingAstVisitor(Mccabe_PathGraphingAstVisitor):  # type: ignore[misc]
    def __init__(self) -> None:
        super().__init__()
        self._bottom_counter = 0
        self.graph: PathGraph | None = None

    def default(self, node: nodes.NodeNG, *args: Any) -> None:
        for child in node.get_children():
            self.dispatch(child, *args)

    def dispatch(self, node: nodes.NodeNG, *args: Any) -> Any:
        self.node = node
        klass = node.__class__
        meth = self._cache.get(klass)
        if meth is None:
            class_name = klass.__name__
            meth = getattr(self.visitor, "visit" + class_name, self.default)
            self._cache[klass] = meth
        return meth(node, *args)

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
