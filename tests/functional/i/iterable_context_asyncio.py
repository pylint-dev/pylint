"""
Checks that we don't erroneously emit not-an-iterable errors for
coroutines built with asyncio.coroutine.

These decorators were deprecated in 3.8 and removed in 3.11.
"""
# pylint: disable=missing-docstring,too-few-public-methods,unused-argument,bad-mcs-method-argument
# pylint: disable=wrong-import-position
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
