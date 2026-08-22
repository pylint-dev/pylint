# pylint: disable=missing-docstring, invalid-name, unused-variable


def func_return_none():
    """function returning none"""
    return None


def func_no_return():
    """function without return"""
    print("no return")


lst = [3, 2, 1]
A: list = lst.reverse()  # [assignment-from-no-return]

lst2 = [3, 2, 1]
if (B := lst2.reverse()) is None:  # [assignment-from-no-return]
    pass

C: object = func_return_none()  # [assignment-from-none]

if (D := func_no_return()) is None:  # [assignment-from-no-return]
    pass

E: int
