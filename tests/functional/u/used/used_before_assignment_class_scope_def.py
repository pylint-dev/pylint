"""A class body may use a module-level or builtin name that a later method shadows.

Names in a class body are looked up in the class namespace first and then in the
globals and builtins. A ``def`` or ``class`` further down the class body has not
run yet, so it does not shadow the outer name at that point.

https://github.com/pylint-dev/pylint/issues/9134
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=too-few-public-methods,invalid-name,unused-argument
from os import path
from string import Template


class ModuleNameShadowedByMethod:
    joined = path.join("a", "b")

    def path(self):
        return self


class ModuleNameShadowedByNestedClass:
    joined = path.join("a", "b")

    class path:
        pass


class ModuleNameShadowedByAsyncMethod:
    joined = path.join("a", "b")

    async def path(self):
        return self


class ModuleClassShadowedByMethod:
    template = Template("$a")

    def Template(self):
        return self


class ModuleNameUsedInDecorator:
    @staticmethod
    def make(arg=path.join("a")):
        return arg

    def path(self):
        return self


class BuiltinShadowedByMethod:
    length = len("abc")

    def len(self):
        return self


class NameOnlyDefinedByLaterMethod:
    joined = missing.join("a")  # [used-before-assignment]

    def missing(self):
        return self


class NameUsedInsideMethodBody:
    def method(self):
        return path.join("a"), Template("$a")

    def path(self):
        return self


class NameUsedAfterMethod:
    def path(self):
        return self

    joined = path(None)
