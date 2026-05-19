# pylint: disable=import-error, missing-module-docstring, missing-function-docstring, missing-class-docstring, too-few-public-methods, unused-variable

from mod import A  # [unguarded-typing-import]
from mod import B


def f(_: A):
    pass


def g(x: B):
    assert isinstance(x, B)


class C:
    pass


class D:
    c: C

    def h(self):
        return [C() for _ in self.c]


def fn():
    d: C
    return [C() for _ in range(3)]
