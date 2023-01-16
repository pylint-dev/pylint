"""Tests for consider-using-augmented-assign."""

# pylint: disable=invalid-name,too-few-public-methods,import-error,consider-using-f-string

from unknown import Unknown

x = 1

# summation is commutative (for integer and float, but not for string)
x = x + 3  # [consider-using-augmented-assign]
x = 3 + x  # [consider-using-augmented-assign]
x = x + "3"  # [consider-using-augmented-assign]
x = "3" + x

# We don't warn on intricate expressions as we lack knowledge of simplifying such
# expressions which is necessary to see if they can become augmented
x, y = 1 + x, 2 + x
x = 1 + x - 2
x = 1 + x + 2

# For anything other than a float or an int we only want to warn on
# assignments where the 'itself' is on the left side of the assignment
my_list = [2, 3, 4]
my_list = [1] + my_list


class MyClass:
    """Simple base class."""

    def __init__(self) -> None:
        self.x = 1
        self.x = self.x + 1  # [consider-using-augmented-assign]
        self.x = 1 + self.x  # [consider-using-augmented-assign]

        x = 1  # [redefined-outer-name]
        self.x = x


instance = MyClass()

x = instance.x + 1

my_str = ""
my_str = my_str + "foo"  # [consider-using-augmented-assign]
my_str = "foo" + my_str

my_bytes = b""
my_bytes = my_bytes + b"foo"  # [consider-using-augmented-assign]
my_bytes = b"foo" + my_bytes


def return_str() -> str:
    """Return a string."""
    return ""


# Currently we disregard all calls
my_str = return_str() + my_str
my_str = my_str % return_str()
my_str = my_str % 1  # [consider-using-augmented-assign]
my_str = my_str % (1, 2)  # [consider-using-augmented-assign]
my_str = "%s" % my_str
my_str = return_str() % my_str
my_str = Unknown % my_str
my_str = my_str % Unknown  # [consider-using-augmented-assign]

# subtraction is anti-commutative
x = x - 3  # [consider-using-augmented-assign]
x = 3 - x

# multiplication is commutative
x = x * 3  # [consider-using-augmented-assign]
x = 3 * x  # [consider-using-augmented-assign]

# division is not commutative
x = x / 3  # [consider-using-augmented-assign]
x = 3 / x

# integer division is not commutative
x = x // 3  # [consider-using-augmented-assign]
x = 3 // x

# Left shift operator is not commutative
x = x << 3  # [consider-using-augmented-assign]
x = 3 << x

# Right shift operator is not commutative
x = x >> 3  # [consider-using-augmented-assign]
x = 3 >> x

# modulo is not commutative
x = x % 3  # [consider-using-augmented-assign]
x = 3 % x

# exponential is not commutative
x = x**3  # [consider-using-augmented-assign]
x = 3**x

# XOR is commutative
x = x ^ 3  # [consider-using-augmented-assign]
x = 3 ^ x  # [consider-using-augmented-assign]

# Bitwise AND operator is commutative
x = x & 3  # [consider-using-augmented-assign]
x = 3 & x  # [consider-using-augmented-assign]

# Bitwise OR operator is commutative
x = x | 3  # [consider-using-augmented-assign]
x = 3 | x  # [consider-using-augmented-assign]

x = x > 3
x = 3 > x

x = x < 3
x = 3 < x

x = x >= 3
x = 3 >= x

x = x <= 3
x = 3 <= x
