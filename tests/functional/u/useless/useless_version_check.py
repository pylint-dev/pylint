"""Tests for sys.version_info comparisons already decided by the py-version setting."""
# pylint: disable=missing-function-docstring
import sys
from sys import version_info
from sys import version_info as version_info_alias  # pylint: disable=reimported

# The py-version is 3.10, so every supported interpreter is 3.10 or newer.
if sys.version_info >= (3, 8):  # [useless-version-check]
    LOWER_BOUND_REACHED = 1

if sys.version_info > (3, 9, 2):  # [useless-version-check]
    STRICT_LOWER_BOUND_REACHED = 1

if sys.version_info < (3, 8):  # [useless-version-check]
    NEVER_TAKEN = 1

if sys.version_info <= (3, 9):  # [useless-version-check]
    ALSO_NEVER_TAKEN = 1

if sys.version_info[:2] == (3, 5):  # [useless-version-check]
    OBSOLETE_BRANCH = 1

if sys.version_info[:2] != (3, 5):  # [useless-version-check]
    ALWAYS_TAKEN = 1

if (3, 8) <= sys.version_info:  # [useless-version-check]
    OPERANDS_CAN_BE_SWAPPED = 1

if sys.version_info[0] >= 3:  # [useless-version-check]
    MAJOR_BY_INDEX = 1

if sys.version_info.major > 2:  # [useless-version-check]
    MAJOR_BY_ATTRIBUTE = 1

PY310_PLUS = sys.version_info >= (3, 10)  # [useless-version-check]


def guarded_by_a_dead_check() -> int:
    if sys.version_info >= (3, 3) and sys.maxsize > 2**32:  # [useless-version-check]
        return 1
    return 0


# The upper bound is unknown: nothing rules out running on a newer interpreter.
if sys.version_info >= (3, 14):
    NOT_RELEASED_YET = 1

if sys.version_info < (3, 14):
    NEITHER_ALWAYS_TRUE_NOR_ALWAYS_FALSE = 1

if sys.version_info[:2] == (3, 10):
    THE_OLDEST_SUPPORTED_VERSION = 1

# The py-version is compared through the same projection as the node, so these
# see (3,), not (3, 10): a 4.0 interpreter would make them false.
if sys.version_info[:1] == (3,):
    MAJOR_ONLY_AS_A_SLICE = 1

if sys.version_info[0] == 3:
    MAJOR_ONLY_AS_AN_INDEX = 1

if sys.version_info.major == 3:
    MAJOR_ONLY_AS_AN_ATTRIBUTE = 1

# Known limitation: only the 'sys.version_info' attribute is recognized, so a
# name imported from sys is missed. Kept simple on purpose, as the attribute is
# by far the most common way to write the check.
if version_info >= (3, 9):  # Known false negative
    IMPORTED_FROM_SYS = 1

if version_info_alias >= (3, 9):  # Known false negative
    IMPORTED_FROM_SYS_UNDER_AN_ALIAS = 1

# 'minor' goes back to 0 on a new major release, so it is not monotonic.
if sys.version_info.minor >= 5:
    MINOR_BY_ATTRIBUTE = 1

if sys.version_info[1] >= 5:
    MINOR_BY_INDEX = 1

# Projections that do not start at the major version are not handled.
if sys.version_info[1:] >= (5, 0):
    SLICE_WITHOUT_THE_MAJOR_VERSION = 1

if sys.version_info[::2] >= (3, 0):
    SLICE_WITH_A_STEP = 1

# Chained comparisons have more than one outcome to decide.
if (3, 8) <= sys.version_info < (3, 14):
    CHAINED_COMPARISON = 1

if sys.version_info is None:
    UNSUPPORTED_OPERATOR = 1

if sys.version_info >= (3, "8"):
    NOT_AN_INTEGER_TUPLE = 1
