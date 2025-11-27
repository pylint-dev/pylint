# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pathlib import Path

from pylint.lint.expand_modules import expand_modules
from pylint.lint.pylinter import PyLinter


def test_ignore_hidden_dir_with_recursive(tmp_path, linter, monkeypatch):
    hidden_dir = tmp_path / ".a"
    hidden_dir.mkdir()
    (hidden_dir / "foo.py").write_text("print('foo')\n", encoding="utf8")
    (tmp_path / "bar.py").write_text("print('bar')\n", encoding="utf8")

    monkeypatch.chdir(tmp_path)
    linter.global_set_option("ignore-paths", r"^\.a")

    discovered = tuple(PyLinter._discover_files(["."]))
    modules, errors = expand_modules(
        discovered,
        list(linter.config.ignore),
        list(linter.config.ignore_patterns),
        linter.config.ignore_paths,
    )

    assert not errors
    paths = {Path(module["path"]) for module in modules}
    assert any(path.name == "bar.py" for path in paths)
    assert all(path.name != "foo.py" for path in paths)


def test_ignore_paths_normalization_removes_leading_dot_slash(
    tmp_path, linter, monkeypatch
):
    hidden_dir = tmp_path / ".a"
    hidden_dir.mkdir()
    (hidden_dir / "foo.py").write_text("print('foo')\n", encoding="utf8")

    monkeypatch.chdir(tmp_path)
    linter.global_set_option("ignore-paths", r"^\.a")

    modules, errors = expand_modules(
        ["./.a/foo.py"],
        list(linter.config.ignore),
        list(linter.config.ignore_patterns),
        linter.config.ignore_paths,
    )

    assert not errors
    assert modules == []


def test_ignore_paths_supports_prefixed_dot_slash(tmp_path, linter, monkeypatch):
    hidden_dir = tmp_path / ".a"
    hidden_dir.mkdir()
    (hidden_dir / "foo.py").write_text("print('foo')\n", encoding="utf8")
    (tmp_path / "bar.py").write_text("print('bar')\n", encoding="utf8")

    monkeypatch.chdir(tmp_path)
    linter.global_set_option("ignore-paths", r"^\./\.a")

    discovered = tuple(PyLinter._discover_files(["."]))
    modules, errors = expand_modules(
        discovered,
        list(linter.config.ignore),
        list(linter.config.ignore_patterns),
        linter.config.ignore_paths,
    )

    assert not errors
    paths = {Path(module["path"]) for module in modules}
    assert any(path.name == "bar.py" for path in paths)
    assert all(path.name != "foo.py" for path in paths)
