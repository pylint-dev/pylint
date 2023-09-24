# pylint: disable=missing-docstring, invalid-name, too-few-public-methods, import-outside-toplevel, fixme, line-too-long, broad-exception-raised

def test_regression_737():
    import xml # [unused-import]

def test_regression_923():
    import unittest.case  # [unused-import]
    import xml as sql # [unused-import]

def test_unused_with_prepended_underscore():
    _foo = 42
    _ = 24
    __a = 24
    dummy = 24
    _a_ = 42 # [unused-variable]
    __a__ = 24 # [unused-variable]
    __never_used = 42

def test_local_field_prefixed_with_unused_or_ignored():
    flagged_local_field = 42 # [unused-variable]
    unused_local_field = 42
    ignored_local_field = 42


class HasUnusedDunderClass:

    def test(self):
        __class__ = 42  # [unused-variable]

    def best(self):
        self.test()


def locals_example_defined_before():
    value = 42  # [possibly-unused-variable]
    return locals()


def locals_example_defined_after():
    local_variables = locals()
    value = 42  # [unused-variable]
    return local_variables


def locals_does_not_account_for_subscopes():
    value = 42  # [unused-variable]

    def some_other_scope():
        return locals()
    return some_other_scope


def unused_import_from():
    from functools import wraps as abc # [unused-import]
    from collections import namedtuple # [unused-import]


def unused_import_in_function(value):
    from string import digits, hexdigits # [unused-import]
    return value if value in digits else "Nope"


def hello(arg):
    my_var = 'something' # [unused-variable]
    if arg:
        return True
    raise Exception

# pylint: disable=wrong-import-position
PATH = OS = collections = deque = None


def function(matches):
    """"yo"""
    aaaa = 1  # [unused-variable]
    index = -1
    for match in matches:
        index += 1
        print(match)

from astroid import nodes
def visit_if(self, node: nodes.If) -> None:
    """increments the branches counter"""
    branches = 1
    # don't double count If nodes coming from some 'elif'
    if node.orelse and len(node.orelse) > 1:
        branches += 1
    self.inc_branch(branches)
    self.stmts += branches


def test_global():
    """ Test various assignments of global
    variables through imports.
    """
    # pylint: disable=redefined-outer-name
    global PATH, OS, collections, deque  # [global-statement]
    from os import path as PATH
    import os as OS
    import collections
    from collections import deque
    # make sure that these triggers unused-variable
    from sys import platform  # [unused-import]
    from sys import version as VERSION  # [unused-import]
    import this  # [unused-import]
    import re as RE  # [unused-import]

# test cases that include exceptions
def function2():
    unused = 1  # [unused-variable]
    try:
        1 / 0
    except ZeroDivisionError as error:
        try:
            1 / 0
        except ZeroDivisionError as error:  # [redefined-outer-name]
            raise Exception("") from error

def func():
    try:
        1 / 0
    except ZeroDivisionError as error:
        try:
            1 / 0
        except error:
            print("error")

def func2():
    try:
        1 / 0
    except ZeroDivisionError as error:
        try:
            1 / 0
        except:
            raise Exception("") from error

def func3():
    try:
        1 / 0
    except ZeroDivisionError as error:
        print(f"{error}")
        try:
            1 / 2
        except TypeError as error:  # [unused-variable, redefined-outer-name]
            print("warning")

def func4():
    try:
        1 / 0
    except ZeroDivisionError as error:  # [unused-variable]
        try:
            1 / 0
        except ZeroDivisionError as error:  # [redefined-outer-name]
            print("error")


def main(lst):
    """https://github.com/pylint-dev/astroid/pull/1111#issuecomment-890367609"""
    try:
        raise ValueError
    except ValueError as e:  # [unused-variable]
        pass

    for e in lst:
        pass

    # e will be undefined if lst is empty
    print(e)  # [undefined-loop-variable]

main([])


def func5():
    """No unused-variable for a container if iterated in comprehension"""
    x = []
    # Test case requires homonym between "for x" and "in x"
    assert [True for x in x]


def sibling_except_handlers():
    try:
        pass
    except ValueError as e:
        print(e)
    try:
        pass
    except ValueError as e:
        print(e)

def func6():
    a = 1

    def nonlocal_writer():
        nonlocal a

        for a in range(10):
            pass

    nonlocal_writer()

    assert a == 9, a

def test_regression_8595():
    # pylint: disable=broad-exception-caught
    import logging
    def compute():
        pass
    try:
        compute()
        error = False
    except Exception as e:
        logging.error(e)
        error = True
    if error:
        try:
            compute()
        except Exception as e:  # [unused-variable]
            pass
