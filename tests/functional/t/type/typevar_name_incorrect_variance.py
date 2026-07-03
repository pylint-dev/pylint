"""Test case for typevar-name-incorrect-variance."""

from typing import TypeVar

# Type variables without variance
T = TypeVar("T")
T_co = TypeVar("T_co")  # [typevar-name-incorrect-variance]
T_contra = TypeVar("T_contra")  # [typevar-name-incorrect-variance]
ScoresT_contra = TypeVar("ScoresT_contra")  # [typevar-name-incorrect-variance]

# Type variables not starting with T
N = TypeVar("N")
N_co = TypeVar("N_co", covariant=True)
N_contra = TypeVar("N_contra", contravariant=True)

# Tests for combinations with contravariance
CT_co = TypeVar("CT_co", contravariant=True)  # [typevar-name-incorrect-variance]
CT_contra = TypeVar("CT_contra")  # [typevar-name-incorrect-variance]
CT_contra = TypeVar("CT_contra", contravariant=True)

# Tests for combinations with covariance
VT = TypeVar("VT", covariant=True)  # [typevar-name-incorrect-variance]
VT_contra = TypeVar("VT_contra", covariant=True)  # [typevar-name-incorrect-variance]
VT_co = TypeVar("VT_co", covariant=True)

# Tests for combinations with bound
VT = TypeVar("VT", bound=int)
VT_co = TypeVar("VT_co", bound=int)  # [typevar-name-incorrect-variance]
VT_contra = TypeVar("VT_contra", bound=int)  # [typevar-name-incorrect-variance]

VT = TypeVar("VT", bound=int, covariant=True)  # [typevar-name-incorrect-variance]
VT_co = TypeVar("VT_co", bound=int, covariant=True)
VT_contra = TypeVar(  # [typevar-name-incorrect-variance]
    "VT_contra", bound=int, covariant=True
)

VT = TypeVar("VT", bound=int, covariant=False)
VT_co = TypeVar(  # [typevar-name-incorrect-variance]
    "VT_co", bound=int, covariant=False
)
VT_contra = TypeVar(  # [typevar-name-incorrect-variance]
    "VT_contra", bound=int, covariant=False
)

VT = TypeVar("VT", bound=int, contravariant=True)  # [typevar-name-incorrect-variance]
VT_co = TypeVar(  # [typevar-name-incorrect-variance]
    "VT_co", bound=int, contravariant=True
)
VT_contra = TypeVar("VT_contra", bound=int, contravariant=True)

VT = TypeVar("VT", bound=int, contravariant=False)
VT_co = TypeVar(  # [typevar-name-incorrect-variance]
    "VT_co", bound=int, contravariant=False
)
VT_contra = TypeVar(  # [typevar-name-incorrect-variance]
    "VT_contra", bound=int, contravariant=False
)

# Tests for combinations with tuple assignment
(
    VT,  # [typevar-name-incorrect-variance]
    VT_contra,  # [typevar-name-incorrect-variance]
) = TypeVar("VT", covariant=True), TypeVar("VT_contra", covariant=True)
VT_co, VT_contra = TypeVar(  # [typevar-name-incorrect-variance]
    "VT_co", covariant=True
), TypeVar("VT_contra", covariant=True)
VAR, VT_contra = "a string", TypeVar(  # [typevar-name-incorrect-variance]
    "VT_contra", covariant=True
)
