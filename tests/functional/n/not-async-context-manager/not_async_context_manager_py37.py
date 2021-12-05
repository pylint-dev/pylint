# pylint: disable=missing-docstring

from contextlib import asynccontextmanager


@asynccontextmanager
async def context_manager(value):
    yield value


async with context_manager(42) as ans:
    assert ans == 42


def async_context_manager():
    @asynccontextmanager
    async def wrapper():
        pass
    return wrapper

async def func():
    async with async_context_manager():
        pass
