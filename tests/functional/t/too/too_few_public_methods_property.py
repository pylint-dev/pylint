"""Properties and descriptors assigned in the class body count as public methods."""

# pylint: disable=missing-class-docstring, missing-function-docstring, invalid-name
# pylint: disable=unnecessary-lambda-assignment


class Decorators:
    @property
    def id(self):
        return None

    @property
    def name(self):
        return None


class Functions:
    id = property(lambda self: None)
    name = property(lambda self: None)


def my_property():
    def getter(_self):
        return None

    return property(getter)


class Functions2:
    id = my_property()
    name = my_property()


class Descriptor:  # [too-few-public-methods]
    def __get__(self, instance, owner=None):
        return None


class Descriptors:
    id = Descriptor()
    name: Descriptor = Descriptor()


class Inherited(Descriptors):
    pass


class OnlyOne:  # [too-few-public-methods]
    id = property(lambda self: None)


class PlainAttributes:  # [too-few-public-methods]
    id = 1
    name = "name"
