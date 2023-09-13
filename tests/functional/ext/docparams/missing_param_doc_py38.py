#pylint: disable= missing-module-docstring

def foobar1(one: int, /, two: str, *, three: float) -> int:
    """Description of the function

    Args:
        one: A number.
        two: Another number.
        three: Yes another number.

    Returns:
        The number one.
    """
    print(one, two, three)
    return 1


def foobar2(one, /, two, * three):
    # type: (int, str, float) -> int
    """Description of the function

    Args:
        one: A number.
        two: Another number.
        three: Yes another number.

    Returns:
        The number one.
    """
    print(one, two, three)
    return 1


def foobar3(
    one,  # type: int
    /,
    two,  # type: str
    *,
    three,  # type: float
):
    # type: (...) -> int
    """Description of the function

    Args:
        one: A number.
        two: Another number.
        three: Yes another number.

    Returns:
        The number one.
    """
    print(one, two, three)
    return 1
