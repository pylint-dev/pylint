# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
import os
from pathlib import Path

import pytest

from pylint.pyreverse.main import Run
from pylint.testutils.pyreverse import (
    FunctionalPyreverseTestfile,
    get_functional_test_files,
    get_functional_test_packages,
)

FUNCTIONAL_DIR = Path(__file__).parent / "functional"
CLASS_DIAGRAMS_DIR = FUNCTIONAL_DIR / "class_diagrams"
CLASS_DIAGRAM_TESTS = get_functional_test_files(CLASS_DIAGRAMS_DIR)
CLASS_DIAGRAM_TEST_IDS = [testfile.source.stem for testfile in CLASS_DIAGRAM_TESTS]
PACKAGE_DIAGRAMS_DIR = FUNCTIONAL_DIR / "packages"
PACKAGE_DIAGRAM_TESTS = get_functional_test_packages(PACKAGE_DIAGRAMS_DIR)
PACKAGE_DIAGRAM_TEST_IDS = [
    test_package.source.name for test_package in PACKAGE_DIAGRAM_TESTS
]


@pytest.mark.parametrize(
    "testfile",
    CLASS_DIAGRAM_TESTS,
    ids=CLASS_DIAGRAM_TEST_IDS,
)
def test_class_diagrams(testfile: FunctionalPyreverseTestfile, tmp_path: Path) -> None:
    input_file = testfile.source
    input_path = os.path.dirname(input_file)
    if testfile.options["source_roots"]:
        source_roots = ",".join(
            [
                os.path.realpath(
                    os.path.expanduser(os.path.join(input_path, source_root))
                )
                for source_root in testfile.options["source_roots"]
            ]
        )
    else:
        source_roots = ""
    for output_format in testfile.options["output_formats"]:
        with pytest.raises(SystemExit) as sys_exit:
            args = ["-o", f"{output_format}", "-d", str(tmp_path)]
            if source_roots:
                args += ["--source-roots", source_roots]
            args.extend(testfile.options["command_line_args"])
            args += [str(input_file)]
            Run(args)
        assert sys_exit.value.code == 0
        assert testfile.source.with_suffix(f".{output_format}").read_text(
            encoding="utf8"
        ) == (tmp_path / f"classes.{output_format}").read_text(encoding="utf8")


@pytest.mark.parametrize(
    "test_package",
    PACKAGE_DIAGRAM_TESTS,
    ids=PACKAGE_DIAGRAM_TEST_IDS,
)
def test_packages(test_package: FunctionalPyreverseTestfile, tmp_path: Path) -> None:
    input_path = test_package.source
    if test_package.options["source_roots"]:
        source_roots = ",".join(
            [
                os.path.realpath(
                    os.path.expanduser(os.path.join(input_path, source_root))
                )
                for source_root in test_package.options["source_roots"]
            ]
        )
    else:
        source_roots = ""
    for output_format in test_package.options["output_formats"]:
        output_file = input_path / f"{input_path.name}.{output_format}"
        with pytest.raises(SystemExit) as sys_exit:
            args = ["-o", f"{output_format}", "-d", str(tmp_path)]
            if source_roots:
                args += ["--source-roots", source_roots]
            args.extend(test_package.options["command_line_args"])
            args += [str(input_path)]
            Run(args)
        assert sys_exit.value.code == 0
        assert output_file.read_text(encoding="utf8") == (
            tmp_path / f"classes.{output_format}"
        ).read_text(encoding="utf8")
