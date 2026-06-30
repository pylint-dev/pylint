"""Tests for non-class inheritance with Python 3.12 generic type syntax."""
# pylint: disable=invalid-name,too-few-public-methods

type T[*P] = None


class TypeVarTupleBase(P):  # [inherit-non-class]
    """A TypeVarTuple cannot be inherited from."""
