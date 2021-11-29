"""Tests for missing-return-doc and missing-return-type-doc for Numpy style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):
    """This is a docstring.

    Returns
    -------
    bool
        Always False
    """
    return False


def my_func(self):
    """This is a docstring.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of strings
    """
    return ["hi", "bye"]


def my_func(self, doc_type):
    """This is a docstring.

    Arguments
    ---------
    doc_type : str
        Numpy
    """
    return


def my_func(self):
    """This is a docstring.

    Returns
    -------
        mymodule.Class
            An object
    """
    return mymodule.Class()


def my_func(self):
    """This is a docstring.

    Returns
    -------
        list(:class:`mymodule.Class`)
            An object
    """
    return [mymodule.Class()]


def my_func(self):  # [redundant-returns-doc]
    """This is a docstring.

    Returns
    -------
        int
            One
    """
    return None


def my_func(self):  # [redundant-returns-doc]
    """This is a docstring.

    Returns
    -------
        int
    """
    return None


def my_func(self):
    """This is a docstring.

    Returns
    -------
        int
            One
        None
            Sometimes
    """
    if a_func():
        return None
    return 1
