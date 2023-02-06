def foo(x: int, y: int):  # [differing-type-doc]
    """A dummy string.

    :param int xy: x value.
    :param str y: y value.
    """

    return x + y
