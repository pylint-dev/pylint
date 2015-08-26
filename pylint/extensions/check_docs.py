"""Pylint plugin for parameter documentation checking in Sphinx, Google or
Numpy style docstrings
"""
from __future__ import print_function, division, absolute_import

import re

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import node_frame_class


def space_indentation(s):
    """The number of leading spaces in a string

    :param str s: input string

    :rtype: int
    :return: number of leading spaces
    """
    return len(s) - len(s.lstrip(' '))


class ParamDocChecker(BaseChecker):
    """Checker for parameter documentation in Sphinx, Google or Numpy style
    docstrings

    * Check that all function, method and constructor parameters are mentioned
      in the params and types part of the docstring. By convention,
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

    name = 'param_checks'
    msgs = {
        'W9003': ('"%s" missing or differing in parameter documentation',
                  'missing-param-doc',
                  'Please add parameter declarations for all parameters.'),
        'W9004': ('"%s" missing or differing in parameter type documentation',
                  'missing-type-doc',
                  'Please add parameter type declarations for all parameters.'),
    }

    options = (('accept-no-param-doc',
                {'default': True, 'type' : 'yn', 'metavar' : '<y or n>',
                 'help': 'Whether to accept totally missing parameter '
                         'documentation in a docstring of a function that has '
                         'parameters'
                }),
              )

    priority = -2

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)

    constructor_names = set(["__init__", "__new__"])

    def visit_functiondef(self, node):
        """Called for function and method definitions (def).

        :param node: Node for a function or method definition in the AST
        :type node: :class:`astroid.scoped_nodes.Function`
        """
        if node.name in self.constructor_names:
            class_node = node_frame_class(node)
            if class_node is not None:
                self.check_arguments_in_docstring(
                    class_node.doc, node.args, class_node)
                return
        self.check_arguments_in_docstring(node.doc, node.args, node)

    re_for_parameters_see = re.compile(r"""
        For\s+the\s+(other)?\s*parameters\s*,\s+see
        """, re.X | re.S)

    re_sphinx_param_in_docstring = re.compile(r"""
        :param                  # Sphinx keyword
        \s+                     # whitespace

        (?:                     # optional type declaration
        (\w+)
        \s+
        )?

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

    re_google_param_section = re.compile(r"""
        ^([ ]*)   Args \s*:   \s*?$   # Google parameter header
        (  .* )                       # section
        """, re.X | re.S | re.M)

    re_google_param_line = re.compile(r"""
        \s*  (\w+)                    # identifier
        \s*  ( [(] .*? [)] )? \s* :   # optional type declaration
        \s*  ( \w+ )?                 # beginning of optional description
    """, re.X)

    re_numpy_param_section = re.compile(r"""
        ^([ ]*)   Parameters   \s*?$   # Numpy parameters header
        \s*     [-=]+   \s*?$          # underline
        (  .* )                        # section
    """, re.X | re.S | re.M)

    re_numpy_param_line = re.compile(r"""
        \s*  (\w+)                    # identifier
        \s*  :                        
        \s*  ( \w+ )?                 # optional type declaration
    """, re.X)

    not_needed_param_in_docstring = set(['self', 'cls'])

    def check_arguments_in_docstring(self, doc, arguments_node, warning_node):
        """Check that all parameters in a function, method or class constructor
        on the one hand and the parameters mentioned in the parameter
        documentation (e.g. the Sphinx tags 'param' and 'type') on the other
        hand are consistent with each other.

        * Undocumented parameters except 'self' are noticed.
        * Undocumented parameter types except for 'self' and the ``*<args>``
          and ``**<kwargs>`` parameters are noticed.
        * Parameters mentioned in the parameter documentation that don't or no
          longer exist in the function parameter list are noticed.
        * If the text "For the parameters, see" or "For the other parameters,
          see" (ignoring additional whitespace) is mentioned in the docstring,
          missing parameter documentation is tolerated.
        * If there's no Sphinx style, Google style or NumPy style parameter
          documentation at all, i.e. ``:param`` is never mentioned etc., the
          checker assumes that the parameters are documented in another format
          and the absence is tolerated.

        :param doc: Docstring for the function, method or class.
        :type doc: str

        :param arguments_node: Arguments node for the function, method or
            class constructor.
        :type arguments_node: :class:`astroid.scoped_nodes.Arguments`

        :param warning_node: The node to assign the warnings to
        :type warning_node: :class:`astroid.scoped_nodes.Node`
        """
        # Tolerate missing param or type declarations if there is a link to
        # another method carrying the same name.
        if doc is None:
            return

        doc = doc.expandtabs()

        tolerate_missing_params = self.re_for_parameters_see.search(doc) is not None

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

        params_with_doc, params_with_type = self.match_param_docs(doc)

        # Tolerate no parameter documentation at all.
        if (not params_with_doc and not params_with_type
                and self.config.accept_no_param_doc):
            tolerate_missing_params = True

        def _compare_args(found_argument_names, message_id, not_needed_names):
            """Compare the found argument names with the expected ones and
            generate a message if there are inconsistencies.

            :param list found_argument_names: argument names found in the
                docstring

            :param str message_id: pylint message id

            :param not_needed_names: names that may be omitted
            :type not_needed_names: set of str
            """
            if not tolerate_missing_params:
                missing_or_differing_argument_names = (
                    (set(expected_argument_names) ^ set(found_argument_names))
                    - not_needed_names)
            else:
                missing_or_differing_argument_names = (
                    (set(found_argument_names) - set(expected_argument_names))
                    - not_needed_names)

            if missing_or_differing_argument_names:
                self.add_message(
                    message_id,
                    args=(', '.join(
                        sorted(missing_or_differing_argument_names)),),
                    node=warning_node)

        _compare_args(params_with_doc, 'missing-param-doc',
                      self.not_needed_param_in_docstring)
        _compare_args(params_with_type, 'missing-type-doc',
                      not_needed_type_in_docstring)

    def match_param_docs(self, doc):
        """Match parameter documentation in docstrings written in Sphinx, Google
        or NumPy style

        :param str doc: docstring

        :return: tuple of lists of str: params_with_doc, params_with_type
        """
        params_with_doc = []
        params_with_type = []

        if self.re_sphinx_param_in_docstring.search(doc) is not None:
            # Sphinx param declarations
            for match in re.finditer(self.re_sphinx_param_in_docstring, doc):
                name = match.group(2)
                params_with_doc.append(name)
                if match.group(1) is not None:
                    params_with_type.append(name)

            # Sphinx type declarations
            params_with_type += re.findall(
                self.re_sphinx_type_in_docstring, doc)
        else:
            match = self.re_google_param_section.search(doc)
            if match is not None:
                is_google = True
                re_line = self.re_google_param_line
            else:
                match = self.re_numpy_param_section.search(doc)
                if match is not None:
                    is_google = False
                    re_line = self.re_numpy_param_line
                else:
                    # some other documentation style
                    return [], []

            min_indentation = len(match.group(1))
            if is_google:
                min_indentation += 1

            prev_param_name = None
            is_first = True
            for line in match.group(2).splitlines():
                if not line.strip():
                    continue
                indentation = space_indentation(line)
                if indentation < min_indentation:
                    break

                # The first line after the header defines the minimum
                # indentation.
                if is_first:
                    min_indentation = indentation
                    is_first = False

                if indentation > min_indentation:
                    # Lines with more than minimum indentation must contain a
                    # description.
                    if (not params_with_doc
                            or params_with_doc[-1] != prev_param_name):
                        assert prev_param_name is not None
                        params_with_doc.append(prev_param_name)
                else:
                    # Lines with minimum indentation must contain the beginning
                    # of a new parameter documentation.
                    match = re_line.match(line)
                    if match is None:
                        break
                    prev_param_name = match.group(1)
                    if match.group(2) is not None:
                        params_with_type.append(prev_param_name)

                    if is_google and match.group(3) is not None:
                        params_with_doc.append(prev_param_name)

        return params_with_doc, params_with_type


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(ParamDocChecker(linter))
