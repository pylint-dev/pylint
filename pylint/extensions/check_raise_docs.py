"""Pylint plugin for raised exception documentation checking in Sphinx, Google
or Numpy style docstrings
"""
from __future__ import print_function, absolute_import

import re

import astroid
import astroid.node_classes

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import node_ignores_exception
from pylint.extensions.check_docs import ParamDocChecker, space_indentation


def _possible_exc_types(node):
    """
    Gets all of the possible raised exception types for the given raise node.

    .. note::

        Caught exception types are ignored.


    :param node: The raise node to find exception types for.

    :returns: A list of exception types possibly raised by :param:`node`.
    :rtype: list(str)
    """
    excs = []
    if isinstance(node.exc, astroid.Name):
        excs = [node.exc.name]
    elif (isinstance(node.exc, astroid.Call) and
          isinstance(node.exc.func, astroid.Name)):
        excs = [node.exc.func.name]
    elif (node.exc is None and
          isinstance(node.parent, astroid.ExceptHandler)):
        handler = node.parent
        excs = astroid.unpack_infer(handler.type)
        excs = (exc.name for exc in excs)

    excs = [exc for exc in excs if not node_ignores_exception(node, exc)]
    return excs

class RaiseDocChecker(BaseChecker):
    """Checker for raised exception documentation in Sphinx, Google or Numpy
    style docstrings

    * Check that all explicity raised exceptions in a function are documented
    in the function docstring. Caught exceptions are ignored.

    Activate this checker by adding the line::

        load-plugins=pylint.extensions.check_raise_docs

    to the ``MASTER`` section of your ``.pylintrc``.

    :param linter: linter object
    :type linter: :class:`pylint.lint.PyLinter`
    """
    __implements__ = IAstroidChecker

    name = 'raise_checks'
    msgs = {
        'W9010': ('Raising a "%s" is not documented.',
                  'missing-raise-doc',
                  'Please document that this exception type is raised.'),
    }

    options = (('accept-no-raise-doc',
                {'default': True, 'type' : 'yn', 'metavar' : '<y or n>',
                 'help': 'Whether to accept totally missing raises'
                         'documentation in a docstring of a function.'
                }),
              )

    priority = -2

    def __init__(self, linter=None):
        super(RaiseDocChecker, self).__init__(linter)

    re_sphinx_raise_in_docstring = re.compile(r"""
        :raises                  # Sphinx keyword
        \s+                     # whitespace

        (?:                     # type declaration
        (\w+)
        \s+
        )?

        (\w+)                   # Parameter name
        \s*                     # whitespace
        :                       # final colon
        """, re.X | re.S)

    re_google_raise_section = re.compile(r"""
        ^([ ]*)   Raises \s*:   \s*?$ # Google parameter header
        (  .* )                       # section
        """, re.X | re.S | re.M)

    re_google_raise_line = re.compile(r"""
        \s*  (\w+) \s* :              # identifier
        \s*  ( \w+ )?                 # beginning of optional description
    """, re.X)

    re_numpy_raise_section = re.compile(r"""
        ^([ ]*)   Raises   \s*?$       # Numpy parameters header
        \s*     [-=]+   \s*?$          # underline
        (  .* )                        # section
    """, re.X | re.S | re.M)

    re_numpy_raise_line = re.compile(r"""
        \s*  (\w+)                    # type declaration
    """, re.X)

    def visit_raise(self, node):
        func_node = node.frame()
        if not isinstance(func_node, astroid.FunctionDef):
            return

        excs = _possible_exc_types(node)
        if not excs:
            return

        doc = func_node.doc
        if doc is None:
            self._handle_no_doc(excs, func_node)
        elif self.re_sphinx_raise_in_docstring.search(doc) is not None:
            self._check_sphinx_doc(doc, excs, func_node)
        else:
            self._check_other_doc(doc, excs, func_node)

    def _handle_no_doc(self, excs, node):
        if self.config.accept_no_raise_doc:
            return

        self._add_all_messages(excs, node)

    def _check_sphinx_doc(self, doc, excs, node):
        """
        Check a docstring known to be a sphinx docstring for exception types.

        :param doc: The docstring to check.
        :type doc: str

        :param excs: The exception types to search for.
        :type excs: list(str)

        :param node: The node to raise warning on.
        """
        for match in re.finditer(self.re_sphinx_raise_in_docstring, doc):
            raise_type = match.group(2)
            if raise_type in excs:
                excs.remove(raise_type)
                if not excs:
                    return

        self._add_all_messages(excs, node)

    def _check_other_doc(self, doc, excs, node):
        match, is_google, re_line = self._establish_section_type(doc)
        if match is None:
            if self.is_known_doc_type(doc):
                self._add_all_messages(excs, node)
            return

        min_indentation = self._establish_min_section_indentation(
            match,
            is_google)

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

            if indentation == min_indentation:
                # Lines with minimum indentation must contain the beginning
                # of a new parameter documentation.
                match = re_line.match(line)
                if match is None:
                    break

                raise_type = match.group(1)
                if raise_type in excs:
                    excs.remove(raise_type)
                    if not excs:
                        return

        self._add_all_messages(excs, node)

    @staticmethod
    def _establish_section_type(doc):
        """
        Find the section type of the docstring (either google or numpy).

        :param doc: The docstring to establish the type for.
        :type doc: str

        :returns: A tuple of the matched section,
            whether the section type is google or not,
            and the regex to use to search for section lines.
        :rtype: tuple(:py:`re.MatchObject`, bool, :py:`re.RegexObject`)
        """
        if not doc:
            return (None, False, None)

        match = RaiseDocChecker.re_google_raise_section.search(doc)
        is_google = False
        re_line = None

        if match is not None:
            is_google = True
            re_line = RaiseDocChecker.re_google_raise_line
        else:
            match = RaiseDocChecker.re_numpy_raise_section.search(doc)
            if match is not None:
                is_google = False
                re_line = RaiseDocChecker.re_numpy_raise_line

        return (match, is_google, re_line)

    @staticmethod
    def _establish_min_section_indentation(match, is_google):
        """
        Get the minimum indentation level for a line in a section.

        :param match: A section match object.
        :type match: :py:`re.MatchObject`

        :param is_google: Whether the match object is for a google (True)
            or numpy section (False):
        :type is_google: bool

        :returns: The minimum indentation level for a line below the section to
            be counted as part of the section.
        :rtype: int
        """
        min_indentation = len(match.group(1))
        if is_google:
            min_indentation += 1
        return min_indentation

    def _add_all_messages(self, excs, node):
        """
        Adds a message on :param:`node` for each exception type.

        :param excs: A list of missing exception types.
        :type excs: list

        :param node: The node show the messages on.
        """
        for exc in excs:
            self.add_message(
                'missing-raises-doc',
                args=(exc,),
                node=node)

    @staticmethod
    def is_known_doc_type(doc):
        if doc is None:
            return True

        # TODO: Look for returns and other sections
        return bool(ParamDocChecker.re_sphinx_param_in_docstring.search(doc) or
                    ParamDocChecker.re_google_param_section.search(doc) or
                    ParamDocChecker.re_numpy_param_section.search(doc))

def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(RaiseDocChecker(linter))
