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
from astroid import modutils

import pylint.lint.expand_modules as expand_modules_module
from pylint.checkers import BaseChecker
from pylint.lint.expand_modules import (
    _canonical_case_path,
    _is_case_insensitive_fs,
    _is_in_ignore_list_re,
    _list_directory,
    expand_modules,
)
from pylint.testutils import CheckerTestCase, set_config
from pylint.typing import MessageDefinitionTuple, ModuleDescriptionDict


def test_expand_modules_with_shadowed_namespace_package(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Expand a namespace package that also exists in site-packages.

    Regression test for https://github.com/pylint-dev/pylint/issues/10278
    """
    # The name is not used by any other test, since astroid caches the result of
    # is_namespace() per module name and this one is resolved differently here.
    namespace = "pylint_shadowed_namespace_10278"
    project = tmp_path / "project"
    subpackage = project / namespace / "subpackage"
    subpackage.mkdir(parents=True)
    (subpackage / "__init__.py").touch()
    (subpackage / "module.py").touch()
    # is_namespace() from astroid reports "not a namespace package" as soon as one
    # portion of the package is in site-packages or in the standard library. Fake it
    # instead of writing into the site-packages of the test environment.
    shadowing_site_packages = tmp_path / "site-packages"
    (shadowing_site_packages / namespace).mkdir(parents=True)
    monkeypatch.syspath_prepend(str(project))
    monkeypatch.syspath_prepend(str(shadowing_site_packages))
    monkeypatch.setattr(
        modutils, "EXT_LIB_DIRS", modutils.EXT_LIB_DIRS | {str(shadowing_site_packages)}
    )

    modules, errors = expand_modules([str(subpackage)], [str(project)], [], [], [])

    assert not errors
    assert {Path(path).name: module["name"] for path, module in modules.items()} == {
        "__init__.py": f"{namespace}.subpackage",
        "module.py": f"{namespace}.subpackage.module",
    }


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
    "isignored": False,
}

this_file_relative_to_parent = {
    "basename": "lint.unittest_expand_modules",
    "basepath": EXPAND_MODULES_BASE,
    "isarg": True,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES_BASE,
    "isignored": False,
}

this_file_from_init = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES,
    "isignored": False,
}

this_file_from_init_deduplicated = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": True,
    "name": "lint.unittest_expand_modules",
    "path": EXPAND_MODULES,
    "isignored": False,
}

unittest_discover_files = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.unittest_discover_files",
    "path": str(TEST_DIRECTORY / "lint/unittest_discover_files.py"),
    "isignored": False,
}

unittest_lint = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.unittest_lint",
    "path": str(TEST_DIRECTORY / "lint/unittest_lint.py"),
    "isignored": False,
}

test_utils = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_utils",
    "path": str(TEST_DIRECTORY / "lint/test_utils.py"),
    "isignored": False,
}

test_run_pylint = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_run_pylint",
    "path": str(TEST_DIRECTORY / "lint/test_run_pylint.py"),
    "isignored": False,
}

test_pylinter = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_pylinter",
    "path": str(TEST_DIRECTORY / "lint/test_pylinter.py"),
    "isignored": False,
}

test_caching = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": False,
    "name": "lint.test_caching",
    "path": str(TEST_DIRECTORY / "lint/test_caching.py"),
    "isignored": False,
}

init_of_package = {
    "basename": "lint",
    "basepath": INIT_PATH,
    "isarg": True,
    "name": "lint",
    "path": INIT_PATH,
    "isignored": False,
}

# A directory that is not a python package.
REPORTERS_PATH = Path(__file__).parent.parent / "reporters"
test_reporters = {  # pylint: disable=consider-using-namedtuple-or-dataclass
    str(REPORTERS_PATH / "__init__.py"): {
        "basename": "reporters",
        "basepath": str(REPORTERS_PATH / "__init__.py"),
        "isarg": True,
        "name": "reporters",
        "path": str(REPORTERS_PATH / "__init__.py"),
        "isignored": False,
    },
    str(REPORTERS_PATH / "unittest_json_reporter.py"): {
        "basename": "reporters",
        "basepath": str(REPORTERS_PATH / "__init__.py"),
        "isarg": False,
        "name": "reporters.unittest_json_reporter",
        "path": str(REPORTERS_PATH / "unittest_json_reporter.py"),
        "isignored": False,
    },
    str(REPORTERS_PATH / "unittest_junit_reporter.py"): {
        "basename": "reporters",
        "basepath": str(REPORTERS_PATH / "__init__.py"),
        "isarg": False,
        "name": "reporters.unittest_junit_reporter",
        "path": str(REPORTERS_PATH / "unittest_junit_reporter.py"),
        "isignored": False,
    },
    str(REPORTERS_PATH / "unittest_reporting.py"): {
        "basename": "reporters",
        "basepath": str(REPORTERS_PATH / "__init__.py"),
        "isarg": False,
        "path": str(REPORTERS_PATH / "unittest_reporting.py"),
        "name": "reporters.unittest_reporting",
        "isignored": False,
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
        unittest_discover_files,
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
        assert {k: v for k, v in modules.items() if not v["isignored"]} == expected
        assert not errors

    @set_config(ignore=["test"])
    def test_expand_modules_with_ignore_list(self) -> None:
        """Test expand_modules with a non-default value of ignore."""
        ignore_list: list[str] = self.linter.config.ignore
        ignore_list_re = [re.compile("^\\.#")]
        path = Path(__file__).parent.parent / "regrtest_data" / "ignore_option_10669"
        modules, errors = expand_modules(
            [str(path)],
            [],
            ignore_list,
            ignore_list_re,
            [],
        )
        expected_keys = {
            str(path / "__init__.py"),
            str(path / "main.py"),
        }
        assert {k for k, v in modules.items() if not v["isignored"]} == expected_keys
        assert not errors


def _pretend_case_insensitive_host(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use the case-insensitive code paths of expand_modules on any host."""
    monkeypatch.setattr(expand_modules_module, "_is_case_insensitive_fs", lambda: True)
    if os.name != "nt":
        monkeypatch.setattr(
            Path,
            "samefile",
            lambda first, second: str(first).lower() == str(second).lower(),
        )


def test__is_case_insensitive_fs() -> None:
    """The host check follows the platform's path comparison."""
    assert _is_case_insensitive_fs() is (os.name == "nt")


@pytest.mark.parametrize(
    "initializer_name", ["__init__.py", "__Init__.py", "__INIT__.PY"]
)
def test_case_insensitive_package_initializer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, initializer_name: str
) -> None:
    """Case-insensitive initializer spellings identify the same input file."""
    _pretend_case_insensitive_host(monkeypatch)
    package = tmp_path / "package"
    package.mkdir()
    initializer = package / "__init__.py"
    initializer.write_text("", encoding="utf-8")
    supplied = package / initializer_name

    expected, expected_errors = expand_modules(
        [str(initializer)], [str(tmp_path)], [], [], []
    )
    modules, errors = expand_modules(
        [str(supplied), str(initializer)], [str(tmp_path)], [], [], []
    )

    assert not errors
    assert not expected_errors
    assert modules == expected
    assert modules[str(initializer)]["name"] == "package.__init__"
    assert modules[str(initializer)]["isarg"]


