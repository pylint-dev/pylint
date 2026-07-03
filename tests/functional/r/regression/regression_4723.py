"""Latest version of astroid (2.6.3) causes RuntimeError:
generator raised StopIteration #4723"""
# pylint: disable=invalid-name,missing-docstring,too-few-public-methods

import contextlib


class A:
    @contextlib.contextmanager
    def get(self):
        yield self


class B(A):
    def play():  # [no-method-argument]
        pass


def func():
    with B().get() as b:
        b.play()  # [too-many-function-args]
