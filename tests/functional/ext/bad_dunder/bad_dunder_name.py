# pylint: disable=missing-module-docstring, missing-class-docstring,
# pylint: disable=missing-function-docstring, unused-private-member


class Apples:
    __slots__ = ("a", "b")

    def __hello__(self):  # [bad-dunder-name]
        # not one of the explicitly defined dunder name methods
        print("hello")

    def hello(self):
        print("hello")

    def __init__(self):
        pass

    def init(self):
        # valid name even though someone could accidentally mean __init__
        pass

    def __init_(self):  # [bad-dunder-name]
        # author likely unintentionally misspelled the correct init dunder.
        pass

    def _init_(self):  # [bad-dunder-name]
        # author likely unintentionally misspelled the correct init dunder.
        pass

    def ___neg__(self):  # [bad-dunder-name]
        # author likely accidentally added an additional `_`
        pass

    def __inv__(self):  # [bad-dunder-name]
        # author likely meant to call the invert dunder method
        pass

    def __allowed__(self):
        # user-configured allowed dunder name
        pass

    def _protected_method(self):
        print("Protected")

    def __private_method(self):
        print("Private")

    @property
    def __doc__(self):
        return "Docstring"

    def __index__(self):
        return 1


def __increase_me__(val):
    return val + 1
