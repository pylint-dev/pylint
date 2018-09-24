# pylint: disable=missing-docstring, invalid-name

numbers = [1, 2, 3, 4, 5, 6]

dict()

dict([])

dict([(number, number*2) for number in numbers])  # [consider-using-dict-comprehension]
