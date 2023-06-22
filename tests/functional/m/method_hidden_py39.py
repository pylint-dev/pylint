# pylint: disable=too-few-public-methods,missing-docstring
"""check method hiding ancestor attribute
"""
import something_else as functools  # pylint: disable=import-error


class Parent:
    def __init__(self):
        self._protected = None


class Child(Parent):
    @functools().cached_property
    def _protected(self):
        # This test case is only valid for python3.9 and above
        pass
