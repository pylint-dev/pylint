# pylint: disable=old-style-class,missing-docstring,too-few-public-methods
__version__ = "1.0"
SOME_CONSTANT = 42  # [invalid-name]


def say_hello(some_argument):
    return [some_argument * some_value for some_value in range(10)]


class MyClass:  # [invalid-name]
    def __init__(self, arg_x):
        self._my_secret_x = arg_x

    @property
    def my_public_x(self):
        return self._my_secret_x * 2

    def __eq__(self, other):
        return isinstance(other, MyClass) and self.my_public_x == other.my_public_x


def sayHello():  # [invalid-name]
    pass
