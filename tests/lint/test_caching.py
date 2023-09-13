# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# Pytest fixtures work like this by design
# pylint: disable=redefined-outer-name

import sys
from pathlib import Path

import pytest

from pylint.constants import PYLINT_HOME
from pylint.lint.caching import _get_pdata_path, load_results, save_results
from pylint.utils import LinterStats
from pylint.utils.linterstats import BadNames

PYLINT_HOME_PATH = Path(PYLINT_HOME)


@pytest.mark.parametrize(
    "path,recur,pylint_home,expected",
    [
        ["", 1, PYLINT_HOME_PATH, PYLINT_HOME_PATH / "_1.stats"],
        ["", 2, PYLINT_HOME_PATH, PYLINT_HOME_PATH / "_2.stats"],
        ["a/path", 42, PYLINT_HOME_PATH, PYLINT_HOME_PATH / "a_path_42.stats"],
    ],
)
def test__get_pdata_path(
    path: str, recur: int, pylint_home: Path, expected: Path
) -> None:
    assert _get_pdata_path(Path(path), recur, pylint_home) == expected


@pytest.mark.skipif(sys.platform == "win32", reason="Path type of *nix")
@pytest.mark.parametrize(
    "path,recur,pylint_home,expected",
    [
        [
            "/workspace/MyDir/test.py",
            1,
            Path("/root/.cache/pylint"),
            Path("/root/.cache/pylint") / "__workspace_MyDir_test.py_1.stats",
        ],
        [
            "/workspace/MyDir/test.py",
            1,
            Path("//host/computer/.cache"),
            Path("//host/computer/.cache") / "__workspace_MyDir_test.py_1.stats",
        ],
    ],
)
def test__get_pdata_path_nix(
    path: str, recur: int, pylint_home: Path, expected: Path
) -> None:
    """test__get_pdata_path but specifically for *nix system paths."""
    assert _get_pdata_path(Path(path), recur, pylint_home) == expected


@pytest.mark.skipif(sys.platform != "win32", reason="Path type of windows")
@pytest.mark.parametrize(
    "path,recur,pylint_home,expected",
    [
        [
            "D:\\MyDir\\test.py",
            1,
            Path("C:\\Users\\MyPylintHome"),
            Path("C:\\Users\\MyPylintHome") / "D___MyDir_test.py_1.stats",
        ],
        [
            "C:\\MyDir\\test.py",
            1,
            Path("C:\\Users\\MyPylintHome"),
            Path("C:\\Users\\MyPylintHome") / "C___MyDir_test.py_1.stats",
        ],
    ],
)
def test__get_pdata_path_windows(
    path: str, recur: int, pylint_home: Path, expected: Path
) -> None:
    """test__get_pdata_path but specifically for windows."""
    assert _get_pdata_path(Path(path), recur, pylint_home) == expected


@pytest.fixture
def linter_stats() -> LinterStats:
    return LinterStats(
        bad_names=BadNames(
            argument=1,
            attr=2,
            klass=3,
            class_attribute=4,
            class_const=5,
            const=6,
            inlinevar=7,
            function=8,
            method=9,
            module=10,
            variable=11,
            typevar=12,
            typealias=13,
        )
    )


@pytest.mark.parametrize("path", [".tests/", ".tests/a/path/"])
def test_save_and_load_result(path: str, linter_stats: LinterStats) -> None:
    save_results(linter_stats, path)
    loaded = load_results(path)
    assert loaded is not None
    assert loaded.bad_names == linter_stats.bad_names


@pytest.mark.parametrize("path", [".tests", ".tests/a/path/"])
def test_save_and_load_not_a_linter_stats(path: str) -> None:
    # type ignore because this is what we're testing
    save_results(1, path)  # type: ignore[arg-type]
    with pytest.warns(UserWarning) as warn:
        loaded = load_results(path)
        assert loaded is None
    warn_str = str(warn.pop().message)
    assert "old pylint cache with invalid data" in warn_str
