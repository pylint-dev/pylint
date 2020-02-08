# pylint: disable=missing-docstring, too-few-public-methods, useless-object-inheritance


class AsyncSuperClass:
    async def async_func(self, arg):
        pass


class SuperClass:
    def func(self, arg):
        pass


class AsyncDerivedValid(AsyncSuperClass):
    async def async_func(self, arg):
        return arg


class AsyncDerivedInvalid(AsyncSuperClass):
    def async_func(self, arg):  # [invalid-overridden-coroutine]
        return arg


class DerivedValid(SuperClass):
    def func(self, arg):
        return arg


class DerivedInvalid(SuperClass):
    async def func(self, arg):  # [invalid-overridden-coroutine]
        return arg
