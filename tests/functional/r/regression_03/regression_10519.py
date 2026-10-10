# Regression test for https://github.com/pylint-dev/pylint/issues/10519
# Inheriting from a generic dataclass that rebinds __init__ in
# __init_subclass__ used to crash with an AstroidBuildingError.
# Fixed with astroid 4.3.0.
"""Crash regression test for generic dataclass with __init_subclass__."""
# pylint: disable=too-few-public-methods
from abc import ABC
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import ParamSpec

_P = ParamSpec("_P")


@dataclass
class Basket[FruitT](ABC):
    """Generic dataclass rebinding __init__ in __init_subclass__."""

    _fruit: FruitT | None = field(init=False)
    _labels: dict[str, str] = field(init=False)

    def __init_subclass__(cls) -> None:
        def _wrap(func: Callable[_P, None]) -> Callable[_P, None]:
            def _wrapped(*args: _P.args, **kwargs: _P.kwargs) -> None:
                self = args[0]
                func(*args, **kwargs)
                if not hasattr(self, "_fruit"):
                    object.__setattr__(self, "_fruit", None)
                if not hasattr(self, "_labels"):
                    object.__setattr__(self, "_labels", {})

            return _wrapped

        cls.__init__ = _wrap(cls.__init__)  # type: ignore[method-assign]


@dataclass
class AppleBasket(Basket):
    """Subclass without subscripting the generic base."""
