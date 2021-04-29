# pylint: disable=missing-docstring,too-few-public-methods
class AbstractFoo:

    def kwonly_1(self, first: int, *, second: int, third: int):
        "Normal positional with two positional only params."

    def kwonly_2(self, *, first: str, second: str):
        "Two positional only parameter."

    def kwonly_3(self, *, first: str, second: str):
        "Two positional only params."

    def kwonly_4(self, *, first: str, second=None):
        "One positional only and another with a default."

    def kwonly_5(self, *, first: bool, **kwargs):
        "Keyword only and keyword variadics."

    def kwonly_6(self, first: float, second: float, *, third: int):
        "Two positional and one keyword"


class Foo(AbstractFoo):

    def kwonly_1(self, first: int, *, second: int): # [arguments-differ]
        "One positional and only one positional only param."

    def kwonly_2(self, *, first: str): # [arguments-differ]
        "Only one positional parameter instead of two positional only parameters."

    def kwonly_3(self, **kwargs):
        "Two positional params."

    def kwonly_4(self, *args): # [arguments-differ]
        "Two positional params."

    def kwonly_5(self, *, first: bool): # [arguments-differ]
        "Keyword only, but no variadics."

    def kwonly_6(self, *args, **kwargs): # valid override
        "Positional and keyword variadics to pass through parent params"


class Foo2(AbstractFoo):

    def kwonly_6(self, first, *args, **kwargs): # valid override
        "One positional with the rest variadics to pass through parent params"
