"""
https://github.com/pylint-dev/pylint/issues/4895
"""

# pylint: disable=missing-docstring

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Metric:
    function: Callable[..., tuple[int, int]]

    def update(self):
        _, _ = self.function()
