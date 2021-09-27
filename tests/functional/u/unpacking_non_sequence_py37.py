# pylint: disable=missing-docstring

# https://github.com/PyCQA/pylint/issues/4895
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Metric:
    function: Callable[..., tuple[int, int]]

    def update(self):
        _, _ = self.function()
