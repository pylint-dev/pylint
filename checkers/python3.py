# Copyright 2014 Google Inc.
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Check Python 2 code for Python 2/3 source-compatible issues."""
from __future__ import absolute_import

import re
import tokenize

import astroid
from pylint import checkers, interfaces
from pylint.utils import WarningScope
from pylint.checkers import utils


_ZERO = re.compile("^0+$")

def _is_old_octal(literal):
    if _ZERO.match(literal):
        return False
    if re.match('0\d+', literal):
        try:
            int(literal, 8)
        except ValueError:
            return False
        return True

def _check_dict_node(node):
    inferred_types = set()
    try:
        inferred = node.infer()
        for inferred_node in inferred:
            inferred_types.add(inferred_node)
    except (astroid.InferenceError, astroid.UnresolvableName):
        pass
    return (not inferred_types
            or any(isinstance(x, astroid.Dict) for x in inferred_types))


class Python3Checker(checkers.BaseChecker):

    __implements__ = interfaces.IAstroidChecker
    enabled = False
    name = 'python3'

    msgs = {
        # Errors for what will syntactically break in Python 3, warnings for
        # everything else.
        'E1601': ('print statement used',
                  'print-statement',
                  'Used when a print statement is used '
                  '(`print` is a function in Python 3)',
                  {'maxversion': (3, 0)}),
        'E1602': ('Parameter unpacking specified',
                  'parameter-unpacking',
                  'Used when parameter unpacking is specified for a function'
                  "(Python 3 doesn't allow it)",
                  {'maxversion': (3, 0)}),
        'E1603': ('Implicit unpacking of exceptions is not supported '
                  'in Python 3',
                  'unpacking-in-except',
                  'Python3 will not allow implicit unpacking of '
                  'exceptions in except clauses. '
                  'See http://www.python.org/dev/peps/pep-3110/',
                  {'maxversion': (3, 0),
                   'old_names': [('W0712', 'unpacking-in-except')]}),
        'E1604': ('Use raise ErrorClass(args) instead of '
                  'raise ErrorClass, args.',
                  'old-raise-syntax',
                  "Used when the alternate raise syntax "
                  "'raise foo, bar' is used "
                  "instead of 'raise foo(bar)'.",
                  {'maxversion': (3, 0),
                   'old_names': [('W0121', 'old-raise-syntax')]}),
        'E1605': ('Use of the `` operator',
                  'backtick',
                  'Used when the deprecated "``" (backtick) operator is used '
                  'instead  of the str() function.',
                  {'scope': WarningScope.NODE,
                   'maxversion': (3, 0),
                   'old_names': [('W0333', 'backtick')]}),
        'W1601': ('apply built-in referenced',
                  'apply-builtin',
                  'Used when the apply built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1602': ('basestring built-in referenced',
                  'basestring-builtin',
                  'Used when the basestring built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1603': ('buffer built-in referenced',
                  'buffer-builtin',
                  'Used when the buffer built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1604': ('cmp built-in referenced',
                  'cmp-builtin',
                  'Used when the cmp built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1605': ('coerce built-in referenced',
                  'coerce-builtin',
                  'Used when the coerce built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1606': ('execfile built-in referenced',
                  'execfile-builtin',
                  'Used when the execfile built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1607': ('file built-in referenced',
                  'file-builtin',
                  'Used when the file built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1608': ('long built-in referenced',
                  'long-builtin',
                  'Used when the long built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1609': ('raw_input built-in referenced',
                  'raw_input-builtin',
                  'Used when the raw_input built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1610': ('reduce built-in referenced',
                  'reduce-builtin',
                  'Used when the reduce built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1611': ('StandardError built-in referenced',
                  'standarderror-builtin',
                  'Used when the StandardError built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1612': ('unicode built-in referenced',
                  'unicode-builtin',
                  'Used when the unicode built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1613': ('xrange built-in referenced',
                  'xrange-builtin',
                  'Used when the xrange built-in function is referenced '
                  '(missing from Python 3)',
                  {'maxversion': (3, 0)}),
        'W1614': ('__coerce__ method defined',
                  'coerce-method',
                  'Used when a __coerce__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1615': ('__delslice__ method defined',
                  'delslice-method',
                  'Used when a __delslice__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1616': ('__getslice__ method defined',
                  'getslice-method',
                  'Used when a __getslice__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1617': ('__setslice__ method defined',
                  'setslice-method',
                  'Used when a __setslice__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1618': ('import missing `from __future__ import absolute_import`',
                  'no-absolute-import',
                  'Used when an import is not accompanied by '
                  '`from __future__ import absolute_import`'
                  ' (default behaviour in Python 3)',
                  {'maxversion': (3, 0)}),
        'W1619': ('division w/o __future__ statement',
                  'old-division',
                  'Used for non-floor division w/o a float literal or '
                  '``from __future__ import division``'
                  '(Python 3 returns a float for int division unconditionally)',
                  {'maxversion': (3, 0)}),
        'W1620': ('Calling a dict.iter*() method',
                  'dict-iter-method',
                  'Used for calls to dict.iterkeys(), itervalues() or iteritems() '
                  '(Python 3 lacks these methods)',
                  {'maxversion': (3, 0)}),
        'W1621': ('Calling a dict.view*() method',
                  'dict-view-method',
                  'Used for calls to dict.viewkeys(), viewvalues() or viewitems() '
                  '(Python 3 lacks these methods)',
                  {'maxversion': (3, 0)}),
        'W1622': ('Called a next() method on an object',
                  'next-method-called',
                  "Used when an object's next() method is called "
                  '(Python 3 uses the next() built-in function)',
                  {'maxversion': (3, 0)}),
        'W1623': ("Assigning to a class' __metaclass__ attribute",
                  'metaclass-assignment',
                  "Used when a metaclass is specified by assigning to __metaclass__ "
                  '(Python 3 specifies the metaclass as a class statement argument)',
                  {'maxversion': (3, 0)}),
        'W1624': ('Indexing exceptions will not work on Python 3',
                  'indexing-exception',
                  'Indexing exceptions will not work on Python 3. Use '
                  '`exception.args[index]` instead.',
                  {'maxversion': (3, 0),
                   'old_names': [('W0713', 'indexing-exception')]}),
        'W1625': ('Raising a string exception',
                  'raising-string',
                  'Used when a string exception is raised. This will not '
                  'work on Python 3.',
                  {'maxversion': (3, 0),
                   'old_names': [('W0701', 'raising-string')]}),
        'W1626': ('reload built-in referenced',
                  'reload-builtin',
                  'Used when the reload built-in function is referenced '
                  '(missing from Python 3). You can use instead imp.reload '
                  'or importlib.reload.',
                  {'maxversion': (3, 0)}),
        'W1627': ('__oct__ method defined',
                  'oct-method',
                  'Used when a __oct__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1628': ('__hex__ method defined',
                  'hex-method',
                  'Used when a __hex__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1629': ('__nonzero__ method defined',
                  'nonzero-method',
                  'Used when a __nonzero__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1630': ('__cmp__ method defined',
                  'cmp-method',
                  'Used when a __cmp__ method is defined '
                  '(method is not used by Python 3)',
                  {'maxversion': (3, 0)}),
        'W1631': ('map is used as implicitly evaluated call',
                  'implicit-map-evaluation',
                  'Used when the map builtin is used as implicitly '
                  'evaluated call, as in "map(func, args)" on a single line. '
                  'This behaviour will not work in Python 3, where '
                  'map is a generator and must be evaluated. '
                  'Prefer a for-loop as alternative.',
                  {'maxversion': (3, 0)}),
        'W1632': ('input built-in referenced',
                  'input-builtin',
                  'Used when the input built-in is referenced '
                  '(backwards-incompatible semantics in Python 3)',
                  {'maxversion': (3, 0)}),
        'W1633': ('round built-in referenced',
                  'round-builtin',
                  'Used when the round built-in is referenced '
                  '(backwards-incompatible semantics in Python 3)',
                  {'maxversion': (3, 0)}),
    }

    _bad_builtins = frozenset([
        'apply',
        'basestring',
        'buffer',
        'cmp',
        'coerce',
        'execfile',
        'file',
        'input',  # Not missing, but incompatible semantics
        'long',
        'raw_input',
        'reduce',
        'round',  # Not missing, but incompatible semantics
        'StandardError',
        'unicode',
        'xrange',
        'reload',
    ])

    _unused_magic_methods = frozenset([
        '__coerce__',
        '__delslice__',
        '__getslice__',
        '__setslice__',
        '__oct__',
        '__hex__',
        '__nonzero__',
        '__cmp__',
    ])

    def __init__(self, *args, **kwargs):
        self._future_division = False
        self._future_absolute_import = False
        super(Python3Checker, self).__init__(*args, **kwargs)

    def visit_function(self, node):
        if node.is_method() and node.name in self._unused_magic_methods:
            method_name = node.name
            if node.name.startswith('__'):
                method_name = node.name[2:-2]
            self.add_message(method_name + '-method', node=node)

    @utils.check_messages('parameter-unpacking')
    def visit_arguments(self, node):
        for arg in node.args:
            if isinstance(arg, astroid.Tuple):
                self.add_message('parameter-unpacking', node=arg)

    @utils.check_messages('implicit-map-evaluation')
    def visit_discard(self, node):
        if (isinstance(node.value, astroid.CallFunc) and
                isinstance(node.value.func, astroid.Name) and
                node.value.func.name == 'map'):
            module = node.value.func.lookup('map')[0]
            if getattr(module, 'name', None) == '__builtin__':
                self.add_message('implicit-map-evaluation', node=node)

    def visit_name(self, node):
        """Detect when a "bad" built-in is referenced."""
        found_node = node.lookup(node.name)[0]
        if getattr(found_node, 'name', None) == '__builtin__':
            if node.name in self._bad_builtins:
                message = node.name.lower() + '-builtin'
                self.add_message(message, node=node)

    @utils.check_messages('print-statement')
    def visit_print(self, node):
        self.add_message('print-statement', node=node)

    @utils.check_messages('no-absolute-import')
    def visit_from(self, node):
        if node.modname == '__future__':
            for name, _ in node.names:
                if name == 'division':
                    self._future_division = True
                elif name == 'absolute_import':
                    self._future_absolute_import = True
        elif not self._future_absolute_import:
            self.add_message('no-absolute-import', node=node)

    @utils.check_messages('no-absolute-import')
    def visit_import(self, node):
        if not self._future_absolute_import:
            self.add_message('no-absolute-import', node=node)

    @utils.check_messages('metaclass-assignment')
    def visit_class(self, node):
        if '__metaclass__' in node.locals:
            self.add_message('metaclass-assignment', node=node)

    @utils.check_messages('old-division')
    def visit_binop(self, node):
        if not self._future_division and node.op == '/':
            for arg in (node.left, node.right):
                if isinstance(arg, astroid.Const) and isinstance(arg.value, float):
                    break
            else:
                self.add_message('old-division', node=node)

    @utils.check_messages('next-method-called',
                          'dict-iter-method',
                          'dict-view-method')
    def visit_callfunc(self, node):
        if not isinstance(node.func, astroid.Getattr):
            return
        if any([node.args, node.starargs, node.kwargs]):
            return
        if node.func.attrname == 'next':
            self.add_message('next-method-called', node=node)
        else:
            if _check_dict_node(node.func.expr):
                if node.func.attrname in ('iterkeys', 'itervalues', 'iteritems'):
                    self.add_message('dict-iter-method', node=node)
                elif node.func.attrname in ('viewkeys', 'viewvalues', 'viewitems'):
                    self.add_message('dict-view-method', node=node)

    @utils.check_messages('indexing-exception')
    def visit_subscript(self, node):
        """ Look for indexing exceptions. """
        try:
            for infered in node.value.infer():
                if not isinstance(infered, astroid.Instance):
                    continue
                if utils.inherit_from_std_ex(infered):
                    self.add_message('indexing-exception', node=node)
        except astroid.InferenceError:
            return

    @utils.check_messages('unpacking-in-except')
    def visit_excepthandler(self, node):
        """Visit an except handler block and check for exception unpacking."""
        if isinstance(node.name, (astroid.Tuple, astroid.List)):
            self.add_message('unpacking-in-except', node=node)

    @utils.check_messages('backtick')
    def visit_backquote(self, node):
        self.add_message('backtick', node=node)

    @utils.check_messages('raising-string', 'old-raise-syntax')
    def visit_raise(self, node):
        """Visit a raise statement and check for raising
        strings or old-raise-syntax.
        """
        if (node.exc is not None and
                node.inst is not None and
                node.tback is None):
            self.add_message('old-raise-syntax', node=node)

        # Ignore empty raise.
        if node.exc is None:
            return
        expr = node.exc
        if self._check_raise_value(node, expr):
            return
        else:
            try:
                value = next(astroid.unpack_infer(expr))
            except astroid.InferenceError:
                return
            self._check_raise_value(node, value)

    def _check_raise_value(self, node, expr):
        if isinstance(expr, astroid.Const):
            value = expr.value
            if isinstance(value, str):
                self.add_message('raising-string', node=node)
                return True


class Python3TokenChecker(checkers.BaseTokenChecker):
    __implements__ = interfaces.ITokenChecker
    name = 'python3'
    enabled = False

    msgs = {
        'E1606': ('Use of long suffix',
                  'long-suffix',
                  'Used when "l" or "L" is used to mark a long integer. '
                  'This will not work in Python 3, since `int` and `long` '
                  'types have merged.',
                  {'maxversion': (3, 0)}),
        'E1607': ('Use of the <> operator',
                  'old-ne-operator',
                  'Used when the deprecated "<>" operator is used instead '
                  'of "!=". This is removed in Python 3.',
                  {'maxversion': (3, 0),
                   'old_names': [('W0331', 'old-ne-operator')]}),
        'E1608': ('Use of old octal literal',
                  'old-octal-literal',
                  'Usen when encountering the old octal syntax, '
                  'removed in Python 3. To use the new syntax, '
                  'prepend 0o on the number.',
                  {'maxversion': (3, 0)}),
    }

    def process_tokens(self, tokens):
        for idx, (tok_type, token, start, _, _) in enumerate(tokens):
            if tok_type == tokenize.NUMBER:
                if token.lower().endswith('l'):
                    # This has a different semantic than lowercase-l-suffix.
                    self.add_message('long-suffix', line=start[0])
                elif _is_old_octal(token):
                    self.add_message('old-octal-literal', line=start[0])
            if tokens[idx][1] == '<>':
                self.add_message('old-ne-operator', line=tokens[idx][2][0])


def register(linter):
    linter.register_checker(Python3Checker(linter))
    linter.register_checker(Python3TokenChecker(linter))
