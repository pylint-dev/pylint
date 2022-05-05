# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check deprecation across the codebase."""

from __future__ import annotations

from typing import Any

import pytest

from pylint.checkers import BaseChecker
from pylint.checkers.mapreduce_checker import MapReduceMixin
from pylint.interfaces import (
    IAstroidChecker,
    IChecker,
    Interface,
    IRawChecker,
    IReporter,
    ITokenChecker,
)
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter
from pylint.reporters.ureports.nodes import Section


def test_mapreducemixin() -> None:
    """Test that MapReduceMixin has been deprecated correctly."""

    class MyChecker(MapReduceMixin):
        def get_map_data(self) -> Any:
            ...

        def reduce_map_data(self, linter: PyLinter, data: list[Any]) -> None:
            ...

    with pytest.warns(DeprecationWarning):
        MyChecker()


def test_reporter_implements() -> None:
    """Test that __implements__ on BaseReporer has been deprecated correctly."""

    class MyReporter(BaseReporter):

        __implements__ = IReporter

        def _display(self, layout: Section) -> None:
            ...

    with pytest.warns(DeprecationWarning):
        MyReporter()


def test_checker_implements() -> None:
    """Test that __implements__ on BaseChecker has been deprecated correctly."""

    class MyChecker(BaseChecker):

        __implements__ = IAstroidChecker

    with pytest.warns(DeprecationWarning):
        MyChecker(PyLinter())


def test_interfaces() -> None:
    """Test that all interfaces have been deprecated correctly."""
    with pytest.warns(DeprecationWarning):
        Interface()
    with pytest.warns(DeprecationWarning):
        IAstroidChecker()
    with pytest.warns(DeprecationWarning):
        IReporter()
    with pytest.warns(DeprecationWarning):
        IRawChecker()
    with pytest.warns(DeprecationWarning):
        IChecker()
    with pytest.warns(DeprecationWarning):
        ITokenChecker()


def test_load_and_save_results() -> None:
    """Test that load_results and save_results are deprecated."""
    # TODO 3.0: Remove this test.
    # pylint: disable=import-outside-toplevel
    from pylint.config import load_results, save_results

    with pytest.warns(DeprecationWarning):
        save_results(object(), "")  # type: ignore[arg-type]
    with pytest.warns(DeprecationWarning):
        load_results("")
