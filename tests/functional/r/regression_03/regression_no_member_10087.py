"""Regression test for https://github.com/pylint-dev/pylint/issues/10087.

Importing a function with ``@overload`` stubs gives all its definitions, and
each stub whose body is only ``...`` used to add ``None`` to the inferred
result of the call, next to the ``FieldInfo`` returned by the implementation.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

from functional.r.regression_03.regression_no_member_10087_fields import Field


class Model:
    items: list = Field(default_factory=list)

    def add(self):
        self.items.append(8)


Model().items.append(13)
