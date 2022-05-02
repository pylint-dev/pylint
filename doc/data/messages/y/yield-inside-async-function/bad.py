async def foo():
    yield from [1, 2, 3]  # [yield-inside-async-function]
