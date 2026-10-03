# pylint: disable=missing-docstring
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .a import LstT

var: "LstT" = [1, 2]
