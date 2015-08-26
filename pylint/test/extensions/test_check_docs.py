"""Unit tests for the pylint checkers in :mod:`pylint.extensions.check_docs`,
in particular the parameter documentation checker `ParamDocChecker`
"""
from __future__ import division, print_function, absolute_import

import unittest

import astroid
from astroid import test_utils
from pylint.testutils import CheckerTestCase, Message, set_config

from pylint.extensions.check_docs import ParamDocChecker, space_indentation


class ParamDocCheckerTest(CheckerTestCase):
    """Tests for pylint_plugin.ParamDocChecker"""
    CHECKER_CLASS = ParamDocChecker

    def test_space_indentation(self):
        self.assertEqual(space_indentation('abc'), 0)
        self.assertEqual(space_indentation(''), 0)
        self.assertEqual(space_indentation('  abc'), 2)
        self.assertEqual(space_indentation('\n  abc'), 0)
        self.assertEqual(space_indentation('   \n  abc'), 3)

    def test_missing_func_params_in_sphinx_docstring(self):
        """Example of a function with missing Sphinx parameter documentation in
        the docstring
        """
        node = test_utils.extract_node("""
        def function_foo(x, y, z):
            '''docstring ...

            :param x: bla

            :param int z: bar
            '''
            pass
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('y',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('x, y',))
        ):
            self.checker.visit_functiondef(node)

    def test_missing_func_params_in_google_docstring(self):
        """Example of a function with missing Google style parameter
        documentation in the docstring
        """
        node = test_utils.extract_node("""
        def function_foo(x, y, z):
            '''docstring ...

            Args:
                x: bla
                z (int): bar

            some other stuff
            '''
            pass
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('y',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('x, y',))
        ):
            self.checker.visit_functiondef(node)

    def test_missing_func_params_in_numpy_docstring(self):
        """Example of a function with missing NumPy style parameter
        documentation in the docstring
        """
        node = test_utils.extract_node("""
        def function_foo(x, y, z):
            '''docstring ...

            Parameters
            ----------
            x:
                bla
            z: int
                bar

            some other stuff
            '''
            pass
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('y',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('x, y',))
        ):
            self.checker.visit_functiondef(node)

    def test_tolerate_no_param_documentation_at_all(self):
        """Example of a function with no parameter documentation at all

        No error message is emitted.
        """
        node = test_utils.extract_node("""
        def function_foo(x, y):
            '''docstring ...

            missing parameter documentation'''
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    @set_config(accept_no_param_doc=False)
    def test_don_t_tolerate_no_param_documentation_at_all(self):
        """Example of a function with no parameter documentation at all

        No error message is emitted.
        """
        node = test_utils.extract_node("""
        def function_foo(x, y):
            '''docstring ...

            missing parameter documentation'''
            pass
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('x, y',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('x, y',))
        ):
            self.checker.visit_functiondef(node)

    def _visit_methods_of_class(self, node):
        """Visit all methods of a class node

        :param node: class node
        :type node: :class:`astroid.scoped_nodes.Class`
        """
        for body_item in node.body:
            if (isinstance(body_item, astroid.FunctionDef)
                    and hasattr(body_item, 'name')):
                self.checker.visit_functiondef(body_item)

    def test_missing_method_params_in_sphinx_docstring(self):
        """Example of a class method with missing parameter documentation in
        the Sphinx style docstring
        """
        node = test_utils.extract_node("""
        class Foo(object):
            def method_foo(self, x, y):
                '''docstring ...

                missing parameter documentation

                :param x: bla
                '''
                pass
        """)
        method_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=method_node,
                args=('y',)),
            Message(
                msg_id='missing-type-doc',
                node=method_node,
                args=('x, y',))
        ):
            self._visit_methods_of_class(node)

    def test_missing_method_params_in_google_docstring(self):
        """Example of a class method with missing parameter documentation in
        the Google style docstring
        """
        node = test_utils.extract_node("""
        class Foo(object):
            def method_foo(self, x, y):
                '''docstring ...

                missing parameter documentation

                Args:
                    x: bla
                '''
                pass
        """)
        method_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=method_node,
                args=('y',)),
            Message(
                msg_id='missing-type-doc',
                node=method_node,
                args=('x, y',))
        ):
            self._visit_methods_of_class(node)

    def test_missing_method_params_in_numpy_docstring(self):
        """Example of a class method with missing parameter documentation in
        the Numpy style docstring
        """
        node = test_utils.extract_node("""
        class Foo(object):
            def method_foo(self, x, y):
                '''docstring ...

                missing parameter documentation

                Parameters
                ----------
                x:
                    bla
                '''
                pass
        """)
        method_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=method_node,
                args=('y',)),
            Message(
                msg_id='missing-type-doc',
                node=method_node,
                args=('x, y',))
        ):
            self._visit_methods_of_class(node)

    def test_existing_func_params_in_sphinx_docstring(self):
        """Example of a function with correctly documented parameters and
        return values (Sphinx style)
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg, zarg):
            '''function foo ...

            :param xarg: bla xarg
            :type xarg: int

            :param yarg: bla yarg
            :type yarg: float

            :param int zarg: bla zarg

            :return: sum
            :rtype: float
            '''
            return xarg + yarg
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_existing_func_params_in_google_docstring(self):
        """Example of a function with correctly documented parameters and
        return values (Google style)
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg, zarg):
            '''function foo ...

            Args:
                xarg (int): bla xarg
                yarg (float): bla
                    bla yarg
        
                zarg (int): bla zarg

            Returns:
                float: sum
            '''
            return xarg + yarg
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_existing_func_params_in_numpy_docstring(self):
        """Example of a function with correctly documented parameters and
        return values (Numpy style)
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg, zarg):
            '''function foo ...

            Parameters
            ----------
            xarg: int
                bla xarg
            yarg: float
                bla yarg

            zarg: int
                bla zarg

            Returns
            -------
            float
                sum
            '''
            return xarg + yarg
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_wrong_name_of_func_params_in_sphinx_docstring(self):
        """Example of functions with inconsistent parameter names in the
        signature and in the Sphinx style documentation
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg, zarg):
            '''function foo ...

            :param xarg1: bla xarg
            :type xarg: int

            :param yarg: bla yarg
            :type yarg1: float

            :param str zarg1: bla zarg
            '''
            return xarg + yarg
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('xarg, xarg1, zarg, zarg1',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('yarg, yarg1, zarg, zarg1',)),
        ):
            self.checker.visit_functiondef(node)

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
                msg_id='missing-param-doc',
                node=node,
                args=('yarg1',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('yarg1',))
        ):
            self.checker.visit_functiondef(node)

    def test_wrong_name_of_func_params_in_google_docstring(self):
        """Example of functions with inconsistent parameter names in the
        signature and in the Google style documentation
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg, zarg):
            '''function foo ...

            Args:
                xarg1 (int): bla xarg
                yarg (float): bla yarg

                zarg1 (str): bla zarg
            '''
            return xarg + yarg
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('xarg, xarg1, zarg, zarg1',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('xarg, xarg1, zarg, zarg1',)),
        ):
            self.checker.visit_functiondef(node)

        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            Args:
                yarg1 (float): bla yarg

            For the other parameters, see bla.
            '''
            return xarg + yarg
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('yarg1',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('yarg1',))
        ):
            self.checker.visit_functiondef(node)

    def test_wrong_name_of_func_params_in_numpy_docstring(self):
        """Example of functions with inconsistent parameter names in the
        signature and in the Numpy style documentation
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg, zarg):
            '''function foo ...

            Parameters
            ----------
            xarg1: int
                bla xarg
            yarg: float
                bla yarg

            zarg1: str
                bla zarg
            '''
            return xarg + yarg
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('xarg, xarg1, zarg, zarg1',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('xarg, xarg1, zarg, zarg1',)),
        ):
            self.checker.visit_functiondef(node)

        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            Parameters
            ----------
            yarg1: float
                bla yarg

            For the other parameters, see bla.
            '''
            return xarg + yarg
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('yarg1',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('yarg1',))
        ):
            self.checker.visit_functiondef(node)

    def test_see_sentence_for_func_params_in_sphinx_docstring(self):
        """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Sphinx style)
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
            self.checker.visit_functiondef(node)

    def test_see_sentence_for_func_params_in_google_docstring(self):
        """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Google style)
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            Args:
                yarg (float): bla yarg

            For the other parameters, see :func:`bla`
            '''
            return xarg + yarg
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_see_sentence_for_func_params_in_numpy_docstring(self):
        """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Numpy style)
        """
        node = test_utils.extract_node("""
        def function_foo(xarg, yarg):
            '''function foo ...

            Parameters
            ----------
            yarg: float
                bla yarg

            For the other parameters, see :func:`bla`
            '''
            return xarg + yarg
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_constr_params_in_class_sphinx(self):
        """Example of a class with missing constructor parameter documentation
        (Sphinx style)

        Everything is completely analogous to functions.
        """
        node = test_utils.extract_node("""
        class ClassFoo(object):
            '''docstring foo

            :param y: bla
            
            missing constructor parameter documentation
            '''

            def __init__(self, x, y):
                pass

        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('x',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('x, y',))
        ):
            self._visit_methods_of_class(node)

    def test_constr_params_in_class_google(self):
        """Example of a class with missing constructor parameter documentation
        (Google style)

        Everything is completely analogous to functions.
        """
        node = test_utils.extract_node("""
        class ClassFoo(object):
            '''docstring foo

            Args:
                y: bla
            
            missing constructor parameter documentation
            '''

            def __init__(self, x, y):
                pass

        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('x',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('x, y',))
        ):
            self._visit_methods_of_class(node)

    def test_constr_params_in_class_numpy(self):
        """Example of a class with missing constructor parameter documentation
        (Numpy style)

        Everything is completely analogous to functions.
        """
        node = test_utils.extract_node("""
        class ClassFoo(object):
            '''docstring foo

            Parameters
            ----------
            y:
                bla
            
            missing constructor parameter documentation
            '''

            def __init__(self, x, y):
                pass

        """)
        with self.assertAddsMessages(
            Message(
                msg_id='missing-param-doc',
                node=node,
                args=('x',)),
            Message(
                msg_id='missing-type-doc',
                node=node,
                args=('x, y',))
        ):
            self._visit_methods_of_class(node)


if __name__ == '__main__':
    unittest.main()
