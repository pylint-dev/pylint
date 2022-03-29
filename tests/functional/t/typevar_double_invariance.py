"""Test case for typevar-name-incorrect-variance with default settings"""

from typing import TypeVar

T_co = TypeVar("T_co", covariant=True, contravariant=True) # [typevar-double-variance]
T_co = TypeVar("T_co", covariant=True, contravariant=False)
T_contra = TypeVar("T_contra", covariant=True, contravariant=True) # [typevar-double-variance]
T_contra = TypeVar("T_contra", covariant=False, contravariant=True)
T = TypeVar("T", covariant=False, contravariant=False)
