"""Puts the check_parallel system under test"""
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2021 Jaehoon Hwang <jaehoonhwang@users.noreply.github.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Julien Palard <julien@palard.fr>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

# pylint: disable=protected-access,missing-function-docstring,no-self-use

import os
from typing import List

import pytest
from astroid import nodes

import pylint.interfaces
import pylint.lint.parallel
from pylint.checkers.base_checker import BaseChecker
from pylint.lint import PyLinter
from pylint.lint.parallel import _worker_check_single_file as worker_check_single_file
from pylint.lint.parallel import _worker_initialize as worker_initialize
from pylint.lint.parallel import check_parallel
from pylint.testutils import GenericTestReporter as Reporter
from pylint.typing import FileItem
from pylint.utils import LinterStats, ModuleStats


def _gen_file_data(idx: int = 0) -> FileItem:
    """Generates a file to use as a stream"""
    filepath = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "input", "similar1")
    )
    file_data = FileItem(
        f"--test-file_data-name-{idx}--",
        filepath,
        f"--test-file_data-modname-{idx}--",
    )
    return file_data


def _gen_file_datas(count: int = 1) -> List[FileItem]:
    return [_gen_file_data(idx) for idx in range(count)]


class SequentialTestChecker(BaseChecker):
    """A checker that does not need to consolidate data across run invocations"""

    __implements__ = (pylint.interfaces.IRawChecker,)

    name = "sequential-checker"
    test_data = "sequential"
    msgs = {
        "R9999": (
            "Test",
            "sequential-test-check",
            "Some helpful text.",
        )
    }

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.data: List[str] = []
        self.linter = linter

    def process_module(self, _node: nodes.Module) -> None:
        """Called once per stream/file/astroid object"""
        # record the number of invocations with the data object
        record = self.test_data + str(len(self.data))
        self.data.append(record)


class ParallelTestChecker(BaseChecker):
    """A checker that does need to consolidate data.

    To simulate the need to consolidate data, this checker only
    reports a message for pairs of files.

    On non-parallel builds: it works on all the files in a single run.

    On parallel builds: lint.parallel calls ``open`` once per file.

    So if files are treated by separate processes, no messages will be
    raised from the individual process, all messages will be raised
    from reduce_map_data.
    """

    __implements__ = (pylint.interfaces.IRawChecker,)

    name = "parallel-checker"
    test_data = "parallel"
    msgs = {
        "R9999": (
            "Test %s",
            "parallel-test-check",
            "Some helpful text.",
        )
    }

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.data: List[str] = []
        self.linter = linter

    def open(self) -> None:
        """init the checkers: reset statistics information"""
        self.linter.stats.reset_node_count()
        self.data = []

    def close(self) -> None:
        for _ in self.data[1::2]:  # Work on pairs of files, see class docstring.
            self.add_message("R9999", args=("From process_module, two files seen.",))

    def get_map_data(self):
        return self.data

    def reduce_map_data(self, linter: PyLinter, data: List[List[str]]) -> None:
        recombined = type(self)(linter)
        recombined.open()
        aggregated = []
        for d in data:
            aggregated.extend(d)
        for _ in aggregated[1::2]:  # Work on pairs of files, see class docstring.
            self.add_message("R9999", args=("From reduce_map_data",))
        recombined.close()

    def process_module(self, _node: nodes.Module) -> None:
        """Called once per stream/file/astroid object"""
        # record the number of invocations with the data object
        record = self.test_data + str(len(self.data))
        self.data.append(record)


class ExtraSequentialTestChecker(SequentialTestChecker):
    """A checker that does not need to consolidate data across run invocations"""

    name = "extra-sequential-checker"
    test_data = "extra-sequential"


class ExtraParallelTestChecker(ParallelTestChecker):
    """A checker that does need to consolidate data across run invocations"""

    name = "extra-parallel-checker"
    test_data = "extra-parallel"


class ThirdSequentialTestChecker(SequentialTestChecker):
    """A checker that does not need to consolidate data across run invocations"""

    name = "third-sequential-checker"
    test_data = "third-sequential"


