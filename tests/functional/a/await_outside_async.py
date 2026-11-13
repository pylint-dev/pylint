# pylint: disable=missing-docstring,unused-variable
import asyncio

async def nested():
    return 42

async def main():
    nested()
    print(await nested())  # This is okay

def not_async():
    print(await nested())  # [await-outside-async]


async def func(i):
    return i**2

async def okay_function():
    var = [await func(i) for i in range(5)]  # This should be okay


# Test nested functions
async def func2():
    def inner_func():
        await asyncio.sleep(1)  # [await-outside-async]


def outer_func():
    async def inner_func():
        await asyncio.sleep(1)

# pylint: disable=unnecessary-lambda-assignment
async def func3():
    f = lambda: await nested() # [await-outside-async]


# An ``await`` inside a generator expression makes it an asynchronous generator
# expression, which is allowed outside of an async function (#10074).
# The first iterable is evaluated in the enclosing scope, so ``await`` there
# is still reported.
def sync_with_async_genexp(items):
    print(await item for item in items)
    print(item for item in await nested())  # [await-outside-async]
    print(other for item in items for other in await item)
    print(item for item in items if await item)
    print((await item for item in items) for _ in items)
    print((item for item in await nested()) for _ in items)
    print([(item for item in await nested()) for _ in items])  # [await-outside-async]
    print((lambda: await nested()) for _ in items)  # [await-outside-async]


ASYNC_GENEXP = (await item for item in range(5))
NOT_ASYNC_GENEXP = (item for item in await nested())  # [await-outside-async]
