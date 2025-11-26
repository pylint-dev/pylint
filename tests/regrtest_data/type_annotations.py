"""Test file for type annotation checker."""


def missing_return_type(x: int, y: int):  # Missing return type
    """Function missing return type annotation."""
    return x + y


def missing_param_types(x, y) -> int:  # Missing parameter types
    """Function missing parameter type annotations."""
    return x + y


def missing_all_annotations(x, y):  # Missing both
    """Function missing all type annotations."""
    return x + y


def fully_annotated(x: int, y: int) -> int:  # OK - fully annotated
    """Function with complete type annotations."""
    return x + y


class TestClass:
    """Test class for type annotations."""

    def __init__(self, value: int):  # OK - __init__ doesn't need return type
        """Initialize with value."""
        self.value = value

    def get_value(self):  # Missing return type
        """Get the value."""
        return self.value

    def set_value(self, value):  # Missing parameter type and return type
        """Set the value."""
        self.value = value

    def compute(self, x: int) -> int:  # OK - fully annotated
        """Compute something."""
        return self.value + x


async def async_missing_return(x: int):  # Missing return type
    """Async function missing return type."""
    return x * 2


async def async_fully_annotated(x: int) -> int:  # OK - fully annotated
    """Async function with complete annotations."""
    return x * 2
