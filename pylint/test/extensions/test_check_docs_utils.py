# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the pylint checkers in :mod:`pylint.extensions.check_docs`,
in particular the parameter documentation checker `DocstringChecker`
"""
from __future__ import division, print_function, absolute_import

import unittest
import sys

import astroid
from astroid import test_utils
from pylint.testutils import CheckerTestCase, Message, set_config

import pylint.extensions._check_docs_utils as utils


class SpaceIndentationTest(unittest.TestCase):
    """Tests for pylint_plugin.ParamDocChecker"""

    def test_space_indentation(self):
        self.assertEqual(utils.space_indentation('abc'), 0)
        self.assertEqual(utils.space_indentation(''), 0)
        self.assertEqual(utils.space_indentation('  abc'), 2)
        self.assertEqual(utils.space_indentation('\n  abc'), 0)
        self.assertEqual(utils.space_indentation('   \n  abc'), 3)

class PossibleExcTypesText(unittest.TestCase):
    def test_exception_class(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            raise NotImplementedError #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set(["NotImplementedError"])
        self.assertEqual(found, expected)

    def test_exception_instance(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            raise NotImplementedError("Not implemented!") #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set(["NotImplementedError"])
        self.assertEqual(found, expected)

    def test_rethrow(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            try:
                fake_func()
            except RuntimeError:
                raise #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set(["RuntimeError"])
        self.assertEqual(found, expected)

    def test_nested_in_if_rethrow(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            try:
                fake_func()
            except RuntimeError:
                if another_func():
                    raise #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set(["RuntimeError"])
        self.assertEqual(found, expected)

    def test_nested_in_try(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            try:
                fake_func()
            except RuntimeError:
                try:
                    another_func()
                    raise #@
                except NameError:
                    pass
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set(["RuntimeError"])
        self.assertEqual(found, expected)

    def test_nested_in_try_except(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            try:
                fake_func()
            except RuntimeError:
                try:
                    another_func()
                except NameError:
                    raise #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set(["NameError"])
        self.assertEqual(found, expected)

    def test_no_rethrow_types(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            try:
                fake_func()
            except:
                raise #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set()
        self.assertEqual(found, expected)

    def test_multiple_rethrow_types(self):
        raise_node = test_utils.extract_node('''
        def my_func():
            try:
                fake_func()
            except (RuntimeError, ValueError):
                raise #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set(["RuntimeError", "ValueError"])
        self.assertEqual(found, expected)

    def test_ignores_uninferable_type(self):
        raise_node = test_utils.extract_node('''
        import not_a_module
        def my_func():
            try:
                fake_func()
            except not_a_module.Error:
                raise #@
        ''')
        found = utils.possible_exc_types(raise_node)
        expected = set()
        self.assertEqual(found, expected)

if __name__ == '__main__':
    unittest.main()
