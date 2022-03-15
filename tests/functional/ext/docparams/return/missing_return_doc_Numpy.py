"""Tests for missing-return-doc and missing-return-type-doc for Numpy style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, too-few-public-methods, disallowed-name
import abc


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


class Foo:
    """test_ignores_return_in_abstract_method_numpy
    Example of an abstract method documenting the return type that an
    implementation should return."""

    @abc.abstractmethod
    def foo(self):
        """docstring ...

        Returns
        -------
        int
            Ten
        """
        return 10


class Foo:
    """test_ignores_return_in_abstract_method_numpy_2
    Example of a method documenting the return type that an
    implementation should return."""

    def foo(self, arg):
        """docstring ...

        Parameters
        ----------
        arg : int
            An argument.
        """
        raise NotImplementedError()


class Foo:
    """test_ignores_ignored_argument_names_numpy
    Example of a method documenting the return type that an
    implementation should return.
    """

    def foo(self, arg, _):
        """docstring ...

        Parameters
        ----------
        arg : int
            An argument.
        """


class Foo:
    """test_useless_docs_ignored_argument_names_numpy
    Example of a method documenting the return type that an
    implementation should return.
    """

    def foo(self, arg, _, _ignored):  # [useless-type-doc, useless-param-doc]
        """docstring ...

        Parameters
        ----------
        arg : int
            An argument.

        _ : float
            Another argument.

        _ignored :
            Ignored Argument
        """
