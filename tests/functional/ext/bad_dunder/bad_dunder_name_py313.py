# pylint: disable=missing-class-docstring, missing-function-docstring,
# pylint: disable=too-few-public-methods, unused-argument
"""Data model methods are accepted on the Python version that introduced them."""


class Meta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):  # PEP 3115
        return {}


class Base:
    def __mro_entries__(self, bases):  # PEP 560
        return (object,)


class Buffer:
    def __buffer__(self, flags):  # PEP 688, Python 3.12
        return memoryview(b"x")

    def __release_buffer__(self, view):  # PEP 688, Python 3.12
        view.release()


class Point:
    def __replace__(self, **changes):  # copy.replace(), Python 3.13
        return self
