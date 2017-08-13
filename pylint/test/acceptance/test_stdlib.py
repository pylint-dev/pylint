# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os
import zipfile

import pytest

import pylint.lint


def is_module(filename):
    return filename.endswith(".py")


def is_package(filename, location):
    return os.path.exists(os.path.join(location, filename, '__init__.py'))

LIB_DIRS = [
    os.path.dirname(os.__file__),
    os.path.dirname(zipfile.__file__)
]
MODULES_TO_CHECK = [(location, module) for location in LIB_DIRS for module in os.listdir(location)
                    if is_module(module) or is_package(module, location)]
MODULES_NAMES = [m[1] for m in MODULES_TO_CHECK]


@pytest.mark.acceptance
@pytest.mark.parametrize(("test_module_location", "test_module_name"),
                         MODULES_TO_CHECK, ids=MODULES_NAMES)
def test_libmodule(test_module_location, test_module_name):
    os.chdir(test_module_location)
    try:
        pylint.lint.Run([test_module_name, '--enable=all'])
    except SystemExit as ex:
        assert ex.code != 32
        return

    assert False, "shouldn't get there"
