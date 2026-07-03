class ContextManager:
    def __enter__(self):
        pass

    def __exit__(self, *exc):
        pass


async def foo():
    async with ContextManager():  # [not-async-context-manager]
        pass
