""" Checks that classes uses valid __slots__ """

# pylint: disable=too-few-public-methods, missing-docstring
# pylint: disable=using-constant-test, wrong-import-position, no-else-return, line-too-long, unused-private-member
from collections import deque

def func():
    if True:
        return ("a", "b", "c")
    else:
        return [str(var) for var in range(3)]


class NotIterable:
    def __iter_(self):
        """ do nothing """

class Good:
    __slots__ = ()

class SecondGood:
    __slots__ = []

class ThirdGood:
    __slots__ = ['a']

class FourthGood:
    __slots__ = (f'a{i}' for i in range(10))

class FifthGood:
    __slots__ = deque(["a", "b", "c"])

class SixthGood:
    __slots__ = {"a": "b", "c": "d"}

class SeventhGood:
    """type-annotated __slots__ with no value"""
    __slots__: str

class EigthGood:
    """Multiple __slots__ declared in the class"""
    x = 1
    if x:
        __slots__: str
    else:
        __slots__ = ("y",)

class Bad: # [invalid-slots]
    __slots__ = list

class SecondBad:  # [invalid-slots]
    __slots__ = 1

class ThirdBad:
    __slots__ = ('a', 2)  # [invalid-slots-object]

class FourthBad:  # [invalid-slots]
    __slots__ = NotIterable()

class FifthBad:
    __slots__ = ("a", "b", "")  # [invalid-slots-object]

class SixthBad:  # [single-string-used-for-slots]
    __slots__ = "a"

class SeventhBad:  # [single-string-used-for-slots]
    __slots__ = ('foo')  # [superfluous-parens]

class EighthBad:  # [single-string-used-for-slots]
    __slots__ = deque.__name__

class NinthBad:
    __slots__ = [str]  # [invalid-slots-object]

class TenthBad:
    __slots__ = [1 + 2 + 3]  # [invalid-slots-object]

class EleventhBad:  # [invalid-slots]
    __slots__ = None

class TwelfthBad:  # [invalid-slots]
    """One valid & one invalid __slots__ value"""
    x = 1
    if x:
        __slots__ = ("y",)
    else:
        __slots__ = None

class PotentiallyGood:
    __slots__ = func()

class PotentiallySecondGood:
    __slots__ = ('a', deque.__name__)


class Metaclass(type):

    def __iter__(cls):
        for value in range(10):
            yield str(value)


class IterableClass(metaclass=Metaclass):
    pass

class PotentiallyThirdGood:
    __slots__ = IterableClass

class PotentiallyFourthGood:
    __slots__ = Good.__slots__


class ValueInSlotConflict:
    __slots__ = ('first', 'second', 'third', 'fourth') # [class-variable-slots-conflict, class-variable-slots-conflict, class-variable-slots-conflict]
    first = None

    @property
    def third(self):
        return 42

    def fourth(self):
        return self.third


class Parent:
    first = 42


class ChildNotAffectedByValueInSlot(Parent):
    __slots__ = ('first', )


class ClassTypeHintNotInSlotsWithoutDict:
    __slots__ = ("a", "b")

    a: int
    b: str
    c: bool # [declare-non-slot]


class ClassTypeHintNotInSlotsWithDict:
    __slots__ = ("a", "b", "__dict__")

    a: int
    b: str
    c: bool


class BaseNoSlots:
    pass


class DerivedWithSlots(BaseNoSlots):
    __slots__ = ("age",)

    price: int


class BaseWithSlots:
    __slots__ = ("a", "b",)


class DerivedWithMoreSlots(BaseWithSlots):
    __slots__ = ("c",)

    # Is in base __slots__
    a: int

    # Not in any base __slots__
    d: int # [declare-non-slot]
    e: str= "AnnAssign.value is not None"


class BaseWithSlotsDict:
    __slots__ = ("__dict__", )

class DerivedTypeHintNotInSlots(BaseWithSlotsDict):
    __slots__ = ("other", )

    a: int
    def __init__(self) -> None:
        super().__init__()
        self.a = 42


class ClassWithEmptySlotsAndAnnotation:
    __slots__ = ()

    a: int


# https://github.com/pylint-dev/pylint/issues/9814
class SlotsManipulationTest:
    __slots__ = ["a", "b", "c"]


class TestChild(SlotsManipulationTest):
    __slots__ += ["d", "e", "f"]  # pylint: disable=undefined-variable


t = TestChild()

print(t.__slots__)
