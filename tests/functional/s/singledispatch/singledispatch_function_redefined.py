# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, too-few-public-methods

from functools import singledispatch, singledispatchmethod

# --- singledispatch function case ---
@singledispatch
def process(value):
    return f"default handler for {value!r}"

@process.register(int)
def _(value):
    return f"int handler for {value}"

@process.register(str)
def _(value):
    return f"str handler for {value}"

# --- singledispatchmethod case ---
class Handler:
    @singledispatchmethod
    def handle(self, value):
        return f"default method handler for {value!r}"

    @handle.register(int)
    def _(self, value):
        return f"int method handler for {value}"

    @handle.register(str)
    def _(self, value):
        return f"str method handler for {value}"
