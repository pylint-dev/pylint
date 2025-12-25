"""Tests ensuring recursive discovery respects ignore options."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from pylint.lint.pylinter import PyLinter


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


def _recursive_discovered_paths(
    linter: PyLinter, base: Path, targets: list[Path]
) -> set[Path]:
    linter.open()
    return {
        Path(path).resolve().relative_to(base)
        for path in linter._discover_files([str(target) for target in targets])
    }


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

    linted = _recursive_discovered_paths(linter, sample_tree, [sample_tree])

    assert Path("single.py") in linted
    assert Path("pkg") in linted
    assert Path("a/foo.py") in linted

    assert Path(".hidden/bar.py") not in linted
    assert Path("pkg/.hiddenpkg/baz.py") not in linted
    assert Path(".a/foo.py") not in linted


def test_recursive_ignore_option_skips_directory(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = True
    linter.config.ignore = tuple(list(linter.config.ignore) + [".a"])

    linted = _recursive_discovered_paths(linter, sample_tree, [sample_tree])

    assert Path(".a/foo.py") not in linted
    assert Path("a/foo.py") in linted
    assert Path("single.py") in linted


def test_recursive_ignore_paths_skip_pattern(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = True
    linter.config.ignore_paths = tuple(
        list(linter.config.ignore_paths)
        + [re.compile(r".*/\.a(?:/|\\|$).*")]
    )

    linted = _recursive_discovered_paths(linter, sample_tree, [sample_tree])

    assert Path(".a/foo.py") not in linted
    assert Path("a/foo.py") in linted
    assert Path("pkg") in linted


def test_recursive_ignore_patterns_on_filename(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = True
    linter.config.ignore_patterns = tuple(
        list(linter.config.ignore_patterns) + [re.compile(r"^foo\.py$")]
    )

    linted = _recursive_discovered_paths(linter, sample_tree, [sample_tree])

    assert Path("a/foo.py") not in linted
    assert Path(".a/foo.py") not in linted
    assert Path("pkg") in linted
    assert Path("single.py") in linted


def test_non_recursive_single_file_unchanged(
    linter: PyLinter, sample_tree: Path
) -> None:
    linter.config.recursive = False

    linter.open()
    module_descriptions = linter._expand_files([str(sample_tree / "single.py")])
    linted = {Path(description["path"]) for description in module_descriptions}

    assert Path(sample_tree / "single.py") in linted
