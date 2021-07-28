# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
# https://github.com/PyCQA/pylint/issues/2439
class TestClass:
    __slots__ = ["_i"]

    def __init__(self):
        self._i = 0

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, v):
        self._i = v

    other = i


instance = TestClass()
instance.other = 42
print(instance.i)
