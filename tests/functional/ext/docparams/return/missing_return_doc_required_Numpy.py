"""Tests for missing-return-doc and missing-return-type-doc for Numpy style docstrings
with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self, doc_type):  # [missing-return-doc]
    """This is a docstring.

    Arguments
    ---------
    doc_type : str
        Numpy

    Returns
    -------
    bool
    """
    return False


def my_func(self, doc_type):  # [missing-return-doc, missing-return-type-doc]
    """This is a docstring.

    Arguments
    ---------
    doc_type : str
        Numpy
    """
    return False


def my_func(self):  # [missing-return-doc]
    """This is a docstring.

    Returns
    -------
        list(:class:`mymodule.Class`)
    """
    return [mymodule.Class()]
