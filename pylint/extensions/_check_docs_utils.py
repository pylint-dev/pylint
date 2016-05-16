"""Utility methods for docstring checking."""

from __future__ import absolute_import, print_function

import re

import astroid

from pylint.checkers.utils import node_ignores_exception

def space_indentation(s):
    """The number of leading spaces in a string

    :param str s: input string

    :rtype: int
    :return: number of leading spaces
    """
    return len(s) - len(s.lstrip(' '))


def possible_exc_types(node):
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
    elif node.exc is None:
        handler = node.parent
        while handler and not isinstance(handler, astroid.ExceptHandler):
            handler = handler.parent

        if handler and handler.type:
            inferred = next(handler.type.infer())
            excs = (exc.name for exc in astroid.unpack_infer(inferred))

    excs = set(exc for exc in excs if not node_ignores_exception(node, exc))
    return excs

def docstringify(docstring):
    for docstring_type in [SphinxDocstring, GoogleDocstring, NumpyDocstring]:
        instance = docstring_type(docstring)
        if instance.is_valid():
            return instance

    return Docstring(docstring)

class Docstring(object):
    re_for_parameters_see = re.compile(r"""
        For\s+the\s+(other)?\s*parameters\s*,\s+see
        """, re.X | re.S)

    # These methods are designed to be overridden
    # pylint: disable=no-self-use
    def __init__(self, doc):
        doc = doc or ""
        self.doc = doc.expandtabs()

    def is_valid(self):
        return False

    def exceptions(self):
        return set()

    def has_params(self):
        return False

    def match_param_docs(self):
        return set(), set()

    def params_documented_elsewhere(self):
        return self.re_for_parameters_see.search(self.doc) is not None

class SphinxDocstring(Docstring):
    re_param_in_docstring = re.compile(r"""
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

    re_type_in_docstring = re.compile(r"""
        :type                   # Sphinx keyword
        \s+                     # whitespace
        (\w+)                   # Parameter name
        \s*                     # whitespace
        :                       # final colon
        """, re.X | re.S)

    re_raise_in_docstring = re.compile(r"""
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

    def is_valid(self):
        return bool(self.re_param_in_docstring.search(self.doc) or
                    self.re_raise_in_docstring.search(self.doc))

    def exceptions(self):
        types = set()

        for match in re.finditer(self.re_raise_in_docstring, self.doc):
            raise_type = match.group(2)
            types.add(raise_type)

        return types

    def has_params(self):
        if not self.doc:
            return False

        return self.re_param_in_docstring.search(self.doc) is not None

    def match_param_docs(self):
        params_with_doc = set()
        params_with_type = set()

        for match in re.finditer(self.re_param_in_docstring, self.doc):
            name = match.group(2)
            params_with_doc.add(name)
            param_type = match.group(1)
            if param_type is not None:
                params_with_type.add(name)

        params_with_type.update(re.findall(self.re_type_in_docstring, self.doc))
        return params_with_doc, params_with_type


class GoogleDocstring(Docstring):
    _re_section_template = r"""
        ^([ ]*)   {0} \s*:   \s*?$   # Google parameter header
        (  .* )                       # section
        """

    re_param_section = re.compile(
        _re_section_template.format(r"(?:Args|Arguments|Parameters)"),
        re.X | re.S | re.M
    )

    re_param_line = re.compile(r"""
        \s*  (\w+)                    # identifier
        \s*  ( [(] .*? [)] )? \s* :   # optional type declaration
        \s*  ( \w+ )?                 # beginning of optional description
    """, re.X)

    re_raise_section = re.compile(
        _re_section_template.format(r"Raises"),
        re.X | re.S | re.M
    )

    re_raise_line = re.compile(r"""
        \s*  (\w+) \s* :              # identifier
        \s*  ( \w+ )?                 # beginning of optional description
    """, re.X)

    def is_valid(self):
        return bool(self.re_param_section.search(self.doc) or
                    self.re_raise_section.search(self.doc))

    def has_params(self):
        if not self.doc:
            return False

        return self.re_param_section.search(self.doc) is not None

    def exceptions(self):
        types = set()

        section_match = self.re_raise_section.search(self.doc)
        if section_match is None:
            return types

        min_indentation = self.min_section_indent(section_match)

        is_first = True
        for line in section_match.group(2).splitlines():
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
                match = self.re_raise_line.match(line)
                if match is None:
                    break

                raise_type = match.group(1)
                if match.group(2) is not None:
                    types.add(raise_type)

        return types

    def match_param_docs(self):
        params_with_doc = []
        params_with_type = []

        section_match = self.re_param_section.search(self.doc)
        if section_match is None:
            return set(), set()

        min_indentation = self.min_section_indent(section_match)

        prev_param_name = None
        is_first = True
        for line in section_match.group(2).splitlines():
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
                match = self.re_param_line.match(line)
                if match is None:
                    break
                prev_param_name = match.group(1)
                if match.group(2) is not None:
                    params_with_type.append(prev_param_name)

                if match.group(3) is not None:
                    params_with_doc.append(prev_param_name)

        return set(params_with_doc), set(params_with_type)

    @staticmethod
    def min_section_indent(section_match):
        return len(section_match.group(1)) + 1

class NumpyDocstring(GoogleDocstring):
    _re_section_template = r"""
        ^([ ]*)   {0}   \s*?$          # Numpy parameters header
        \s*     [-=]+   \s*?$          # underline
        (  .* )                        # section
    """

    re_param_section = re.compile(
        _re_section_template.format(r"(?:Args|Arguments|Parameters)"),
        re.X | re.S | re.M
    )

    re_param_line = re.compile(r"""
        \s*  (\w+)                    # identifier
        \s*  :                        
        \s*  ( \w+ )?                 # optional type declaration
        ()                            # null group for match_param_docs
    """, re.X)

    re_raise_section = re.compile(
        _re_section_template.format(r"Raises"),
        re.X | re.S | re.M
    )

    re_raise_line = re.compile(r"""
        \s*  (\w+)                    # type declaration
        ()                            # null group for exceptions
    """, re.X)

    @staticmethod
    def min_section_indent(section_match):
        return len(section_match.group(1))
