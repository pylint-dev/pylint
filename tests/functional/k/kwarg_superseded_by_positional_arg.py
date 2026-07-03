"""
The `kwarg-superseded-by-positional-arg` warning message is emitted when a function is called with
a keyword argument which shares a name with a positional-only parameter and
the function contains a keyword variadic parameter dictionary.
It may be surprising behaviour when the keyword argument is added to the
keyword variadic parameter dictionary.
"""


def name1(apple, /, banana="Yellow banana", **kwargs):
    """
    Positional-only parameter, positional-or-keyword parameter and `**kwargs`.

    >>> name1("Red apple", apple="Green apple", banana="Green banana")
    Red apple
    Green banana
    {"apple": "Green apple"}
    """

    print(apple)
    print(banana)
    print(kwargs)


# +1: [kwarg-superseded-by-positional-arg]
name1("Red apple", apple="Green apple", banana="Green banana")
name1("Red apple", banana="Green banana")


def name2(apple="Green apple", /, **kwargs):
    """
    >>> name2(apple="Red apple")
    Green apple
    {'apple': 'Red apple'}
    """
    print(apple)
    print(kwargs)

name2(apple="Red apple")  # [kwarg-superseded-by-positional-arg]
