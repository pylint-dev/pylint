"""
Test that no StopIteration is raised inside a generator
"""
# pylint: disable=missing-docstring,invalid-name,import-error
import asyncio

class RebornStopIteration(StopIteration):
    """
    A class inheriting from StopIteration exception
    """

# This one is ok
def gen_ok():
    yield 1
    yield 2
    yield 3
    return

# pylint should warn about this one
# because of a direct raising of StopIteration inside generator
def gen_stopiter():
    yield 1
    yield 2
    yield 3
    raise StopIteration  # [stop-iteration-return]

# pylint should warn about this one
# because of a direct raising of an exception inheriting from StopIteration inside generator
def gen_stopiterchild():
    yield 1
    yield 2
    yield 3
    raise RebornStopIteration  # [stop-iteration-return]

# pylint should warn here
# because of the possibility that next raises a StopIteration exception
def gen_next_raises_stopiter():
    g = gen_ok()
    while True:
        yield next(g)  # [stop-iteration-return]

# This one is the same as gen_next_raises_stopiter
# but is ok because the next function is inside
# a try/except block handling StopIteration
def gen_next_inside_try_except():
    g = gen_ok()
    while True:
        try:
            yield next(g)
        except StopIteration:
            return

# This one is the same as gen_next_inside_try_except
# but is not ok because the next function is inside
# a try/except block that don't handle StopIteration
def gen_next_inside_wrong_try_except():
    g = gen_ok()
    while True:
        try:
            yield next(g)  # [stop-iteration-return]
        except ValueError:
            return

# This one is the same as gen_next_inside_try_except
# but is not ok because the next function is inside
# a try/except block that handle StopIteration but reraise it
def gen_next_inside_wrong_try_except2():
    g = gen_ok()
    while True:
        try:
            yield next(g)
        except StopIteration:
            raise StopIteration  # [stop-iteration-return]

# Those two last are ok
def gen_in_for():
    for el in gen_ok():
        yield el

def gen_yield_from():
    yield from gen_ok()


def gen_dont_crash_on_no_exception():
    g = gen_ok()
    while True:
        try:
            yield next(g) # [stop-iteration-return]
        except ValueError:
            raise


def gen_dont_crash_on_uninferable():
    # https://github.com/PyCQA/pylint/issues/1779
    yield from iter()
    raise asyncio.TimeoutError()
