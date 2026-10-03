"""Tests for missing-return-doc and missing-return-type-doc for Sphinx style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, disallowed-name, too-few-public-methods, missing-class-docstring
# pylint: disable=unnecessary-pass, use-yield-from
import abc


def my_func(self):
    """find_sphinx_returns

    :return: Always False
    :rtype: bool
    """
    return False


def my_func(self, doc_type):
    """ignores_sphinx_return_none

    :param doc_type: Sphinx
    :type doc_type: str
    """
    return


def my_func(self):
    """finds_sphinx_return_custom_class

    :returns: An object
    :rtype: :class:`mymodule.Class`
    """
    return mymodule.Class()


def my_func(self):
    """finds_sphinx_return_list_of_custom_class

    :returns: An object
    :rtype: list(:class:`mymodule.Class`)
    """
    return [mymodule.Class()]


def my_func(self):  # [redundant-returns-doc]
    """warns_sphinx_redundant_return_doc

    :returns: One
    """
    return None


def my_func(self):  # [redundant-returns-doc]
    """warns_sphinx_redundant_rtype_doc

    :rtype: int
    """
    return None


def my_func(self):
    """ignores_sphinx_redundant_return_doc_multiple_returns

    :returns: One
    :rtype: int

    :returns: None sometimes
    :rtype: None
    """
    if a_func():
        return None
    return 1


def my_func_with_yield(self):
    """ignore_sphinx_redundant_return_doc_yield

    :returns: One
    :rtype: generator
    """
    for value in range(3):
        yield value


class Foo:
    """test_ignores_return_in_abstract_method_sphinx
    Example of an abstract method documenting the return type that an
    implementation should return.
    """

    @abc.abstractmethod
    def foo(self):
        """docstring ...

        :returns: Ten
        :rtype: int
        """
        return 10


class Foo:
    def test_ignores_ignored_argument_names_sphinx(self, arg, _):
        """Example of a method documenting the return type that an
        implementation should return.


        :param arg: An argument.
        :type arg: int
        """
        pass
