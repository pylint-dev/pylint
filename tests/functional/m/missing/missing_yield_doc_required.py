"""Tests for missing-yield-doc and missing-yield-type-doc with accept-no-yields-doc = no"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined

# Test missing docstring
def my_func(self):  # [missing-yield-doc, missing-yield-type-doc]
    yield False


# Test Sphinx docstring
def my_func(self):
    """This is a docstring.

    :return: Always False
    :rtype: bool
    """
    yield False


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


# Test Google docstring
def my_func(self):
    """This is a docstring.

    Yields:
        bool: Always False
    """
    yield False


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


# Test Numpy docstring
def my_func(self):
    """This is a docstring.

    Yields
    -------
    bool
        Always False
    """
    yield False


def my_func(self, doc_type):  # [missing-yield-doc, missing-yield-type-doc]
    """This is a docstring.

    Arguments
    ---------
    doc_type : str
        Numpy
    """
    yield False
