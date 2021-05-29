# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE


import re
from pathlib import Path

import pytest

from pylint.lint.expand_modules import _is_in_ignore_list_re, expand_modules


def test__is_in_ignore_list_re_match():
    patterns = [
        re.compile(".*enchilada.*"),
        re.compile("unittest_.*"),
        re.compile(".*tests/.*"),
    ]
    assert _is_in_ignore_list_re("unittest_utils.py", patterns)
    assert _is_in_ignore_list_re("cheese_enchiladas.xml", patterns)
    assert _is_in_ignore_list_re("src/tests/whatever.xml", patterns)


def test__is_in_ignore_list_re_nomatch():
    patterns = [
        re.compile(".*enchilada.*"),
        re.compile("unittest_.*"),
        re.compile(".*tests/.*"),
    ]
    assert not _is_in_ignore_list_re("test_utils.py", patterns)
    assert not _is_in_ignore_list_re("enchilad.py", patterns)
    assert not _is_in_ignore_list_re("src/tests.py", patterns)


TEST_DIRECTORY = Path(__file__).parent.parent
INIT_PATH = str(TEST_DIRECTORY / "lint/__init__.py")
EXPAND_MODULES = str(TEST_DIRECTORY / "lint/unittest_expand_modules.py")
this_file = {
    "basename": "lint.unittest_expand_modules",
    "basepath": EXPAND_MODULES,
    "isarg": True,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES,
}

this_file_from_init = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES,
}

unittest_lint = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.unittest_lint",
    "path": str(TEST_DIRECTORY / "lint/unittest_lint.py"),
}


init_of_package = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": True,
    "name": "lint",
    "path": INIT_PATH,
}


@pytest.mark.parametrize(
    "files_or_modules,expected",
    [
        ([__file__], [this_file]),
        (
            [Path(__file__).parent],
            [init_of_package, this_file_from_init, unittest_lint],
        ),
    ],
)
def test_expand_modules(files_or_modules, expected):
    ignore_list, ignore_list_re, ignore_list_paths_re = [], [], []
    modules, errors = expand_modules(
        files_or_modules, ignore_list, ignore_list_re, ignore_list_paths_re
    )
    modules.sort(key=lambda d: d["name"])
    assert modules == expected
    assert not errors
