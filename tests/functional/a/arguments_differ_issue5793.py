"""Better message when the parameter kinds differ but the total count does not.

https://github.com/pylint-dev/pylint/issues/5793
"""

# pylint: disable=missing-class-docstring, missing-function-docstring, too-few-public-methods


class Base:
    def fun(self, var):
        print(var)

    def keyword_to_keyword_only(self, param1, /, param2):
        return param1 + param2

    def keyword_only_renamed(self, param1, *, param2):
        return param1 + param2

    def renamed_before_variadic(self, param1, *args):
        return param1, args


class Child(Base):
    def fun(self, *, var):  # [arguments-differ]
        print(var)

    def keyword_to_keyword_only(self, param1, /, *, param2):  # [arguments-differ]
        return param1 - param2

    def keyword_only_renamed(self, param1, *, param3):  # [arguments-differ]
        return param1 - param3

    def renamed_before_variadic(self, param3, *args):  # [arguments-differ]
        return param3, args


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
