"""Test for a regression with Enums not being recognized when imported with an alias.

Reported in https://github.com/pylint-dev/pylint/issues/5776
"""

from enum import Enum as PyEnum


class MyEnum(PyEnum):
    """My enum"""

    ENUM_KEY = "enum_value"


print(MyEnum.ENUM_KEY.value)
