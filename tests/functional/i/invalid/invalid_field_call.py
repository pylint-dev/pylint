"""Tests for the invalid-field-call message."""

# pylint: disable=invalid-name, missing-class-docstring, missing-function-docstring, too-few-public-methods

from dataclasses import dataclass, field, make_dataclass
import dataclasses as dc

class MyClass:
    def field(self):
        return "Not an actual dataclasses.field function"

mc = MyClass()

C = make_dataclass('C',
                   [('x', int),
                     'y',
                    ('z', int, field(default=5))],
                   namespace={'add_one': lambda self: self.x + 1})

bad = print(field(init=False))  # [invalid-field-call]

a: float = field()  # [invalid-field-call]

class NotADataClass:
    field()  # [invalid-field-call]
    a: float = field(init=False)  # [invalid-field-call]
    dc.field()  # [invalid-field-call]
    b: float = dc.field(init=False)  # [invalid-field-call]

@dataclass
class DC:
    field()  # [invalid-field-call]
    dc.field()  # [invalid-field-call]
    mc.field()
    a: float = field(init=False)
    b: float = dc.field(init=False)
    c: list[float] = [field(), field()]  # [invalid-field-call, invalid-field-call]

@dc.dataclass
class IsAlsoDC:
    field()  # [invalid-field-call]
    a: float = field(init=False)
    b: float = dc.field(init=False)
    c: list[float] = [field(), field()]  # [invalid-field-call, invalid-field-call]

@dc.dataclass(frozen=True)
class FrozenDC:
    a: float = field(init=False)
    b: float = dc.field(init=False)

def my_decorator(func):
    def wrapper():
        func()

    return wrapper

@my_decorator
class AlsoNotADataClass:
    a: float = field(init=False)  # [invalid-field-call]
