"""Tests for self-defined Enum members (https://github.com/PyCQA/pylint/issues/6805)"""
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods


class Foo(type):
    pass


class Parent:
    def __new__(cls, *_args, **_kwargs):
        return object.__new__(cls)


class NotEnumHasDynamicGetAttrMetaclass(metaclass=Foo):
    def __new__(cls):
        return Parent.__new__(cls)

    def __getattr__(self, item):
        return item

    def magic(self):
        return self.dynamic


NotEnumHasDynamicGetAttrMetaclass().magic()
