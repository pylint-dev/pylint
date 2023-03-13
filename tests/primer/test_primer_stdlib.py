# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import contextlib
import io
import os
import sys
import warnings
from collections.abc import Iterator

import pytest
from pytest import CaptureFixture

from pylint.testutils._run import _Run as Run


def is_module(filename: str) -> bool:
    return filename.endswith(".py")


def is_package(filename: str, location: str) -> bool:
    return os.path.exists(os.path.join(location, filename, "__init__.py"))


@contextlib.contextmanager
def _patch_stdout(out: io.StringIO) -> Iterator[None]:
    sys.stdout = out
    try:
        yield
    finally:
        sys.stdout = sys.__stdout__


LIB_DIRS = [os.path.dirname(os.__file__)]
MODULES_TO_CHECK = [
    (location, module)
    for location in LIB_DIRS
    for module in os.listdir(location)
    if is_module(module) or is_package(module, location)
]
MODULES_NAMES = [m[1] for m in MODULES_TO_CHECK]


@pytest.mark.primer_stdlib
@pytest.mark.parametrize(
    ("test_module_location", "test_module_name"), MODULES_TO_CHECK, ids=MODULES_NAMES
)
def test_primer_stdlib_no_crash(
    test_module_location: str, test_module_name: str, capsys: CaptureFixture
) -> None:
    """Test that pylint does not produce any crashes or fatal errors on stdlib modules."""
    __tracebackhide__ = True  # pylint: disable=unused-variable
    os.chdir(test_module_location)
    with _patch_stdout(io.StringIO()):
        try:
            # We want to test all the code we can
            enables = ["--enable-all-extensions", "--enable=all"]
            # Duplicate code takes too long and is relatively safe
            # We don't want to lint the test directory which are repetitive
            disables = ["--disable=duplicate-code", "--ignore=test"]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                Run([test_module_name, *enables, *disables])
        except SystemExit as ex:
            out, err = capsys.readouterr()
            assert not err, err
            assert not out
            msg = f"Encountered {{}} during primer stlib test for {test_module_name}"
            assert ex.code != 32, msg.format("a crash")
            assert ex.code % 2 == 0, msg.format("a message of category 'fatal'")  # type: ignore[operator]
