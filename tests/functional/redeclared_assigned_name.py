# pylint: disable=missing-docstring

FIRST, FIRST = (1, 2)  # [redeclared-assigned-name]

for SECOND, SECOND in enumerate(range(5, 10)):  # [redeclared-assigned-name]
    print(SECOND)

for FIRST, (SECOND, FIRST, SECOND) in enumerate(range(5, 10)):  # [redeclared-assigned-name]
    print(SECOND)
