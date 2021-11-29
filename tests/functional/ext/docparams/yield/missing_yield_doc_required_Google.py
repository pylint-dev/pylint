"""Tests for missing-yield-doc and missing-yield-type-doc for Google style docstrings
with accept-no-yields-doc = no"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined
# pylint: disable=invalid-name, undefined-variable


def my_func(self):
    """This is a docstring.

    Yields:
        bool: Always False
    """
    yield False


def my_func(self):
    """This is a docstring.

    Yields:
        mymodule.Class: An object
    """
    yield mymodule.Class()


def my_func(self):
    """This is a docstring.

    Yields:
        list(:class:`mymodule.Class`): An object
    """
    yield [mymodule.Class()]


def my_func(self):  # [missing-yield-doc]
    """This is a docstring.

    Yields:
        list(:class:`mymodule.Class`):
    """
    yield [mymodule.Class()]


def my_func(self):  # [missing-yield-type-doc]
    """This is a docstring.

    Yields:
        Always False
    """
    yield False


def my_func(self):  # [missing-yield-doc]
    """This is a docstring.

    Yields:
        bool:
    """
    yield False


def my_func(self, doc_type):  # [missing-yield-doc, missing-yield-type-doc]
    """This is a docstring.

    Parameters:
        doc_type (str): Google
    """
    yield False
