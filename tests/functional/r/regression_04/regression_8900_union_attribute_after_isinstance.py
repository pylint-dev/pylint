"""Regression test for https://github.com/pylint-dev/pylint/issues/8900

An attribute set in both branches of an ``if`` to two different classes,
then narrowed with ``isinstance``, is an instance of the narrowed class:
setting its attribute is not defining one outside ``__init__``. Example from
https://github.com/pylint-dev/pylint/issues/11470. Fixed in astroid by
pylint-dev/astroid#3387.
"""

# pylint: disable=missing-docstring,too-few-public-methods,using-constant-test


class Apple:
    def __init__(self, size: int):
        self.size: int = size


class Banana:
    pass


class Basket:
    fruit: Apple | Banana

    def __init__(self) -> None:
        if True:
            self.fruit: Apple = Apple(size=1)
        else:
            self.fruit: Banana = Banana()

    def grow(self) -> None:
        if not isinstance(self.fruit, Apple):
            raise TypeError("not an apple")
        apple: Apple = self.fruit
        apple.size = 2
