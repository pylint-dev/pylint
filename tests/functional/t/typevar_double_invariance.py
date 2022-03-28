"""Test case for typevar-name-incorrect-variance with default settings"""

from typing import TypeVar

T_co = TypeVar("T", covariant=True, contravariant=True) # [typevar-double-variance]
T_co = TypeVar("T", covariant=True, contravariant=False)
T_contra = TypeVar("T", covariant=True, contravariant=True) # [typevar-double-variance]
T_contra = TypeVar("T", covariant=False, contravariant=True)
T = TypeVar("T", covariant=False, contravariant=False)
