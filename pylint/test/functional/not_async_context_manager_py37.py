# pylint: disable=missing-docstring

from contextlib import asynccontextmanager


@asynccontextmanager
async def context_manager(value):
    yield value


async with context_manager(42) as ans:
    assert ans == 42
