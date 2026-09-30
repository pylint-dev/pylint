"""Regression test for https://github.com/pylint-dev/pylint/issues/11511."""

# pylint: disable=too-few-public-methods,undefined-variable,unused-variable


class Outer:
    """Class that provides a synthetic ``__annotations__`` local."""

    def method(self) -> None:
        """Define a class whose metaclass name resolves past the class scope."""

        class Inner(metaclass=__annotations__):
            """Nested class using an undefined metaclass."""
