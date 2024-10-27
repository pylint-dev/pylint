# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import copy
import os
import re
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest

from pylint.checkers import BaseChecker
from pylint.lint.expand_modules import (
    _is_in_ignore_list_re,
    discover_package_path,
    expand_modules,
)
from pylint.testutils import CheckerTestCase, set_config
from pylint.typing import MessageDefinitionTuple, ModuleDescriptionDict


def test__is_in_ignore_list_re_match() -> None:
    patterns = [
        re.compile(".*enchilada.*"),
        re.compile("unittest_.*"),
        re.compile(".*tests/.*"),
    ]
    assert _is_in_ignore_list_re("unittest_utils.py", patterns)
    assert _is_in_ignore_list_re("cheese_enchiladas.xml", patterns)
    assert _is_in_ignore_list_re("src/tests/whatever.xml", patterns)


TEST_DIRECTORY = Path(__file__).parent.parent
INIT_PATH = str(TEST_DIRECTORY / "lint/__init__.py")
EXPAND_MODULES_BASE = "unittest_expand_modules.py"
EXPAND_MODULES = str(TEST_DIRECTORY / "lint" / EXPAND_MODULES_BASE)
this_file = {
    "basename": "lint.unittest_expand_modules",
    "basepath": EXPAND_MODULES,
    "isarg": True,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES,
}

this_file_relative_to_parent = {
    "basename": "lint.unittest_expand_modules",
    "basepath": EXPAND_MODULES_BASE,
    "isarg": True,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES_BASE,
}

this_file_from_init = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES,
}

this_file_from_init_deduplicated = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": True,
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

test_utils = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_utils",
    "path": str(TEST_DIRECTORY / "lint/test_utils.py"),
}

test_run_pylint = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_run_pylint",
    "path": str(TEST_DIRECTORY / "lint/test_run_pylint.py"),
}

test_pylinter = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_pylinter",
    "path": str(TEST_DIRECTORY / "lint/test_pylinter.py"),
}

test_caching = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_caching",
    "path": str(TEST_DIRECTORY / "lint/test_caching.py"),
}

init_of_package = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": True,
    "name": "lint",
    "path": INIT_PATH,
}

# A directory that is not a python package.
REPORTERS_PATH = Path(__file__).parent.parent / "reporters"
test_reporters = {  # pylint: disable=consider-using-namedtuple-or-dataclass
    str(REPORTERS_PATH / "unittest_json_reporter.py"): {
        "path": str(REPORTERS_PATH / "unittest_json_reporter.py"),
        "name": "reporters.unittest_json_reporter",
        "isarg": False,
        "basepath": str(REPORTERS_PATH / "__init__.py"),
        "basename": "reporters",
    },
    str(REPORTERS_PATH / "unittest_reporting.py"): {
        "path": str(REPORTERS_PATH / "unittest_reporting.py"),
        "name": "reporters.unittest_reporting",
        "isarg": False,
        "basepath": str(REPORTERS_PATH / "__init__.py"),
        "basename": "reporters",
    },
}


def _list_expected_package_modules(
    deduplicating: bool = False,
) -> tuple[dict[str, object], ...]:
    """Generates reusable list of modules for our package."""
    return (
        init_of_package,
        test_caching,
        test_pylinter,
        test_run_pylint,
        test_utils,
        this_file_from_init_deduplicated if deduplicating else this_file_from_init,
        unittest_lint,
    )


def _list_expected_package_modules_relative() -> tuple[dict[str, object], ...]:
    """Generates reusable list of modules for our package with relative path input."""
    abs_result = copy.deepcopy(_list_expected_package_modules())
    for item in abs_result:
        assert isinstance(item["basepath"], str)
        assert isinstance(item["path"], str)
        item["basepath"] = os.path.relpath(item["basepath"], str(Path(__file__).parent))
        item["path"] = os.path.relpath(item["path"], str(Path(__file__).parent))
    return abs_result


@contextmanager
def pushd(path: Path) -> Iterator[None]:
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


