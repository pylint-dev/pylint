#pylint: disable = missing-any-param-doc
"""demonstrate FP with useless-type-doc"""


def function(public_param: int, _some_private_param: bool = False) -> None:
    """does things

    Args:
        public_param: an ordinary parameter
    """
    for _ in range(public_param):
        ...
    if _some_private_param:
        ...
    else:
        ...


def smart_function(public_param: int, _some_private_param: bool = False) -> None:
    """We're speaking about _some_private_param without really documenting it.

    Args:
        public_param: an ordinary parameter
    """
    for _ in range(public_param):
        ...
    if _some_private_param:
        ...
    else:
        ...


# +1: [useless-type-doc,useless-param-doc]
def function_useless_doc(public_param: int, _some_private_param: bool = False) -> None:
    """does things

    Args:
        public_param: an ordinary parameter
        _some_private_param (bool): private param

    """
    for _ in range(public_param):
        ...
    if _some_private_param:
        ...
    else:
        ...


def test(_new: str) -> str:
    """foobar

    :return: comment
    """
    return ""


def smarter_test(_new: str) -> str:
    """We're speaking about _new without really documenting it.

    :return: comment
    """
    return ""


# +1: [useless-type-doc,useless-param-doc]
def test_two(_new: str) -> str:
    """foobar

    :param str _new:
    :return: comment
    """
    return ""
