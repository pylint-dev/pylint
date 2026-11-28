# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Resolve private spelling dictionaries relative to their configuration file."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pylint.testutils._run import _Run as Run

EMPTY_MODULE = Path(__file__).parents[1] / "regrtest_data" / "empty.py"


def _write_config(directory: Path, config_format: str, value: str) -> Path:
    if config_format == "ini":
        config = directory / "pylintrc"
        text = f"[SPELLING]\nspelling-private-dict-file={value}\n"
    else:
        config = directory / "pyproject.toml"
        text = (
            f"[tool.pylint.spelling]\nspelling-private-dict-file={json.dumps(value)}\n"
        )
    config.write_text(text, encoding="utf-8")
    return config


def _run(*args: str) -> Run:
    return Run(
        [
            "--disable=all",
            "--enable=syntax-error",
            "--persistent=no",
            "--score=no",
            *args,
            str(EMPTY_MODULE),
        ],
        exit=False,
    )


@pytest.mark.parametrize("config_format", ["ini", "toml"])
@pytest.mark.parametrize("relative_config", [False, True])
def test_private_dictionary_relative_to_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    config_format: str,
    relative_config: bool,
) -> None:
    config = _write_config(tmp_path, config_format, ".pylint_dictionary")
    dictionary = tmp_path / ".pylint_dictionary"
    dictionary.write_text("pylintword\n", encoding="utf-8")
    subdirectory = tmp_path / "package"
    subdirectory.mkdir()
    monkeypatch.chdir(subdirectory)
    config_argument = Path("..") / config.name if relative_config else config

    runner = _run(f"--rcfile={config_argument}")

    actual = Path(runner.linter.config.spelling_private_dict_file)
    assert actual == dictionary
    assert actual.read_text(encoding="utf-8") == "pylintword\n"


@pytest.mark.parametrize("config_format", ["ini", "toml"])
@pytest.mark.parametrize("path_kind", ["absolute", "home", "environment", "empty"])
def test_private_dictionary_expansion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    config_format: str,
    path_kind: str,
) -> None:
    dictionary = tmp_path / "dictionary"
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv("PYLINT_TEST_DICTIONARY", str(dictionary))
    values = {
        "absolute": str(dictionary),
        "home": "~/dictionary",
        "environment": "$PYLINT_TEST_DICTIONARY",
        "empty": "",
    }
    config = _write_config(tmp_path, config_format, values[path_kind])
    runner = _run(f"--rcfile={config}")
    actual = runner.linter.config.spelling_private_dict_file
    if path_kind == "empty":
        assert actual == ""
    else:
        assert Path(actual) == dictionary


@pytest.mark.parametrize("config_format", ["ini", "toml"])
@pytest.mark.parametrize("override", ["local_dictionary", ""])
def test_private_dictionary_cli_override(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    config_format: str,
    override: str,
) -> None:
    config = _write_config(tmp_path, config_format, ".pylint_dictionary")
    subdirectory = tmp_path / "package"
    subdirectory.mkdir()
    monkeypatch.chdir(subdirectory)
    runner = _run(f"--rcfile={config}", f"--spelling-private-dict-file={override}")
    assert runner.linter.config.spelling_private_dict_file == override


def test_private_dictionary_cli_without_config() -> None:
    runner = _run("--rcfile=", "--spelling-private-dict-file=local_dictionary")
    assert runner.linter.config.spelling_private_dict_file == "local_dictionary"


@pytest.mark.parametrize("config_format", ["ini", "toml"])
def test_private_dictionary_spelling_from_subdirectory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    config_format: str,
) -> None:
    enchant = pytest.importorskip("enchant", exc_type=ImportError)
    if not enchant.dict_exists("en_US"):
        pytest.skip("en_US spelling dictionary is unavailable")
    word = "pylintprivateword"
    assert not enchant.Dict("en_US").check(word)
    dictionary = tmp_path / ".pylint_dictionary"
    dictionary.write_text(f"{word}\n", encoding="utf-8")
    config = _write_config(tmp_path, config_format, dictionary.name)
    subdirectory = tmp_path / "package"
    subdirectory.mkdir()
    module = subdirectory / "module.py"
    module.write_text(f"# {word}\n", encoding="utf-8")
    monkeypatch.chdir(subdirectory)

    runner = Run(
        [
            f"--rcfile={config}",
            "--disable=all",
            "--enable=wrong-spelling-in-comment",
            "--spelling-dict=en_US",
            "--persistent=no",
            "--score=no",
            str(module),
        ],
        exit=False,
    )

    assert runner.linter.stats.by_msg == {}
    assert not (subdirectory / dictionary.name).exists()
