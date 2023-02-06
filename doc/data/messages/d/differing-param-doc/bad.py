def foo(x, y):  # [differing-param-doc]
    """A dummy string.

    :param int x: x value.
    :param int z: z value.
    :returns: a result.
    :rtype: int
    """

    return x + y
