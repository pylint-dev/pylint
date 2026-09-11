"""Better message when the parameter kinds differ but the total count does not.

https://github.com/pylint-dev/pylint/issues/5793
"""

# pylint: disable=missing-class-docstring, missing-function-docstring, too-few-public-methods


class Base:
    def fun(self, var):
        print(var)

    def positional_only(self, param1, param2, /):
        return param1 + param2


class Child(Base):
    def fun(self, *, var):  # [arguments-differ]
        print(var)

    def positional_only(self, param1, param2):  # [arguments-differ]
        return param1 - param2


class VariadicBase:
    def variadic_positional(self, *args):
        print(args)

    def variadic_keyword(self, **kwargs):
        print(kwargs)


class VariadicChild(VariadicBase):
    def variadic_positional(self, arg):  # [arguments-differ, arguments-differ]
        print(arg)

    def variadic_keyword(self, *, arg):  # [arguments-differ, arguments-differ]
        print(arg)
