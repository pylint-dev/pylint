# pylint: disable=old-style-class,missing-docstring,too-few-public-methods
SOME_CONSTANT = 42


def sayHello(someArgument):
    return [someArgument * someValue for someValue in range(10)]


class MyClass:
    def __init__(self, argX):
        self._mySecretX = argX

    @property
    def myPublicX(self):
        return self._mySecretX * 2


def say_hello():  # [invalid-name]
    pass
