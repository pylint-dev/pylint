"""Tests for missing-keyword-arg"""
# pylint: disable=unused-argument, missing-function-docstring, missing-class-docstring,
# pylint: disable=invalid-name, too-few-public-methods, line-too-long, too-many-arguments

def print_hello(one, two):
    return f"{one}:{two}"


print_hello(one="1", two="2")
print_hello("1", two="2")  # [missing-keyword-arg]
print_hello("1", "2")  # [missing-keyword-arg, missing-keyword-arg]

def print_one_thing(one):
    return f"{one}"

print_one_thing("1")
print_one_thing(one="1")

def print_two_kwarg(one, two="2", ok=True):
    return f"{one}:{two}"

print_two_kwarg("1")
print_two_kwarg("1", ok=False)


class Fruit:
    def __init__(self, color):
        self.color = color

    def print_color(self, skip_header=False):
        if not skip_header:
            print("Color is: ")
        print(self.color)

apple = Fruit("red")
orange = Fruit(color="orange")
orange.print_color()
orange.print_color(True)
orange.print_color(skip_header=True)


def keep_self_arg(one, self):
    # Tests that an arg called `self` is not affected in module-level functions
    return f"{one}: {self}"

keep_self_arg("one", 2)  # [missing-keyword-arg, missing-keyword-arg]
keep_self_arg("one", self=2)  # [missing-keyword-arg]


"".join(["apple", "pear", "peach"])
"".join(iterable=["apple", "pear", "peach"])

print()
print("hello")
print("hello", "world", sep="-")


class Car:
    def __init__(self, name, owner, title, color="red", year=2022):
        self.name = name
        self.color = color
        self.year = year
        self.owner = owner
        self.title = title

    def run(self, speed, distance, location):
        pass

car = Car("a car", "name", "title") # [missing-keyword-arg, missing-keyword-arg, missing-keyword-arg]
car.run(123, "north", "walmart")  # [missing-keyword-arg, missing-keyword-arg, missing-keyword-arg]


class Robot:
    def __init__(self, name, color="red", year=2022):
        self.name = name
        self.color = color
        self.year = year

robot = Robot("a robot")
