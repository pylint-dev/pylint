# pylint: disable=too-few-public-methods, invalid-name
"""Test typing with a protected member"""
from __future__ import annotations


class MyClass:
    """Class with protected members."""

    class _Inner_Class:
        """Inner class with protected members."""

        def __init__(self) -> None:
            self.data = 1

        def return_data(self) -> int:
            """Return data"""
            return self.data

    def return_private_class(self) -> MyClass._Inner_Class:
        """Doing nothing."""
        return self._Inner_Class()


def access_protected_class(data: MyClass._Inner_Class) -> int:
    """Function that always receives a protected class."""
    return data.return_data() + 1


def pass_protected_class() -> None:
    """Function that passes a protected class to another function."""
    data_value = access_protected_class(MyClass().return_private_class())
    print(data_value)
