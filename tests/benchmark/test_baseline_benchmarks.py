"""Profiles basic -jX functionality."""

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=missing-function-docstring

import os
import pprint
import time
from unittest.mock import patch

import pytest
from astroid import nodes
from pytest_benchmark.fixture import BenchmarkFixture

from pylint.checkers import BaseRawFileChecker
from pylint.lint import PyLinter, check_parallel
from pylint.testutils import GenericTestReporter as Reporter
from pylint.testutils._run import _Run as Run
from pylint.typing import FileItem
from pylint.utils import register_plugins


def _empty_filepath() -> str:
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "input", "benchmark_minimal_file.py"
        )
    )


class SleepingChecker(BaseRawFileChecker):
    """A checker that sleeps, the wall-clock time should reduce as we add workers.

    As we apply a roughly constant amount of "work" in this checker any variance is
    likely to be caused by the pylint system.
    """

    name = "sleeper"
    msgs = {
        "R9999": (
            "Test",
            "test-check",
            "Some helpful text.",
        )
    }
    sleep_duration = 0.5  # the time to pretend we're doing work for

    def process_module(self, node: nodes.Module) -> None:
        """Sleeps for `sleep_duration` on each call.

        This effectively means each file costs ~`sleep_duration`+framework overhead
        """
        time.sleep(self.sleep_duration)


class SleepingCheckerLong(BaseRawFileChecker):
    """A checker that sleeps, the wall-clock time should reduce as we add workers.

    As we apply a roughly constant amount of "work" in this checker any variance is
    likely to be caused by the pylint system.
    """

    name = "long-sleeper"
    msgs = {
        "R9999": (
            "Test",
            "test-check",
            "Some helpful text.",
        )
    }
    sleep_duration = 0.5  # the time to pretend we're doing work for

    def process_module(self, node: nodes.Module) -> None:
        """Sleeps for `sleep_duration` on each call.

        This effectively means each file costs ~`sleep_duration`+framework overhead
        """
        time.sleep(self.sleep_duration)


class NoWorkChecker(BaseRawFileChecker):
    """A checker that sleeps, the wall-clock time should change as we add threads."""

    name = "sleeper"
    msgs = {
        "R9999": (
            "Test",
            "test-check",
            "Some helpful text.",
        )
    }

    def process_module(self, node: nodes.Module) -> None:
        pass