class TestExpandModules(CheckerTestCase):
    """Test the expand_modules function while allowing options to be set."""

    class Checker(BaseChecker):
        """This dummy checker is needed to allow options to be set."""

        name = "checker"
        msgs: dict[str, MessageDefinitionTuple] = {}
        options = (("test-opt", {"action": "store_true", "help": "help message"}),)

    CHECKER_CLASS: type = Checker

    @pytest.mark.parametrize(
        "files_or_modules,expected",
        [
            ([__file__], {this_file["path"]: this_file}),
            (
                [str(Path(__file__).parent)],
                {
                    module["path"]: module  # pylint: disable=unsubscriptable-object
                    for module in _list_expected_package_modules()
                },
            ),
            ([str(Path(__file__).parent.parent / "reporters")], test_reporters),
        ],
    )
    @set_config(ignore_paths="")
    def test_expand_modules(
        self, files_or_modules: list[str], expected: dict[str, ModuleDescriptionDict]
    ) -> None:
        """Test expand_modules with the default value of ignore-paths."""
        ignore_list: list[str] = []
        ignore_list_re: list[re.Pattern[str]] = []
        modules, errors = expand_modules(
            files_or_modules,
            [],
            ignore_list,
            ignore_list_re,
            self.linter.config.ignore_paths,
        )
        assert modules == expected
        assert not errors

    @pytest.mark.parametrize(
        "files_or_modules,expected",
        [
            (
                [Path(__file__).name],
                {this_file_relative_to_parent["path"]: this_file_relative_to_parent},
            ),
            (
                ["./"],
                {
                    module["path"]: module  # pylint: disable=unsubscriptable-object
                    for module in _list_expected_package_modules_relative()
                },
            ),
        ],
    )
    @set_config(ignore_paths="")
    def test_expand_modules_relative_path(
        self, files_or_modules: list[str], expected: dict[str, ModuleDescriptionDict]
    ) -> None:
        """Test expand_modules with the default value of ignore-paths and relative path as input."""
        ignore_list: list[str] = []
        ignore_list_re: list[re.Pattern[str]] = []
        with pushd(Path(__file__).parent):
            modules, errors = expand_modules(
                files_or_modules,
                [],
                ignore_list,
                ignore_list_re,
                self.linter.config.ignore_paths,
            )
            assert modules == expected
            assert not errors

    @pytest.mark.parametrize(
        "files_or_modules,expected",
        [
            ([__file__, __file__], {this_file["path"]: this_file}),
            (
                [EXPAND_MODULES, str(Path(__file__).parent), EXPAND_MODULES],
                {
                    module["path"]: module  # pylint: disable=unsubscriptable-object
                    for module in _list_expected_package_modules(deduplicating=True)
                },
            ),
        ],
    )
    @set_config(ignore_paths="")
    def test_expand_modules_deduplication(
        self, files_or_modules: list[str], expected: dict[str, ModuleDescriptionDict]
    ) -> None:
        """Test expand_modules deduplication."""
        ignore_list: list[str] = []
        ignore_list_re: list[re.Pattern[str]] = []
        modules, errors = expand_modules(
            files_or_modules,
            [],
            ignore_list,
            ignore_list_re,
            self.linter.config.ignore_paths,
        )
        assert modules == expected
        assert not errors

    @pytest.mark.parametrize(
        "files_or_modules,expected",
        [
            ([__file__], {}),
            (
                [str(Path(__file__).parent)],
                {
                    module["path"]: module  # pylint: disable=unsubscriptable-object
                    for module in (init_of_package,)
                },
            ),
        ],
    )
    @set_config(ignore_paths=".*/lint/.*")
    def test_expand_modules_with_ignore(
        self, files_or_modules: list[str], expected: dict[str, ModuleDescriptionDict]
    ) -> None:
        """Test expand_modules with a non-default value of ignore-paths."""
        ignore_list: list[str] = []
        ignore_list_re: list[re.Pattern[str]] = []
        modules, errors = expand_modules(
            files_or_modules,
            [],
            ignore_list,
            ignore_list_re,
            self.linter.config.ignore_paths,
        )
        assert modules == expected
        assert not errors


def test_discover_package_path_no_source_root_overlap(tmp_path: Path) -> None:
    """Test whether source_roots is returned even if module doesn't overlap
    with source_roots
    """
    source_roots = [str(tmp_path)]
    package_paths = discover_package_path(__file__, source_roots)

    expected = source_roots
    assert package_paths == expected


def test_discover_package_path_legacy() -> None:
    """Test for legacy path discovery when source_roots is empty"""
    source_roots: list[str] = []
    package_paths = discover_package_path(__file__, source_roots)

    # First ancestor directory without __init__.py
    expected = [str(Path(__file__).parent.parent.absolute())]

    assert package_paths == expected


def test_discover_package_path_legacy_no_parent_without_init_py(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test to return current directory if no parent directory without
    __init__.py is found
    """
    source_roots: list[str] = []

    monkeypatch.setattr(os.path, "exists", lambda path: True)
    monkeypatch.setattr(os.path, "dirname", lambda path: path)

    package_paths = discover_package_path(str(tmp_path), source_roots)

    expected = [os.getcwd()]

    assert package_paths == expected
