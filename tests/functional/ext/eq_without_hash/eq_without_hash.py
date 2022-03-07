"""Regression test for #5025"""

# pylint: disable=invalid-name,missing-docstring, too-few-public-methods


class AClass:  # [eq-without-hash]
    def __init__(self) -> None:
        self.x = 5

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AClass) and other.x == self.x
