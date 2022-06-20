"""Warnings for using next() without specifying a default value."""

next((i for i in (1, 2)), None)
next(i for i in (1, 2))  # [unspecified-default-for-next]
var = next(i for i in (1, 2))  # [unspecified-default-for-next]

try:
    next(i for i in (1, 2))
except StopIteration:
    pass

try:
    next(i for i in (1, 2))  # [unspecified-default-for-next]
except ValueError:
    pass

try:
    next(i for i in (1, 2))
except (ValueError, StopIteration):
    pass

try:
    next(i for i in (1, 2))
except ValueError:
    pass
except StopIteration:
    pass

redefined_next = next
redefined_next(i for i in (1, 2))  # [unspecified-default-for-next]


# Redefine builtin next. Keep these tests at the bottom of the file:
next = bool  # pylint: disable=redefined-builtin, invalid-name
next(i for i in (1, 2))
