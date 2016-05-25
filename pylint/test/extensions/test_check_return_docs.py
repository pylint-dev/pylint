"""Unit tests for the return documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""
from __future__ import division, print_function, absolute_import

import unittest

import astroid
from astroid import test_utils
from pylint.testutils import CheckerTestCase, Message, set_config

from pylint.extensions.check_docs import DocstringChecker


class DocstringCheckerReturnTest(CheckerTestCase):
    """Tests for pylint_plugin.RaiseDocChecker"""
    CHECKER_CLASS = DocstringChecker

    def test_ignores_no_docstring(self):
        return_node = test_utils.extract_node('''
        def my_func(self):
            return False #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    @set_config(accept_no_return_doc=False)
    def test_warns_no_docstring(self):
        node = test_utils.extract_node('''
        def my_func(self):
            return False
        ''')
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-returns-doc',
                node=node)):
            self.checker.visit_return(return_node)

    def test_ignores_unknown_style(self):
        return_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring."""
            return False #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_warn_partial_sphinx_returns(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :returns: Always False
            """
            return False
        ''')
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-returns-doc',
                node=node)):
            self.checker.visit_return(return_node)

    def test_warn_partial_sphinx_returns_type(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :rtype: bool
            """
            return False
        ''')
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-returns-doc',
                node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_sphinx_returns(self):
        node = test_utils.extract_node('''
        def my_func(self, doc_type):
            """This is a docstring.

            :param doc_type: Sphinx
            :type doc_type: str
            """
            return False
        ''')
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-returns-doc',
                node=node)):
            self.checker.visit_return(return_node)

    def test_warn_partial_google_returns(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Returns:
                Always False
            """
            return False
        ''')
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-returns-doc',
                node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_google_returns(self):
        node = test_utils.extract_node('''
        def my_func(self, doc_type):
            """This is a docstring.

            Parameters:
                doc_type (str): Google
            """
            return False
        ''')
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-returns-doc',
                node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_numpy_returns(self):
        node = test_utils.extract_node('''
        def my_func(self, doc_type):
            """This is a docstring.

            Arguments
            ---------
            doc_type : str
                Numpy
            """
            return False
        ''')
        return_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-returns-doc',
                node=node)):
            self.checker.visit_return(return_node)

    def test_find_sphinx_returns(self):
        return_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :return: Always False
            :rtype: bool
            """
            return False #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_google_returns(self):
        return_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Returns:
                bool: Always False
            """
            return False #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_numpy_returns(self):
        return_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
            bool
                Always False
            """
            return False #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_sphinx_return_none(self):
        return_node = test_utils.extract_node('''
        def my_func(self, doc_type):
            """This is a docstring.

            :param doc_type: Sphinx
            :type doc_type: str
            """
            return #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_google_return_none(self):
        return_node = test_utils.extract_node('''
        def my_func(self, doc_type):
            """This is a docstring.

            Args:
                doc_type (str): Google
            """
            return #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_numpy_return_none(self):
        return_node = test_utils.extract_node('''
        def my_func(self, doc_type):
            """This is a docstring.

            Arguments
            ---------
            doc_type : str
                Numpy
            """
            return #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

if __name__ == '__main__':
    unittest.main()
