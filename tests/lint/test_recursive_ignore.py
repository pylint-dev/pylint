"""Tests ensuring recursive discovery respects ignore options."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pytest

from pylint.lint.pylinter import PyLinter
from pylint.testutils import GenericTestReporter


def _write_module(path: Path) -> None:
    path.write_text("import os\n", encoding="utf-8")


def _build_sample_tree(root: Path) -> None:
    (root / "a").mkdir()
    _write_module(root / "a" / "foo.py")

    (root / ".hidden").mkdir()
    _write_module(root / ".hidden" / "bar.py")

    (root / "pkg").mkdir()
    _write_module(root / "pkg" / "__init__.py")
    _write_module(root / "pkg" / "mod.py")

    (root / "pkg" / ".hiddenpkg").mkdir()
    _write_module(root / "pkg" / ".hiddenpkg" / "baz.py")

    (root / ".a").mkdir()
    _write_module(root / ".a" / "foo.py")

    _write_module(root / "single.py")


def _run_linter(linter: PyLinter, targets: Iterable[str | Path]) -> set[Path]:
    linter.set_reporter(GenericTestReporter())
    linter.check([str(target) for target in targets])
    return {
        Path(message.path)
        for message in linter.reporter.messages
    }


def _relative_paths(messages: set[Path], base: Path) -> set[Path]:
    return {path.relative_to(base) for path in messages}


@pytest.fixture()
def sample_tree(tmp_path: Path) -> Path:
    _build_sample_tree(tmp_path)
    return tmp_path


def test_recursive_ignore_patterns_skip_hidden_directories(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = True
    linter.config.ignore_patterns = tuple(
        list(linter.config.ignore_patterns) + [re.compile(r"^\.")]
    )

    linted = _relative_paths(_run_linter(linter, [sample_tree]), sample_tree)

    assert Path("single.py") in linted
    assert Path("pkg/__init__.py") in linted
    assert Path("pkg/mod.py") in linted
    assert Path("a/foo.py") in linted

    assert Path(".hidden/bar.py") not in linted
    assert Path("pkg/.hiddenpkg/baz.py") not in linted
    assert Path(".a/foo.py") not in linted


def test_recursive_ignore_option_skips_directory(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = True
    linter.config.ignore = tuple(list(linter.config.ignore) + [".a"])

    linted = _relative_paths(_run_linter(linter, [sample_tree]), sample_tree)

    assert Path(".a/foo.py") not in linted
    assert Path("a/foo.py") in linted


def test_recursive_ignore_paths_skip_pattern(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = True
    linter.config.ignore_paths = [re.compile(r".*/\.a(/|\\).*")]

    linted = _relative_paths(_run_linter(linter, [sample_tree]), sample_tree)

    assert Path(".a/foo.py") not in linted
    assert Path("a/foo.py") in linted


def test_recursive_ignore_patterns_on_filename(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = True
    linter.config.ignore_patterns = tuple(
        list(linter.config.ignore_patterns) + [re.compile(r"^foo\.py$")]
    )

    linted = _relative_paths(_run_linter(linter, [sample_tree]), sample_tree)

    assert Path("a/foo.py") not in linted
    assert Path(".a/foo.py") not in linted
    assert Path("pkg/mod.py") in linted
    assert Path("single.py") in linted


def test_non_recursive_single_file_unchanged(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = False

    linted = _run_linter(linter, [sample_tree / "single.py"])

    assert Path(sample_tree / "single.py") in linted
