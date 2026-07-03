"""Tests for no-member in relation to AugAssign operations."""
# pylint: disable=missing-module-docstring, too-few-public-methods, missing-class-docstring, invalid-name

# Test for: https://github.com/pylint-dev/pylint/issues/4562
class A:
    value: int

obj_a = A()
obj_a.value += 1  # [no-member]


class B:
    value: int

obj_b = B()
obj_b.value = 1 + obj_b.value  # [no-member]


class C:
    value: int


obj_c = C()
obj_c.value += 1  # [no-member]
obj_c.value = 1 + obj_c.value  # [no-member]
