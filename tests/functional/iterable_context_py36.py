# pylint: disable=missing-docstring,too-few-public-methods,unused-variable
import asyncio

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


async def some_iter_func(number):
    """ emits 1 number per second  """
    for i in range(1, number):
        yield i
        await asyncio.sleep(1)


async def count_to(number):
    """ counts to n in async manner"""
    async for i in some_iter_func(number):
        print(i)


async def gen_values(num_values):
    for value in range(num_values):
        yield value


async def do_some_comprehensions():
    sets = {elem async for elem in gen_values(10)}
    lists = [elem async for elem in gen_values(10)]
    dicts = {elem: elem async for elem in gen_values(10)}
    gen = (elem async for elem in gen_values(10))
    return sets, lists, dicts, gen
