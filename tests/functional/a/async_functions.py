"""Check that Python 3.5's async functions are properly analyzed by Pylint."""
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# pylint: disable=using-constant-test, useless-object-inheritance

async def next(): # [redefined-builtin]
    pass

async def some_function(arg1, arg2): # [unused-argument]
    await arg1


class OtherClass(object):

    @staticmethod
    def test():
        return 42


class Class(object):

    async def some_method(self):
        super(OtherClass, self).test() # [bad-super-call]


# +1: [too-many-arguments,too-many-return-statements, too-many-branches]
async def complex_function(this, function, has, more, arguments, than,
                           one, _, should, have):
    if 1:
        return this
    if 1:
        return function
    if 1:
        return has
    if 1:
        return more
    if 1:
        return arguments
    if 1:
        return than
    try:
        return one
    finally:
        pass
    if 2:
        return should
    while True:
        pass
    if 1:
        return have
    if 2:
        return function
    if 3:
        pass


# +1: [duplicate-argument-name, duplicate-argument-name, dangerous-default-value]
async def func(a, a, b=[]):
    return a, b


# +1: [empty-docstring, blacklisted-name]
async def foo():
    ""
