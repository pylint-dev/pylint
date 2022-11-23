# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from pathlib import Path

import pytest

from pylint.pyreverse.main import Run
from pylint.testutils.pyreverse import (
    FunctionalPyreverseTestfile,
    get_functional_test_files,
)

FUNCTIONAL_DIR = Path(__file__).parent / "functional"
CLASS_DIAGRAM_TESTS = get_functional_test_files(FUNCTIONAL_DIR / "class_diagrams")
CLASS_DIAGRAM_TEST_IDS = [testfile.source.stem for testfile in CLASS_DIAGRAM_TESTS]


@pytest.mark.parametrize(
    "testfile",
    CLASS_DIAGRAM_TESTS,
    ids=CLASS_DIAGRAM_TEST_IDS,
)
def test_class_diagrams(testfile: FunctionalPyreverseTestfile, tmp_path: Path) -> None:
    input_file = testfile.source
    for output_format in testfile.options["output_formats"]:
        with pytest.raises(SystemExit) as sys_exit:
            args = ["-o", f"{output_format}", "-d", str(tmp_path)]
            args.extend(testfile.options["command_line_args"])
            args += [str(input_file)]
            Run(args)
        assert sys_exit.value.code == 0
        assert testfile.source.with_suffix(f".{output_format}").read_text(
            encoding="utf8"
        ) == (tmp_path / f"classes.{output_format}").read_text(encoding="utf8")
