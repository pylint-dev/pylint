# pylint: disable=missing-docstring, invalid-name
# https://github.com/pylint-dev/pylint/issues/3165

import asyncio

any([])
all([])

any([0 for x in list(range(10))]) # [use-a-generator]
all([0 for y in list(range(10))]) # [use-a-generator]

any(0 for x in list(range(10)))
all(0 for y in list(range(10)))


# https://github.com/pylint-dev/pylint/issues/7271
# An asynchronous comprehension would become an asynchronous generator,
# which any() and all() cannot consume.
async def apples():
    for apple in range(10):
        await asyncio.sleep(0)
        yield apple


async def is_ripe(apple):
    await asyncio.sleep(0)
    return apple % 2


async def basket():
    await asyncio.sleep(0)
    return list(range(10))


async def main():
    any([apple async for apple in apples()])
    all([apple async for apple in apples()])
    # Any of the generators can be the asynchronous one.
    any([apple for apple in range(10) async for _ in apples()])
    all([apple for apple in range(10) async for _ in apples()])
    # An await has the same effect as an 'async for'.
    any([await is_ripe(apple) for apple in range(10)])
    all([apple for apple in range(10) if await is_ripe(apple)])
    # The outermost iterable is evaluated outside of the generator, so awaiting
    # there is fine.
    any([apple > 1 for apple in await basket()]) # [use-a-generator]
    all([apple > 1 for apple in await basket()]) # [use-a-generator]