class ThirdParallelTestChecker(ParallelTestChecker):
    """A checker that does need to consolidate data across run invocations"""

    name = "third-parallel-checker"
    test_data = "third-parallel"


class TestCheckParallelFramework:
    """Tests the check_parallel() function's framework"""

    def setup_class(self):
        self._prev_global_linter = pylint.lint.parallel._worker_linter

    def teardown_class(self):
        pylint.lint.parallel._worker_linter = self._prev_global_linter

    def test_worker_initialize(self) -> None:
        linter = PyLinter(reporter=Reporter())
        worker_initialize(linter=linter)
        assert pylint.lint.parallel._worker_linter == linter

    def test_worker_check_single_file_uninitialised(self) -> None:
        pylint.lint.parallel._worker_linter = None
        with pytest.raises(  # Objects that do not match the linter interface will fail
            Exception, match="Worker linter not yet initialised"
        ):
            worker_check_single_file(_gen_file_data())

    def test_worker_check_single_file_no_checkers(self) -> None:
        linter = PyLinter(reporter=Reporter())
        worker_initialize(linter=linter)

        (
            _,  # proc-id
            name,
            _,  # file_path
            _,  # base_name
            msgs,
            stats,
            msg_status,
            _,  # mapreduce_data
        ) = worker_check_single_file(_gen_file_data())
        assert name == "--test-file_data-name-0--"
        assert not msgs
        no_errors_status = 0
        assert no_errors_status == msg_status
        assert {
            "--test-file_data-name-0--": {
                "convention": 0,
                "error": 0,
                "fatal": 0,
                "info": 0,
                "refactor": 0,
                "statement": 18,
                "warning": 0,
            }
        } == stats.by_module
        assert not stats.by_msg
        assert stats.convention == 0
        assert stats.error == 0
        assert stats.fatal == 0
        assert stats.info == 0
        assert stats.refactor == 0
        assert stats.statement == 18
        assert stats.warning == 0

    def test_worker_check_sequential_checker(self) -> None:
        """Same as test_worker_check_single_file_no_checkers with SequentialTestChecker"""
        linter = PyLinter(reporter=Reporter())
        worker_initialize(linter=linter)

        # Add the only checker we care about in this test
        linter.register_checker(SequentialTestChecker(linter))

        (
            _,  # proc-id
            name,
            _,  # file_path
            _,  # base_name
            msgs,
            stats,
            msg_status,
            _,  # mapreduce_data
        ) = worker_check_single_file(_gen_file_data())

        # Ensure we return the same data as the single_file_no_checkers test
        assert name == "--test-file_data-name-0--"
        assert not msgs
        no_errors_status = 0
        assert no_errors_status == msg_status
        assert {
            "--test-file_data-name-0--": {
                "convention": 0,
                "error": 0,
                "fatal": 0,
                "info": 0,
                "refactor": 0,
                "statement": 18,
                "warning": 0,
            }
        } == stats.by_module
        assert not stats.by_msg
        assert stats.convention == 0
        assert stats.error == 0
        assert stats.fatal == 0
        assert stats.info == 0
        assert stats.refactor == 0
        assert stats.statement == 18
        assert stats.warning == 0


