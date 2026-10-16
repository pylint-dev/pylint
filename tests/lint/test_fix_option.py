# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""End to end tests of the --fix, --unsafe-fixes, --fix-diff and --unfixable options."""

# pylint: disable=redefined-outer-name

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from pylint.lint import PyLinter
from pylint.lint.fixer import fix_files
from pylint.message import Applicability
from pylint.reporters.json_reporter import JSON2Reporter
from pylint.testutils._run import _Run as Run

PLUGIN_DIRECTORY = str(Path(__file__).parent.parent / "regrtest_data" / "fix")

SOURCE = '''"""Module docstring."""
old_name = 1
print(old_name, "é", old_name)  # comment
x = double((old_name  +  1))


def function():
    """Function docstring."""
    print(1)
    pass
'''

SAFE_FIXED = '''"""Module docstring."""
old_name = 1
print(new_name, "é", new_name)  # comment
x = (new_name  +  1) * 2


def function():
    """Function docstring."""
    print(1)
    pass
'''

ENABLED = "old-name-used,useless-pass-statement,double-number"


@pytest.fixture
def sample(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.syspath_prepend(PLUGIN_DIRECTORY)
    monkeypatch.setenv(
        "PYTHONPATH",
        os.pathsep.join([PLUGIN_DIRECTORY, os.environ.get("PYTHONPATH", "")]),
    )
    path = tmp_path / "sample.py"
    path.write_text(SOURCE, encoding="utf-8")
    return path


def _run(path: Path, *options: str) -> int:
    with pytest.raises(SystemExit) as exit_info:
        Run(
            [
                "--rcfile=/dev/null",
                "--load-plugins=fix_plugin",
                "--disable=all",
                f"--enable={ENABLED}",
                "--persistent=no",
                "--score=no",
                *options,
                str(path),
            ]
        )
    return int(exit_info.value.code or 0)


def test_fix_applies_safe_fixes_until_nothing_changes(
    sample: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # 'double-number' overlaps an 'old-name-used' fix, it is fixed on a second pass
    assert _run(sample, "--fix") == 4
    assert sample.read_text(encoding="utf-8") == SAFE_FIXED
    out, err = capsys.readouterr()
    assert "Fixed 4 message(s) in 1 file(s)." in err
    assert "useless-pass-statement" in out
    assert "old-name-used" not in out
    assert "Fixes available: 1 more with --fix --unsafe-fixes." in err


def test_unsafe_fixes(sample: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run(sample, "--fix", "--unsafe-fixes") == 0
    assert sample.read_text(encoding="utf-8") == SAFE_FIXED.replace(
        "    print(1)\n    pass\n", "    print(1)\n    \n"
    )
    out, err = capsys.readouterr()
    assert not out
    assert "Fixes available" not in err


def test_unsafe_fixes_alone_changes_nothing(sample: Path) -> None:
    assert _run(sample, "--unsafe-fixes") == 4
    assert sample.read_text(encoding="utf-8") == SOURCE


def test_fix_diff_does_not_write(
    sample: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _run(sample, "--fix-diff") == 1
    assert sample.read_text(encoding="utf-8") == SOURCE
    out, err = capsys.readouterr()
    assert '-print(old_name, "é", old_name)  # comment\n' in out
    assert '+print(new_name, "é", new_name)  # comment\n' in out
    # A single pass is done, the fix overlapping the first one is not shown
    assert "-x = double((old_name  +  1))\n" in out
    assert "+x = (old_name  +  1) * 2\n" in out
    assert "Would fix 3 message(s) in 1 file(s)." in err


def test_fix_diff_without_fixes(
    sample: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sample.write_text("print(1)\n", encoding="utf-8")
    assert _run(sample, "--fix-diff") == 0
    assert capsys.readouterr().out == ""


def test_unfixable(sample: Path) -> None:
    assert _run(sample, "--fix", "--unfixable=W9901") == 4
    assert sample.read_text(encoding="utf-8") == SOURCE.replace(
        "x = double((old_name  +  1))", "x = (old_name  +  1) * 2"
    )


def _linter_with_plugin() -> PyLinter:
    linter = PyLinter()
    linter.load_default_plugins()
    linter.load_plugin_modules(["fix_plugin"])
    linter.disable("all")
    for symbol in ENABLED.split(","):
        linter.enable(symbol)
    linter.load_plugin_configuration()
    linter.config.persistent = False
    return linter


@pytest.mark.needs_two_cores
def test_fix_in_parallel(sample: Path) -> None:
    # Run() creates a reporter that cannot be pickled under pytest capture
    linter = _linter_with_plugin()
    linter.config.jobs = 2
    summary = fix_files(linter, [str(sample)], {Applicability.SAFE})
    assert sample.read_text(encoding="utf-8") == SAFE_FIXED
    assert summary.applied == 4


def test_hint_without_fix(sample: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run(sample) == 4
    assert sample.read_text(encoding="utf-8") == SOURCE
    assert (
        "Fixes available: 4 fixable with the --fix option, "
        "1 more with --fix --unsafe-fixes." in capsys.readouterr().err
    )


def test_fix_refuses_stdin(sample: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert _run(sample, "--fix", "--from-stdin") == 32
    assert "cannot be used with --from-stdin" in capsys.readouterr().err


def test_files_with_syntax_errors_are_not_fixed(sample: Path) -> None:
    broken = SOURCE + "def (:\n"
    sample.write_text(broken, encoding="utf-8")
    _run(sample, "--fix", "--enable=syntax-error")
    assert sample.read_text(encoding="utf-8") == broken


def test_json2_output_round_trip(
    sample: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _run(
        sample,
        "--output-format=json2",
        "--enable=double-number",
        "--disable=W9901,W9902",
    )
    messages = json.loads(capsys.readouterr().out)["messages"]
    assert messages[0]["fix"] == {
        "description": "Multiply by two",
        "applicability": "safe",
        "edits": [
            {
                "line": 4,
                "column": 4,
                "endLine": 4,
                "endColumn": 28,
                "newText": "(old_name  +  1) * 2",
            }
        ],
    }
    message = JSON2Reporter.deserialize(messages[0])
    assert message.fix is not None
    assert JSON2Reporter.serialize(message) == messages[0]
    del messages[0]["fix"]
    message = JSON2Reporter.deserialize(messages[0])
    assert message.fix is None
    assert "fix" not in JSON2Reporter.serialize(message)


def test_fix_files_reports_files_that_did_not_converge(sample: Path) -> None:
    linter = _linter_with_plugin()
    summary = fix_files(linter, [str(sample)], {Applicability.SAFE}, max_passes=1)
    assert summary.not_converged == [str(sample)]
    assert summary.applied == 3
