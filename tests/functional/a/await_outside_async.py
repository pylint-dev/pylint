# pylint: disable=missing-docstring
import asyncio

async def nested():
    return 42

async def main():
    nested()

    print(await nested())  # This is okay

asyncio.run(main())

def not_async():
    print(await nested())  # [await-outside-async]
