# pylint: disable=missing-module-docstring, missing-class-docstring,
# pylint: disable=missing-function-docstring, unused-private-member


class Apples:
    def __hello__(self):  # [bad-dunder-name]
        print("hello")

    def hello(self):
        print("hello")

    def init(self):
        # valid name even though someone could accidentally mean __init__
        pass

    def __init_(self):  # [bad-dunder-name]
        pass

    def _init_(self):  # [bad-dunder-name]
        pass

    def ___neg__(self):  # [bad-dunder-name]
        pass

    def __inv__(self):  # [bad-dunder-name]
        pass


def __increase_me__(val):
    return val + 1
