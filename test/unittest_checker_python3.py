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
"""Tests for the python3 checkers."""
from __future__ import absolute_import

import sys
import unittest
import textwrap

from astroid import test_utils

from pylint import testutils
from pylint.checkers import python3 as checker


def python2_only(test):
    """Decorator for any tests that will fail under Python 3."""
    return unittest.skipIf(sys.version_info[0] > 2, 'Python 2 only')(test)

# TODO(cpopa): Port these to the functional test framework instead.

class Python3CheckerTest(testutils.CheckerTestCase):
    CHECKER_CLASS = checker.Python3Checker

    def check_bad_builtin(self, builtin_name):
        node = test_utils.extract_node(builtin_name + '  #@')
        message = builtin_name.lower() + '-builtin'
        with self.assertAddsMessages(testutils.Message(message, node=node)):
            self.checker.visit_name(node)

    @python2_only
    def test_bad_builtins(self):
        builtins = [
            'apply',
            'buffer',
            'cmp',
            'coerce',
            'execfile',
            'file',
            'input',
            'long',
            'raw_input',
            'round',
            'reduce',
            'StandardError',
            'unicode',
            'xrange',
            'reload',
        ]
        for builtin in builtins:
            self.check_bad_builtin(builtin)

    def _test_defined_method(self, method, warning):
        node = test_utils.extract_node("""
            class Foo(object):
                def __{0}__(self, other):  #@
                    pass""".format(method))
        message = testutils.Message(warning, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_function(node)

    def test_delslice_method(self):
        self._test_defined_method('delslice', 'delslice-method')

    def test_getslice_method(self):
        self._test_defined_method('getslice', 'getslice-method')

    def test_setslice_method(self):
        self._test_defined_method('setslice', 'setslice-method')

    def test_coerce_method(self):
        self._test_defined_method('coerce', 'coerce-method')

    def test_oct_method(self):
        self._test_defined_method('oct', 'oct-method')

    def test_hex_method(self):
        self._test_defined_method('hex', 'hex-method')

    def test_nonzero_method(self):
        self._test_defined_method('nonzero', 'nonzero-method')

    def test_cmp_method(self):
        self._test_defined_method('cmp', 'cmp-method')

    @python2_only
    def test_print_statement(self):
        node = test_utils.extract_node('print "Hello, World!" #@')
        message = testutils.Message('print-statement', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_print(node)

    @python2_only
    def test_backtick(self):
        node = test_utils.extract_node('`test`')
        message = testutils.Message('backtick', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_backquote(node)

    def test_relative_import(self):
        node = test_utils.extract_node('import string  #@')
        message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_import(node)

    def test_relative_from_import(self):
        node = test_utils.extract_node('from os import path  #@')
        message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_import(node)

    def test_absolute_import(self):
        module_import = test_utils.build_module(
                'from __future__ import absolute_import; import os')
        module_from = test_utils.build_module(
                'from __future__ import absolute_import; from os import path')
        with self.assertNoMessages():
            for module in (module_import, module_from):
                self.walk(module)

    def test_division(self):
        node = test_utils.extract_node('3 / 2  #@')
        message = testutils.Message('old-division', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_binop(node)

    def test_division_with_future_statement(self):
        module = test_utils.build_module('from __future__ import division; 3 / 2')
        with self.assertNoMessages():
            self.walk(module)

    def test_floor_division(self):
        node = test_utils.extract_node(' 3 // 2  #@')
        with self.assertNoMessages():
            self.checker.visit_binop(node)

    def test_division_by_float(self):
        left_node = test_utils.extract_node('3.0 / 2 #@')
        right_node = test_utils.extract_node(' 3 / 2.0  #@')
        with self.assertNoMessages():
            for node in (left_node, right_node):
                self.checker.visit_binop(node)

    def test_dict_iter_method(self):
        for meth in ('keys', 'values', 'items'):
            node = test_utils.extract_node('x.iter%s()  #@' % meth)
            message = testutils.Message('dict-iter-method', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_callfunc(node)

    def test_dict_iter_method_on_dict(self):
        node = test_utils.extract_node('{}.iterkeys()')
        message = testutils.Message('dict-iter-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_callfunc(node)

    def test_dict_not_iter_method(self):
        arg_node = test_utils.extract_node('x.iterkeys(x)  #@')
        stararg_node = test_utils.extract_node('x.iterkeys(*x)  #@')
        kwarg_node = test_utils.extract_node('x.iterkeys(y=x)  #@')
        non_dict_node = test_utils.extract_node('x=[]\nx.iterkeys() #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node, non_dict_node):
                self.checker.visit_callfunc(node)

    def test_dict_view_method(self):
        for meth in ('keys', 'values', 'items'):
            node = test_utils.extract_node('x.view%s()  #@' % meth)
            message = testutils.Message('dict-view-method', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_callfunc(node)

    def test_dict_view_method_on_dict(self):
        node = test_utils.extract_node('{}.viewkeys()')
        message = testutils.Message('dict-view-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_callfunc(node)

    def test_dict_not_view_method(self):
        arg_node = test_utils.extract_node('x.viewkeys(x)  #@')
        stararg_node = test_utils.extract_node('x.viewkeys(*x)  #@')
        kwarg_node = test_utils.extract_node('x.viewkeys(y=x)  #@')
        non_dict_node = test_utils.extract_node('x=[]\nx.viewkeys() #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node, non_dict_node):
                self.checker.visit_callfunc(node)

    def test_next_method(self):
        node = test_utils.extract_node('x.next()  #@')
        message = testutils.Message('next-method-called', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_callfunc(node)

    @python2_only
    def test_implicit_map_evaluation(self):
        node = test_utils.extract_node('map(str, [1, 2, 3])')
        discard = node.parent
        message = testutils.Message('implicit-map-evaluation', node=discard)
        with self.assertAddsMessages(message):
            # Use node.parent because extract_node returns the value
            # of a discard node, not the discard itself.
            self.checker.visit_discard(discard)

    def test_not_next_method(self):
        arg_node = test_utils.extract_node('x.next(x)  #@')
        stararg_node = test_utils.extract_node('x.next(*x)  #@')
        kwarg_node = test_utils.extract_node('x.next(y=x)  #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node):
                self.checker.visit_callfunc(node)

    def test_metaclass_assignment(self):
        node = test_utils.extract_node("""
            class Foo(object):  #@
                __metaclass__ = type""")
        message = testutils.Message('metaclass-assignment', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_class(node)

    def test_metaclass_global_assignment(self):
        module = test_utils.build_module('__metaclass__ = type')
        with self.assertNoMessages():
            self.walk(module)

    @python2_only
    def test_parameter_unpacking(self):
        node = test_utils.extract_node('def func((a, b)):#@\n pass')
        arg = node.args.args[0]
        with self.assertAddsMessages(testutils.Message('parameter-unpacking', node=arg)):
            self.checker.visit_arguments(node.args)

    @python2_only
    def test_old_raise_syntax(self):
        node = test_utils.extract_node('raise Exception, "test"')
        message = testutils.Message('old-raise-syntax', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    @python2_only
    def test_raising_string(self):
        node = test_utils.extract_node('raise "Test"')
        message = testutils.Message('raising-string', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    @python2_only
    def test_checker_disabled_by_default(self):
        node = test_utils.build_module(textwrap.dedent("""
        abc = 1l
        raise Exception, "test"
        raise "test"
        `abc`
        """))
        with self.assertNoMessages():
            self.walk(node)


@python2_only
class Python3TokenCheckerTest(testutils.CheckerTestCase):

    CHECKER_CLASS = checker.Python3TokenChecker

    def _test_token_message(self, code, symbolic_message):
        tokens = testutils.tokenize_str(code)
        message = testutils.Message(symbolic_message, line=1)
        with self.assertAddsMessages(message):
            self.checker.process_tokens(tokens)

    def test_long_suffix(self):
        for code in ("1l", "1L"):
            self._test_token_message(code, 'long-suffix')

    def test_old_ne_operator(self):
        self._test_token_message("1 <> 2", "old-ne-operator")

    def test_old_octal_literal(self):
        for octal in ("045", "055", "075", "077", "076543"):
            self._test_token_message(octal, "old-octal-literal")

        # Make sure we are catching only octals.
        for non_octal in ("45", "00", "085", "08", "1"):
            tokens = testutils.tokenize_str(non_octal)
            with self.assertNoMessages():
                self.checker.process_tokens(tokens)


if __name__ == '__main__':
    unittest.main()
