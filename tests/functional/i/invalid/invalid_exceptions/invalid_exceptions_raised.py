# pylint:disable=too-few-public-methods,import-error,missing-docstring, not-callable, import-outside-toplevel
"""test pb with exceptions and classes"""


class ValidException(Exception):
    """Valid Exception."""

class NewStyleClass:
    """Not an exception."""

def good_case():
    """raise"""
    raise ValidException('hop')

def good_case1():
    """zlib.error is defined in C module."""
    import zlib
    raise zlib.error(4)

def good_case2():
    """decimal.DivisionByZero is defined in C on Python 3."""
    import decimal
    raise decimal.DivisionByZero(4)

def good_case3():
    """io.BlockingIOError is defined in C."""
    import io
    raise io.BlockingIOError

def bad_case1():
    """raise"""
    raise NewStyleClass()  # [raising-non-exception]

def bad_case3():
    """raise"""
    raise NewStyleClass  # [raising-non-exception]

def bad_case4():
    """raise"""
    raise NotImplemented('hop')  # [notimplemented-raised]

def bad_case5():
    """raise"""
    raise 1  # [raising-bad-type]

def bad_case6():
    """raise"""
    raise None  # [raising-bad-type]

def bad_case7():
    """raise list"""
    raise list # [raising-non-exception]

def bad_case8():
    """raise tuple"""
    raise tuple # [raising-non-exception]

def bad_case9():
    """raise dict"""
    raise dict # [raising-non-exception]

def unknown_bases():
    """Don't emit when we don't know the bases."""
    from lala import bala  # pylint: disable=import-outside-toplevel
    class MyException(bala):
        pass
    raise MyException


def exception_instance_regression():
    """Exceptions have a particular class type"""
    try:
        int("9a")
    except ValueError as exc:
        raise exc


def reusing_same_name_picks_the_latest_raised_value():
    class Error(Exception):
        """some error"""

    exceptions = tuple([ValueError, TypeError])
    try:
        raise ValueError
    except exceptions as exc:  # pylint: disable=catching-non-exception
        # https://github.com/pylint-dev/pylint/issues/1756
        exc = Error(exc)
        if exc:
            raise exc


def bad_case10():
    """raise string"""
    raise "string"  # [raising-bad-type]


class AmbiguousValue:
    """Don't emit when there is ambiguity on the node for the exception."""
    def __init__(self):
        self.stored_exception = None

    def fail(self):
        try:
            1 / 0
        except ZeroDivisionError as zde:
            self.stored_exception = zde

    def raise_stored_exception(self):
        if self.stored_exception is not None:
            exc = self.stored_exception
            self.stored_exception = None
            raise exc
