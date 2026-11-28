# pylint: disable=missing-module-docstring, missing-class-docstring,
# pylint: disable=missing-function-docstring, unused-private-member, too-few-public-methods
# pylint: disable=invalid-overridden-method


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


class AwaitedResults:
    # Python returns the coroutine unchanged: 'await basket[key]' works.
    async def __getitem__(self, key):
        return key

    async def __getattr__(self, name):
        return name

    async def __add__(self, other):
        return other

    async def __reversed__(self):
        return self


class AsyncGeneratorApples:
    async def __aiter__(self):
        yield 1


class AsyncMistakes:
    async def __aenterr__(self):  # [bad-dunder-name]
        return self

    async def __enter__(self):  # [bad-dunder-name]
        # only __aenter__ is awaited by 'async with'
        return self

    async def __exit__(self, *args):  # [bad-dunder-name]
        # the coroutine is truthy: every exception would be swallowed
        return False

    async def __iter__(self):  # [bad-dunder-name]
        return self

    async def __next__(self):  # [bad-dunder-name]
        return 1

    async def __aiter__(self):  # [bad-dunder-name]
        # 'async for' needs the async iterator itself, not a coroutine
        return self

    async def __await__(self):  # [bad-dunder-name]
        # must return an iterator, not a coroutine
        return self

    async def __init__(self):  # [bad-dunder-name]
        # a coroutine instead of None: TypeError when instantiated
        pass

    async def __eq__(self, other):  # [bad-dunder-name]
        # the coroutine is truthy: 'in' and dict lookups always match
        return False

    async def __setitem__(self, key, value):  # [bad-dunder-name]
        # the coroutine is discarded and never awaited
        pass


class AsyncCopyMistakes:
    async def __getstate__(self):  # [bad-dunder-name]
        # pickle cannot serialize the coroutine
        return {}

    async def __setstate__(self, state):  # [bad-dunder-name]
        # copy and pickle discard the coroutine and never await it
        pass

    async def __reduce_ex__(self, protocol):  # [bad-dunder-name]
        return (AsyncCopyMistakes, ())

    async def __getnewargs__(self):  # [bad-dunder-name]
        return ()

    async def __getnewargs_ex__(self):  # [bad-dunder-name]
        return ((), {})

    @classmethod
    async def __subclasshook__(cls, subclass):  # [bad-dunder-name]
        # issubclass() asserts True, False or NotImplemented
        return subclass is int


class MyError(Exception):
    @property
    def __suppress_context__(self):
        return True


def __increase_me__(val):
    return val + 1


async def __enter__(val):
    return val
