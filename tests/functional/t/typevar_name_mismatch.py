"""Test case for TypeVar name not matching assigned variable name."""
from typing import TypeVar

# Control examples
T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)

# Mismatching names
X = TypeVar("T")  # [typevar-name-mismatch]
X_co = TypeVar("T_co", covariant=True)  # [typevar-name-mismatch]
X_contra = TypeVar("T_contra", contravariant=True)  # [typevar-name-mismatch]
X_co, X_contra = (  # [typevar-name-mismatch,typevar-name-mismatch]
    TypeVar("T", covariant=True),
    TypeVar("T", contravariant=True),
)

# The user may also violate typevar-double-variance
# or typevar-name-incorrect-variance
# on top of not matching the variable and TypeVar names.
# This rule does not suggest what the correct name is
# (that's already handled by the aforementioned rules),
# it just highlights that the names don't match.
X = TypeVar("T", contravariant=True)  # [typevar-name-mismatch,typevar-name-incorrect-variance]
X = TypeVar(  # [typevar-name-mismatch,typevar-name-incorrect-variance,typevar-double-variance]
    "T",
    covariant=True,
    contravariant=True
)
X_co = TypeVar("T_co")  # [typevar-name-mismatch,typevar-name-incorrect-variance]
X_contra = TypeVar(  # [typevar-name-mismatch,typevar-name-incorrect-variance]
    "T_contra",
    covariant=True
)

# name can be specified as a keyword argument as well.
T = TypeVar(name="T")
T_co = TypeVar(name="T_co", covariant=True)
T_contra = TypeVar(name="T_contra", contravariant=True)
T_co = TypeVar(covariant=True, name="T_co")
T_contra = TypeVar(contravariant=True, name="T_contra")

X = TypeVar(name="T")  # [typevar-name-mismatch]
X_co = TypeVar(name="T_co", covariant=True)  # [typevar-name-mismatch]
X_contra = TypeVar(name="T_contra", contravariant=True) # [typevar-name-mismatch]
X_co = TypeVar(covariant=True, name="T_co")  # [typevar-name-mismatch]
X_contra = TypeVar(contravariant=True, name="T_contra") # [typevar-name-mismatch]
