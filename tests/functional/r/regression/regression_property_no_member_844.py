# pylint: disable=missing-docstring,too-few-public-methods,invalid-overridden-method
# https://github.com/pylint-dev/pylint/issues/844
class Parent:
    def __init__(self):
        self.__thing = 'foo'

    @property
    def thing(self):
        return self.__thing


class Child(Parent):
    @Parent.thing.getter
    def thing(self):
        return super().thing + '!'


print(Child().thing)
