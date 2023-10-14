# pylint: disable = missing-docstring, unused-variable
import contextlib
from contextlib import contextmanager
import weakref

# Positive


@contextlib.contextmanager
def cm():  # [contextmanager-generator-missing-cleanup]
    print("cm enter")
    a = yield
    print("cm exit")


@contextmanager
def bad_error_handler_cm():  # [contextmanager-generator-missing-cleanup]
    print("cm enter")
    try:
        a = yield
    except ValueError:
        pass
    print("cm exit")


def genfunc():
    with cm():
        print("stepping")
        yield


def main():
    gen = genfunc()
    ref = weakref.ref(gen, print)
    next(gen)


# Negative


@contextlib.contextmanager
def good_contextmanager():
    print("good cm enter")
    try:
        a = yield
    finally:
        print("good cm exit")


@contextmanager
def other_good_contextmanager():
    print("good cm enter")
    try:
        a = yield
    finally:
        print("good cm exit")


@contextmanager
def good_cm_except():
    print("good cm enter")
    try:
        a = yield
    except GeneratorExit:
        print("good cm exit")
