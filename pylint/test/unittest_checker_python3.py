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

import astroid
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
            'intern',
            'long',
            'raw_input',
            'round',
            'reduce',
            'StandardError',
            'unichr',
            'unicode',
            'xrange',
            'reload',
        ]
        for builtin in builtins:
            self.check_bad_builtin(builtin)

    def as_iterable_in_for_loop_test(self, fxn):
        code = "for x in {}(): pass".format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_used_by_iterable_in_for_loop_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = test_utils.extract_node("""
        for x in (whatever(
            {}() #@
        )):
            pass
        """.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_iterable_in_genexp_test(self, fxn):
        code = "x = (x for x in {}())".format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_listcomp_test(self, fxn):
        code = "x = [x for x in {}(None, [1])]".format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_used_in_variant_in_genexp_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = test_utils.extract_node("""
        list(
            __({}(x))
            for x in [1]
        )
        """.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_used_in_variant_in_listcomp_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = test_utils.extract_node("""
        [
            __({}(None, x))
        for x in [[1]]]
        """.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_argument_to_callable_constructor_test(self, fxn, callable_fn):
        module = astroid.parse("x = {}({}())".format(callable_fn, fxn))
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_random_fxn_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = test_utils.extract_node("""
        y(
            {}() #@
        )
        """.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_argument_to_str_join_test(self, fxn):
        code = "x = ''.join({}())".format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_unpacking(self, fxn):
        node = test_utils.extract_node("""
        a, b = __({}())
        """.format(fxn))
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def as_assignment(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = test_utils.extract_node("""
        a = __({}())
        """.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def iterating_context_tests(self, fxn):
        """Helper for verifying a function isn't used as an iterator."""
        self.as_iterable_in_for_loop_test(fxn)
        self.as_used_by_iterable_in_for_loop_test(fxn)
        self.as_iterable_in_genexp_test(fxn)
        self.as_iterable_in_listcomp_test(fxn)
        self.as_used_in_variant_in_genexp_test(fxn)
        self.as_used_in_variant_in_listcomp_test(fxn)
        self.as_argument_to_random_fxn_test(fxn)
        self.as_argument_to_str_join_test(fxn)
        self.as_iterable_in_unpacking(fxn)
        self.as_assignment(fxn)

        for func in ('iter', 'list', 'tuple', 'sorted',
                     'set', 'sum', 'any', 'all',
                     'enumerate', 'dict'):
            self.as_argument_to_callable_constructor_test(fxn, func)

    @python2_only
    def test_map_in_iterating_context(self):
        self.iterating_context_tests('map')

    @python2_only
    def test_zip_in_iterating_context(self):
        self.iterating_context_tests('zip')

    @python2_only
    def test_range_in_iterating_context(self):
        self.iterating_context_tests('range')

    @python2_only
    def test_filter_in_iterating_context(self):
        self.iterating_context_tests('filter')

    def defined_method_test(self, method, warning):
        """Helper for verifying that a certain method is not defined."""
        node = test_utils.extract_node("""
            class Foo(object):
                def __{0}__(self, other):  #@
                    pass""".format(method))
        message = testutils.Message(warning, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)

    def test_delslice_method(self):
        self.defined_method_test('delslice', 'delslice-method')

    def test_getslice_method(self):
        self.defined_method_test('getslice', 'getslice-method')

    def test_setslice_method(self):
        self.defined_method_test('setslice', 'setslice-method')

    def test_coerce_method(self):
        self.defined_method_test('coerce', 'coerce-method')

    def test_oct_method(self):
        self.defined_method_test('oct', 'oct-method')

    def test_hex_method(self):
        self.defined_method_test('hex', 'hex-method')

    def test_nonzero_method(self):
        self.defined_method_test('nonzero', 'nonzero-method')

    def test_cmp_method(self):
        self.defined_method_test('cmp', 'cmp-method')

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
            self.checker.visit_repr(node)

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
        module_import = astroid.parse(
                'from __future__ import absolute_import; import os')
        module_from = astroid.parse(
                'from __future__ import absolute_import; from os import path')
        with self.assertNoMessages():
            for module in (module_import, module_from):
                self.walk(module)

    def test_import_star_module_level(self):
        node = test_utils.extract_node('''
        def test():
            from lala import * #@
        ''')
        absolute = testutils.Message('no-absolute-import', node=node)
        star = testutils.Message('import-star-module-level', node=node)
        with self.assertAddsMessages(absolute, star):
            self.checker.visit_importfrom(node)

    def test_division(self):
        node = test_utils.extract_node('3 / 2  #@')
        message = testutils.Message('old-division', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_binop(node)

    def test_division_with_future_statement(self):
        module = astroid.parse('from __future__ import division; 3 / 2')
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
                self.checker.visit_call(node)

    def test_dict_iter_method_on_dict(self):
        node = test_utils.extract_node('{}.iterkeys()')
        message = testutils.Message('dict-iter-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_dict_not_iter_method(self):
        arg_node = test_utils.extract_node('x.iterkeys(x)  #@')
        stararg_node = test_utils.extract_node('x.iterkeys(*x)  #@')
        kwarg_node = test_utils.extract_node('x.iterkeys(y=x)  #@')
        non_dict_node = test_utils.extract_node('x=[]\nx.iterkeys() #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node, non_dict_node):
                self.checker.visit_call(node)

    def test_dict_view_method(self):
        for meth in ('keys', 'values', 'items'):
            node = test_utils.extract_node('x.view%s()  #@' % meth)
            message = testutils.Message('dict-view-method', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_dict_view_method_on_dict(self):
        node = test_utils.extract_node('{}.viewkeys()')
        message = testutils.Message('dict-view-method', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_dict_not_view_method(self):
        arg_node = test_utils.extract_node('x.viewkeys(x)  #@')
        stararg_node = test_utils.extract_node('x.viewkeys(*x)  #@')
        kwarg_node = test_utils.extract_node('x.viewkeys(y=x)  #@')
        non_dict_node = test_utils.extract_node('x=[]\nx.viewkeys() #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node, non_dict_node):
                self.checker.visit_call(node)

    def test_next_method(self):
        node = test_utils.extract_node('x.next()  #@')
        message = testutils.Message('next-method-called', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_not_next_method(self):
        arg_node = test_utils.extract_node('x.next(x)  #@')
        stararg_node = test_utils.extract_node('x.next(*x)  #@')
        kwarg_node = test_utils.extract_node('x.next(y=x)  #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node):
                self.checker.visit_call(node)

    def test_metaclass_assignment(self):
        node = test_utils.extract_node("""
            class Foo(object):  #@
                __metaclass__ = type""")
        message = testutils.Message('metaclass-assignment', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(node)

    def test_metaclass_global_assignment(self):
        module = astroid.parse('__metaclass__ = type')
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
        node = astroid.parse(textwrap.dedent("""
        abc = 1l
        raise Exception, "test"
        raise "test"
        `abc`
        """))
        with self.assertNoMessages():
            self.walk(node)

    def test_using_cmp_argument(self):
        nodes = test_utils.extract_node("""
        [].sort(cmp=lambda x: x) #@
        a = list(range(x))
        a.sort(cmp=lambda x: x) #@

        sorted([], cmp=lambda x: x) #@
        """)
        for node in nodes:
            message = testutils.Message('using-cmp-argument', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)


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
