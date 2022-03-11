"""Test case for typevar-name-incorrect-variance with default settings"""
# pylint: disable=too-few-public-methods

from typing import TypeVar

# PascalCase names with prefix
GoodNameT = TypeVar("GoodNameT")
_T = TypeVar("_T")
_GoodNameT = TypeVar("_GoodNameT")
__GoodNameT = TypeVar("__GoodNameT")
GoodNameWithoutContra = TypeVar(  # [typevar-name-incorrect-variance]
    "GoodNameWithoutContra", contravariant=True
)
GoodNameT_co = TypeVar("GoodNameT_co", covariant=True)
GoodNameT_contra = TypeVar("GoodNameT_contra", contravariant=True)
GoodBoundNameT = TypeVar("GoodBoundNameT", bound=int)
GoodBoundNameT_co = TypeVar(  # [typevar-name-incorrect-variance]
    "GoodBoundNameT_co", bound=int
)
GoodBoundNameT_contra = TypeVar(  # [typevar-name-incorrect-variance]
    "GoodBoundNameT_contra", bound=int
)
GoodBoundNameT_co = TypeVar("GoodBoundNameT_co", bound=int, covariant=True)
GoodBoundNameT_contra = TypeVar("GoodBoundNameT_contra", bound=int, contravariant=True)

GoodBoundNameT_co = TypeVar("GoodBoundNameT_co", int, str, covariant=True)
GoodBoundNameT_co = TypeVar(  # [typevar-name-incorrect-variance]
    "GoodBoundNameT_co", int, str, contravariant=True
)
GoodBoundNameT_contra = TypeVar("GoodBoundNameT_contra", int, str, contravariant=True)
GoodBoundNameT_contra = TypeVar(  # [typevar-name-incorrect-variance]
    "GoodBoundNameT_contra", int, str, covariant=True
)

# Some of these will create a RunTime error but serve as a regression test
T = TypeVar(  # [typevar-name-incorrect-variance]
    "T", covariant=True, contravariant=True
)
T = TypeVar("T", covariant=False, contravariant=False)
T_co = TypeVar("T_co", covariant=True, contravariant=True)
T_contra = TypeVar(  # [typevar-name-incorrect-variance]
    "T_contra", covariant=True, contravariant=True
)
T_co = TypeVar("T_co", covariant=True, contravariant=False)
T_contra = TypeVar("T_contra", covariant=False, contravariant=True)

# PascalCase names without prefix
AnyStr = TypeVar("AnyStr")
DeviceTypeT = TypeVar("DeviceTypeT")
CALLABLE_T = TypeVar("CALLABLE_T")  # [invalid-name]
DeviceType = TypeVar("DeviceType")  # [invalid-name]
GoodNameWithoutContra = TypeVar(  # [typevar-name-incorrect-variance]
    "GoodNameWithoutContra", contravariant=True
)

# camelCase names with prefix
badName = TypeVar("badName")  # [invalid-name]
badNameWithoutContra = TypeVar(  # [invalid-name, typevar-name-incorrect-variance]]
    "badNameWithoutContra", contravariant=True
)
badName_co = TypeVar("badName_co", covariant=True)  # [invalid-name]
badName_contra = TypeVar("badName_contra", contravariant=True)  # [invalid-name]

# PascalCase names with lower letter prefix in tuple assignment
(
    a_BadName,  # [invalid-name]
    a_BadNameWithoutContra,  # [invalid-name, typevar-name-incorrect-variance]
) = TypeVar("a_BadName"), TypeVar("a_BadNameWithoutContra", contravariant=True)
GoodName_co, a_BadName_contra = TypeVar(  # [invalid-name]
    "GoodName_co", covariant=True
), TypeVar("a_BadName_contra", contravariant=True)
GoodName_co, VAR = TypeVar("GoodName_co", covariant=True), "a string"
