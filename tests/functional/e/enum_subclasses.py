# pylint: disable=missing-docstring, invalid-name
from enum import Enum, IntEnum, auto


class Issue1932(IntEnum):
    """https://github.com/PyCQA/pylint/issues/1932"""

    FOO = 1

    def whats_my_name(self):
        return self.name.lower()


class Issue2062(Enum):
    """https://github.com/PyCQA/pylint/issues/2062"""

    FOO = 1
    BAR = 2

    def __str__(self):
        return self.name.lower()


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value  # line 11
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value  # line 16
        return NotImplemented


class Color(OrderedEnum):
    red = 0
    green = 1


class People(Enum):
    jack = 0
    john = 1


print(Color.red.value)  # line 29
print(People.jack.name)


class BaseEnum(Enum):
    def some_behavior(self):
        pass


class MyEnum(BaseEnum):

    FOO = 1
    BAR = 2


print(MyEnum.FOO.value)

class TestBase(Enum):
    """Adds a special method to enums."""

    def hello_pylint(self) -> str:
        """False positive."""
        return self.name


class TestEnum(TestBase):
    """Tests the false positive for enums."""

    a = auto()
    b = auto()


test_enum = TestEnum.a
assert test_enum.hello_pylint() == test_enum.name
