"""Unittest for our pylint plugin."""
from __future__ import division, print_function

import unittest

from astroid import test_utils
from pylint.testutils import CheckerTestCase, Message, set_config

from pylint.extensions.check_docs import SphinxDocChecker


class SpinxDocCheckerTest(CheckerTestCase):
    """Tests for pylint_plugin.SphinxDocChecker"""
    CHECKER_CLASS = SphinxDocChecker

    def test_missing_func_params_in_docstring(self):
        """Example of a function with missing parameter documentation in the
        docstring
        """
        node = test_utils.extract_node("""
        def function_foo(x, y):
            '''docstring ...

            missing parameter documentation'''
            pass
        """)
        with self.assertAddsMessages(
                Message(
                    msg_id='W9003',
                    node=node,
                    args=('x, y',)),
                Message(
                    msg_id='W9004',
                    node=node,
                    args=('x, y',))):
            self.checker.visit_function(node)

    def test_missing_method_params_in_docstring(self):
        """Example of a class method with missing parameter documentation in the
        docstring
        """
        node = test_utils.extract_node("""
        class Foo(object):
            def method_foo(self, x, y):
                '''docstring ...

                missing parameter documentation'''
                pass
        """)
        method_node = node.body[0]
        with self.assertAddsMessages(
                Message(
                    msg_id='W9003',
                    node=method_node,
                    args=('x, y',)),
                Message(
                    msg_id='W9004',
                    node=method_node,
                    args=('x, y',))):
            self.checker.visit_class(node)

    def test_existing_func_params_in_docstring(self):
        """Example of a function with correctly documented parameters and return
        values
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            :param xarg: bla xarg
            :type xarg: int

            :param yarg: bla yarg
            :type yarg: float

            :return: sum
            :rtype: float
            '''
            return xarg + yarg
        """)
        with self.assertNoMessages():
            self.checker.visit_function(node)

    def test_wrong_name_of_func_params_in_docstring(self):
        """Example of functions with inconsistent parameter names in the
        signature and in the documentation
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            :param xarg1: bla xarg
            :type xarg: int

            :param yarg: bla yarg
            :type yarg1: float
            '''
            return xarg + yarg
        """)
        with self.assertAddsMessages(
                Message(
                    msg_id='W9003',
                    node=node,
                    args=('xarg, xarg1',)),
                Message(
                    msg_id='W9004',
                    node=node,
                    args=('yarg, yarg1',))):
            self.checker.visit_function(node)

        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            :param yarg1: bla yarg
            :type yarg1: float

            For the other parameters, see bla.
            '''
            return xarg + yarg
        """)
        with self.assertAddsMessages(
                Message(
                    msg_id='W9003',
                    node=node,
                    args=('yarg1',)),
                Message(
                    msg_id='W9004',
                    node=node,
                    args=('yarg1',))):
            self.checker.visit_function(node)

    def test_see_sentence_for_func_params_in_docstring(self):
        """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a given
        interface
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            :param yarg: bla yarg
            :type yarg: float

            For the other parameters, see :func:`bla`
            '''
            return xarg + yarg
        """)
        with self.assertNoMessages():
            self.checker.visit_function(node)

    def test_constr_params_in_class(self):
        """Example of a class with missing constructor parameter documentation

        Everything is completely analogous to functions.
        """
        node = test_utils.extract_node("""
        class ClassFoo(object):
            '''docstring foo

            missing constructor parameter documentation'''

            def __init__(self, x, y):
                pass

        """)
        with self.assertAddsMessages(
                Message(
                    msg_id='W9003',
                    node=node,
                    args=('x, y',)),
                Message(
                    msg_id='W9004',
                    node=node,
                    args=('x, y',))):
            self.checker.visit_class(node)


if __name__ == '__main__':
    unittest.main()
