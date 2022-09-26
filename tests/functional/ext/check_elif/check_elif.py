# pylint: disable=no-else-raise,unsupported-membership-test,using-constant-test, comparison-of-constants

"""Checks use of "else if" triggers a refactor message"""
from typing import Union, Sequence, Any, Mapping


def my_function():
    """docstring"""
    myint = 2
    if myint > 5:
        pass
    else:
        if myint <= 5:  # [else-if-used]
            pass
        else:
            myint = 3
            if myint > 2:
                if myint > 3:
                    pass
                elif myint == 3:
                    pass
                elif myint < 3:
                    pass
                else:
                    if myint:  # [else-if-used]
                        pass
            else:
                if myint:
                    pass
                myint = 4


def _if_in_fstring_comprehension_with_elif(
    params: Union[Sequence[Any], Mapping[str, Any]]
):
    order = {}
    if "z" not in "false":
        raise TypeError(
            f" {', '.join(sorted(i for i in order or () if i not in params))}"
        )
    elif "z" not in "true":
        pass
    else:
        if "t" not in "false":  # [else-if-used]
            raise TypeError("d")
        else:
            if "y" in "life":  # [else-if-used]
                print("e")
