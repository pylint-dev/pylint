from contextlib import asynccontextmanager


@asynccontextmanager
async def async_context():
    yield


with async_context():  # [async-context-manager-with-regular-with]
    print("This will cause an error at runtime")
