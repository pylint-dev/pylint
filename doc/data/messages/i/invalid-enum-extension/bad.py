from enum import Enum


class A(Enum):
    x = 1
    y = 2


class B(A):  # [invalid-enum-extension]
    z = 3
