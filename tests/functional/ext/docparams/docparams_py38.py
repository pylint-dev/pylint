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
