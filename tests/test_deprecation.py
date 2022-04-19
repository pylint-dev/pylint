# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check deprecation across the codebase."""

from __future__ import annotations

from typing import Any

import pytest

from pylint.checkers.mapreduce_checker import MapReduceMixin
from pylint.lint import PyLinter


def test_mapreducemixin() -> None:
    """Test that MapReduceMixin has been deprecated correctly."""

    class MyChecker(MapReduceMixin):
        def get_map_data(self) -> Any:
            ...

        def reduce_map_data(self, linter: PyLinter, data: list[Any]) -> None:
            ...

    with pytest.warns(DeprecationWarning):
        MyChecker()
