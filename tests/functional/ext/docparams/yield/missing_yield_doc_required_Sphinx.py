"""Tests for missing-yield-doc and missing-yield-type-doc for Sphinx style docstrings
with accept-no-yields-doc = no"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined
# pylint: disable=invalid-name, undefined-variable


# Test Sphinx docstring
def my_func(self):
    """This is a docstring.

    :return: Always False
    :rtype: bool
    """
    yield False


def my_func(self):
    """This is a docstring.

    :returns: An object
    :rtype: :class:`mymodule.Class`
    """
    yield mymodule.Class()


def my_func(self):
    """This is a docstring.

    :returns: An object
    :rtype: list(:class:`mymodule.Class`)
    """
    yield [mymodule.Class()]


def my_func(self):  # [missing-yield-doc]
    """This is a docstring.

    :rtype: list(:class:`mymodule.Class`)
    """
    yield [mymodule.Class()]


def my_func(self):  # [missing-yield-type-doc]
    """This is a docstring.

    :returns: Always False
    """
    yield False


def my_func(self):  # [missing-yield-doc]
    """This is a docstring.

    :rtype: bool
    """
    yield False


def my_func(self, doc_type):  # [missing-yield-doc, missing-yield-type-doc]
    """This is a docstring.

    :param doc_type: Sphinx
    :type doc_type: str
    """
    yield False
