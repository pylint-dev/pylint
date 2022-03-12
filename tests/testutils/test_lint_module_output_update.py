# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

# pylint: disable=redefined-outer-name
from pathlib import Path
from typing import Callable, Tuple

import pytest

from pylint.constants import PY38_PLUS
from pylint.testutils import FunctionalTestFile
from pylint.testutils.functional import LintModuleOutputUpdate


@pytest.fixture()
def lint_module_fixture(
    tmp_path: Path,
) -> Callable[[str], Tuple[Path, Path, LintModuleOutputUpdate]]:
    def inner(base: str) -> Tuple[Path, Path, LintModuleOutputUpdate]:
        filename = tmp_path / f"{base}.py"
        expected_output_file = tmp_path / f"{base}.txt"
        lmou = LintModuleOutputUpdate(
            test_file=FunctionalTestFile(str(tmp_path), str(filename))
        )
        return filename, expected_output_file, lmou

    return inner


@pytest.mark.skipif(PY38_PLUS, reason="Requires python 3.7 or lower")
def test_not_py38(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="new AST parser"):
        LintModuleOutputUpdate(
            test_file=FunctionalTestFile(str(tmp_path), str(tmp_path / "filename.py"))
        )


@pytest.mark.skipif(not PY38_PLUS, reason="Requires python 3.8 or superior")
def test_lint_module_output_update_fail_before(
    lint_module_fixture: Callable[[str], Tuple[Path, Path, LintModuleOutputUpdate]]
) -> None:
    """There is a fail before the output need to be updated."""
    filename, expected_output_file, lmou = lint_module_fixture("foo")
    filename.write_text("", encoding="utf8")
    assert not expected_output_file.exists()
    with pytest.raises(AssertionError, match="1: disallowed-name"):
        lmou.runTest()
    assert not expected_output_file.exists()


@pytest.mark.skipif(not PY38_PLUS, reason="Requires python 3.8 or superior")
def test_lint_module_output_update_effective(
    lint_module_fixture: Callable[[str], Tuple[Path, Path, LintModuleOutputUpdate]]
) -> None:
    """The file is updated following a successful tests with wrong output."""
    filename, expected_output_file, lmou = lint_module_fixture("foo")
    filename.write_text("# [disallowed-name]\n", encoding="utf8")
    lmou.runTest()
    assert (expected_output_file).exists()
    assert (
        expected_output_file.read_text(encoding="utf8")
        == 'disallowed-name:1:0:None:None::"Disallowed name ""foo""":UNDEFINED\n'
    )


@pytest.mark.skipif(not PY38_PLUS, reason="Requires python 3.8 or superior")
def test_lint_module_output_update_remove_useless_txt(
    lint_module_fixture: Callable[[str], Tuple[Path, Path, LintModuleOutputUpdate]]
) -> None:
    """The file is updated following a successful tests with wrong output."""
    filename, expected_output_file, lmou = lint_module_fixture("fine_name")
    expected_output_file.write_text("", encoding="utf8")
    filename.write_text("", encoding="utf8")
    lmou.runTest()
    assert not (expected_output_file).exists()
