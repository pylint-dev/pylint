# pylint: disable=missing-docstring, invalid-name
# https://github.com/pylint-dev/pylint/issues/3165

import asyncio


async def arange(n: int):
    for i in range(n):
        await asyncio.sleep(0.0)
        yield i


any([])
all([])

any([0 for x in list(range(10))]) # [use-a-generator]
all([0 for y in list(range(10))]) # [use-a-generator]

any([0 async for x in arange(10)])
all([0 async for y in arange(10)])

any([0 for x in list(range(10)) for y in list(range(10))]) # [use-a-generator]
all([0 for y in list(range(10)) for x in list(range(10))]) # [use-a-generator]

any([0 async for x in arange(10) for y in range(10)])
all([0 async for y in arange(10) for x in range(10)])

any([0 for x in range(10) async for y in arange(10)])
all([0 for y in range(10) async for x in arange(10)])

any([0 async for x in arange(10) async for y in arange(10)])
all([0 async for y in arange(10) async for x in arange(10)])

any(0 for x in list(range(10)))
all(0 for y in list(range(10)))

any(0 async for x in arange(10))
all(0 async for y in arange(10))

any(0 for x in list(range(10)) for y in list(range(10)))
all(0 for y in list(range(10)) for x in list(range(10)))

any(0 async for x in arange(10) for y in range(10))
all(0 async for y in arange(10) for x in range(10))

any(0 for x in range(10) async for y in arange(10))
all(0 for y in range(10) async for x in arange(10))

any(0 async for x in arange(10) async for y in arange(10))
all(0 async for y in arange(10) async for x in arange(10))
