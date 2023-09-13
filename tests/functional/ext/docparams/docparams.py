"""Fixture for testing missing documentation in docparams."""
# pylint: disable=broad-exception-raised

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


# Only check raise nodes within FunctionDefs
raise Exception()
