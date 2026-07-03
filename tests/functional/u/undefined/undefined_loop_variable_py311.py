"""Tests for undefined-loop-variable using Python 3.11 syntax."""

from typing import Never


def for_else_never(iterable):
    """Test for-else with Never type."""

    def idontreturn() -> Never:
        """This function never returns."""

    while True:
        for thing in iterable:
            break
        else:
            idontreturn()
        print(thing)
