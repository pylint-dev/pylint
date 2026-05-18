# pylint: disable=missing-docstring, superfluous-parens


try:
    1/0
except (ValueError | TypeError): # [catching-non-exception,wrong-exception-operation]
    pass

try:
    1/0
except (ValueError + TypeError): # [wrong-exception-operation]
    pass


try:
    1/0
except (ValueError < TypeError): # [wrong-exception-operation]
    pass


# Concatenation of exception type tuples
DIVISION_BY_ZERO = (ZeroDivisionError,)
VALUE_ERROR = (ValueError,)
UNINFERABLE = DIVISION_BY_ZERO | VALUE_ERROR

try:
    1/0
except (ValueError, ) + DIVISION_BY_ZERO:
    pass

try:
    1/0
except (ValueError, ) | DIVISION_BY_ZERO:  # [wrong-exception-operation]
    pass

try:
    1/0
except (ValueError, ) + UNINFERABLE:
    pass
