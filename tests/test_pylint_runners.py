# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import contextlib
import os
import pathlib
import shlex
import sys
from collections.abc import Sequence
from io import BufferedReader
from typing import Any, Protocol
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint import run_pylint, run_pyreverse, run_symilar
from pylint.lint.run import _query_cpu
from pylint.testutils import GenericTestReporter as Reporter
from pylint.testutils._run import _Run as Run
from pylint.testutils.utils import _test_cwd


class _RunCallable(Protocol):  # pylint: disable=too-few-public-methods
    def __call__(self, argv: Sequence[str] | None = None) -> None: ...


@pytest.mark.parametrize("runner", [run_pylint, run_pyreverse, run_symilar])
def test_runner(runner: _RunCallable, tmp_path: pathlib.Path) -> None:
    filepath = os.path.abspath(__file__)
    testargs = ["", filepath]
    with _test_cwd(tmp_path):
        with patch.object(sys, "argv", testargs):
            with pytest.raises(SystemExit) as err:
                runner()
            assert err.value.code == 0


@pytest.mark.parametrize("runner", [run_pylint, run_pyreverse, run_symilar])
def test_runner_with_arguments(runner: _RunCallable, tmp_path: pathlib.Path) -> None:
    """Check the runners with arguments as parameter instead of sys.argv."""
    filepath = os.path.abspath(__file__)
    testargs = [filepath]
    with _test_cwd(tmp_path):
        with pytest.raises(SystemExit) as err:
            runner(testargs)
        assert err.value.code == 0


def test_pylint_argument_deduplication(
    tmp_path: pathlib.Path, tests_directory: pathlib.Path
) -> None:
    """Check that the Pylint runner does not over-report on duplicate
    arguments.

    See https://github.com/pylint-dev/pylint/issues/6242 and
    https://github.com/pylint-dev/pylint/issues/4053
    """
    filepath = str(tests_directory / "functional/t/too/too_many_branches.py")
    testargs = shlex.split("--report n --score n --max-branches 13")
    testargs.extend([filepath] * 4)
    exit_stack = contextlib.ExitStack()
    exit_stack.enter_context(_test_cwd(tmp_path))
    exit_stack.enter_context(patch.object(sys, "argv", testargs))
    err = exit_stack.enter_context(pytest.raises(SystemExit))
    with exit_stack:
        run_pylint(testargs)
    assert err.value.code == 0


@pytest.mark.parametrize(
    "quota,shares,period",
    [
        # Shares path
        ("-1", "2", ""),
        ("-1", "1023", ""),
        ("-1", "1024", ""),
        # Periods path
        ("100", "", "200"),
        ("999", "", "1000"),
        ("1000", "", "1000"),
    ],
)
def test_pylint_run_dont_crash_with_cgroupv1(
    tmp_path: pathlib.Path,
    quota: str,
    shares: str,
    period: str,
) -> None:
    """Check that the pylint runner does not crash if `pylint.lint.run._query_cpu`
    determines only a fraction of a CPU core to be available.
    """
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]

    with _test_cwd(tmp_path):
        with pytest.raises(SystemExit) as err:
            with patch(
                "builtins.open",
                mock_cgroup_fs(quota=quota, shares=shares, period=period),
            ):
                with patch("pylint.lint.run.Path", mock_cgroup_path(v2=False)):
                    Run(testargs, reporter=Reporter())
        assert err.value.code == 0


@pytest.mark.parametrize(
    "contents",
    [
        "1 2",
        "max 100000",
    ],
)
def test_pylint_run_dont_crash_with_cgroupv2(
    tmp_path: pathlib.Path,
    contents: str,
) -> None:
    """Check that the pylint runner does not crash if `pylint.lint.run._query_cpu`
    determines only a fraction of a CPU core to be available.
    """
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]

    with _test_cwd(tmp_path):
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", mock_cgroup_fs(max_v2=contents)):
                with patch("pylint.lint.run.Path", mock_cgroup_path(v2=True)):
                    Run(testargs, reporter=Reporter())
        assert err.value.code == 0


@pytest.mark.parametrize(
    "contents,expected",
    [
        ("50000 100000", 1),
        ("100000 100000", 1),
        ("200000 100000", 2),
        ("299999 100000", 2),
        ("300000 100000", 3),
        # Unconstrained cgroup
        ("max 100000", None),
    ],
)
def test_query_cpu_cgroupv2(
    tmp_path: pathlib.Path,
    contents: str,
    expected: int,
) -> None:
    """Check that `pylint.lint.run._query_cpu` generates realistic values in cgroupsv2
    systems.
    """
    with _test_cwd(tmp_path):
        with patch("builtins.open", mock_cgroup_fs(max_v2=contents)):
            with patch("pylint.lint.run.Path", mock_cgroup_path(v2=True)):
                cpus = _query_cpu()
                assert cpus == expected


@pytest.mark.parametrize(
    "quota,shares,period,expected",
    [
        # Shares path
        ("-1", "2", "", 1),
        ("-1", "1023", "", 1),
        ("-1", "1024", "", 1),
        ("-1", "2048", "", 2),
        # Periods path
        ("100", "", "200", 1),
        ("999", "", "1000", 1),
        ("1000", "", "1000", 1),
        ("2000", "", "1000", 2),
    ],
)
def test_query_cpu_cgroupv1(
    tmp_path: pathlib.Path,
    quota: str,
    shares: str,
    period: str,
    expected: int,
) -> None:
    """Check that `pylint.lint.run._query_cpu` generates realistic values in cgroupsv1
    systems.
    """
    with _test_cwd(tmp_path):
        with patch(
            "builtins.open", mock_cgroup_fs(quota=quota, shares=shares, period=period)
        ):
            with patch("pylint.lint.run.Path", mock_cgroup_path(v2=False)):
                cpus = _query_cpu()
                assert cpus == expected


def mock_cgroup_path(v2: bool) -> Any:
    def _mock_path(*args: str, **kwargs: Any) -> pathlib.Path:
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return MagicMock(is_file=lambda: not v2)
        if args[0] == "/sys/fs/cgroup/cpu/cpu.shares":
            return MagicMock(is_file=lambda: not v2)
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return MagicMock(is_file=lambda: not v2)
        if args[0] == "/sys/fs/cgroup/cpu.max":
            return MagicMock(is_file=lambda: v2)
        return pathlib.Path(*args, **kwargs)

    return _mock_path


def mock_cgroup_fs(
    quota: str = "", shares: str = "", period: str = "", max_v2: str = ""
) -> Any:
    builtin_open = open

    def _mock_open(*args: Any, **kwargs: Any) -> BufferedReader:
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data=quota)(*args, **kwargs)  # type: ignore[no-any-return]
        if args[0] == "/sys/fs/cgroup/cpu/cpu.shares":
            return mock_open(read_data=shares)(*args, **kwargs)  # type: ignore[no-any-return]
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return mock_open(read_data=period)(*args, **kwargs)  # type: ignore[no-any-return]
        if args[0] == "/sys/fs/cgroup/cpu.max":
            return mock_open(read_data=max_v2)(*args, **kwargs)  # type: ignore[no-any-return]
        return builtin_open(*args, **kwargs)  # type: ignore[no-any-return]

    return _mock_open
