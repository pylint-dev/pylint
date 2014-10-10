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

from pylint import checkers, interfaces
from pylint.checkers import utils


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
                  {'maxversion': (3,0)}),
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

    def visit_function(self, node):
        if node.is_method() and node.name in self._unused_magic_methods:
            method_name = node.name
            if node.name.startswith('__'):
                method_name = node.name[2:-2]
            self.add_message(method_name + '-method', node=node)

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


def register(linter):
    linter.register_checker(Python3Checker(linter))
