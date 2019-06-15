# pylint: disable=missing-docstring,too-few-public-methods, useless-object-inheritance

class SomeClass(object):
    def __init__(self): # [init-is-generator]
        yield None
