# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import io
import os
import sys
import warnings
from collections import defaultdict
from typing import Iterator, Sequence, List
from pathlib import Path

from pylint import config
from pylint.config.callback_actions import (
    _DoNothingAction,
    _ErrorsOnlyModeAction,
    _FullDocumentationAction,
    _GenerateConfigFileAction,
    _GenerateRCFileAction,
    _ListCheckGroupsAction,
    _ListConfidenceLevelsAction,
    _ListExtensionsAction,
    _ListMessagesAction,
    _ListMessagesEnabledAction,
    _LongHelpAction,
    _MessageHelpAction,
)
from pylint.config.config_initialization import _config_initialization
from pylint.config.exceptions import ArgumentPreprocessingError
from pylint.config.utils import _preprocess_options
from pylint.lint.pylinter import PyLinter

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

    def __init__(self, rcfile=None):
        self._rcfile = rcfile
        self._output = None
        self._version_asked = False
        self._plugins = []
        self.verbose = None

    def initialize(
        self,
        args,
        reporter=None,
    ):  # pylint: disable=redefined-builtin
        try:
            args = _preprocess_options(self, args)
        except ArgumentPreprocessingError as ex:
            print(ex, file=sys.stderr)
            sys.exit(32)

        # Determine configuration file
        if self._rcfile is None:
            self._rcfile = next(config.find_default_config_files(), None)

        self.linter = linter = self.LinterClass(
            (
                (
                    "rcfile",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "group": "Commands",
                        "help": "Specify a configuration file to load.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "output",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "group": "Commands",
                        "help": "Specify an output file.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "init-hook",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "help": "Python code to execute, usually for sys.path "
                        "manipulation such as pygtk.require().",
                    },
                ),
                (
                    "help-msg",
                    {
                        "action": _MessageHelpAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Display a help message for the given message id and "
                        "exit. The value may be a comma separated list of message ids.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "list-msgs",
                    {
                        "action": _ListMessagesAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Display a list of all pylint's messages divided by whether "
                        "they are emittable with the given interpreter.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "list-msgs-enabled",
                    {
                        "action": _ListMessagesEnabledAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Display a list of what messages are enabled, "
                        "disabled and non-emittable with the given configuration.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "list-groups",
                    {
                        "action": _ListCheckGroupsAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "List pylint's message groups.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "list-conf-levels",
                    {
                        "action": _ListConfidenceLevelsAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Generate pylint's confidence levels.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "list-extensions",
                    {
                        "action": _ListExtensionsAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "List available extensions.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "full-documentation",
                    {
                        "action": _FullDocumentationAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Generate pylint's full documentation.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "generate-rcfile",
                    {
                        "action": _GenerateRCFileAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Generate a sample configuration file according to "
                        "the current configuration. You can put other options "
                        "before this one to get them in the generated "
                        "configuration.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "generate-toml-config",
                    {
                        "action": _GenerateConfigFileAction,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Generate a sample configuration file according to "
                        "the current configuration. You can put other options "
                        "before this one to get them in the generated "
                        "configuration. The config is in the .toml format.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "errors-only",
                    {
                        "action": _ErrorsOnlyModeAction,
                        "kwargs": {"Run": self},
                        "short": "E",
                        "help": "In error mode, checkers without error messages are "
                        "disabled and for others, only the ERROR messages are "
                        "displayed, and no reports are done by default.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "verbose",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "short": "v",
                        "help": "In verbose mode, extra non-checker-related info "
                        "will be displayed.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "enable-all-extensions",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "help": "Load and enable all available extensions. "
                        "Use --list-extensions to see a list all available extensions.",
                        "hide_from_config_file": True,
                    },
                ),
                (
                    "long-help",
                    {
                        "action": _LongHelpAction,
                        "kwargs": {"Run": self},
                        "help": "Show more verbose help.",
                        "group": "Commands",
                        "hide_from_config_file": True,
                    },
                ),
            ),
            option_groups=self.option_groups,
            pylintrc=self._rcfile,
        )
        # register standard checkers
        linter.load_default_plugins()
        # load command line plugins
        linter.load_plugin_modules(self._plugins)

        linter.disable("I")
        linter.enable("c-extension-no-member")

        args = _config_initialization(
            linter, args, reporter, config_file=self._rcfile, verbose_mode=self.verbose
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
        self, linter: PyLinter, args: list, do_exit, exit: bool
    ) -> None:  # pylint: disable=redefined-builtin
        if self._output:
            try:
                with open(self._output, "w", encoding="utf-8") as output:
                    linter.reporter.out = output
                    linter.check(args)
                    score_value = linter.generate_reports()
            except OSError as ex:
                print(ex, file=sys.stderr)
                sys.exit(32)
        else:
            output = io.StringIO()
            linter.reporter.out = output
            linter.check(args)
            score_value = linter.generate_reports()
            print(output.getvalue())

        if do_exit is not UNUSED_PARAM_SENTINEL:
            warnings.warn(
                "do_exit is deprecated and it is going to be removed in a future version.",
                DeprecationWarning,
            )
            exit = do_exit

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


class RunSubLinter(RunLinter):
    def cb_set_rcfile(self, name, value):
        # Sublinter ignores rcfile option from CLI
        pass


class Run:
    def __init__(
        self,
        args,
        reporter=None,
        exit=True,
        do_exit=UNUSED_PARAM_SENTINEL,
    ):  # pylint: disable=redefined-builtin

        self.sub_linter_files = defaultdict(list)  # rcfile -> [files]
        self.root_linter_files = []

        self.root_linter_runner = RunLinter()
        root_linter, files_or_modules = self.root_linter_runner.initialize(
            [*args], reporter
        )
        self.root_linter_runner.initialize_jobs(root_linter)

        if root_linter.config.recursive is True:
            files_or_modules = tuple(self._discover_files(files_or_modules))

        for path in files_or_modules:
            self.register_linter(path)

        self.root_linter_runner.run(
            root_linter, self.root_linter_files, do_exit, exit=False
        )

        for rcfile, files in self.sub_linter_files.items():
            sub_linter_runner = RunSubLinter(rcfile)

            sublinter, _ = sub_linter_runner.initialize([*args], reporter)

            sub_linter_runner.initialize_jobs(sublinter)
            sub_linter_runner.run(sublinter, files, do_exit, exit=False)

    def register_linter(self, path):
        rcfile = self._search_rcfile(path)
        if rcfile:
            self.sub_linter_files[rcfile].append(path)
        else:
            self.root_linter_files.append(path)

    def _search_rcfile(self, path):
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        while True:
            rcfile = os.path.join(path, ".pylintrc")
            if os.path.exists(rcfile):
                return rcfile
            path = os.path.dirname(path)
            if path in ("/", ""):
                break

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