class TestCheckParallel:
    """Tests the check_parallel() function"""

    def test_sequential_checkers_work(self) -> None:
        """Tests original basic types of checker works as expected in -jN

        This means that a sequential checker should return the same data for a given
        file-stream irrespective of whether its run in -j1 or -jN
        """
        linter = PyLinter(reporter=Reporter())

        # Add a sequential checker to ensure it records data against some streams
        linter.register_checker(SequentialTestChecker(linter))
        linter.enable("R9999")

        # Create a dummy file, the actual contents of which will be ignored by the
        # register test checkers, but it will trigger at least a single-job to be run.
        single_file_container = _gen_file_datas(count=1)

        # Invoke the lint process in a multiprocess way, although we only specify one
        # job.
        check_parallel(
            linter, jobs=1, files=iter(single_file_container), arguments=None
        )
        assert len(linter.get_checkers()) == 2, (
            "We should only have the 'master' and 'sequential-checker' "
            "checkers registered"
        )
        assert {
            "--test-file_data-name-0--": {
                "convention": 0,
                "error": 0,
                "fatal": 0,
                "info": 0,
                "refactor": 0,
                "statement": 18,
                "warning": 0,
            }
        } == linter.stats.by_module
        assert not linter.stats.by_msg
        assert linter.stats.convention == 0
        assert linter.stats.error == 0
        assert linter.stats.fatal == 0
        assert linter.stats.info == 0
        assert linter.stats.refactor == 0
        assert linter.stats.statement == 18
        assert linter.stats.warning == 0

        # now run the regular mode of checking files and check that, in this proc, we
        # collect the right data
        filepath = [single_file_container[0][1]]  # get the filepath element
        linter.check(filepath)
        assert {
            "input.similar1": {  # module is the only change from previous
                "convention": 0,
                "error": 0,
                "fatal": 0,
                "info": 0,
                "refactor": 0,
                "statement": 18,
                "warning": 0,
            }
        } == linter.stats.by_module
        assert not linter.stats.by_msg
        assert linter.stats.convention == 0
        assert linter.stats.error == 0
        assert linter.stats.fatal == 0
        assert linter.stats.info == 0
        assert linter.stats.refactor == 0
        assert linter.stats.statement == 18
        assert linter.stats.warning == 0

    def test_invoke_single_job(self) -> None:
        """Tests basic checkers functionality using just a single workderdo

        This is *not* the same -j1 and does not happen under normal operation"""
        linter = PyLinter(reporter=Reporter())

        linter.register_checker(SequentialTestChecker(linter))

        # Create a dummy file, the actual contents of which will be ignored by the
        # register test checkers, but it will trigger at least a single-job to be run.
        single_file_container = _gen_file_datas(count=1)

        # Invoke the lint process in a multiprocess way, although we only specify one
        # job.
        check_parallel(
            linter, jobs=1, files=iter(single_file_container), arguments=None
        )

        assert {
            "--test-file_data-name-0--": {
                "convention": 0,
                "error": 0,
                "fatal": 0,
                "info": 0,
                "refactor": 0,
                "statement": 18,
                "warning": 0,
            }
        } == linter.stats.by_module
        assert not linter.stats.by_msg
        assert linter.stats.convention == 0
        assert linter.stats.error == 0
        assert linter.stats.fatal == 0
        assert linter.stats.info == 0
        assert linter.stats.refactor == 0
        assert linter.stats.statement == 18
        assert linter.stats.warning == 0
        assert linter.msg_status == 0, "We expect a single-file check to exit cleanly"

    @pytest.mark.parametrize(
        "num_files,num_jobs,num_checkers",
        [
            (1, 2, 1),
            (1, 2, 2),
            (1, 2, 3),
            (2, 2, 1),
            (2, 2, 2),
            (2, 2, 3),
            (3, 2, 1),
            (3, 2, 2),
            (3, 2, 3),
            (3, 1, 1),
            (3, 1, 2),
            (3, 1, 3),
            (3, 5, 1),
            (3, 5, 2),
            (3, 5, 3),
            (10, 2, 1),
            (10, 2, 2),
            (10, 2, 3),
            (2, 10, 1),
            (2, 10, 2),
            (2, 10, 3),
        ],
    )
    def test_compare_workers_to_single_proc(self, num_files, num_jobs, num_checkers):
        """Compares the 3 key parameters for check_parallel() produces the same results

        The intent here is to ensure that the check_parallel() operates on each file,
        without ordering issues, irrespective of the number of workers used and the
        number of checkers applied.

        This test becomes more important if we want to change how we parametrise the
        checkers, for example if we aim to batch the files across jobs."""

        # define the stats we expect to get back from the runs, these should only vary
        # with the number of files.
        expected_stats = LinterStats(
            by_module={
                # pylint: disable-next=consider-using-f-string
                "--test-file_data-name-%d--"
                % idx: ModuleStats(
                    convention=0,
                    error=0,
                    fatal=0,
                    info=0,
                    refactor=0,
                    statement=18,
                    warning=0,
                )
                for idx in range(num_files)
            }
        )
        expected_stats.by_msg = {}
        expected_stats.convention = 0
        expected_stats.error = 0
        expected_stats.fatal = 0
        expected_stats.info = 0
        expected_stats.refactor = 0
        expected_stats.statement = 18 * num_files
        expected_stats.warning = 0

        file_infos = _gen_file_datas(num_files)

        # Loop for single-proc and mult-proc so we can ensure the same linter-config
        for do_single_proc in range(2):
            linter = PyLinter(reporter=Reporter())

            # Assign between 1 and 3 checkers to the linter, they should not change the
            # results of the lint
            linter.register_checker(SequentialTestChecker(linter))
            if num_checkers > 1:
                linter.register_checker(ExtraSequentialTestChecker(linter))
            if num_checkers > 2:
                linter.register_checker(ThirdSequentialTestChecker(linter))

            if do_single_proc:
                # establish the baseline
                assert (
                    linter.config.jobs == 1
                ), "jobs>1 are ignored when calling _check_files"
                linter._check_files(linter.get_ast, file_infos)
                assert linter.msg_status == 0, "We should not fail the lint"
                stats_single_proc = linter.stats
            else:
                check_parallel(
                    linter,
                    jobs=num_jobs,
                    files=file_infos,
                    arguments=None,
                )
                stats_check_parallel = linter.stats
                assert linter.msg_status == 0, "We should not fail the lint"

        assert str(stats_single_proc) == str(
            stats_check_parallel
        ), "Single-proc and check_parallel() should return the same thing"
        assert str(stats_check_parallel) == str(
            expected_stats
        ), "The lint is returning unexpected results, has something changed?"

    @pytest.mark.parametrize(
        "num_files,num_jobs,num_checkers",
        [
            (2, 2, 1),
            (2, 2, 2),
            (2, 2, 3),
            (3, 2, 1),
            (3, 2, 2),
            (3, 2, 3),
            (3, 1, 1),
            (3, 1, 2),
            (3, 1, 3),
            (3, 5, 1),
            (3, 5, 2),
            (3, 5, 3),
            (10, 2, 1),
            (10, 2, 2),
            (10, 2, 3),
            (2, 10, 1),
            (2, 10, 2),
            (2, 10, 3),
        ],
    )
    def test_map_reduce(self, num_files, num_jobs, num_checkers):
        """Compares the 3 key parameters for check_parallel() produces the same results

        The intent here is to validate the reduce step: no stats should be lost.

        Checks regression of https://github.com/PyCQA/pylint/issues/4118
        """

        # define the stats we expect to get back from the runs, these should only vary
        # with the number of files.
        file_infos = _gen_file_datas(num_files)

        # Loop for single-proc and mult-proc so we can ensure the same linter-config
        for do_single_proc in range(2):
            linter = PyLinter(reporter=Reporter())

            # Assign between 1 and 3 checkers to the linter, they should not change the
            # results of the lint
            linter.register_checker(ParallelTestChecker(linter))
            if num_checkers > 1:
                linter.register_checker(ExtraParallelTestChecker(linter))
            if num_checkers > 2:
                linter.register_checker(ThirdParallelTestChecker(linter))

            if do_single_proc:
                # establish the baseline
                assert (
                    linter.config.jobs == 1
                ), "jobs>1 are ignored when calling _check_files"
                linter._check_files(linter.get_ast, file_infos)
                stats_single_proc = linter.stats
            else:
                check_parallel(
                    linter,
                    jobs=num_jobs,
                    files=file_infos,
                    arguments=None,
                )
                stats_check_parallel = linter.stats
        assert str(stats_single_proc.by_msg) == str(
            stats_check_parallel.by_msg
        ), "Single-proc and check_parallel() should return the same thing"
