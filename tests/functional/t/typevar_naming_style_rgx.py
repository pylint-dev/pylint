"""Test case for typevar-name-missing-variance with non-default settings"""

from typing import TypeVar

# Name set by regex pattern
TypeVarsShouldBeLikeThis = TypeVar("TypeVarsShouldBeLikeThis")
TypeVarsShouldBeLikeThis_contra = TypeVar(
    "TypeVarsShouldBeLikeThis_contra", contravariant=True
)
TypeVarsShouldBeLikeThis_co = TypeVar("TypeVarsShouldBeLikeThis_co", covariant=True)

# Name using the standard style
GoodNameT = TypeVar("GoodNameT")  # [invalid-name]
GoodNameT_co = TypeVar("GoodNameT_co", covariant=True)  # [invalid-name]
GoodNameT_contra = TypeVar("GoodNameT_contra", contravariant=True)  # [invalid-name]
