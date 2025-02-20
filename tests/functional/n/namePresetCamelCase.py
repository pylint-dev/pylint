# pylint: disable=missing-docstring,too-few-public-methods,unused-private-member
__version__ = "1.0"
SOME_CONSTANT = 42  # [invalid-name]


def sayHello(someArgument):
    return [someArgument * someValue for someValue in range(10)]


class MyClass:  # [invalid-name]
    def __init__(self, argX):
        self._mySecretX = argX

    @property
    def myPublicX(self):
        return self._mySecretX * 2

    def __eq__(self, other):
        return isinstance(other, MyClass) and self.myPublicX == other.myPublicX

    def __privateMethod(self):
        pass

    def _protectedMethod(self):
        pass

def say_hello():  # [invalid-name]
    pass
