""" Checks that reversed() receive proper argument """
# pylint: disable=missing-docstring,invalid-name,unused-variable
# pylint: disable=too-few-public-methods


def test():
    def parent():
        a = 42

        def stuff():
            nonlocal a

    c = 24

    def parent2():
        a = 42

        def stuff():
            def other_stuff():
                nonlocal a
                nonlocal c


b = 42


def func():
    def other_func():
        nonlocal b  # [nonlocal-without-binding]

    # Case where `nonlocal-without-binding` was not emitted when
    # the nonlocal name was assigned later in the same scope.
    # https://github.com/pylint-dev/pylint/issues/6883
    def other_func2():
        nonlocal c  # [nonlocal-without-binding]
        c = 1


class SomeClass:
    nonlocal x  # [nonlocal-without-binding]

    def func(self):
        nonlocal some_attr  # [nonlocal-without-binding]


def func2():
    nonlocal_ = None
    local = None

    class Class:

        nonlocal nonlocal_

        nonlocal_ = 1
        local = 1

    return local + nonlocal_


def function():
    """Test for `unused-variable` when multiple-assignment contains a `nonlocal`"""
    myint, mylist = 0, []

    print(mylist)

    def inner():
        nonlocal myint
        mylist.append(myint)
        myint += 1

    return inner()


nonlocal APPLE  # [nonlocal-without-binding]
APPLE = 42
