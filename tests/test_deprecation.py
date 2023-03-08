# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check deprecation across the codebase."""

from __future__ import annotations

from typing import Any

import pytest
from astroid import nodes

from pylint import lint
from pylint.checkers.mapreduce_checker import MapReduceMixin
from pylint.config import load_results, save_results
from pylint.lint import PyLinter
from pylint.message import MessageDefinitionStore
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


def test_patch_sys_path() -> None:
    """Test that _patch_sys_path() is deprecated"""
    with pytest.deprecated_call():
        lint._patch_sys_path([])


def test_fix_import_path() -> None:
    """Test that fix_import_path() is deprecated"""
    with pytest.deprecated_call():
        with lint.fix_import_path([]):
            pass
