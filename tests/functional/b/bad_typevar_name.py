"""Test case for bad-typevar-name."""

from typing import TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co")  # [bad-typevar-name]
T_contra = TypeVar("T_contra")  # [bad-typevar-name]

CT_co = TypeVar("CT_co", contravariant=True)  # [bad-typevar-name]
RT_contra = TypeVar("RT_contra")  # [bad-typevar-name]
VT_contra = TypeVar("VT_contra", contravariant=True)
VT = TypeVar("VT", covariant=True)  # [bad-typevar-name]

K = TypeVar("K")
K_co = TypeVar("K_co", covariant=True)
K_contra = TypeVar("K_contra", covariant=True)  # [bad-typevar-name]

N = TypeVar("N")
N_co = TypeVar("N_co", covariant=True)
N_contra = TypeVar("N_contra", contravariant=True)

BadName = TypeVar("BadName", contravariant=True)  # [bad-typevar-name]
GoodName_co = TypeVar("GoodName_co", covariant=True)
