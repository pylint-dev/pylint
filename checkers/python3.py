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

import astroid
from pylint import checkers, interfaces
from pylint.checkers import utils

def _check_dict_node(node):
    inferred = node.infer()
    inferred_types = set()
    try:
        for inferred_node in inferred:
            inferred_types.add(inferred_node)
    except (astroid.InferenceError, astroid.UnresolvableName):
        pass
    return (not inferred_types
            or any(isinstance(x, astroid.Dict) for x in inferred_types))


class Python3Checker(checkers.BaseChecker):

    __implements__ = interfaces.IAstroidChecker

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
    }

    _missing_builtins = frozenset([
        'apply',
        'basestring',
        'buffer',
        'cmp',
        'coerce',
        'execfile',
        'file',
        'long',
        'raw_input',
        'reduce',
        'StandardError',
        'unicode',
        'xrange',
    ])

    _unused_magic_methods = frozenset([
        '__coerce__',
        '__delslice__',
        '__getslice__',
        '__setslice__',
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

    def visit_name(self, node):
        """Detect when a built-in that is missing in Python 3 is referenced."""
        found_node = node.lookup(node.name)[0]
        if getattr(found_node, 'name', None) == '__builtin__':
            if node.name in self._missing_builtins:
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


def register(linter):
    linter.register_checker(Python3Checker(linter))
