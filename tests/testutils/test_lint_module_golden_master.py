# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for ``LintModuleTest.runTest`` with the golden_master fixture."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest
from pytest_remaster import GoldenMaster

from pylint.testutils import FunctionalTestFile, LintModuleTest

FIXTURE_DIRECTORY = Path(__file__).parent / "data/functional"
DIRECTORIES = sorted(FIXTURE_DIRECTORY.iterdir())
EXPECTED_OUTPUT = "exec-used:7:0:7:14::Use of exec:UNDEFINED\n"
CURRENT = "".join(str(v) for v in sys.version_info[:2])


def _lint_module(directory: Path, filename: str) -> LintModuleTest:
    return LintModuleTest(FunctionalTestFile(str(directory), filename))


@pytest.mark.parametrize("remaster", [True, False], ids=["remaster", "strict"])
@pytest.mark.parametrize(
    "directory_path", DIRECTORIES, ids=[p.name for p in DIRECTORIES]
)
def test_run_test_golden_master(
    directory_path: Path, tmp_path: Path, remaster: bool
) -> None:
    """The messages are checked first, then the output is a golden master."""
    new_path = tmp_path / directory_path.name
    shutil.copytree(directory_path, new_path)
    expected_file = new_path / "exec_used.txt"
    before = expected_file.read_text("utf8") if expected_file.exists() else None
    golden_master = GoldenMaster(remaster=remaster)
    lint_module = _lint_module(new_path, "exec_used.py")
    if directory_path.name.endswith("wrong_test"):
        # pytest-remaster cannot fix the annotations, the .txt is not touched
        with pytest.raises(AssertionError, match=r"Wrong message\(s\) raised"):
            lint_module.runTest(golden_master)
        assert (
            expected_file.read_text("utf8") if expected_file.exists() else None
        ) == before
        return
    if directory_path.name.startswith("ok_output"):
        lint_module.runTest(golden_master)
        golden_master.assert_remastered()
    elif remaster:
        lint_module.runTest(golden_master)
        with pytest.raises(pytest.fail.Exception, match="Expected files updated"):
            golden_master.assert_remastered()
    else:
        with pytest.raises(pytest.fail.Exception, match="--remaster"):
            lint_module.runTest(golden_master)
        return
    assert expected_file.read_text("utf8") == EXPECTED_OUTPUT


def test_run_test_golden_master_fallback_is_strict(tmp_path: Path) -> None:
    """The output of an older Python version is not rewritten from this one."""
    shutil.copytree(FIXTURE_DIRECTORY / "wrong_output_ok_test", tmp_path / "test")
    fallback = tmp_path / "test" / "exec_used.30.txt"
    (tmp_path / "test" / "exec_used.txt").rename(fallback)
    before = fallback.read_text("utf8")
    with pytest.raises(pytest.fail.Exception, match=rf"exec_used\.{CURRENT}\.txt"):
        _lint_module(tmp_path / "test", "exec_used.py").runTest(
            GoldenMaster(remaster=True)
        )
    assert fallback.read_text("utf8") == before


def test_run_test_golden_master_empty_version_file_is_kept(tmp_path: Path) -> None:
    """Deleting this version's file would make it read the generic one."""
    version_file = tmp_path / f"fine_name.{CURRENT}.txt"
    version_file.write_text(EXPECTED_OUTPUT, "utf8")
    (tmp_path / "fine_name.txt").write_text(EXPECTED_OUTPUT, "utf8")
    (tmp_path / "fine_name.py").write_text("", "utf8")
    with pytest.raises(pytest.fail.Exception, match="empty it by hand"):
        _lint_module(tmp_path, "fine_name.py").runTest(GoldenMaster(remaster=True))
    assert version_file.read_text("utf8") == EXPECTED_OUTPUT


def test_run_test_golden_master_absolute_filename(tmp_path: Path) -> None:
    """Plugins give an absolute filename: an emptied base file is still deleted."""
    expected_file = tmp_path / "fine_name.txt"
    expected_file.write_text(EXPECTED_OUTPUT, "utf8")
    source = tmp_path / "fine_name.py"
    source.write_text("", "utf8")
    golden_master = GoldenMaster(remaster=True)
    _lint_module(tmp_path, str(source)).runTest(golden_master)
    with pytest.raises(pytest.fail.Exception, match="deleted"):
        golden_master.assert_remastered()
    assert not expected_file.exists()
