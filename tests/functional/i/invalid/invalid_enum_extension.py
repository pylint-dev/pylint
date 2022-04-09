"""Test check for classes extending an Enum class."""
# pylint: disable=missing-class-docstring,invalid-name
from enum import Enum

# We don't flag the Enum class itself
class A(Enum):
    x = 1
    y = 2

# But we do flag any inheriting classes
# that try to extend the Enum class.
class B(A):  # [invalid-enum-extension]
    z = 3

# If no items have been added to the base
# Enum class then the lint is not raised.
class C(Enum):
    pass

class D(C):
    x = 3
