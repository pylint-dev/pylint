# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest
from py._path.local import LocalPath  # type: ignore[import]

from pylint.pyreverse.main import Run


class FunctionalPyreverseTestfile(NamedTuple):
    """Named tuple containing the test file and the expected output."""

    source: Path
    expectation: Path


def get_functional_test_files(
    root_directory: Path,
) -> list[FunctionalPyreverseTestfile]:
    """Get all functional test files from the given directory."""
    return [
        FunctionalPyreverseTestfile(
            source=test_file, expectation=test_file.with_suffix(".mmd")
        )
        for test_file in root_directory.rglob("*.py")
    ]


FUNCTIONAL_DIR = Path(__file__).parent / "functional"
CLASS_DIAGRAM_TESTS = get_functional_test_files(FUNCTIONAL_DIR / "class_diagrams")
CLASS_DIAGRAM_TEST_IDS = [testfile.source.stem for testfile in CLASS_DIAGRAM_TESTS]


@pytest.mark.parametrize(
    "testfile",
    CLASS_DIAGRAM_TESTS,
    ids=CLASS_DIAGRAM_TEST_IDS,
)
def test_class_diagrams(
    testfile: FunctionalPyreverseTestfile, tmpdir: LocalPath
) -> None:
    input_file = testfile.source
    with pytest.raises(SystemExit) as sys_exit:
        Run(["-o", "mmd", "-d", str(tmpdir), str(input_file)])
    assert sys_exit.value.code == 0
    assert testfile.expectation.read_text(encoding="utf8") == Path(
        tmpdir / "classes.mmd"
    ).read_text(encoding="utf8")
