# pylint: disable=missing-docstring, invalid-name
# https://github.com/pylint-dev/pylint/issues/3165

import asyncio

list([])
tuple([])
sum([])
min([])
max([])

list([0 for y in list(range(10))])  # [consider-using-generator]
tuple([0 for y in list(range(10))])  # [consider-using-generator]
sum([x*x for x in range(10)])  # [consider-using-generator]
min([x*x for x in range(10)])  # [consider-using-generator]
max([x*x for x in range(10)])  # [consider-using-generator]

list(0 for y in list(range(10)))
tuple(0 for y in list(range(10)))
sum(x*x for x in range(10))
min(x*x for x in range(10))
max(x*x for x in range(10))

# Keyword arguments
# https://github.com/pylint-dev/pylint/issues/8563
min([x*x for x in range(10)], default=42)  # [consider-using-generator]
min((x*x for x in range(10)), default=42)


# https://github.com/pylint-dev/pylint/issues/7271
# An asynchronous comprehension would become an asynchronous generator,
# which none of these functions can consume.
async def grow_apples():
    for apple in range(10):
        await asyncio.sleep(0)
        yield apple


async def pick_apples():
    await asyncio.sleep(0)
    return list(range(10))


async def weigh(apple):
    await asyncio.sleep(0)
    return apple * 100


def is_red(apple):
    return apple % 2 == 0


async def main():
    list([apple async for apple in grow_apples()])
    tuple([apple async for apple in grow_apples()])
    sum([apple async for apple in grow_apples()])
    min([apple async for apple in grow_apples()])
    max([apple async for apple in grow_apples()])
    min([apple async for apple in grow_apples()], default=42)
    # Any of the generators can be the asynchronous one.
    sum([apple for apple in range(10) async for _ in grow_apples()])
    # An await has the same effect as an 'async for'.
    sum([await weigh(apple) for apple in range(10)])
    sum([apple for apple in range(10) if await weigh(apple)])
    # The outermost iterable is evaluated outside of the generator, so awaiting
    # there is fine.
    sum([apple for apple in await pick_apples() if is_red(apple)])  # [consider-using-generator]
