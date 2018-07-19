# pylint: disable=missing-docstring,too-few-public-methods,unused-variable


class AIter:
    async def __aiter__(self):
        for value in range(20):
            yield value

    async def to_list(self):
        values = [m async for m in self]
        other_values = [m for m in self] # [not-an-iterable]
        for value in self: # [not-an-iterable]
            yield value
        async for value in self:
            yield value
