import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def async_context():
    yield


async def main():
    async with async_context():
        print("This works correctly")
