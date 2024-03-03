# pylint: disable = missing-docstring, unused-variable
import contextlib
from contextlib import contextmanager

# Positive


@contextlib.contextmanager
def cm():
    contextvar = "acquired context"
    print("cm enter")
    yield contextvar
    print("cm exit")


def genfunc_with_cm():  # [contextmanager-generator-missing-cleanup]
    with cm() as context:
        yield context * 2


@contextmanager
def name_cm():
    contextvar = "acquired context"
    print("cm enter")
    yield contextvar
    print("cm exit")


def genfunc_with_name_cm():  # [contextmanager-generator-missing-cleanup]
    with name_cm() as context:
        yield context * 2


# Negative


@contextlib.contextmanager
def good_cm_except():
    contextvar = "acquired context"
    print("good cm enter")
    try:
        yield contextvar
    except GeneratorExit:
        print("good cm exit")


def good_genfunc_with_cm():
    with good_cm_except() as context:
        yield context * 2


def genfunc_with_discard():
    with good_cm_except():
        yield "discarded"


@contextlib.contextmanager
def good_cm_yield_none():
    print("good cm enter")
    yield
    print("good cm exit")


def genfunc_with_none_yield():
    with good_cm_yield_none() as var:
        print(var)
        yield "discarded"


@contextlib.contextmanager
def good_cm_finally():
    contextvar = "acquired context"
    print("good cm enter")
    try:
        yield contextvar
    finally:
        print("good cm exit")


def good_cm_finally_genfunc():
    with good_cm_finally() as context:
        yield context * 2
