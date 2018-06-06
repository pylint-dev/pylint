# pylint: disable=missing-docstring,no-self-use,unused-argument,pointless-statement
# pylint: disable=too-few-public-methods,no-name-in-module
from __future__ import annotations

class Class:
    @classmethod
    def from_string(cls, source) -> Class:
        ...

    def validate_b(self, obj: OtherClass) -> bool:
        ...


class OtherClass:
    ...
