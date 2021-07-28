"""Calling a super property"""
# pylint: disable=too-few-public-methods,invalid-name

class A:
    """A parent class"""

    @property
    def test(self):
        """A property"""
        return "test"


class B:
    """A child class"""

    @property
    def test(self):
        """Overriding implementation of prop which calls the parent"""
        return A.test.fget(self) + " overriden"


if __name__ == "__main__":
    print(B().test)
