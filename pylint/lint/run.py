# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import io
import functools
import os
import sys
import warnings
from io import TextIOWrapper
from itertools import chain
from collections import defaultdict
from typing import Iterator, List
from collections.abc import Sequence
from pathlib import Path
from typing import Any


import astroid
from pylint import config
from pylint import reporters
from pylint.config.config_initialization import _config_initialization
from pylint.config.exceptions import ArgumentPreprocessingError
from pylint.config.utils import _preprocess_options
from pylint.config.find_default_config_files import (
    search_parent_config_files,
    RC_NAMES,
    find_per_directory_config_files,
)
from pylint.constants import full_version
from pylint.lint.base_options import _make_run_options
from pylint.lint.parallel import check_parallel
from pylint.lint.pylinter import PyLinter
from pylint.lint.utils import merge_linters, fix_import_path
from pylint.reporters.base_reporter import BaseReporter
from pylint.typing import FileItem

try:
    import multiprocessing
    from multiprocessing import synchronize  # noqa pylint: disable=unused-import
except ImportError:
    multiprocessing = None  # type: ignore[assignment]


def _query_cpu() -> int | None:
    """Try to determine number of CPUs allotted in a docker container.

    This is based on discussion and copied from suggestions in
    https://bugs.python.org/issue36054.
    """
    cpu_quota, avail_cpu = None, None

    if Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").is_file():
        with open("/sys/fs/cgroup/cpu/cpu.cfs_quota_us", encoding="utf-8") as file:
            # Not useful for AWS Batch based jobs as result is -1, but works on local linux systems
            cpu_quota = int(file.read().rstrip())

    if (
        cpu_quota
        and cpu_quota != -1
        and Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").is_file()
    ):
        with open("/sys/fs/cgroup/cpu/cpu.cfs_period_us", encoding="utf-8") as file:
            cpu_period = int(file.read().rstrip())
        # Divide quota by period and you should get num of allotted CPU to the container, rounded down if fractional.
        avail_cpu = int(cpu_quota / cpu_period)
    elif Path("/sys/fs/cgroup/cpu/cpu.shares").is_file():
        with open("/sys/fs/cgroup/cpu/cpu.shares", encoding="utf-8") as file:
            cpu_shares = int(file.read().rstrip())
        # For AWS, gives correct value * 1024.
        avail_cpu = int(cpu_shares / 1024)
    return avail_cpu


def _cpu_count() -> int:
    """Use sched_affinity if available for virtualized or containerized environments."""
    cpu_share = _query_cpu()
    cpu_count = None
    sched_getaffinity = getattr(os, "sched_getaffinity", None)
    # pylint: disable=not-callable,using-constant-test,useless-suppression
    if sched_getaffinity:
        cpu_count = len(sched_getaffinity(0))
    elif multiprocessing:
        cpu_count = multiprocessing.cpu_count()
    else:
        cpu_count = 1
    if cpu_share is not None:
        return min(cpu_share, cpu_count)
    return cpu_count


UNUSED_PARAM_SENTINEL = object()


