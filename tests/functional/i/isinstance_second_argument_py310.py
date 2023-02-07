'''Tests for isinstance with compound types'''

# True negatives
isinstance(0, int | str)
isinstance(0, int | int | int)
isinstance(0, int | str | list | float)
isinstance(0, (int | str) | (list | float))

# True positives
isinstance(0, int | 5)  # [isinstance-second-argument-not-valid-type]
isinstance(0, str | 5 | int)  # [isinstance-second-argument-not-valid-type]


# FALSE POSITIVES

# Type aliases cannot be inferred
IntOrStr = int | str
isinstance(0, IntOrStr)  # [isinstance-second-argument-not-valid-type]
ListOrDict = list | dict
isinstance(0, (float | ListOrDict) | IntOrStr)  # [isinstance-second-argument-not-valid-type]


# FALSE NEGATIVES

# Parameterized generics will raise type errors at runtime.
# Warnings should be raised, but aren't (yet).
isinstance(0, list[int])
ListOfInts = list[int]
isinstance(0, ListOfInts)
