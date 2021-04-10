# pylint: disable=missing-docstring, invalid-name, unnecessary-comprehension

numbers = [1, 2, 3, 4, 5, 6]

set()

set([])

set([number for number in numbers])  # [consider-using-set-comprehension]
