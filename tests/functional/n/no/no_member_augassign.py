"""Tests that no-member is not emitted for value-less annotations in relation
   to AugAssign operations.
"""
# pylint: disable=too-few-public-methods, missing-class-docstring, invalid-name


# Test for: https://github.com/pylint-dev/pylint/issues/4562
class A:
    value: int


obj_a = A()
obj_a.value += 1


class B:
    value: int


obj_b = B()
obj_b.value = 1 + obj_b.value


class C:
    value: int


obj_c = C()
obj_c.value += 1
obj_c.value = 1 + obj_c.value
