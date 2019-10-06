# pylint: disable=global-statement,missing-docstring,blacklisted-name
foo = "test"


def broken():
    global foo

    bar = len(foo)
    foo = foo[bar]
