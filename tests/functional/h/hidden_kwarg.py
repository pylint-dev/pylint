"""
The `hidden-kwarg` warning message is emitted when a function is called with
a keyword argument which shares a name with a positional-only parameter and
the function contains a keyword variadic parameter dictionary.
It may be surprising behaviour when the keyword argument is added to the
keyword variadic parameter dictionary.
"""


def name1(apple, /, banana="Yellow banana", **kwargs):
    """
    Positional-only parameter, positional-or-keyword parameter and `**kwargs`.

    `apple` is considered to be a hidden kwarg.
    `banana` is not hidden since it is a positional-or-keyword parameter.

    >>> name1("Red apple", apple="Green apple", banana="Green banana")
    Red apple
    Green banana
    {"apple": "Green apple"}
    """

    print(apple)
    print(banana)
    print(kwargs)


# `apple` is hidden:
name1("Red apple", apple="Green apple", banana="Green banana")  # [hidden-kwarg]

name1("Red apple", banana="Green banana")
