"""Tests for invalid isinstance with compound types"""

# True negatives
isinstance(0, int | str)
isinstance(0, int | int | int)
isinstance(0, int | str | list | float)
isinstance(0, (int | str) | (list | float))
isinstance(0, int | None)
isinstance(0, None | int)

IntOrStr = int | str
isinstance(0, IntOrStr)
IntOrNone = int | None
isinstance(0, IntOrNone)
ListOrDict = list | dict
isinstance(0, (float | ListOrDict) | IntOrStr)

# True positives
isinstance(0, int | 5)  # [isinstance-second-argument-not-valid-type]
isinstance(0, str | 5 | int)  # [isinstance-second-argument-not-valid-type]
INT = 5
isinstance(0, INT | int)  # [isinstance-second-argument-not-valid-type]


# FALSE NEGATIVES

# Parameterized generics will raise type errors at runtime.
# Warnings should be raised, but aren't (yet).
isinstance(0, list[int])
ListOfInts = list[int]
isinstance(0, ListOfInts)
