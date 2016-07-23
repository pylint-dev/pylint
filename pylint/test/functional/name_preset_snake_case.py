# pylint: disable=old-style-class,missing-docstring,too-few-public-methods
SOME_CONSTANT = 42


def say_hello(some_argument):
    return [some_argument * some_value for some_value in range(10)]


class MyClass:
    def __init__(self, arg_x):
        self._my_secret_x = arg_x

    @property
    def my_public_x(self):
        return self._my_secret_x * 2


def sayHello():  # [invalid-name]
    pass
