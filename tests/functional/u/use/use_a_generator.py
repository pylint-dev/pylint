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
async def grow_apples():
    for apple in range(10):
        await asyncio.sleep(0)
        yield apple


async def pick_apples():
    await asyncio.sleep(0)
    return list(range(10))


async def is_ripe(apple):
    await asyncio.sleep(0)
    return apple % 2


def is_red(apple):
    return apple % 2 == 0


async def main():
    any([apple async for apple in grow_apples()])
    all([apple async for apple in grow_apples()])
    # Any of the generators can be the asynchronous one.
    any([apple for apple in range(10) async for _ in grow_apples()])
    all([apple for apple in range(10) async for _ in grow_apples()])
    # An await has the same effect as an 'async for'.
    any([await is_ripe(apple) for apple in range(10)])
    all([apple for apple in range(10) if await is_ripe(apple)])
    # The outermost iterable is evaluated outside of the generator, so awaiting
    # there is fine.
    any([is_red(apple) for apple in await pick_apples()]) # [use-a-generator]
    all([is_red(apple) for apple in await pick_apples()]) # [use-a-generator]
