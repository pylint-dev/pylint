# -*- coding: utf-8 -*-
"""Module to add McCabe checker class for pylint. """

import ast

from mccabe import McCabeChecker
from pylint.checkers.base import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import HIGH, IAstroidChecker


class MethodMcCabeChecker(BaseChecker):
    """Checks McCabe complexity cyclomatic threshold in methods and functions
    to validate a too complex code.
    """

    __implements__ = IAstroidChecker
    name = 'methodmccabechecker'

    msgs = {
        'R1260': (
            '%s is too complex. The McCabe rating is %d',
            'too-complex',
            'Used when a method or function is too complex based on '
            'McCabe Complexity Cyclomatic'),
    }
    options = (
        ('max-complexity', {
            'group': 'design',
            'default': 10,
            'type': 'int',
            'metavar': '<int>',
            'help': 'McCabe complexity cyclomatic threshold',
        }),
    )

    @staticmethod
    def _get_ast_tree(node):
        """Get a compile python tree of nodes from code"""
        # TODO: Check if astroid get build a similar tree
        code = node.as_string()
        tree = compile(code, '', "exec", ast.PyCF_ONLY_AST)
        return tree

    def _check_too_complex(self, node):
        """Check too complex rating and
        add message if is greather than max_complexity stored from options"""
        tree = self._get_ast_tree(node)
        max_complexity = self.config.max_complexity
        McCabeChecker.max_complexity = max_complexity
        results = McCabeChecker(tree, '').run()
        for _, _, msg, _ in results:
            mccabe_rating = int(msg[msg.index('(') + 1:msg.index(')')])
            self.add_message(
                'too-complex', node=node, confidence=HIGH,
                args=(node.name, mccabe_rating)
            )

    @check_messages('too-complex')
    def visit_functiondef(self, node):
        """visit an astroid.Function node"""
        self._check_too_complex(node)
    visit_asyncfunctiondef = visit_functiondef


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(MethodMcCabeChecker(linter))
