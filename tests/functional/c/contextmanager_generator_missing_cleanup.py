# pylint: disable = missing-docstring, unused-variable, bare-except, broad-exception-caught
from collections import namedtuple
import contextlib
from contextlib import contextmanager

# Positive


@contextlib.contextmanager
def cm():
    contextvar = "acquired context"
    print("cm enter")
    yield contextvar
    print("cm exit")


def genfunc_with_cm():
    with cm() as context:  # [contextmanager-generator-missing-cleanup]
        yield context * 2


@contextmanager
def name_cm():
    contextvar = "acquired context"
    print("cm enter")
    yield contextvar
    print("cm exit")


def genfunc_with_name_cm():
    with name_cm() as context:  # [contextmanager-generator-missing-cleanup]
        yield context * 2


def genfunc_with_cm_after():
    with after_cm() as context:  # [contextmanager-generator-missing-cleanup]
        yield context * 2


@contextlib.contextmanager
def after_cm():
    contextvar = "acquired context"
    print("cm enter")
    yield contextvar
    print("cm exit")


@contextmanager
def cm_with_improper_handling():
    contextvar = "acquired context"
    print("cm enter")
    try:
        yield contextvar
    except ValueError:
        pass
    print("cm exit")


def genfunc_with_cm_improper():
    with cm_with_improper_handling() as context:  # [contextmanager-generator-missing-cleanup]
        yield context * 2


# Negative


class Enterable:
    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, *args):
        print("exit")


def genfunc_with_enterable():
    enter = Enterable()
    with enter as context:
        yield context * 2


def genfunc_with_enterable_attr():
    EnterableTuple = namedtuple("EnterableTuple", ["attr"])
    t = EnterableTuple(Enterable())
    with t.attr as context:
        yield context.attr * 2


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


def genfunc_with_cm_finally_odd_body():
    with good_cm_finally() as context:
        if context:
            yield context * 2
        else:
            yield context * 3


@cm_with_improper_handling
def genfunc_wrapped():
    yield "wrapped"


@contextmanager
def cm_bare_handler():
    contextvar = "acquired context"
    print("cm enter")
    try:
        yield contextvar
    except:
        print("cm exit")


@contextmanager
def cm_base_exception_handler():
    contextvar = "acquired context"
    print("cm enter")
    try:
        yield contextvar
    except Exception:
        print("cm exit")


def genfunc_with_cm_bare_handler():
    with cm_bare_handler() as context:
        yield context * 2


def genfunc_with_cm_base_exception_handler():
    with cm_base_exception_handler() as context:
        yield context * 2


@contextlib.contextmanager
def good_cm_no_cleanup():
    contextvar = "acquired context"
    print("cm enter")
    yield contextvar


def good_cm_no_cleanup_genfunc():
    with good_cm_no_cleanup() as context:
        yield context * 2
