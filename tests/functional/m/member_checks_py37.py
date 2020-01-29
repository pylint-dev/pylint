# pylint: disable=missing-docstring
import collections
import asyncio

isinstance([], collections.Iterable)


async def gen():
    await asyncio.sleep(0.1)
    value = yield 42
    print(value)
    await asyncio.sleep(0.2)


async def test():
    generator = gen()

    await generator.asend(None)
    await generator.send(None)  # [no-member]
