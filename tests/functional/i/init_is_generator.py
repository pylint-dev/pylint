# pylint: disable=missing-docstring,too-few-public-methods

class SomeClass:
    def __init__(self): # [init-is-generator]
        yield None
