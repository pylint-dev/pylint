"""Tests for loopvar-in-closure."""

__revision__ = 0


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
        print i
        lst.append(lambda i: i)


def good_case5():
    """No problems here."""
    return (i for i in range(10))


def good_case6():
    """Accept use of the variable after the loop.

    There's already a warning about possibly undefined loop variables, and
    the value will not change any more."""
    for i in range(10):
        print i
    return lambda: i


def good_case7():
    """Accept use of the variable inside return."""
    for i in range(10):
        if i == 8:
            return lambda: i
    return lambda: -1


def bad_case():
    """Closing over a loop variable."""
    lst = []
    for i in range(10):
        print i
        lst.append(lambda: i)


def bad_case2():
    """Closing over a loop variable."""
    return [lambda: i for i in range(10)]


def bad_case3():
    """Closing over variable defined in loop."""
    lst = []
    for i in range(10):
        j = i * i
        lst.append(lambda: j)
    return lst


def bad_case4():
    """Closing over variable defined in loop."""
    lst = []
    for i in range(10):
        def nested():
            """Nested function."""
            return i**2
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
    return (lambda: i for i in range(10))


def bad_case6():
    """Closing over variable defined in loop."""
    lst = []
    for i, j in zip(range(10), range(10, 20)):
        print j
        lst.append(lambda: i)
    return lst
