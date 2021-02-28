"""Puts the check_parallel system under test"""
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

# pylint: disable=protected-access,missing-function-docstring,no-self-use

import collections
import os

import pytest

import pylint.interfaces
import pylint.lint.parallel
from pylint.checkers.base_checker import BaseChecker
from pylint.lint import PyLinter
from pylint.lint.parallel import _worker_check_single_file as worker_check_single_file
from pylint.lint.parallel import _worker_initialize as worker_initialize
from pylint.lint.parallel import check_parallel
from pylint.testutils import GenericTestReporter as Reporter


def _gen_file_data(idx=0):
    """Generates a file to use as a stream"""
    filepath = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "input", "similar1")
    )
    file_data = (
        "--test-file_data-name-%d--" % idx,
        filepath,
        "--test-file_data-modname-%d--" % idx,
    )
    return file_data


def _gen_file_datas(count=1):
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

    def __init__(self, linter, *args, **kwargs):
        super().__init__(linter, *args, **kwargs)
        self.data = []
        self.linter = linter

    def process_module(self, _astroid):
        """Called once per stream/file/astroid object"""
        # record the number of invocations with the data object
        record = self.test_data + str(len(self.data))
        self.data.append(record)


class ExtraSequentialTestChecker(SequentialTestChecker):
    """A checker that does not need to consolidate data across run invocations"""

    name = "extra-sequential-checker"
    test_data = "extra-sequential"


class ThirdSequentialTestChecker(SequentialTestChecker):
    """A checker that does not need to consolidate data across run invocations"""

    name = "third-sequential-checker"
    test_data = "third-sequential"


class TestCheckParallelFramework:
    """Tests the check_parallel() function's framework"""

    def setup_class(self):
        self._prev_global_linter = pylint.lint.parallel._worker_linter

    def teardown_class(self):
        pylint.lint.parallel._worker_linter = self._prev_global_linter

    def test_worker_initialize(self):
        linter = PyLinter(reporter=Reporter())
        worker_initialize(linter=linter)
        assert pylint.lint.parallel._worker_linter == linter

    def test_worker_check_single_file_uninitialised(self):
        pylint.lint.parallel._worker_linter = None
        with pytest.raises(  # Objects that do not match the linter interface will fail
            AttributeError, match="'NoneType' object has no attribute 'open'"
        ):
            worker_check_single_file(_gen_file_data())

    def test_worker_check_single_file_no_checkers(self):
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
        assert [] == msgs
        no_errors_status = 0
        assert no_errors_status == msg_status
        assert {
            "by_module": {
                "--test-file_data-name-0--": {
                    "convention": 0,
                    "error": 0,
                    "fatal": 0,
                    "info": 0,
                    "refactor": 0,
                    "statement": 18,
                    "warning": 0,
                }
            },
            "by_msg": {},
            "convention": 0,
            "error": 0,
            "fatal": 0,
            "info": 0,
            "refactor": 0,
            "statement": 18,
            "warning": 0,
        } == stats

    def test_worker_check_sequential_checker(self):
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
        assert [] == msgs
        no_errors_status = 0
        assert no_errors_status == msg_status
        assert {
            "by_module": {
                "--test-file_data-name-0--": {
                    "convention": 0,
                    "error": 0,
                    "fatal": 0,
                    "info": 0,
                    "refactor": 0,
                    "statement": 18,
                    "warning": 0,
                }
            },
            "by_msg": {},
            "convention": 0,
            "error": 0,
            "fatal": 0,
            "info": 0,
            "refactor": 0,
            "statement": 18,
            "warning": 0,
        } == stats


class TestCheckParallel:
    """Tests the check_parallel() function"""

    def test_sequential_checkers_work(self):
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
        check_parallel(linter, jobs=1, files=single_file_container, arguments=None)
        assert len(linter.get_checkers()) == 2, (
            "We should only have the 'master' and 'sequential-checker' "
            "checkers registered"
        )
        assert {
            "by_module": {
                "--test-file_data-name-0--": {
                    "convention": 0,
                    "error": 0,
                    "fatal": 0,
                    "info": 0,
                    "refactor": 0,
                    "statement": 18,
                    "warning": 0,
                }
            },
            "by_msg": {},
            "convention": 0,
            "error": 0,
            "fatal": 0,
            "info": 0,
            "refactor": 0,
            "statement": 18,
            "warning": 0,
        } == linter.stats

        # now run the regular mode of checking files and check that, in this proc, we
        # collect the right data
        filepath = single_file_container[0][1]  # get the filepath element
        linter.check(filepath)
        assert {
            "by_module": {
                "input.similar1": {  # module is the only change from previous
                    "convention": 0,
                    "error": 0,
                    "fatal": 0,
                    "info": 0,
                    "refactor": 0,
                    "statement": 18,
                    "warning": 0,
                }
            },
            "by_msg": {},
            "convention": 0,
            "error": 0,
            "fatal": 0,
            "info": 0,
            "refactor": 0,
            "statement": 18,
            "warning": 0,
        } == linter.stats

    def test_invoke_single_job(self):
        """Tests basic checkers functionality using just a single workderdo

        This is *not* the same -j1 and does not happen under normal operation"""
        linter = PyLinter(reporter=Reporter())

        linter.register_checker(SequentialTestChecker(linter))

        # Create a dummy file, the actual contents of which will be ignored by the
        # register test checkers, but it will trigger at least a single-job to be run.
        single_file_container = _gen_file_datas(count=1)

        # Invoke the lint process in a multiprocess way, although we only specify one
        # job.
        check_parallel(linter, jobs=1, files=single_file_container, arguments=None)

        assert {
            "by_module": {
                "--test-file_data-name-0--": {
                    "convention": 0,
                    "error": 0,
                    "fatal": 0,
                    "info": 0,
                    "refactor": 0,
                    "statement": 18,
                    "warning": 0,
                }
            },
            "by_msg": collections.Counter(),
            "convention": 0,
            "error": 0,
            "fatal": 0,
            "info": 0,
            "refactor": 0,
            "statement": 18,
            "warning": 0,
        } == linter.stats
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
        expected_stats = {
            "by_module": {
                "--test-file_data-name-%d--"
                % idx: {
                    "convention": 0,
                    "error": 0,
                    "fatal": 0,
                    "info": 0,
                    "refactor": 0,
                    "statement": 18,
                    "warning": 0,
                }
                for idx in range(num_files)
            },
            "by_msg": {},
            "convention": 0,
            "error": 0,
            "fatal": 0,
            "info": 0,
            "refactor": 0,
            "statement": 18 * num_files,
            "warning": 0,
        }

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

        assert (
            stats_single_proc == stats_check_parallel
        ), "Single-proc and check_parallel() should return the same thing"
        assert (
            stats_check_parallel == expected_stats
        ), "The lint is returning unexpected results, has something changed?"
