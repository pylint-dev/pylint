"""Checks for unnecessary-dunder-call on __aiter__/__anext__ with py-version=3.9."""


class MyClass:
    """A class implementing __aiter__ and __anext__."""

    def __aiter__(self):
        ...

    async def __anext__(self):
        ...


MyClass().__aiter__()
MyClass().__anext__()
