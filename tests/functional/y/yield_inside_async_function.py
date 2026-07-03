"""Test that `yield` or `yield from` can't be used inside an async function."""
# pylint: disable=missing-docstring, unused-variable

async def good():
    def _inner():
        yield 42
        yield from [1, 2, 3]

async def good_two():
    # Starting from python 3.6 it's possible to yield inside async
    # https://www.python.org/dev/peps/pep-0525/
    yield 42


async def bad():
    yield from [1, 2, 3] # [yield-inside-async-function]
