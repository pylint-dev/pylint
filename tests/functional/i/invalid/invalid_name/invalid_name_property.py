"""Tests for invalid-name checker with properties."""
# pylint: disable=missing-class-docstring, missing-function-docstring, deprecated-decorator
# pylint: disable=too-few-public-methods


import abc


def custom_prop(F): # [invalid-name]
    return property(F)


class FooClass:
    """Test properties with attr-rgx and property-classes options."""

    @property
    def FOO(self):
        pass

    @property
    def bar(self):  # [invalid-name]
        pass

    @abc.abstractproperty
    def BAZ(self):
        pass

    @custom_prop
    def QUX(self):
        pass


class AnotherFooClass:
    """Test property setter for pattern set in attr-rgx."""

    @property
    def foo(self): # [invalid-name]
        pass

    @foo.setter
    def FOOSETTER(self):
        pass
