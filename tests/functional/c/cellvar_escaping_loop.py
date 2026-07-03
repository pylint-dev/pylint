# pylint: disable=unnecessary-comprehension,missing-docstring,too-few-public-methods,unnecessary-direct-lambda-call
"""Tests for loopvar-in-closure."""


from enum import Enum


def good_case():
    """No problems here."""
    lst = []
    for i in range(10):
        lst.append(i)


def good_case2():
    """No problems here."""
    return [i for i in range(10)]


def good_case3():
    """No problems here."""
    lst = []
    for i in range(10):
        lst.append(lambda i=i: i)


def good_case4():
    """No problems here."""
    lst = []
    for i in range(10):
        print(i)
        lst.append(lambda i: i)


def good_case5():
    """No problems here."""
    return (i for i in range(10))


def good_case6():
    """Accept use of the variable inside return."""
    for i in range(10):
        if i == 8:
            return lambda: i
    return lambda: -1


def good_case7():
    """Lambda defined and called in loop."""
    for i in range(10):
        print((lambda x: i + x)(1))


def good_case8():
    """Another eager binding of the cell variable."""
    funs = []
    for i in range(10):
        def func(bound_i=i):
            """Ignore."""
            return bound_i
        funs.append(func)
    return funs


def good_case9():
    """Ignore when the cell var is not defined in a loop"""
    i = 10
    lst = []
    for _ in range(10):
        lst.append(lambda: i)
    return lst


def good_case10():
    """Ignore when a loop variable is shadowed by an inner function"""
    lst = []
    for i in range(10):  # pylint: disable=unused-variable
        def func():
            i = 100
            def func2(arg=i):
                return arg

            return func2

        lst.append(func)
    return lst


def good_case_issue3107():
    """Eager binding of cell variable when used in a non-trivial default argument expression.
    """
    for i in [[2], [3]]:
        next(filter(lambda j, ix=i[0]: j == ix, [1, 3]))


def good_case_issue_5012():
    """Eager binding of cell variable when used as the default value of a keyword-only argument.
    https://github.com/pylint-dev/pylint/issues/5012
    """
    funs = []
    for i in range(5):
        def func(*, _i=i):
            print(_i)
        funs.append(func)

        def func2(_i=i):
            print(_i)
        funs.append(func2)

    return funs

def bad_case():
    """Closing over a loop variable."""
    lst = []
    for i in range(10):
        print(i)
        lst.append(lambda: i)  # [cell-var-from-loop]


def bad_case2():
    """Closing over a loop variable."""
    return [lambda: i for i in range(10)]  # [cell-var-from-loop]


def bad_case3():
    """Closing over variable defined in loop."""
    lst = []
    for i in range(10):
        j = i * i
        lst.append(lambda: j)  # [cell-var-from-loop]
    return lst


def bad_case4():
    """Closing over variable defined in loop."""
    lst = []
    for i in range(10):
        def nested():
            """Nested function."""
            return i**2  # [cell-var-from-loop]
        lst.append(nested)
    return lst


def bad_case5():
    """Problematic case.

    If this function is used as

    >>> [x() for x in bad_case5()]

    it behaves 'as expected', i.e. the result is range(10).

    If it's used with

    >>> lst = list(bad_case5())
    >>> [x() for x in lst]

    the result is [9] * 10 again.
    """
    return (lambda: i for i in range(10))  # [cell-var-from-loop]


def bad_case6():
    """Closing over variable defined in loop."""
    lst = []
    for i, j in zip(range(10), range(10, 20)):
        print(j)
        lst.append(lambda: i)  # [cell-var-from-loop]
    return lst


def bad_case7():
    """Multiple variables unpacked in comprehension."""
    return [
        lambda: (
            x  # [cell-var-from-loop]
            + y)  # [cell-var-from-loop]
        for x, y in ((1, 2), (3, 4), (5, 6))
    ]


def bad_case8():
    """Closing over variable defined in loop below the function."""
    lst = []
    for i in range(10):
        lst.append(lambda: j)  # [cell-var-from-loop]
        j = i * i
    return lst


def bad_case9():
    """Detect when loop variable shadows an outer assignment."""
    lst = []
    i = 100
    for i in range(10):
        lst.append(lambda: i)  # [cell-var-from-loop]
    return lst


def bad_case10():
    """Detect when a loop variable is the default argument for a nested function"""
    lst = []
    for i in range(10):
        def func():
            def func2(arg=i):  # [cell-var-from-loop]
                return arg

            return func2

        lst.append(func)
    return lst


def bad_case_issue2846():
    """Closing over variable that is used within a comprehension in the function body."""
    lst_a = [
        (lambda: n)  # [cell-var-from-loop]
        for n in range(3)
    ]

    lst_b = [
        (lambda: [n for _ in range(3)])  # [cell-var-from-loop]
        for n in range(3)
    ]

    return lst_a, lst_b


class Test(Enum):
    TEST = (40, 160)

    @staticmethod
    def new_test(minimum=TEST[0], maximum=TEST[1]):
        return minimum, maximum
