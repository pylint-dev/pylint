"""Regression test for https://github.com/pylint-dev/pylint/issues/7991.

A parent method that returns ``self``, called with ``super()`` from a
subclass, returns the subclass instance with all its members.
"""

# pylint: disable=too-few-public-methods,useless-parent-delegation


class Parent:
    """Returns itself."""

    def save(self):
        """Return the instance."""
        return self


class Child(Parent):
    """Adds an attribute and calls the parent's ``save``."""

    def __init__(self):
        self.value = 12

    def save(self):
        """Return what the parent returns: this instance."""
        return super().save()


print(Child().save().value)
