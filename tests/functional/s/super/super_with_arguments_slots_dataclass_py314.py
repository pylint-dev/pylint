"""Since Python 3.14, ``super()`` without arguments works in a dataclass created
with ``slots=True``, so ``super-with-arguments`` is emitted there too.

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
        return super(SlotsChild, self).greet()  # [super-with-arguments]
