# pylint: disable=missing-docstring, import-error, yield-outside-function
import factory
from magic import shazam, turbogen

yield 1

def bad(generator):
    for item in generator:  # [use-yield-from]
        yield item


def out_of_names():
    for item in turbogen():  # [use-yield-from]
        yield item


def good(generator):
    for item in generator:
        shazam()
        yield item


def yield_something():
    yield 5


def yield_attr():
    for item in factory.gen():  # [use-yield-from]
        yield item


def yield_attr_nested():
    for item in factory.kiwi.gen():  # [use-yield-from]
        yield item


def yield_expr():
    for item in [1, 2, 3]:  # [use-yield-from]
        yield item


def for_else_yield(gen, something):
    for item in gen():
        if shazam(item):
            break
    else:
        yield something


# yield from is not supported in async functions, so the following are fine

async def async_for_yield(agen):
    async for item in agen:
        yield item


async def async_yield(agen):
    for item in agen:
        yield item


# If the return from `yield` is used inline, don't suggest delegation.

def yield_use_send():
    for item in (1, 2, 3):
        _ = yield item
    total = 0
    for item in (1, 2, 3):
        total += yield item