def test_case_sensitive_initializer_spelling_is_preserved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On case-sensitive hosts, a differently spelled file is an ordinary module."""
    monkeypatch.setattr(expand_modules_module, "_is_case_insensitive_fs", lambda: False)
    package = tmp_path / "package"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    module = package / "__Init__.py"
    module.write_text("", encoding="utf-8")

    modules, errors = expand_modules([str(module)], [str(tmp_path)], [], [], [])

    assert not errors
    assert modules[str(module)]["name"] == "package.__Init__"


@pytest.mark.parametrize("spelling", ["PACKAGE", "Package", "pAcKaGe"])
def test__canonical_case_path_uses_file_system_spelling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, spelling: str
) -> None:
    """Paths that differ from the file system only in case get its spelling."""
    _pretend_case_insensitive_host(monkeypatch)
    package = tmp_path / "package"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")

    canonical = _canonical_case_path(str(package / "__init__.py"))
    fixed = _canonical_case_path(str(tmp_path / spelling / "__Init__.py"))
    assert fixed == canonical
    assert Path(fixed).parts[-2:] == ("package", "__init__.py")
    # A path that is already spelled correctly, and one that does not exist, are
    # both returned unchanged.
    assert _canonical_case_path(canonical) == canonical
    missing = str(tmp_path / "missing" / "__init__.py")
    assert _canonical_case_path(missing) == missing
    assert Path(_canonical_case_path(str(package / os.pardir))).parts[-2:] == (
        "package",
        os.pardir,
    )
    root = os.path.abspath(os.sep)
    assert _canonical_case_path(root) == root
    # Relative paths are resolved against the current directory.
    monkeypatch.chdir(tmp_path)
    assert _canonical_case_path(spelling) == "package"
    assert _canonical_case_path(f"{spelling}/__Init__.py") == os.path.join(
        "package", "__init__.py"
    )
    assert Path(_canonical_case_path(f"{spelling}/")) == Path("package")


@pytest.mark.parametrize("spelling", ["straße.py", "STRAßE.py"])
def test_canonical_case_path_preserves_distinct_unicode_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, spelling: str
) -> None:
    _pretend_case_insensitive_host(monkeypatch)
    first = tmp_path / "strasse.py"
    second = tmp_path / "straße.py"
    first.write_text("FIRST = 1\n", encoding="utf-8")
    second.write_text("SECOND = 2\n", encoding="utf-8")
    list_directory = expand_modules_module._list_directory

    def ordered_names(directory: str) -> list[str]:
        if Path(directory) == tmp_path:
            return [first.name, second.name]
        return list_directory(directory)

    monkeypatch.setattr(expand_modules_module, "_list_directory", ordered_names)
    assert _canonical_case_path(str(tmp_path / spelling)) == str(second)
    assert _canonical_case_path(str(first)) == str(first)


def test_canonical_case_path_does_not_select_a_different_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _pretend_case_insensitive_host(monkeypatch)
    (tmp_path / "strasse.py").write_text("", encoding="utf-8")
    missing = str(tmp_path / "STRAßE.py")

    def missing_file(first: Path, second: Path) -> bool:
        raise FileNotFoundError(second)

    monkeypatch.setattr(Path, "samefile", missing_file)
    assert _canonical_case_path(missing) == missing


def test__canonical_case_path_on_case_sensitive_host(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On case-sensitive file systems a differently spelled path is kept."""
    monkeypatch.setattr(expand_modules_module, "_is_case_insensitive_fs", lambda: False)
    (tmp_path / "package").mkdir()
    differently_cased = str(tmp_path / "PACKAGE")
    assert _canonical_case_path(differently_cased) == differently_cased


def test__list_directory_returns_nothing_for_missing_directory(tmp_path: Path) -> None:
    """An unreadable directory never raises but yields no names."""
    assert _list_directory(str(tmp_path / "missing")) == []


def test_case_insensitive_path_names_the_same_module(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A path spelled differently from the file system is not another module."""
    _pretend_case_insensitive_host(monkeypatch)
    package = tmp_path / "package"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "module.py").write_text("", encoding="utf-8")

    def expand(*files_or_modules: str) -> dict[str, ModuleDescriptionDict]:
        modules, errors = expand_modules(list(files_or_modules), [], [], [], [])
        assert not errors
        return modules

    expected = expand(str(package), str(package / "__init__.py"))
    actual = expand(
        str(tmp_path / "PACKAGE"), str(tmp_path / "PACKAGE" / "__Init__.py")
    )
    assert {k: v["name"] for k, v in actual.items()} == {
        k: v["name"] for k, v in expected.items()
    }
    assert "PACKAGE" not in " ".join(v["name"] for v in actual.values())
