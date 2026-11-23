"""astroid infers methods decorated with a property-like decorator as properties.

It decides that from the decorator's name (see ``astroid.bases.POSSIBLE_PROPERTIES``).
An attribute assigned in ``__init__`` then overrides the property's value on purpose.
"""

# pylint: disable=too-few-public-methods,missing-docstring


class cached_property:  # pylint: disable=invalid-name
    """Same shape as ``django.utils.functional.cached_property``: no ``__set__``."""

    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner=None):
        return self.function(instance)


class Memoized(cached_property):
    """The same descriptor under a name astroid does not know."""


def lazy(function):
    """A plain function wrapper, not a descriptor."""

    def wrapper(*args):
        return function(*args)

    return wrapper


class OverriddenCachedProperty:
    def __init__(self, value=None):
        if value is not None:
            self.value = value

    @cached_property
    def value(self):
        return 1


class UnknownDescriptor:
    def __init__(self):
        self.value = 1

    @Memoized
    def value(self):  # [method-hidden]
        return 1


class PlainWrapperWithPropertyName:
    def __init__(self):
        self.value = 1

    @lazy
    def value(self):  # FALSE NEGATIVE: astroid only looks at the name ``lazy``
        return 1
