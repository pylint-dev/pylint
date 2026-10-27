# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os
from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from pylint import run_pylint
from pylint.lint import Run
from pylint.reporters import CollectingReporter


def test_run_pylint_with_invalid_argument(capsys: CaptureFixture[str]) -> None:
    """Check that appropriate exit code is used with invalid argument."""
    with pytest.raises(SystemExit) as ex:
        run_pylint(["--never-use-this"])
    captured = capsys.readouterr()
    assert captured.err.startswith("usage: pylint [options]")
    assert ex.value.code == 32


def test_run_pylint_with_invalid_argument_in_config(
    capsys: CaptureFixture[str], tmp_path: Path
) -> None:
    """Check that appropriate exit code is used with an ambiguous
    argument in a config file.
    """
    test_file = tmp_path / "testpylintrc"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("[MASTER]\nno=")

    with pytest.raises(SystemExit) as ex:
        run_pylint(["--rcfile", f"{test_file}"])
    captured = capsys.readouterr()
    assert captured.err.startswith("usage: pylint [options]")
    assert ex.value.code == 32


@pytest.mark.skipif(
    os.name != "nt", reason="requires Windows case-insensitive filenames"
)
@pytest.mark.parametrize("initializer_name", ["__Init__.py", "__INIT__.PY"])
def test_run_pylint_case_insensitive_initializer(
    tmp_path: Path, initializer_name: str
) -> None:
    """Alternate initializer spellings do not produce an invalid module name."""
    package = tmp_path / "package"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    reporter = CollectingReporter()

    run = Run(
        [
            "--rcfile=",
            "--persistent=n",
            "--disable=all",
            "--enable=invalid-name",
            "--reports=n",
            "--score=n",
            str(package / initializer_name),
        ],
        reporter=reporter,
        exit=False,
    )

    assert not reporter.messages
    assert run.linter.msg_status == 0
