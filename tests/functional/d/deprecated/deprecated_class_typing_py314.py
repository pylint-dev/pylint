"""Test ``typing._UnionGenericAlias``, deprecated in Python 3.14."""
# pylint: disable=protected-access,unused-import,no-name-in-module

import typing
from typing import _UnionGenericAlias  # [deprecated-class]

typing._UnionGenericAlias(typing.Union, (int, str))  # [deprecated-class]
