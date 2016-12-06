# Copyright (c) 2016 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the pylint checkers in :mod:`pylint.extensions.check_docs`,
in particular the parameter documentation checker `DocstringChecker`
"""
from __future__ import division, print_function, absolute_import

import astroid

import pylint.extensions._check_docs_utils as utils


def test_space_indentation():
    """Test for pylint_plugin.ParamDocChecker"""
    assert utils.space_indentation('abc') == 0
    assert utils.space_indentation('') == 0
    assert utils.space_indentation('  abc') == 2
    assert utils.space_indentation('\n  abc') == 0
    assert utils.space_indentation('   \n  abc') == 3


def test_exception_class():
    raise_node = astroid.extract_node('''
    def my_func():
        raise NotImplementedError #@
    ''')
    found = utils.possible_exc_types(raise_node)
    expected = set(["NotImplementedError"])
    assert found == expected


def test_exception_instance():
    raise_node = astroid.extract_node('''
    def my_func():
        raise NotImplementedError("Not implemented!") #@
    ''')
    found = utils.possible_exc_types(raise_node)
    expected = set(["NotImplementedError"])
    assert found == expected


def test_rethrow():
    raise_node = astroid.extract_node('''
    def my_func():
        try:
            fake_func()
        except RuntimeError:
            raise #@
    ''')
    found = utils.possible_exc_types(raise_node)
    expected = set(["RuntimeError"])
    assert found == expected


def test_nested_in_if_rethrow():
    raise_node = astroid.extract_node('''
    def my_func():
        try:
            fake_func()
        except RuntimeError:
            if another_func():
                raise #@
    ''')
    found = utils.possible_exc_types(raise_node)
    expected = set(["RuntimeError"])
    assert found == expected


def test_nested_in_try():
    raise_node = astroid.extract_node('''
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
    assert found == expected


def test_nested_in_try_except():
    raise_node = astroid.extract_node('''
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
    assert found == expected


def test_no_rethrow_types():
    raise_node = astroid.extract_node('''
    def my_func():
        try:
            fake_func()
        except:
            raise #@
    ''')
    found = utils.possible_exc_types(raise_node)
    expected = set()
    assert found == expected


def test_multiple_rethrow_types():
    raise_node = astroid.extract_node('''
    def my_func():
        try:
            fake_func()
        except (RuntimeError, ValueError):
            raise #@
    ''')
    found = utils.possible_exc_types(raise_node)
    expected = set(["RuntimeError", "ValueError"])
    assert found == expected


def test_ignores_uninferable_type():
    raise_node = astroid.extract_node('''
    import not_a_module
    def my_func():
        try:
            fake_func()
        except not_a_module.Error:
            raise #@
    ''')
    found = utils.possible_exc_types(raise_node)
    expected = set()
    assert found == expected


if __name__ == '__main__':
    import sys
    import pytest
    pytest.main(sys.argv)