@pytest.mark.benchmark(
    group="baseline",
)
class TestEstablishBaselineBenchmarks:
    """Naive benchmarks for the high-level pylint framework.

    Because this benchmarks the fundamental and common parts and changes seen here will
    impact everything else
    """

    empty_filepath = _empty_filepath()
    empty_file_info = FileItem(
        "name-emptyfile-file",
        _empty_filepath(),
        "modname-emptyfile-mod",
    )
    lot_of_files = 500

    def test_baseline_benchmark_j1(self, benchmark: BenchmarkFixture) -> None:
        """Establish a baseline of pylint performance with no work.

        We will add extra Checkers in other benchmarks.

        Because this is so simple, if this regresses something very serious has happened
        """
        linter = PyLinter(reporter=Reporter())
        fileinfos = [self.empty_filepath]  # Single file to end-to-end the system
        assert linter.config.jobs == 1
        assert len(linter._checkers) == 1, "Should just have 'main'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    @pytest.mark.needs_two_cores
    def test_baseline_benchmark_j2(self, benchmark: BenchmarkFixture) -> None:
        """Establish a baseline of pylint performance with no work across threads.

        Same as `test_baseline_benchmark_j1` but we use -j2 with 2 fake files to
        ensure end-to-end-system invoked.

        Because this is also so simple, if this regresses something very serious has
        happened.
        """
        linter = PyLinter(reporter=Reporter())
        linter.config.jobs = 2

        # Create file per worker, using all workers
        fileinfos = [self.empty_filepath for _ in range(linter.config.jobs)]

        assert linter.config.jobs == 2
        assert len(linter._checkers) == 1, "Should have 'main'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    @pytest.mark.needs_two_cores
    def test_baseline_benchmark_check_parallel_j2(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Should demonstrate times very close to `test_baseline_benchmark_j2`."""
        linter = PyLinter(reporter=Reporter())

        # Create file per worker, using all workers
        fileinfos = [self.empty_file_info for _ in range(linter.config.jobs)]

        assert len(linter._checkers) == 1, "Should have 'main'"
        benchmark(check_parallel, linter, jobs=2, files=fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    def test_baseline_lots_of_files_j1(self, benchmark: BenchmarkFixture) -> None:
        """Establish a baseline with only 'main' checker being run in -j1.

        We do not register any checkers except the default 'main', so the cost is just
        that of the system with a lot of files registered
        """
        if benchmark.disabled:
            benchmark(print, "skipping, only benchmark large file counts")
            return  # _only_ run this test is profiling
        linter = PyLinter(reporter=Reporter())
        linter.config.jobs = 1
        fileinfos = [self.empty_filepath for _ in range(self.lot_of_files)]
        assert linter.config.jobs == 1
        assert len(linter._checkers) == 1, "Should have 'main'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    @pytest.mark.needs_two_cores
    def test_baseline_lots_of_files_j2(self, benchmark: BenchmarkFixture) -> None:
        """Establish a baseline with only 'main' checker being run in -j2.

        As with the -j1 variant above `test_baseline_lots_of_files_j1`, we do not
        register any checkers except the default 'main', so the cost is just that of
        the check_parallel system across 2 workers, plus the overhead of PyLinter
        """
        if benchmark.disabled:
            benchmark(print, "skipping, only benchmark large file counts")
            return  # _only_ run this test is profiling
        linter = PyLinter(reporter=Reporter())
        linter.config.jobs = 2
        fileinfos = [self.empty_filepath for _ in range(self.lot_of_files)]
        assert linter.config.jobs == 2
        assert len(linter._checkers) == 1, "Should have 'main'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    def test_baseline_lots_of_files_j1_empty_checker(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Baselines pylint for a single extra checker being run in -j1, for N-files.

        We use a checker that does no work, so the cost is just that of the system at
        scale
        """
        if benchmark.disabled:
            benchmark(print, "skipping, only benchmark large file counts")
            return  # _only_ run this test is profiling
        linter = PyLinter(reporter=Reporter())
        linter.config.jobs = 1
        linter.register_checker(NoWorkChecker(linter))
        fileinfos = [self.empty_filepath for _ in range(self.lot_of_files)]
        assert linter.config.jobs == 1
        assert len(linter._checkers) == 2, "Should have 'main' and 'sleeper'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    @pytest.mark.needs_two_cores
    def test_baseline_lots_of_files_j2_empty_checker(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Baselines pylint for a single extra checker being run in -j2, for N-files.

        We use a checker that does no work, so the cost is just that of the system at
        scale, across workers
        """
        if benchmark.disabled:
            benchmark(print, "skipping, only benchmark large file counts")
            return  # _only_ run this test is profiling
        linter = PyLinter(reporter=Reporter())
        linter.config.jobs = 2
        linter.register_checker(NoWorkChecker(linter))
        fileinfos = [self.empty_filepath for _ in range(self.lot_of_files)]
        assert linter.config.jobs == 2
        assert len(linter._checkers) == 2, "Should have 'main' and 'sleeper'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    def test_baseline_benchmark_j1_single_working_checker(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Establish a baseline of single-worker performance for PyLinter.

        Here we mimic a single Checker that does some work so that we can see the
        impact of running a simple system with -j1 against the same system with -j2.

        We expect this benchmark to take very close to
        `numfiles*SleepingChecker.sleep_duration`
        """
        if benchmark.disabled:
            benchmark(print, "skipping, do not want to sleep in main tests")
            return  # _only_ run this test is profiling
        linter = PyLinter(reporter=Reporter())
        linter.register_checker(SleepingChecker(linter))

        # Check the same number of files as
        # `test_baseline_benchmark_j2_single_working_checker`
        fileinfos = [self.empty_filepath for _ in range(2)]

        assert linter.config.jobs == 1
        assert len(linter._checkers) == 2, "Should have 'main' and 'sleeper'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    @pytest.mark.needs_two_cores
    def test_baseline_benchmark_j2_single_working_checker(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Establishes baseline of multi-worker performance for PyLinter/check_parallel.

        We expect this benchmark to take less time that test_baseline_benchmark_j1,
        `error_margin*(1/J)*(numfiles*SleepingChecker.sleep_duration)`

        Because of the cost of the framework and system the performance difference will
        *not* be 1/2 of -j1 versions.
        """
        if benchmark.disabled:
            benchmark(print, "skipping, do not want to sleep in main tests")
            return  # _only_ run this test is profiling
        linter = PyLinter(reporter=Reporter())
        linter.config.jobs = 2
        linter.register_checker(SleepingChecker(linter))

        # Check the same number of files as
        # `test_baseline_benchmark_j1_single_working_checker`
        fileinfos = [self.empty_filepath for _ in range(2)]

        assert linter.config.jobs == 2
        assert len(linter._checkers) == 2, "Should have 'main' and 'sleeper'"
        benchmark(linter.check, fileinfos)
        assert (
            linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(linter.reporter.messages)}"

    def test_baseline_benchmark_j1_all_checks_single_file(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Runs a single file, with -j1, against all checkers/Extensions."""
        args = [self.empty_filepath, "--enable=all", "--enable-all-extensions"]
        runner = benchmark(Run, args, reporter=Reporter(), exit=False)
        assert runner.linter.config.jobs == 1
        print("len(runner.linter._checkers)", len(runner.linter._checkers))
        assert len(runner.linter._checkers) > 1, "Should have more than 'main'"

        assert (
            runner.linter.msg_status == 0
        ), f"Expected no errors to be thrown: {pprint.pformat(runner.linter.reporter.messages)}"

    def test_baseline_benchmark_j1_all_checks_lots_of_files(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Runs lots of files, with -j1, against all plug-ins.

        ... that's the intent at least.
        """
        if benchmark.disabled:
            benchmark(print, "skipping, only benchmark large file counts")
            return  # _only_ run this test is profiling
        linter = PyLinter()

        # Register all checkers/extensions and enable them
        with patch("os.listdir", return_value=["pylint", "tests"]):
            register_plugins(
                linter,
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
            )
        linter.load_default_plugins()
        linter.enable("all")

        # Just 1 file, but all Checkers/Extensions
        fileinfos = [self.empty_filepath for _ in range(self.lot_of_files)]

        assert linter.config.jobs == 1
        print("len(linter._checkers)", len(linter._checkers))
        assert len(linter._checkers) > 1, "Should have more than 'main'"
        benchmark(linter.check, fileinfos)
