"""Tests for missing-return-doc and missing-return-type-doc for Google style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, too-few-public-methods


def my_func(self):
    """find_google_returns

    Returns:
        bool: Always False
    """
    return False


def my_func(self, doc_type):
    """ignores_google_return_none

    Args:
        doc_type (str): Google
    """
    return


def my_func(self):
    """finds_google_return_custom_class

    Returns:
        mymodule.Class: An object
    """
    return mymodule.Class()


def my_func(self):
    """finds_google_return_list_of_custom_class

    Returns:
        list(:class:`mymodule.Class`): An object
    """
    return [mymodule.Class()]


def my_func(self):  # [redundant-returns-doc]
    """warns_google_redundant_return_doc

    Returns:
        One
    """
    return None


def my_func(self):  # [redundant-returns-doc]
    """warns_google_redundant_rtype_doc

    Returns:
        int:
    """
    return None


def my_func(self):  # [redundant-returns-doc]
    """warns_google_redundant_return_doc_yield

    Returns:
        int: One
    """
    yield 1


def my_func(self):
    """ignores_google_redundant_return_doc_multiple_returns

    Returns:
        int or None: One, or sometimes None.
    """
    if a_func():
        return None
    return 1


class Foo:
    """test_finds_property_return_type_google
    Example of a property having return documentation in
    a Google style docstring
    """

    @property
    def foo_method(self):
        """int: docstring ...

        Raises:
            RuntimeError: Always
        """
        raise RuntimeError()
        return 10  # [unreachable]


class Foo:
    """test_finds_annotation_property_return_type_google
    Example of a property having return documentation in
    a Google style docstring
    """

    @property
    def foo_method(self) -> int:
        """docstring ...

        Raises:
            RuntimeError: Always
        """
        raise RuntimeError()
        return 10  # [unreachable]
