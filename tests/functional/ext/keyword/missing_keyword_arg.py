"""Tests for missing-keyword-arg"""
# pylint: disable=unused-argument, missing-function-docstring, missing-class-docstring, too-few-public-methods

def print_hello(one, two):
    return f"{one}:{two}"


print_hello("1", two="2")  # [missing-keyword-arg]
print_hello("1", "2")  # [missing-keyword-arg, missing-keyword-arg]

print()
print("hello")
print("hello", "world", sep="-")

class Fruit:
    def __init__(self, color):
        self.color = color

    def print_color(self, skip_header=False):
        if not skip_header:
            print("Color is: ")
        print(self.color)

apple = Fruit("red")   # [missing-keyword-arg]
orange = Fruit(color="orange")
orange.print_color()  # [missing-keyword-arg]
orange.print_color(True)  # [missing-keyword-arg]
orange.print_color(skip_header=True)


def keep_self_arg(one, self):
    # Tests that an arg called `self` is not affected in module-level functions
    return f"{one}: {self}"

keep_self_arg("one", 2)  # [missing-keyword-arg, missing-keyword-arg]


"".join(["apple", "pear", "peach"])  # [missing-keyword-arg]
"".join(iterable=["apple", "pear", "peach"])
