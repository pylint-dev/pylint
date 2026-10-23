# pylint: disable=missing-module-docstring, missing-class-docstring,
# pylint: disable=missing-function-docstring, unused-private-member, too-few-public-methods


class Apples:
    __slots__ = ("a", "b")

    def __hello__(self):  # [bad-dunder-name]
        # not one of the explicitly defined dunder name methods
        print("hello")

    def hello(self):
        print("hello")

    def __init__(self):
        pass

    def init(self):
        # valid name even though someone could accidentally mean __init__
        pass

    def __init_(self):  # [bad-dunder-name]
        # author likely unintentionally misspelled the correct init dunder.
        pass

    def _init_(self):  # [bad-dunder-name]
        # author likely unintentionally misspelled the correct init dunder.
        pass

    def ___neg__(self):  # [bad-dunder-name]
        # author likely accidentally added an additional `_`
        pass

    def __inv__(self):  # [bad-dunder-name]
        # author likely meant to call the invert dunder method
        pass

    def __allowed__(self):
        # user-configured allowed dunder name
        pass

    def _protected_method(self):
        print("Protected")

    def __private_method(self):
        print("Private")

    @property
    def __doc__(self):
        return "Docstring"

    def __index__(self):
        return 1


class AsyncApples:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def __anext__(self):
        return 1

    async def __call__(self):
        return 1

    async def __allowed__(self):
        # user-configured allowed dunder name
        pass

    def __aiter__(self):
        return self

    def __await__(self):
        yield


class AsyncGeneratorApples:
    async def __aiter__(self):
        yield 1


class AsyncMistakes:
    async def __aenterr__(self):  # [bad-dunder-name]
        return self

    async def __enter__(self):  # [bad-dunder-name]
        # only __aenter__ is awaited by 'async with'
        return self

    async def __aiter__(self):  # [bad-dunder-name]
        # 'async for' needs the async iterator itself, not a coroutine
        return self

    async def __await__(self):  # [bad-dunder-name]
        # must return an iterator, not a coroutine
        return self

    async def __init__(self):  # [bad-dunder-name]
        # a coroutine instead of None: TypeError when instantiated
        pass


class MyError(Exception):
    @property
    def __suppress_context__(self):
        return True


def __increase_me__(val):
    return val + 1
