"""A function only declared in a stub does not return None."""
from stub_without_implementation import pair


def unpack():
    """Unpack the result of the stubbed function."""
    _, second = pair()
    return second
