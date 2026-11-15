# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Benchmarks measured by CodSpeed, see ``.github/workflows/codspeed.yaml``.

CodSpeed measures most benchmarks in simulation mode: it counts the CPU
instructions of the test process instead of time, so results do not depend on
the runner, and it records a call graph to show which function got slower.

Simulation cannot see work done in other processes: benchmarks using
``--jobs`` or a new interpreter are marked ``wall_clock`` and measured in
walltime mode instead. Wall time on a shared runner is noisier: raise a
benchmark's threshold on the CodSpeed dashboard if it reports false
regressions.
"""

from __future__ import annotations

import subprocess
import sys
from typing import TYPE_CHECKING

import pytest
from astroid import MANAGER, nodes

from pylint.checkers import BaseRawFileChecker
from pylint.lint import PyLinter
from pylint.testutils._primer import PackageToLint
from pylint.testutils._run import _Run as Run
from pylint.testutils.reporter_for_tests import GenericTestReporter

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_codspeed import BenchmarkFixture

ALL_CHECKS = ["--enable=all", "--enable-all-extensions"]


class NoWorkChecker(BaseRawFileChecker):
    """A checker doing nothing, to measure the cost of the framework alone."""

    name = "no-work"
    msgs = {"R9999": ("Test", "test-check", "Some helpful text.")}

    def process_module(self, node: nodes.Module) -> None:
        pass


def _framework_only_linter(jobs: int) -> PyLinter:
    linter = PyLinter(reporter=GenericTestReporter())
    linter.register_checker(NoWorkChecker(linter))
    linter.config.jobs = jobs
    return linter


def _lint(args: list[str]) -> Run:
    """Lint from a cold astroid cache, like a new pylint process would.

    CodSpeed runs a warmup round before measuring: without clearing the cache
    the measured round would skip parsing and most of the inference.
    """
    MANAGER.clear_cache()
    return Run(args, reporter=GenericTestReporter(), exit=False)


def _lint_in_new_interpreter(path: Path) -> None:
    # pylint exits with a non-zero code when it emits a message, only the time
    # matters here.
    subprocess.run(
        [sys.executable, "-m", "pylint", str(path)], check=False, capture_output=True
    )


def test_bench_framework_only_many_files(
    benchmark: BenchmarkFixture, many_files: list[str]
) -> None:
    """Lint many small files with a checker doing nothing.

    Measures what pylint costs per file before any real checker runs.
    """
    linter = _framework_only_linter(jobs=1)
    benchmark(linter.check, many_files)
    assert linter.msg_status == 0, linter.reporter.messages
    assert len(linter.stats.by_module) == len(many_files)


def test_bench_all_checks_single_file(
    benchmark: BenchmarkFixture, minimal_file: Path
) -> None:
    """Configure every checker and extension, then lint one small file.

    Dominated by startup work: option parsing and plugin registration.
    """
    runner = benchmark(_lint, [str(minimal_file), *ALL_CHECKS])
    assert runner.linter.msg_status == 0, runner.linter.reporter.messages


def test_bench_all_checks_flask(
    benchmark: BenchmarkFixture, flask: PackageToLint
) -> None:
    """Lint flask with every checker and extension enabled."""
    runner = benchmark(_lint, [*flask.paths_to_lint, *ALL_CHECKS])
    assert runner.linter.stats.statement > 0


def test_bench_default_config_black(
    benchmark: BenchmarkFixture, black: PackageToLint
) -> None:
    """Lint black with the default configuration, like most users do."""
    runner = benchmark(_lint, black.paths_to_lint)
    assert runner.linter.stats.statement > 0


@pytest.mark.wall_clock
def test_bench_cold_start(benchmark: BenchmarkFixture, minimal_file: Path) -> None:
    """Lint one small file in a new interpreter.

    Catches what in-process benchmarks cannot see: slower imports and startup.
    """
    benchmark(_lint_in_new_interpreter, minimal_file)


@pytest.mark.wall_clock
@pytest.mark.needs_two_cores
def test_bench_framework_only_many_files_j2(
    benchmark: BenchmarkFixture, many_files: list[str]
) -> None:
    """Like ``test_bench_framework_only_many_files``, with two worker processes.

    Measures the cost of starting workers and sending them the linter.
    """
    linter = _framework_only_linter(jobs=2)
    benchmark(linter.check, many_files)
    assert linter.msg_status == 0, linter.reporter.messages
    assert len(linter.stats.by_module) == len(many_files)


@pytest.mark.wall_clock
@pytest.mark.needs_two_cores
def test_bench_default_config_flask_j2(
    benchmark: BenchmarkFixture, flask: PackageToLint
) -> None:
    """Lint flask with two worker processes.

    Shows if parallel linting stops being faster than ``--jobs=1``.
    """
    runner = benchmark(_lint, [*flask.paths_to_lint, "--jobs=2"])
    assert runner.linter.stats.statement > 0
