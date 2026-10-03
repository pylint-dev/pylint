# pylint: disable=missing-docstring, invalid-name, use-dict-literal, line-too-long

numbers = [1, 2, 3, 4, 5, 6]

dict()

dict([])

dict([(number, number*2) for number in numbers])  # [consider-using-dict-comprehension]

stuff = {1: 10, 2: -20}
dict([(k, v) if v > 0 else (k, 0) for k, v in stuff.items()])  # [consider-using-dict-comprehension]
dict([(k, v) if v > 0 else (k*2, v) for k, v in stuff.items()])  # [consider-using-dict-comprehension]
dict([(k, v) if v > 0 else (k * 2, 0) for k, v in stuff.items()])

# Cannot emit as this cannot be written as a comprehension
dict([value.split("=") for value in ["a=b", "c=d"]])
