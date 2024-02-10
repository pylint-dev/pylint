# pylint: disable=missing-docstring, import-error, yield-outside-function
import factory
from magic import shazam, turbogen

yield 1

def bad(generator):
    for item in generator:
        yield item  # [use-yield-from]


def out_of_names():
    for item in turbogen():
        yield item  # [use-yield-from]


def good(generator):
    for item in generator:
        shazam()
        yield item


def yield_something():
    yield 5


def yield_attr():
    for item in factory.gen():
        yield item  # [use-yield-from]


def yield_attr_nested():
    for item in factory.kiwi.gen():
        yield item  # [use-yield-from]


def yield_expr():
    for item in [1, 2, 3]:
        yield item  # [use-yield-from]


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
