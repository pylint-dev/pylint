"""Tests for missing-raises-doc and missing-raises-type-doc"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-error, unused-variable, no-member, try-except-raise
import collections

from fake_package import BadError
from unknown import Unknown


def test_ignores_no_docstring(self):
    raise RuntimeError("hi")


def test_ignores_unknown_style(self):
    """This is a docstring."""
    raise RuntimeError("hi")


def test_ignores_raise_uninferable(self):
    """This is a docstring.

    :raises NameError: Never
    """
    raise Unknown("hi")
    raise NameError("hi")  # [unreachable]


def test_ignores_returns_from_inner_functions(self):  # [missing-raises-doc]
    """This is a docstring.
    We do NOT expect a warning about the OSError in inner_func!

    :raises NameError: Never
    """

    def ex_func(val):
        def inner_func(value):
            return OSError(value)

        return RuntimeError(val)

    raise ex_func("hi")
    raise NameError("hi")  # [unreachable]


def test_ignores_returns_use_only_names():
    """This is a docstring

    :raises NameError: Never
    """

    def inner_func():
        return 42

    raise inner_func()  # [raising-bad-type]


def test_ignores_returns_use_only_exception_instances():
    """This is a docstring

    :raises MyException: Never
    """

    class MyException(Exception):
        """A docstring"""

    def inner_func():
        return MyException

    raise inner_func()


def test_no_crash_when_inferring_handlers():
    """raises

    :raise U: pass
    """
    try:
        pass
    except collections.U as exc:
        raise


def test_no_crash_when_cant_find_exception():
    """raises

    :raise U: pass
    """
    try:
        pass
    except U as exc:
        raise


def test_no_error_notimplemented_documented():
    """
    Raises:
        NotImplementedError: When called.
    """
    raise NotImplementedError


def test_finds_short_name_exception():
    """Do something.

    Raises:
        ~fake_package.exceptions.BadError: When something bad happened.
    """
    raise BadError("A bad thing happened.")
