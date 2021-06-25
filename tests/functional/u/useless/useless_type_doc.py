"""demonstrate FP with useless-type-doc"""
# line-too-long


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


def test(_new: str) -> str:  # We don't expect useless-type-doc here
    """foobar

    :return: comment
    """
    return ""


# +1: [useless-type-doc,useless-param-doc]
def test_two(_new: str) -> str:  # We don't expect useless-type-doc here
    """foobar

    :param str _new:
    :return: comment
    """
    return ""
