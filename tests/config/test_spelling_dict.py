# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Spelling dictionary configuration without platform-specific dictionaries."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pytest

from pylint.checkers.spelling import SpellingChecker
from pylint.testutils._run import _Run as Run

EMPTY_MODULE = Path(__file__).parents[1] / "regrtest_data" / "empty.py"


@pytest.fixture(
    name="dictionaries",
    params=[[], ["en_US", "en_GB"]],
    ids=["no-dictionaries", "dictionaries"],
)
def fixture_dictionaries(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> list[str]:
    """Control available dictionaries independently of the Enchant installation."""
    available: list[str] = request.param
    monkeypatch.setattr(
        SpellingChecker,
        "options",
        tuple(
            (
                (name, {**option, "choices": ["", *available]})
                if name == "spelling-dict"
                else (name, option)
            )
            for name, option in SpellingChecker.options
        ),
    )
    return available


def _run(*args: str) -> Run:
    return Run(
        [
            "--disable=all",
            "--enable=syntax-error",
            "--reports=no",
            "--score=no",
            *args,
            str(EMPTY_MODULE),
        ],
        exit=False,
    )


def _assert_dictionary_error(stderr: str, dictionaries: list[str]) -> None:
    if dictionaries:
        assert "invalid choice" in stderr
        assert "en_US" in stderr
        assert "en_GB" in stderr
        assert "pyenchant" not in stderr
    else:
        assert "No spelling dictionaries available" in stderr
        assert "pyenchant" in stderr
        assert "system dependencies" in stderr


@pytest.mark.usefixtures("dictionaries")
def test_spelling_dict_default_and_help() -> None:
    runner = _run()
    assert runner.linter.config.spelling_dict == ""
    help_text = runner.linter._arg_parser.format_help()
    spelling_help = help_text.split("  --spelling-dict <dict name>")[1].split(
        "  --spelling-ignore-words"
    )[0]
    assert "(default: )" in spelling_help


@pytest.mark.parametrize("value", ["", "en_US", "missing"])
def test_spelling_dict_cli(
    dictionaries: list[str], value: str, capsys: pytest.CaptureFixture[str]
) -> None:
    if not value or value in dictionaries:
        assert _run(f"--spelling-dict={value}").linter.config.spelling_dict == value
    else:
        with pytest.raises(SystemExit) as exc:
            _run(f"--spelling-dict={value}")
        assert exc.value.code == 2
        _assert_dictionary_error(capsys.readouterr().err, dictionaries)


@pytest.mark.parametrize("config_format", ["rc", "toml"])
def test_spelling_dict_configuration_error(
    dictionaries: list[str],
    config_format: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config = tmp_path / ("pylintrc" if config_format == "rc" else "pyproject.toml")
    config.write_text(
        (
            "[SPELLING]\nspelling-dict=missing\n"
            if config_format == "rc"
            else '[tool.pylint.spelling]\nspelling-dict="missing"\n'
        ),
        encoding="utf-8",
    )
    with pytest.raises(SystemExit) as exc:
        _run(f"--rcfile={config}")
    assert exc.value.code == 32
    _assert_dictionary_error(capsys.readouterr().err, dictionaries)


@pytest.mark.parametrize("config_format", ["rc", "toml"])
def test_spelling_dict_configuration_roundtrip(
    dictionaries: list[str], config_format: str, tmp_path: Path
) -> None:
    value = "en_US" if dictionaries else ""
    runner = _run(f"--spelling-dict={value}")
    config = tmp_path / ("pylintrc" if config_format == "rc" else "pyproject.toml")
    if config_format == "rc":
        stream = StringIO()
        runner.linter._generate_config(stream)
        config.write_text(stream.getvalue(), encoding="utf-8")
    else:
        config.write_text(runner.linter._generate_config_file(), encoding="utf-8")
    assert _run(f"--rcfile={config}").linter.config.spelling_dict == value
    assert (
        _run(f"--rcfile={config}", "--spelling-dict=").linter.config.spelling_dict == ""
    )
    if dictionaries:
        assert (
            _run(
                f"--rcfile={config}", "--spelling-dict=en_GB"
            ).linter.config.spelling_dict
            == "en_GB"
        )


def test_spelling_dict_set_option(dictionaries: list[str]) -> None:
    linter = _run().linter
    if dictionaries:
        linter.set_option("spelling-dict", "en_US")
        assert linter.config.spelling_dict == "en_US"
    linter.set_option("spelling-dict", "")
    assert linter.config.spelling_dict == ""
