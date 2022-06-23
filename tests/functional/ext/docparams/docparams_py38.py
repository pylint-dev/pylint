"""Fixture for testing missing documentation in docparams (Python >=3.8 only)."""


def differing_param_doc_pos_only(par1: int, /) -> int:  # [differing-param-doc]
    """This is a test docstring documenting one non-existing param

    :param par1: some param
    :param param: some param
    :return: the sum of the params
    """

    return par1


def missing_type_doc_pos_only(par1, /) -> int:  # [missing-type-doc]
    """This is a test docstring params where the type is not specified

    :param par1: some param
    :return: the param
    """

    return par1


def params_are_documented(par1: int, /, par2: int, *, par3: int) -> int:
    """This is a test docstring params where nothing is raised as it is all documented

    :param par1: some param
    :param par2: some other param
    :param par3: some other param
    :return: the sum of params
    """

    return par1 + par2 + par3
