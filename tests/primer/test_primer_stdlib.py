# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import contextlib
import io
import os
import sys

import pytest
from pytest import CaptureFixture

import pylint.lint


def is_module(filename: str) -> bool:
    return filename.endswith(".py")


def is_package(filename: str, location: str) -> bool:
    return os.path.exists(os.path.join(location, filename, "__init__.py"))


@contextlib.contextmanager
def _patch_stdout(out):
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


@pytest.mark.acceptance
@pytest.mark.parametrize(
    ("test_module_location", "test_module_name"), MODULES_TO_CHECK, ids=MODULES_NAMES
)
def test_lib_module_no_crash(
    test_module_location: str, test_module_name: str, capsys: CaptureFixture
) -> None:
    """Test that pylint does not produces any crashes or fatal errors on stdlib modules"""
    os.chdir(test_module_location)
    with _patch_stdout(io.StringIO()):
        try:
            pylint.lint.Run(
                [
                    test_module_name,
                    "--enable=all",
                    "--enable-all-extensions",
                    "--ignore=test",
                ]
            )
        except SystemExit as ex:
            out, err = capsys.readouterr()
            assert not err, err
            assert not out
            msg = f"Encountered {{}} during primer stlib test for {test_module_name}"
            assert ex.code != 32, msg.format("a crash")
            assert ex.code % 2 == 0, msg.format("a message of category 'fatal'")
