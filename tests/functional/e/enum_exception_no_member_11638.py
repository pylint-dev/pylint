"""Regression test for issue 11638: Enum exception instance attribute access crash."""
# pylint: disable=catching-non-exception,pointless-statement
from enum import Enum

try:
    pass
except Enum as e:
    e.message  # [no-member]
