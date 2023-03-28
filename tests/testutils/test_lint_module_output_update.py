# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import pytest

from pylint.constants import IS_PYPY, PY38_PLUS, PY39_PLUS
from pylint.testutils import FunctionalTestFile, LintModuleTest
from pylint.testutils.functional import LintModuleOutputUpdate

FIXTURE_DIRECTORY = Path(__file__).parent / "data/functional"
DIRECTORIES = list(FIXTURE_DIRECTORY.iterdir())


@pytest.fixture()
def lint_module_fixture(
    tmp_path: Path,
) -> Callable[[str], tuple[Path, Path, LintModuleOutputUpdate]]:
    def inner(base: str) -> tuple[Path, Path, LintModuleOutputUpdate]:
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
    lint_module_fixture: Callable[[str], tuple[Path, Path, LintModuleOutputUpdate]]
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
    lint_module_fixture: Callable[[str], tuple[Path, Path, LintModuleOutputUpdate]]
) -> None:
    """The file is updated following a successful tests with wrong output."""
    filename, expected_output_file, lmou = lint_module_fixture("foo")
    filename.write_text("# [disallowed-name]\n", encoding="utf8")
    lmou.runTest()
    assert (expected_output_file).exists()
    assert (
        expected_output_file.read_text(encoding="utf8")
        == 'disallowed-name:1:0:None:None::"Disallowed name ""foo""":HIGH\n'
    )


@pytest.mark.skipif(not PY38_PLUS, reason="Requires python 3.8 or superior")
def test_lint_module_output_update_remove_useless_txt(
    lint_module_fixture: Callable[[str], tuple[Path, Path, LintModuleOutputUpdate]]
) -> None:
    """The file is updated following a successful tests with wrong output."""
    filename, expected_output_file, lmou = lint_module_fixture("fine_name")
    expected_output_file.write_text("", encoding="utf8")
    filename.write_text("", encoding="utf8")
    lmou.runTest()
    assert not expected_output_file.exists()


@pytest.mark.skipif(
    not PY38_PLUS or (IS_PYPY and not PY39_PLUS),
    reason="Requires accurate 'end_col' value to update output",
)
@pytest.mark.parametrize(
    "directory_path", DIRECTORIES, ids=[str(p) for p in DIRECTORIES]
)
def test_update_of_functional_output(directory_path: Path, tmp_path: Path) -> None:
    """Functional test for the functional tests' helper."""

    def _check_expected_output(_ftf: FunctionalTestFile) -> None:
        new_output_path = _ftf.expected_output
        assert Path(
            new_output_path
        ).exists(), "The expected output file does not exists"
        with open(new_output_path, encoding="utf8") as f:
            new_output = f.read()
        assert (
            new_output == "exec-used:7:0:7:14::Use of exec:UNDEFINED\n"
        ), f"The content was wrongly updated in {new_output_path}"

    def _assert_behavior_is_correct(
        _ftf: FunctionalTestFile,
        _lint_module: LintModuleTest,
        _lint_module_output_update: LintModuleOutputUpdate,
        _new_path: Path,
    ) -> None:
        new_path_str = str(_new_path)
        if "wrong_test" in new_path_str:
            expected = r'Wrong message\(s\) raised for "exec_used.py"'
            with pytest.raises(AssertionError, match=expected):
                _lint_module.runTest()
            # When the tests are wrong we do not update the output at all
            # and the test should fail
            with pytest.raises(AssertionError, match=expected):
                _lint_module_output_update.runTest()
        elif "ok_test" in new_path_str:
            if any(f"{x}_output" in new_path_str for x in ("wrong", "no", "broken")):
                with pytest.raises(
                    AssertionError, match='Wrong output for "exec_used.txt"'
                ):
                    _lint_module.runTest()
            elif "ok_output" in new_path_str:
                _lint_module.runTest()
                _check_expected_output(_ftf)
            else:
                raise AssertionError(f"Unhandled test case: {new_path_str}")

            # When the tests are ok we update the output whatever it's state
            # was originally
            _lint_module_output_update.runTest()
            _check_expected_output(_ftf)
        else:
            raise AssertionError(
                f"Do not pollute '{FIXTURE_DIRECTORY}' with unrelated "
                f"or badly named test files."
            )

    new_path = tmp_path / directory_path.name
    shutil.copytree(directory_path, new_path)
    for filename in new_path.iterdir():
        if filename.suffix != ".py":
            continue
        ftf = FunctionalTestFile(directory=str(new_path), filename=filename.name)
        # Standard functional test helper
        lint_module = LintModuleTest(ftf)
        # Functional test helper that automatically update the output
        lint_module_output_update = LintModuleOutputUpdate(ftf)

        _assert_behavior_is_correct(
            ftf, lint_module, lint_module_output_update, new_path
        )
