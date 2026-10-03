class AsyncContextManager:
    def __aenter__(self):
        pass

    def __aexit__(self, *exc):
        pass


async def foo():
    async with AsyncContextManager():
        pass
