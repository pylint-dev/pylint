"""Tests for consider-using-augmented-assign."""

# pylint: disable=invalid-name,too-few-public-methods,import-error,consider-using-f-string,missing-docstring

from unknown import Unknown, elixir, random_object

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

# Should also apply to dictionaries when subscripts are the same
my_dict = {"count": 5}
my_dict["count"] = my_dict["count"] + 2  # [consider-using-augmented-assign]
my_dict["apples"] = my_dict["count"] + 1

my_dict = {"msg": {"title": "Hello"}}
my_dict["msg"]["title"] = my_dict["msg"]["title"] + " world!"  # [consider-using-augmented-assign]
my_dict["msg"]["body"] = my_dict["msg"]["title"] + " everyone, this should not raise messages"

# Applies to lists as well
test_list = [1, 2]
test_list[0] = test_list[0] - 1  # [consider-using-augmented-assign]
test_list[1] = test_list[0] + 10

# Can't infer, don't mark message
random_object[elixir] = random_object[elixir] + 1

# https://github.com/pylint-dev/pylint/issues/8086
# consider-using-augmented-assign should only be flagged
# if names attribute names match exactly.

class A:
    def __init__(self) -> None:
        self.a = 1
        self.b = A()
        self.c = [1, 2, 3]

    def test(self) -> None:
        self.a = self.a + 1  # [consider-using-augmented-assign]
        self.b.a = self.a + 1  # Names don't match!

    def line(self) -> None:
        self.c[1] = self.c[1] + 1  # [consider-using-augmented-assign]
