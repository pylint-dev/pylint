"""Class variables are not restricted by instance slots (regression for #9950)."""
import typing
from typing import ClassVar


class ClassVariables:
    __slots__ = ("value",)

    value: int
    direct: ClassVar[int]
    qualified: typing.ClassVar[int]
    unsubscripted: ClassVar
    initialized: ClassVar[int] = 1
    instance: int  # [declare-non-slot]


class Derived(ClassVariables):
    __slots__ = ("extra",)

    extra: int
    shared: ClassVar[str]
    missing: int  # [declare-non-slot]
