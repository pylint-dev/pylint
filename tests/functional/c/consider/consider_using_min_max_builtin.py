# pylint: disable=missing-docstring, invalid-name, too-few-public-methods, redefined-outer-name

value = 10
value2 = 0
value3 = 3

# Positive
if value < 10:  # [consider-using-max-builtin]
    value = 10

if value >= 10:  # [consider-using-min-builtin]
    value = 10

if value <= 10:  # [consider-using-max-builtin]
    value = 10

if value > 10:  # [consider-using-min-builtin]
    value = 10

if value < value2:  # [consider-using-max-builtin]
    value = value2

if value > value2:  # [consider-using-min-builtin]
    value = value2

if value2 > value3:  # [consider-using-max-builtin]
    value3 = value2

if value < value2:  # [consider-using-min-builtin]
    value2 = value

if value > float(value3):  # [consider-using-min-builtin]
    value = float(value3)

offset = 1
if offset + value < value2:  # [consider-using-min-builtin]
    value2 = offset + value

class A:
    def __init__(self):
        self.value = 13


A1 = A()
if A1.value > 10:  # [consider-using-min-builtin]
    A1.value = 10


class AA:
    def __init__(self, value):
        self.value = value

    def __gt__(self, b):
        return self.value > b

    def __ge__(self, b):
        return self.value >= b

    def __lt__(self, b):
        return self.value < b

    def __le__(self, b):
        return self.value <= b


A1 = AA(0)
A2 = AA(3)

if A1 > A2:  # [consider-using-min-builtin]
    A1 = A2

if A2 < A1:  # [consider-using-max-builtin]
    A2 = A1

if A1 >= A2:  # [consider-using-min-builtin]
    A1 = A2

if A2 <= A1:  # [consider-using-max-builtin]
    A2 = A1

# Negative
if value > 10:
    value = 2

if 10 < value:
    value = 2

if 10 > value:
    value = 2

if value > 10:
    value = 2
    value2 = 3

if value > value2:
    value = value3

if value > 5:
    value = value3

if 2 < value <= 3:
    value = 1

if value <= 3:
    value = 5

if value <= 3:
    value = 5
elif value == 3:
    value = 2

if value > 10:
    value = 10
else:
    value = 3

if value > float(value3):
    value = float(value2)

offset = 1
if offset + value < value2:
    value2 = offset


# https://github.com/pylint-dev/pylint/issues/4379
var = 1
if var == -1:
    var = None

var2 = 1
if var2 in [1, 2]:
    var2 = None
