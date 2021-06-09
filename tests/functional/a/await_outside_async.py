# pylint: disable=missing-docstring, unused-variable
import asyncio

async def nested():
    return 42

async def main():
    nested()

    print(await nested())  # This is okay

asyncio.run(main())

def not_async():
    print(await nested())  # [await-outside-async]

async def func(i):
    return i**2

async def okay_function():
    var = [await func(i) for i in range(5)]  # This should be okay
