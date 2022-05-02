async def foo():
    def _inner_foo():
        yield from [1, 2, 3]


async def foo():
    yield 42
