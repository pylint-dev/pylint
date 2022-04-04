from typing import TypeVar

T = TypeVar("T", covariant=True, contravariant=True)  # [typevar-double-variance]
