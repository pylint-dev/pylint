"""Regression test for https://github.com/pylint-dev/pylint/issues/981.

A classmethod that calls the parent classmethod through ``super()`` gets an
instance of ``cls``, the subclass, not of the parent class. Its members are
those of the subclass.
"""

# pylint: disable=too-few-public-methods


class Parent:
    """Builds an instance of whatever class it is called on."""

    @classmethod
    def build(cls):
        """Return a new instance of ``cls``."""
        return cls()

    def parent_method(self):
        """Defined on the parent."""
        print(self)


class Child(Parent):
    """Calls the parent's classmethod with ``super()``."""

    @classmethod
    def build(cls):
        """Return a new instance of ``cls``, built by the parent."""
        instance = super(Child, cls).build()
        instance.parent_method()
        instance.child_method()
        other = super().build()
        other.child_method()
        return instance

    def child_method(self):
        """Defined on the child only."""
        print(self)
