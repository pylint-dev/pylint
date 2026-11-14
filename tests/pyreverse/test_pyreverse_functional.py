# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
import os
from collections.abc import Iterator
from pathlib import Path

import astroid
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
PACKAGE_TESTS = get_functional_test_packages(FUNCTIONAL_DIR / "packages")
PACKAGE_TESTS += get_functional_test_packages(FUNCTIONAL_DIR / "package_diagrams")


@pytest.fixture(autouse=True)
def isolated_astroid_cache() -> Iterator[None]:
    """Clear the astroid cache before and after each functional test."""
    astroid.MANAGER.clear_cache()
    yield
    astroid.MANAGER.clear_cache()


def _test_marks(marker: str, reason: str) -> tuple[pytest.MarkDecorator, ...]:
    if not marker:
        return ()
    if marker == "xfail":
        return (pytest.mark.xfail(reason=reason, strict=True, raises=AssertionError),)
    return (pytest.mark.skip(reason=reason),)


@pytest.mark.parametrize(
    "testfile",
    [
        pytest.param(
            testfile,
            marks=_test_marks(testfile.options["marker"], testfile.options["reason"]),
        )
        for testfile in CLASS_DIAGRAM_TESTS
    ],
    ids=CLASS_DIAGRAM_TEST_IDS,
)
def test_class_diagrams(testfile: FunctionalPyreverseTestfile, tmp_path: Path) -> None:
    _test_diagrams(testfile, tmp_path)


@pytest.mark.parametrize(
    "testfile",
    [
        pytest.param(
            testfile,
            id=testfile.source.name,
            marks=_test_marks(testfile.options["marker"], testfile.options["reason"]),
        )
        for testfile in PACKAGE_TESTS
    ],
)
def test_packages(testfile: FunctionalPyreverseTestfile, tmp_path: Path) -> None:
    _test_diagrams(testfile, tmp_path)


def _test_diagrams(testfile: FunctionalPyreverseTestfile, tmp_path: Path) -> None:
    input_source = testfile.source
    is_package = input_source.is_dir()
    input_path = input_source if is_package else input_source.parent
    # Pyreverse expects __init__.py when given a directory. Pass namespace
    # package files explicitly without changing the package's structure.
    input_sources = (
        sorted(input_source.rglob("*.py"))
        if is_package and not (input_source / "__init__.py").is_file()
        else [input_source]
    )
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
        args = ["-o", f"{output_format}", "-d", str(tmp_path)]
        if source_roots:
            args += ["--source-roots", source_roots]
        args.extend(testfile.options["command_line_args"])
        args += [str(source) for source in input_sources]
        exit_code = Run(args).run()
        assert exit_code == 0
        expected_output = (
            input_source / f"{input_source.name}.{output_format}"
            if is_package
            else input_source.with_suffix(f".{output_format}")
        )
        diagram_type = testfile.options["diagram_type"]
        assert expected_output.read_text(encoding="utf8") == (
            tmp_path / f"{diagram_type}.{output_format}"
        ).read_text(encoding="utf8")
