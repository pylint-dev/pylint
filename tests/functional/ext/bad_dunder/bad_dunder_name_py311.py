# pylint: disable=missing-class-docstring, missing-function-docstring,
# pylint: disable=too-few-public-methods, unused-argument
"""Data model methods newer than the configured py-version are still reported."""


class Meta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):  # PEP 3115
        return {}


class Base:
    def __mro_entries__(self, bases):  # PEP 560
        return (object,)


class Buffer:
    def __buffer__(self, flags):  # [bad-dunder-name]
        return memoryview(b"x")

    def __release_buffer__(self, view):  # [bad-dunder-name]
        view.release()


class Point:
    def __replace__(self, **changes):  # [bad-dunder-name]
        return self
