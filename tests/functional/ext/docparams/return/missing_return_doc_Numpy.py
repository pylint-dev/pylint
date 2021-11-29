"""Tests for missing-return-doc and missing-return-type-doc for Numpy style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):
    """find_numpy_returns

    Returns
    -------
    bool
        Always False
    """
    return False


def my_func(self):
    """find_numpy_returns_with_of

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of strings
    """
    return ["hi", "bye"]


def my_func(self, doc_type):
    """ignores_numpy_return_none

    Arguments
    ---------
    doc_type : str
        Numpy
    """
    return


def my_func(self):
    """finds_numpy_return_custom_class

    Returns
    -------
        mymodule.Class
            An object
    """
    return mymodule.Class()


def my_func(self):
    """finds_numpy_return_list_of_custom_class

    Returns
    -------
        list(:class:`mymodule.Class`)
            An object
    """
    return [mymodule.Class()]


def my_func(self):  # [redundant-returns-doc]
    """warns_numpy_redundant_return_doc

    Returns
    -------
        int
            One
    """
    return None


def my_func(self):  # [redundant-returns-doc]
    """warns_numpy_redundant_rtype_doc

    Returns
    -------
        int
    """
    return None


def my_func(self):
    """ignores_numpy_redundant_return_doc_multiple_returns

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


def my_func(self):  # [redundant-returns-doc]
    """warns_numpy_redundant_return_doc_yield

    Returns
    -------
        int
            One
    """
    yield 1
