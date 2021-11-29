"""Tests for missing-return-doc and missing-return-type-doc for Sphinx style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):
    """This is a docstring.

    :return: Always False
    :rtype: bool
    """
    return False


def my_func(self, doc_type):
    """This is a docstring.

    :param doc_type: Sphinx
    :type doc_type: str
    """
    return


def my_func(self):
    """This is a docstring.

    :returns: An object
    :rtype: :class:`mymodule.Class`
    """
    return mymodule.Class()


def my_func(self):
    """This is a docstring.

    :returns: An object
    :rtype: list(:class:`mymodule.Class`)
    """
    return [mymodule.Class()]


def my_func(self):  # [redundant-returns-doc]
    """This is a docstring.

    :returns: One
    """
    return None
