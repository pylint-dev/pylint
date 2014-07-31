"""Pylint plugin for Sphinx parameter documentation checking
"""
from __future__ import print_function, division

import re

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
import astroid.scoped_nodes


class SphinxDocChecker(BaseChecker):
    """Checker for Sphinx documentation parameters

    * Check that all function, method and constructor parameters are mentioned
      in the Sphinx params and types part of the docstring. By convention,
      constructor parameters are documented in the class docstring.
    * Check that there are no naming inconsistencies between the signature and
      the documentation, i.e. also report documented parameters that are missing
      in the signature. This is important to find cases where parameters are
      renamed only in the code, not in the documentation.

    Activate this checker by adding the line::

        load-plugins=pylint.extensions.check_docs

    to the ``MASTER`` section of your ``.pylintrc``.

    :param linter: linter object
    :type linter: :class:`pylint.lint.PyLinter`
    """
    __implements__ = IAstroidChecker

    name = 'Sphinx doc checks'
    msgs = {
        'W9003': ('"%s" missing or differing in Sphinx params',
                  'missing-sphinx-param',
                  'Please add Sphinx param declarations for all arguments.'),
        'W9004': ('"%s" missing or differing in Sphinx types',
                  'missing-sphinx-type',
                  'Please add Sphinx type declarations for all arguments.'),
    }

    options = ()

    priority = -2

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)

    def visit_function(self, node):
        """Called for function and method definitions (def).

        :param node: Node for a function or method definition in the AST
        :type node: :class:`astroid.scoped_nodes.Function`
        """
        self.check_arguments_mentioned_in_docstring(node, node.doc, node.args)

    re_for_parameters_see = re.compile(r"""
        For\s+the\s+(other)?\s*parameters\s*,\s+see
        """, re.X | re.S)

    re_prefix_of_func_name = re.compile(r"""
        .*                      # part before final dot
        \.                      # final dot
        """, re.X | re.S)

    re_sphinx_param_in_docstring = re.compile(r"""
        :param                  # Sphinx keyword
        \s+                     # whitespace
        (\w+)                   # Parameter name
        \s*                     # whitespace
        :                       # final colon
        """, re.X | re.S)

    re_sphinx_type_in_docstring = re.compile(r"""
        :type                   # Sphinx keyword
        \s+                     # whitespace
        (\w+)                   # Parameter name
        \s*                     # whitespace
        :                       # final colon
        """, re.X | re.S)

    not_needed_param_in_docstring = set(['self', 'cls'])

    def check_arguments_mentioned_in_docstring(self, node, doc, arguments_node):
        """Check that all arguments in a function, method or class constructor
        on the one hand and the arguments mentioned in the Sphinx tags 'param'
        and 'type' on the other hand are consistent with each other.

        * Undocumented parameters except 'self' are noticed.
        * Undocumented parameter types except for 'self' and the ``*<args>``
          and ``**<kwargs>`` parameters are noticed.
        * Parameters mentioned in the Sphinx documentation that don't or no
          longer exist in the function parameter list are noticed.
        * If there is a Sphinx link like ``:meth:...`` or ``:func:...`` to a
          function carrying the same name as the current function, missing
          parameter documentations are tolerated, but the existing parameters
          mentioned in the documentation are checked.

        :param node: Node for a function, method or class definition in the AST.
        :type node: :class:`astroid.scoped_nodes.Function` or
            :class:`astroid.scoped_nodes.Class`

        :param doc: Docstring for the function, method or class.
        :type doc: str

        :param arguments_node: Arguments node for the function, method or
            class constructor.
        :type arguments_node: :class:`astroid.scoped_nodes.Arguments`
        """
        # Tolerate missing param or type declarations if there is a link to
        # another method carrying the same name.
        if node.doc is None:
            return

        tolerate_missing_params = False
        if self.re_for_parameters_see.search(doc) is not None:
            tolerate_missing_params = True

        # Collect the function arguments.
        expected_argument_names = [arg.name for arg in arguments_node.args]
        not_needed_type_in_docstring = (
            self.not_needed_param_in_docstring.copy())

        if arguments_node.vararg is not None:
            expected_argument_names.append(arguments_node.vararg)
            not_needed_type_in_docstring.add(arguments_node.vararg)
        if arguments_node.kwarg is not None:
            expected_argument_names.append(arguments_node.kwarg)
            not_needed_type_in_docstring.add(arguments_node.kwarg)

        # Compare the function arguments with the ones found in the Sphinx
        # docstring.
        for message_id, pattern, not_needed in [
                ('missing-sphinx-param', self.re_sphinx_param_in_docstring,
                 self.not_needed_param_in_docstring),
                ('missing-sphinx-type', self.re_sphinx_type_in_docstring,
                 not_needed_type_in_docstring),
        ]:
            found_argument_names = re.findall(pattern, doc)
            if not tolerate_missing_params:
                missing_or_differing_argument_names = (
                    (set(expected_argument_names) ^ set(found_argument_names))
                    - not_needed)
            else:
                missing_or_differing_argument_names = (
                    (set(found_argument_names) - set(expected_argument_names))
                    - not_needed)

            if missing_or_differing_argument_names:
                self.add_message(
                    message_id,
                    args=(', '.join(
                        sorted(missing_or_differing_argument_names)),),
                    node=node)

    constructor_names = set(["__init__", "__new__"])

    def visit_class(self, node):
        """Called for class definitions.

        :param node: Node for a class definition in the AST
        :type node: :class:`astroid.scoped_nodes.Class`
        """
        for body_item in node.body:
            if (isinstance(body_item, astroid.scoped_nodes.Function)
                    and hasattr(body_item, 'name')):
                if body_item.name in self.constructor_names:
                    self.check_arguments_mentioned_in_docstring(
                        node, node.doc, body_item.args)
                else:
                    self.visit_function(body_item)


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(SphinxDocChecker(linter))
