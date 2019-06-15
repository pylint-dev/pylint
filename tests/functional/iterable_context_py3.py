"""
Checks that iterable metaclasses are recognized by pylint.
"""
# pylint: disable=missing-docstring,too-few-public-methods,no-init,no-self-use,unused-argument,bad-mcs-method-argument
# pylint: disable=wrong-import-position
# metaclasses as iterables
class Meta(type):
    def __iter__(self):
        return iter((1, 2, 3))

class SomeClass(metaclass=Meta):
    pass


for i in SomeClass:
    print(i)
for i in SomeClass():  # [not-an-iterable]
    print(i)


import asyncio


@asyncio.coroutine
def coroutine_function_return_none():
    return


@asyncio.coroutine
def coroutine_function_return_object():
    return 12


@asyncio.coroutine
def coroutine_function_return_future():
    return asyncio.Future()


@asyncio.coroutine
def coroutine_function_pass():
    pass


@asyncio.coroutine
def coroutine_generator():
    yield


@asyncio.coroutine
def main():
    yield from coroutine_function_return_none()
    yield from coroutine_function_return_object()
    yield from coroutine_function_return_future()
    yield from coroutine_function_pass()
    yield from coroutine_generator()
