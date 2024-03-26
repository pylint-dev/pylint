# pylint: disable=unnecessary-pass, consider-using-f-string

"""
Test fixme in docstrings.
"""

def func1(): # [fixme-in-docstring]
    """
    TODO: Implement
    """

# fixme-in-docstring
def func2(): # [fixme-in-docstring]
    """
    FIXME: Implement
    """

# fixme-in-docstring
def func3(): # [fixme-in-docstring]
    """
    XXX: Implement
    """

def func4():
    """
    This is regular docstring
    """
