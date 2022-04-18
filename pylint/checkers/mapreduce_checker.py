# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class MapReduceMixin(metaclass=abc.ABCMeta):
    """A mixin design to allow multiprocess/threaded runs of a Checker."""

    @abc.abstractmethod
    def get_map_data(self) -> Any:
        """Returns mergeable/reducible data that will be examined."""

    @abc.abstractmethod
    def reduce_map_data(self, linter: PyLinter, data: list[Any]) -> None:
        """For a given Checker, receives data for all mapped runs."""
