# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test the pyreverse primer commands."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from _pytest.capture import CaptureFixture

from pylint.testutils._primer.pyreverse_primer import PyreversePrimer

HERE = Path(__file__).parent
TEST_DIR_ROOT = HERE.parent.parent
PACKAGES_TO_PRIME_PATH = TEST_DIR_ROOT / "primer/packages_to_prime.json"
PYREVERSE_TARGETS_TO_PRIME_PATH = (
    TEST_DIR_ROOT / "primer/pyreverse_targets_to_prime.json"
)
CASES_PATH = HERE / "pyreverse_cases"

DEFAULT_ARGS = [
    "python tests/primer/pyreverse_primer.py",
    "compare",
    "--commit=deadbeef",
]

COMMIT = "1234567890abcdef"


def _load_fixture(directory: Path, filename: str) -> dict[str, dict[str, str]]:
    data: dict[str, dict[str, str]] = {}
    path = directory / filename
    if path.exists():
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw) if raw.strip() else {}
    prefix = filename.removesuffix(".json")
    for mmd_file in directory.glob(f"{prefix}_*.mmd"):
        target_name = mmd_file.stem.removeprefix(f"{prefix}_")
        if target_name not in data:
            data[target_name] = {}
        data[target_name]["commit"] = COMMIT
        data[target_name]["diagram"] = mmd_file.read_text(encoding="utf-8")
    return data


@pytest.mark.parametrize("args", [[], ["wrong_command"]])
def test_pyreverse_primer_launch_bad_args(
    args: list[str], capsys: CaptureFixture[str], tmp_path: Path
) -> None:
    with pytest.raises(SystemExit):
        with patch("sys.argv", ["python tests/primer/pyreverse_primer.py", *args]):
            PyreversePrimer(
                tmp_path,
                PACKAGES_TO_PRIME_PATH,
                PYREVERSE_TARGETS_TO_PRIME_PATH,
            ).run()
    out, err = capsys.readouterr()
    assert not out
    assert "usage: Pylint Pyreverse Primer" in err


@pytest.mark.parametrize(
    "directory",
    [
        pytest.param(path, id=path.name)
        for path in CASES_PATH.iterdir()
        if path.is_dir()
    ],
)
def test_compare(directory: Path, tmp_path: Path) -> None:
    base_data = _load_fixture(directory, "main.json")
    new_data = _load_fixture(directory, "pr.json")
    base_file = tmp_path / "main.json"
    new_file = tmp_path / "pr.json"
    base_file.write_text(json.dumps(base_data), encoding="utf-8")
    new_file.write_text(json.dumps(new_data), encoding="utf-8")
    with patch(
        "sys.argv",
        [
            *DEFAULT_ARGS,
            f"--base-file={base_file}",
            f"--new-file={new_file}",
        ],
    ):
        PyreversePrimer(
            tmp_path,
            PACKAGES_TO_PRIME_PATH,
            PYREVERSE_TARGETS_TO_PRIME_PATH,
        ).run()
    content = (tmp_path / "comment.txt").read_text(encoding="utf-8")
    expected = (directory / "expected_comment.md").read_text(encoding="utf-8")
    assert content == expected.rstrip("\n")


def test_truncated_compare(tmp_path: Path) -> None:
    directory = CASES_PATH / "multiple_targets"
    base_data = _load_fixture(directory, "main.json")
    new_data = _load_fixture(directory, "pr.json")
    base_file = tmp_path / "main.json"
    new_file = tmp_path / "pr.json"
    base_file.write_text(json.dumps(base_data), encoding="utf-8")
    new_file.write_text(json.dumps(new_data), encoding="utf-8")
    with patch(
        "pylint.testutils._primer.pyreverse_primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
        525,
    ):
        with patch(
            "sys.argv",
            [
                *DEFAULT_ARGS,
                f"--base-file={base_file}",
                f"--new-file={new_file}",
            ],
        ):
            PyreversePrimer(
                tmp_path,
                PACKAGES_TO_PRIME_PATH,
                PYREVERSE_TARGETS_TO_PRIME_PATH,
            ).run()
    content = (tmp_path / "comment.txt").read_text(encoding="utf-8")
    expected = (directory / "expected_comment_truncated.md").read_text(encoding="utf-8")
    assert content == expected.rstrip("\n")
    assert len(content) < 525


def test_run_writes_output(tmp_path: Path) -> None:
    fake_repo = Mock()
    fake_repo.head.object.hexsha = COMMIT

    def _render_diagram(*_: object, target_name: str) -> str:
        return f"classDiagram\n  class {target_name} {{\n  }}\n"

    with patch(
        "pylint.testutils._primer.pyreverse_primer_run_command.Repo",
        return_value=fake_repo,
    ):
        with patch(
            "pylint.testutils._primer.pyreverse_primer_run_command.RunCommand._render_target",
            autospec=True,
            side_effect=lambda _self, _package_directory, target_name: _render_diagram(
                target_name=target_name
            ),
        ) as mock_render_target:
            with patch(
                "sys.argv",
                [
                    "python tests/primer/pyreverse_primer.py",
                    "run",
                    "--type=main",
                ],
            ):
                PyreversePrimer(
                    tmp_path,
                    PACKAGES_TO_PRIME_PATH,
                    PYREVERSE_TARGETS_TO_PRIME_PATH,
                ).run()

    output_path = (
        tmp_path
        / f"pyreverse_output_{'.'.join(str(i) for i in sys.version_info[:2])}_main.txt"
    )
    content = json.loads(output_path.read_text(encoding="utf-8"))
    assert mock_render_target.call_count == 3
    assert list(content) == ["classdef", "functiondef", "assignname"]
    assert content["classdef"] == {
        "commit": COMMIT,
        "diagram": "classDiagram\n  class classdef {\n  }\n",
    }
