# pylint: disable=missing-docstring


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import math


VAR = 'pylint'  # [unused-variable]


try:
    pass
except TypeError as exc:
    print(exc)
except ValueError as exc:
    print(exc)
