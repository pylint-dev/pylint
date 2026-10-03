"""Test that valid class attribute doesn't trigger errors"""
# pylint: disable=missing-docstring,too-few-public-methods


class Clazz:
    "dummy class"

    def __init__(self):
        self.topic = 5
        self._data = 45

    def change_type(self, new_class):
        """Change type"""
        self.__class__ = new_class

    def do_nothing(self):
        "I do nothing useful"
        return self.topic + 56


class Base:
    _class_prop: int


class Child(Base):
    _class_prop = 42

    def method(self):
        print(self._class_prop)


Child().method()