class RunLinter:
    """Helper class to use as main for pylint with 'run(*sys.argv[1:])'."""

    LinterClass = PyLinter
    option_groups = (
        (
            "Commands",
            "Options which are actually commands. Options in this \
group are mutually exclusive.",
        ),
    )

    @staticmethod
    def _return_one(*args):  # pylint: disable=unused-argument
        return 1

    def __init__(self, rcfiles=None):
        self._rcfiles = rcfiles
        self._version_asked = False
        self._plugins = []
        self.verbose = None

    def initialize(
        self,
        args: Sequence[str],
        reporter: BaseReporter | None = None,
    ) -> None:
        self.args = args
        try:
            args = _preprocess_options(self, args)
        except ArgumentPreprocessingError as ex:
            print(ex, file=sys.stderr)
            sys.exit(32)

        # Determine configuration file
        if self._rcfiles is None:
            default_file = next(config.find_default_config_files(), None)
            if default_file:
                self._rcfiles = [str(default_file)]

        self.linter = linter = self.LinterClass(
            _make_run_options(self),
            option_groups=self.option_groups,
            pylintrc=self._rcfiles,
        )
        # register standard checkers
        linter.load_default_plugins()
        # load command line plugins
        linter.load_plugin_modules(self._plugins)

        linter.disable("I")
        linter.enable("c-extension-no-member")

        args = _config_initialization(
            linter,
            args,
            reporter,
            config_files=self._rcfiles,
            verbose_mode=self.verbose,
        )
        return linter, args

    def initialize_jobs(self, linter: PyLinter) -> None:
        if linter.config.jobs < 0:
            print(
                f"Jobs number ({linter.config.jobs}) should be greater than or equal to 0",
                file=sys.stderr,
            )
            sys.exit(32)
        if linter.config.jobs > 1 or linter.config.jobs == 0:
            if multiprocessing is None:
                print(
                    "Multiprocessing library is missing, fallback to single process",
                    file=sys.stderr,
                )
                linter.set_option("jobs", 1)
            elif linter.config.jobs == 0:
                linter.config.jobs = _cpu_count()

    def run(
        self,
        linter: PyLinter,
        args: list,
        exit: bool,
    ) -> None:  # pylint: disable=redefined-builtin

        if linter.config.recursive is True:
            files_or_modules = tuple(self._discover_files(args))

        if linter.config.from_stdin:
            self.run_from_stdin(linter, args)
        elif linter.config.jobs == 1:
            self.run_simple(linter, files_or_modules)
        else:
            self.run_parallel(linter, files_or_modules)


        if exit:
            if linter.config.exit_zero:
                sys.exit(0)
            elif linter.any_fail_on_issues():
                # We need to make sure we return a failing exit code in this case.
                # So we use self.linter.msg_status if that is non-zero, otherwise we just return 1.
                sys.exit(self.linter.msg_status or 1)
            elif score_value is not None:
                if score_value >= linter.config.fail_under:
                    sys.exit(0)
                else:
                    # We need to make sure we return a failing exit code in this case.
                    # So we use self.linter.msg_status if that is non-zero, otherwise we just return 1.
                    sys.exit(self.linter.msg_status or 1)
            else:
                sys.exit(self.linter.msg_status)


    @staticmethod
    def _read_stdin() -> str:
        # See https://github.com/python/typeshed/pull/5623 for rationale behind assertion
        assert isinstance(sys.stdin, TextIOWrapper)
        sys.stdin = TextIOWrapper(sys.stdin.detach(), encoding="utf-8")
        return sys.stdin.read()

    @staticmethod
    def _get_file_descr_from_stdin(filepath: str) -> FileItem:
        """Return file description (tuple of module name, file path, base name) from given file path.

        This method is used for creating suitable file description for _check_files when the
        source is standard input.
        """
        try:
            # Note that this function does not really perform an
            # __import__ but may raise an ImportError exception, which
            # we want to catch here.
            modname = ".".join(astroid.modutils.modpath_from_file(filepath))
        except ImportError:
            modname = os.path.splitext(os.path.basename(filepath))[0]

        return FileItem(modname, filepath, filepath)

    def run_from_stdin(self, linter, files_or_modules):
        if len(files_or_modules) != 1:
            raise exceptions.InvalidArgsError(
                "Missing filename required for --from-stdin"
            )

        filepath = files_or_modules[0]
        with fix_import_path(files_or_modules):
            linter._check_files(
                functools.partial(linter.get_ast, data=self._read_stdin()),
                [self._get_file_descr_from_stdin(filepath)],
            )

    def run_parallel(self, linter, files_or_modules):
        sub_linter_files = defaultdict(list)  # rcfile -> [files]

        sub_linters = {} # rcfile -> linter

        for path in self._iterate_file_descrs(linter, files_or_modules):
            self.register_linter(path, sub_linter_files)

        for rcfiles in sub_linter_files:
            sub_linter_runner = RunLinter(reversed(rcfiles))

            sublinter, _ = sub_linter_runner.initialize(
                [*self.args], reporters.CollectingReporter()
            )
            sub_linters[rcfiles] = sublinter

        check_parallel(
            linter,
            sub_linters,
            linter.config.jobs,
            (chain.from_iterable(((rcfiles, file) for file in files) for rcfiles, files in sub_linter_files.items())),
            files_or_modules
        )
        linter.generate_reports()

    def run_simple(self, linter, files_or_modules):
        linter.initialize()
        sub_linters = []
        sub_linter_files = defaultdict(list)  # rcfile -> [files]

        with fix_import_path(files_or_modules):
            for path in self._iterate_file_descrs(linter, files_or_modules):
                self.register_linter(path, sub_linter_files)


            for rcfiles, files in sub_linter_files.items():
                sub_linter_runner = RunLinter(reversed(rcfiles))

                sublinter, _ = sub_linter_runner.initialize(
                    [*self.args], reporters.CollectingReporter()
                )

                sublinter._check_files(sublinter.get_ast, files)

                sub_linters.append(sublinter)

        merge_linters(linter, *sub_linters)

        linter.generate_reports()

    def _iterate_file_descrs(
        self, linter, files_or_modules: Sequence[str]
    ) -> Iterator[FileItem]:
        """Return generator yielding file descriptions (tuples of module name, file path, base name).

        The returned generator yield one item for each Python module that should be linted.
        """
        from pylint.typing import FileItem

        for descr in self._expand_files(linter, files_or_modules):
            name, filepath, is_arg = descr["name"], descr["path"], descr["isarg"]
            if linter.should_analyze_file(name, filepath, is_argument=is_arg):
                config_files = tuple(
                    find_per_directory_config_files(Path(filepath).parent)
                )
                yield FileItem(name, filepath, descr["basename"], config_files)

    def _expand_files(
        self, linter, modules: Sequence[str]
    ) -> list[ModuleDescriptionDict]:
        """Get modules and errors from a list of modules and handle errors."""
        from pylint.lint.expand_modules import expand_modules

        result, errors = expand_modules(
            modules,
            linter.config.ignore,
            linter.config.ignore_patterns,
            linter._ignore_paths,
        )
        for error in errors:
            message = modname = error["mod"]
            key = error["key"]
            linter.set_current_module(modname)
            if key == "fatal":
                message = str(error["ex"]).replace(os.getcwd() + os.sep, "")
            linter.add_message(key, args=message)
        return result

    def register_linter(self, path, sub_linter_files):
        # if path.rc_conf[0] != Path(self._rcfiles[0]):
        sub_linter_files[path.rc_conf].append(path)
        # else:
        #     self.root_linter_files.append(path)

    @staticmethod
    def _discover_files(files_or_modules: Sequence[str]) -> Iterator[str]:
        """Discover python modules and packages in subdirectory.

        Returns iterator of paths to discovered modules and packages.
        """
        for something in files_or_modules:
            if os.path.isdir(something) and not os.path.isfile(
                os.path.join(something, "__init__.py")
            ):
                skip_subtrees: List[str] = []
                for root, _, files in os.walk(something):
                    if any(root.startswith(s) for s in skip_subtrees):
                        # Skip subtree of already discovered package.
                        continue
                    if "__init__.py" in files:
                        skip_subtrees.append(root)
                        yield root
                    else:
                        yield from (
                            os.path.join(root, file)
                            for file in files
                            if file.endswith(".py")
                        )
            else:
                yield something


class Run:
    def __init__(
        self,
        args,
        reporter=None,
        exit=True,
        do_exit=UNUSED_PARAM_SENTINEL,
    ):  # pylint: disable=redefined-builtin

        self.root_linter_runner = RunLinter()
        root_linter, files_or_modules = self.root_linter_runner.initialize(
            [*args], reporter
        )
        self.root_linter_runner.initialize_jobs(root_linter)

        self.root_linter_runner.run(
            root_linter,
            files_or_modules,
            exit=False,
        )




