"""Tests for pylint.extensions.typing unnecessary-string-literal-type-annotation.

'py-version' needs to be set to '3.13' and postponed evaluation is not enabled.
"""

# pylint: disable=missing-docstring,invalid-name,too-few-public-methods


class Foo:
    def some_function(self) -> "Bar":
        raise NotImplementedError


class Bar:
    def another_function(self) -> "Foo":
        raise NotImplementedError
