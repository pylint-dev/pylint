# pylint:disable=too-few-public-methods,old-style-class,no-init
"""test pb with exceptions and old/new style classes"""


class ValidException(Exception):
    """Valid Exception."""

class OldStyleClass:
    """Not an exception."""

class NewStyleClass(object):
    """Not an exception."""


def good_case():
    """raise"""
    raise ValidException('hop')

def bad_case0():
    """raise"""
    # +2:<3.0:[nonstandard-exception]
    # +1:>=3.0:[raising-non-exception]
    raise OldStyleClass('hop')

def bad_case1():
    """raise"""
    raise NewStyleClass()  # [raising-non-exception]

def bad_case2():
    """raise"""
    # +2:<3.0:[old-raise-syntax,nonstandard-exception]
    # +1:>=3.0:[raising-non-exception]
    raise OldStyleClass, 'hop'

def bad_case3():
    """raise"""
    raise NewStyleClass  # [raising-non-exception]

def bad_case4():
    """raise"""
    # +1:<3.0:[old-raise-syntax]
    raise NotImplemented, 'hop'  # [notimplemented-raised]

def bad_case5():
    """raise"""
    raise 1  # [raising-bad-type]

def base_case6():
    """raise"""
    raise None  # [raising-bad-type]

