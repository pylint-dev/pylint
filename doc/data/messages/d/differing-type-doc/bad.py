def foo(x: int, y: int):  # [differing-type-doc]
    """A dummy string.

    :param int xy: x value.
    :param str y: y value.
    :returns: a result.
    :rtype: int
    """

    return x + y
