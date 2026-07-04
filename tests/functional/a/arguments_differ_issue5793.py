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
