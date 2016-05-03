# -*- coding: utf-8 -*-
"""Module to add McCabe checker class for pylint. """

from mccabe import PathGraph as Mccabe_PathGraph, \
        PathGraphingAstVisitor as Mccabe_PathGraphingAstVisitor
from pylint.checkers.base import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import HIGH, IAstroidChecker


class PathGraph(Mccabe_PathGraph):
    def __init__(self, node):
        super(PathGraph, self).__init__(name='', entity='', lineno=1)
        self.root = node


class PathGraphingAstVisitor(Mccabe_PathGraphingAstVisitor):
    def __init__(self):
        super(PathGraphingAstVisitor, self).__init__()
        self._bottom_counter = 0

    def default(self, node, *args):
        # We don't need original 'iter_child_nodes(node)' here
        pass

    def dispatch(self, node, *args):
        self.node = node
        klass = node.__class__
        meth = self._cache.get(klass)
        if meth is None:
            className = klass.__name__
            meth = getattr(self.visitor, 'visit' + className, self.default)
            self._cache[klass] = meth
        return meth(node, *args)

    def visitFunctionDef(self, node):
        if self.graph is not None:
            # closure
            pathnode = self._append_node(node)
            self.tail = pathnode
            self.dispatch_list(node.body)
            bottom = "%s" % self._bottom_counter
            self._bottom_counter += 1
            self.graph.connect(self.tail, bottom)
            self.graph.connect(node, bottom)
            self.tail = bottom
        else:
            self.graph = PathGraph(node)
            self.tail = node
            self.dispatch_list(node.body)
            self.graphs["%s%s" % (self.classname, node.name)] = self.graph
            self.reset()

    visitAsyncFunctionDef = visitFunctionDef

    def visitSimpleStatement(self, node):
        self._append_node(node)

    visitAssert = visitAssign = visitAugAssign = visitDelete = visitPrint = \
        visitRaise = visitYield = visitImport = visitCall = visitSubscript = \
        visitPass = visitContinue = visitBreak = visitGlobal = visitReturn = \
        visitExpr = visitAwait = visitSimpleStatement

    def visitIf(self, node):
        name = "If %d" % node.lineno
        self._subgraph(node, name)

    def visitTryExcept(self, node):
        name = "TryExcept %d" % node.lineno
        self._subgraph(node, name, extra_blocks=node.handlers)

    visitTry = visitTryExcept

    def visitWith(self, node):
        self._append_node(node)
        self.dispatch_list(node.body)

    def _append_node(self, node):
        if not self.tail:
            return
        self.graph.connect(self.tail, node)
        self.tail = node
        return node

    def _subgraph(self, node, name, extra_blocks=()):
        """create the subgraphs representing any `if` and `for` statements"""
        if self.graph is None:
            # global loop
            self.graph = PathGraph(node)
            self._subgraph_parse(node, node, extra_blocks)
            self.graphs["%s%s" % (self.classname, name)] = self.graph
            self.reset()
        else:
            self._append_node(node)
            self._subgraph_parse(node, node, extra_blocks)

    def _subgraph_parse(self, node, pathnode, extra_blocks):  # pylint: disable=unused-argument
        """parse the body and any `else` block of `if` and `for` statements"""
        loose_ends = []
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
        if node:
            bottom = "%s" % self._bottom_counter
            self._bottom_counter += 1
            for le in loose_ends:
                self.graph.connect(le, bottom)
            self.tail = bottom


class McCabeMethodChecker(BaseChecker):
    """Checks McCabe complexity cyclomatic threshold in methods and functions
    to validate a too complex code.
    """

    __implements__ = IAstroidChecker
    name = 'design'

    msgs = {
        'R1260': (
            '%s is too complex. The McCabe rating is %d',
            'too-complex',
            'Used when a method or function is too complex based on '
            'McCabe Complexity Cyclomatic'),
    }
    options = (
        ('max-complexity', {
            'default': 10,
            'type': 'int',
            'metavar': '<int>',
            'help': 'McCabe complexity cyclomatic threshold',
        }),
    )

    def _check_too_complex(self, node):
        """Check too complex rating and
        add message if is greather than max_complexity stored from options"""
        visitor = PathGraphingAstVisitor()
        for child in node.body:
            visitor.preorder(child, visitor)
        for graph in visitor.graphs.values():
            complexity = graph.complexity()
            if complexity >= self.config.max_complexity:
                node = graph.root
                self.add_message(
                    'too-complex', node=node, confidence=HIGH,
                    args=(node.name, complexity))

    @check_messages('too-complex')
    def visit_module(self, node):
        """visit an astroid.Module node"""
        self._check_too_complex(node)


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(McCabeMethodChecker(linter))
