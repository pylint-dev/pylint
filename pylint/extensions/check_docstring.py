from pylint.checkers.base import BaseChecker
from pylint.interfaces import IAstroidChecker, HIGH
from pylint.checkers.utils import check_messages


class _BasicChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = 'basic'


class DocStringAddicChecker(_BasicChecker):
    """Checks format of docstrings based on PEP 0257
    """
    msgs = {
        'C0198': ('Bad docstring quotes in %s, expected """, given %s',
                  'bad-docstring-quotes',
                  'Used when docstring do not have triple double quotes.'),
        'C0199': ('First line empty in %s docstring',
                  'docstring-first-line-empty',
                  'Used when blank line from the beginning of the docstring.'),
        }

    @check_messages('docstring-first-line-empty', 'bad-docstring-quotes')
    def visit_module(self, node):
        self._check_docstring('module', node)

    def visit_classdef(self, node):
        self._check_docstring('class', node)

    def visit_functiondef(self, node):
        ftype = node.is_method() and 'method' or 'function'
        self._check_docstring(ftype, node)

    visit_asyncfunctiondef = visit_functiondef

    def _check_docstring(self, node_type, node):
        docstring = node.doc
        # Docstring First Line Empty
        if docstring and docstring[0] == '\n':
            self.add_message('docstring-first-line-empty', node=node,
                             args=(node_type,), confidence=HIGH)
        # Bad Docstring Quotes
        # I had to use "file_stream" because node.as_string() renders contents
        # of the file and change triple single quotes by triple double quotes
        elif docstring:
            lineno = node.fromlineno
            line = node.root().file_stream.readlines()[lineno].lstrip()
            line = line.decode('utf-8')
            if line and line.find('"""') == 0:
                return
            quotes = line and '\'\'\'' in line and '\'\'\'' or line and \
                line[0] == '"' and '"' or line and line[0] == '\'' and \
                '\'' or False
            if quotes:
                self.add_message('bad-docstring-quotes', node=node,
                                 args=(node_type, quotes), confidence=HIGH)


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(DocStringAddicChecker(linter))
