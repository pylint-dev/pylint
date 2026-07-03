"""
Test that no StopIteration is raised inside a generator
"""
# pylint: disable=missing-docstring,invalid-name,import-error, try-except-raise, wrong-import-position
# pylint: disable=not-callable,raise-missing-from,broad-exception-raised,use-yield-from
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
# because of the possibility that next raises a StopIteration exception
def gen_next_raises_stopiter():
    g = gen_ok()
    while True:
        yield next(g)  # [stop-iteration-return]


# This one is the same as gen_next_raises_stopiter
# but is ok because the next function is inside
# a try/except block handling StopIteration
def gen_next_inside_try_except():
    g = gen_ok()
    while True:
        try:
            yield next(g)
        except StopIteration:
            return


# This one is the same as gen_next_inside_try_except
# but is not ok because the next function is inside
# a try/except block that don't handle StopIteration
def gen_next_inside_wrong_try_except():
    g = gen_ok()
    while True:
        try:
            yield next(g)  # [stop-iteration-return]
        except ValueError:
            return


# This one is the same as gen_next_inside_try_except
# but is not ok because the next function is inside
# a try/except block that handle StopIteration but reraise it
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
            yield next(g)  # [stop-iteration-return]
        except ValueError:
            raise


def gen_dont_crash_on_uninferable():
    # https://github.com/pylint-dev/pylint/issues/1779
    yield from iter()
    raise asyncio.TimeoutError()


# https://github.com/pylint-dev/pylint/issues/1830
def gen_next_with_sentinel():
    yield next([], 42)  # No bad return


from itertools import count, cycle

# https://github.com/pylint-dev/pylint/issues/2158
def generator_using_next():
    counter = count()
    number = next(counter)
    yield number * 2

# https://github.com/pylint-dev/pylint/issues/7765
def infinite_iterator_itertools_cycle():
    counter = cycle('ABCD')
    val = next(counter)
    yield val


# pylint: disable=too-few-public-methods
class SomeClassWithNext:
    def next(self):
        return iter([1, 2, 3])

    def some_gen(self):
        for value in self.next():
            yield value


SomeClassWithNext().some_gen()


def something_invalid():
    raise Exception("cannot iterate this")


def invalid_object_passed_to_next():
    yield next(something_invalid())  # [stop-iteration-return]


# pylint: disable=redefined-builtin,too-many-function-args
def safeiter(it):
    """Regression test for issue #7610 when ``next`` builtin is redefined"""

    def next():
        while True:
            try:
                return next(it)
            except StopIteration:
                raise

    it = iter(it)
    while True:
        yield next()

def other_safeiter(it):
    """Regression test for issue #7610 when ``next`` builtin is redefined"""

    def next(*things):
        print(*things)
        while True:
            try:
                return next(it)
            except StopIteration:
                raise

    it = iter(it)
    while True:
        yield next(1, 2)

def data(filename):
    """
    Ensure pylint doesn't crash if `next` is incorrectly called without args
    See https://github.com/pylint-dev/pylint/issues/7828
    """
    with open(filename, encoding="utf8") as file:
        next() # attempt to skip header but this is incorrect code
        for line in file:
            yield line
