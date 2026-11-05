"""Before Python 3.14, ``super()`` without arguments fails in a dataclass created
with ``slots=True``, so ``super-with-arguments`` is not emitted there.

https://github.com/pylint-dev/pylint/issues/5823
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
from dataclasses import dataclass


@dataclass
class Base:
    name: str

    def greet(self):
        return self.name


@dataclass(slots=True)
class SlotsChild(Base):
    def greet(self):
        return super(SlotsChild, self).greet()


@dataclass(slots=False)
class NoSlotsChild(Base):
    def greet(self):
        return super(NoSlotsChild, self).greet()  # [super-with-arguments]


@dataclass(eq=False)
class OtherKeywordChild(Base):
    def greet(self):
        return super(OtherKeywordChild, self).greet()  # [super-with-arguments]


@dataclass
class PlainChild(Base):
    def greet(self):
        return super(PlainChild, self).greet()  # [super-with-arguments]
