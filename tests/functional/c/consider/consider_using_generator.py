# pylint: disable=missing-docstring, invalid-name
# https://github.com/pylint-dev/pylint/issues/3165

import asyncio


async def arange(n: int):
    for i in range(n):
        await asyncio.sleep(0.0)
        yield i


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

list([0 async for y in arange(10)])
tuple([0 async for y in arange(10)])
sum([x*x async for x in arange(10)])
min([x*x async for x in arange(10)])
max([x*x async for x in arange(10)])

list([0 for z in list(range(10)) for z in list(range(10))])  # [consider-using-generator]
tuple([0 for z in list(range(10)) for z in list(range(10))])  # [consider-using-generator]
sum([x*y for x in range(10) for y in range(10)])  # [consider-using-generator]
min([x*y for x in range(10) for y in range(10)])  # [consider-using-generator]
max([x*y for x in range(10) for y in range(10)])  # [consider-using-generator]

list([0 async for z in arange(10) for z in range(10)])
tuple([0 async for z in arange(10) for z in range(10)])
sum([x*x async for x in arange(10) for y in range(10)])
min([x*x async for x in arange(10) for y in range(10)])
max([x*x async for x in arange(10) for y in range(10)])

list([0 for z in range(10) async for z in arange(10)])
tuple([0 for z in range(10) async for z in arange(10)])
sum([x*x for x in range(10) async for y in arange(10)])
min([x*x for x in range(10) async for y in arange(10)])
max([x*x for x in range(10) async for y in arange(10)])

list([0 async for z in arange(10) async for z in arange(10)])
tuple([0 async for z in arange(10) async for z in arange(10)])
sum([x*x async for x in arange(10) async for y in arange(10)])
min([x*x async for x in arange(10) async for y in arange(10)])
max([x*x async for x in arange(10) async for y in arange(10)])

list(0 for y in list(range(10)))
tuple(0 for y in list(range(10)))
sum(x*x for x in range(10))
min(x*x for x in range(10))
max(x*x for x in range(10))

list(0 async for y in arange(10))
tuple(0 async for y in arange(10))
sum(x*x async for x in arange(10))
min(x*x async for x in arange(10))
max(x*x async for x in arange(10))

list(0 for z in list(range(10)) for z in list(range(10)))
tuple(0 for z in list(range(10)) for z in list(range(10)))
sum(x*y for x in range(10) for y in range(10))
min(x*y for x in range(10) for y in range(10))
max(x*y for x in range(10) for y in range(10))

list(0 async for z in arange(10) for z in range(10))
tuple(0 async for z in arange(10) for z in range(10))
sum(x*y async for x in arange(10) for y in range(10))
min(x*y async for x in arange(10) for y in range(10))
max(x*y async for x in arange(10) for y in range(10))

list(0 for z in range(10) async for z in arange(10))
tuple(0 for z in range(10) async for z in arange(10))
sum(x*y for x in range(10) async for y in arange(10))
min(x*y for x in range(10) async for y in arange(10))
max(x*y for x in range(10) async for y in arange(10))

list(0 async for z in arange(10) async for z in arange(10))
tuple(0 async for z in arange(10) async for z in arange(10))
sum(x*y async for x in arange(10) async for y in arange(10))
min(x*y async for x in arange(10) async for y in arange(10))
max(x*y async for x in arange(10) async for y in arange(10))

# Keyword arguments
# https://github.com/pylint-dev/pylint/issues/8563
min([x*x for x in range(10)], default=42)  # [consider-using-generator]
min([x*x async for x in arange(10)], default=42)
min((x*x for x in range(10)), default=42)

min([x*y for x in range(10) for y in range(10)], default=42)  # [consider-using-generator]
min([x*y async for x in arange(10) for y in range(10)], default=42)
min([x*y for x in range(10) async for y in arange(10)], default=42)
min([x*y async for x in arange(10) async for y in arange(10)], default=42)
min((x*y for x in range(10) for y in range(10)), default=42)
