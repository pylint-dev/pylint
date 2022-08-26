"""Fixture for testing missing documentation in docparams."""
from __future__ import annotations


def _private_func1(  # [missing-return-doc, missing-return-type-doc, missing-any-param-doc]
    param1,
):
    """This is a test docstring without returns"""
    return param1


def _private_func2(  # [missing-yield-doc, missing-yield-type-doc, missing-any-param-doc]
    param1,
):
    """This is a test docstring without yields"""
    yield param1


def _private_func3(param1):  # [missing-raises-doc, missing-any-param-doc]
    """This is a test docstring without raises"""
    raise Exception("Example")


def public_func1(param1):  # [missing-any-param-doc]
    """This is a test docstring without params"""
    print(param1)


# pylint: disable-next=line-too-long
async def _async_private_func1(  # [missing-return-doc, missing-return-type-doc, missing-any-param-doc]
    param1,
):
    """This is a test docstring without returns"""
    return param1


# pylint: disable-next=line-too-long
async def _async_private_func2(  # [missing-yield-doc, missing-yield-type-doc, missing-any-param-doc]
    param1,
):
    """This is a test docstring without yields"""
    yield param1


async def _async_private_func3(param1):  # [missing-raises-doc, missing-any-param-doc]
    """This is a test docstring without raises"""
    raise Exception("Example")


async def async_public_func1(param1):  # [missing-any-param-doc]
    """This is a test docstring without params"""
    print(param1)


def differing_param_doc(par1: int) -> int:  # [differing-param-doc]
    """This is a test docstring documenting one non-existing param

    :param par1: some param
    :param param: some param
    :return: the sum of the params
    """

    return par1


def differing_param_doc_kwords_only(*, par1: int) -> int:  # [differing-param-doc]
    """This is a test docstring documenting one non-existing param

    :param par1: some param
    :param param: some param
    :return: the sum of the params
    """

    return par1


def missing_type_doc(par1) -> int:  # [missing-type-doc]
    """This is a test docstring params where the type is not specified

    :param par1: some param
    :return: the param
    """

    return par1


def missing_type_doc_kwords_only(*, par1) -> int:  # [missing-type-doc]
    """This is a test docstring params where the type is not specified

    :param par1: some param
    :return: the param
    """

    return par1


def params_are_documented(par1: int, *, par2: int) -> int:
    """This is a test docstring params where nothing is raised as it is all documented

    :param par1: some param
    :param par2: some other param
    :return: the sum of params
    """

    return par1 + par2


def params_with_pipe(arg1: int | bool, arg2: str | None = None) -> None:
    """No errors raised when pipe symbol used for or.

    `PEP 604`_ allows writing Union types as X | Y. Can be enabled in Python <3.10
    using `from __future__ import annotations`.

    Parameters
    ----------
    arg1 : int | bool
        The first arg
    arg2 : str | None, default=None
        The second arg

    .. _`PEP 604`:
        https://peps.python.org/pep-0604/
    """

    print(arg1, arg2)


def regression_6211(number: int = 0) -> None:
    """This is a regression test for issue #6211.

    False negative of "missing param doc" was being issued when "default" used in
    NumPy-style docs. This test should return no errors.

    See https://github.com/PyCQA/pylint/issues/6211

    Parameter
    ---------
    number : int, default 0
        The number parameter
    """

    print(number)
