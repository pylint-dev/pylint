# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check deprecation across the codebase."""

from __future__ import annotations

from typing import Any

import pytest
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.mapreduce_checker import MapReduceMixin
from pylint.config import load_results, save_results
from pylint.interfaces import (
    IAstroidChecker,
    IChecker,
    Interface,
    IRawChecker,
    IReporter,
    ITokenChecker,
)
from pylint.lint import PyLinter
from pylint.message import MessageDefinitionStore
from pylint.reporters import BaseReporter
from pylint.reporters.ureports.nodes import Section
from pylint.utils import FileState


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
    """Test that __implements__ on BaseReporter has been deprecated correctly."""

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
    with pytest.warns(DeprecationWarning):
        save_results(object(), "")  # type: ignore[arg-type]
    with pytest.warns(DeprecationWarning):
        load_results("")


def test_filestate() -> None:
    """Test that FileState needs its arguments."""
    with pytest.warns(DeprecationWarning):
        FileState()
    with pytest.warns(DeprecationWarning):
        FileState("foo")
    with pytest.warns(DeprecationWarning):
        FileState(msg_store=MessageDefinitionStore())
    FileState("foo", MessageDefinitionStore())


def test_collectblocklines() -> None:
    """Test FileState.collect_block_lines."""
    state = FileState("foo", MessageDefinitionStore())
    with pytest.warns(DeprecationWarning):
        state.collect_block_lines(MessageDefinitionStore(), nodes.Module("foo"))
