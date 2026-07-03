# pylint: disable=missing-module-docstring,missing-class-docstring,too-few-public-methods,invalid-name

from typing import ForwardRef

Cls = ForwardRef("Cls")


class Cls:
    pass
