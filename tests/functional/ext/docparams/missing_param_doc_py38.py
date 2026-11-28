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


def foobar4(one, /, two: str):  # [missing-type-doc]
    """Only the positional-only argument is missing a type.

    Args:
        one: A number.
        two: Another number.
    """
    print(one, two)


class Foobar:
    """Methods with positional-only arguments, see #11843."""

    def method1(self, one, /, two: str):  # [missing-type-doc]
        """Only the positional-only argument is missing a type.

        Args:
            one: A number.
            two: Another number.
        """
        print(self, one, two)

    def method2(self, /, one, two: str):  # [missing-type-doc]
        """Only the first regular argument is missing a type.

        Args:
            one: A number.
            two: Another number.
        """
        print(self, one, two)

    def method3(self, one, two: str, /):  # [missing-type-doc]
        """Only the positional-only argument is missing a type.

        Args:
            one: A number.
            two: Another number.
        """
        print(self, one, two)

    def method4(self, /, one: int, two: str):
        """All arguments are annotated.

        Args:
            one: A number.
            two: Another number.
        """
        print(self, one, two)


def foobar5(one: int, /, two, three: str):  # [missing-type-doc]
    """Only the first regular argument is missing a type.

    Args:
        one: A number.
        two: Another number.
        three: Yes another number.
    """
    print(one, two, three)


def foobar6(
    one: int,
    /,
    two,  # type: str
):
    """The annotation and the type comment both count.

    Args:
        one: A number.
        two: Another number.
    """
    print(one, two)
