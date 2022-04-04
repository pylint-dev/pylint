# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import os
import sys
import warnings
from typing import Optional

from pylint import config, extensions, interfaces
from pylint.config.callback_actions import (
    _DoNothingAction,
    _ErrorsOnlyModeAction,
    _FullDocumentationAction,
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
from pylint.constants import full_version
from pylint.lint.pylinter import PyLinter
from pylint.lint.utils import ArgumentPreprocessingError, preprocess_options
from pylint.utils import utils

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

try:
    import multiprocessing
    from multiprocessing import synchronize  # noqa pylint: disable=unused-import
except ImportError:
    multiprocessing = None  # type: ignore[assignment]


def _cpu_count() -> int:
    """Use sched_affinity if available for virtualized or containerized environments."""
    sched_getaffinity = getattr(os, "sched_getaffinity", None)
    # pylint: disable=not-callable,using-constant-test,useless-suppression
    if sched_getaffinity:
        return len(sched_getaffinity(0))
    if multiprocessing:
        return multiprocessing.cpu_count()
    return 1


def cb_list_extensions(option, optname, value, parser):
    """List all the extensions under pylint.extensions."""

    for filename in os.listdir(os.path.dirname(extensions.__file__)):
        if filename.endswith(".py") and not filename.startswith("_"):
            extension_name, _, _ = filename.partition(".")
            print(f"pylint.extensions.{extension_name}")
    sys.exit(0)


def cb_list_confidence_levels(option, optname, value, parser):
    for level in interfaces.CONFIDENCE_LEVELS:
        print(f"%-18s: {level}")
    sys.exit(0)


def cb_init_hook(optname, value):
    """Execute arbitrary code to set 'sys.path' for instance."""
    exec(value)  # pylint: disable=exec-used


UNUSED_PARAM_SENTINEL = object()


class Run:
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
    def _not_implemented_callback(*args, **kwargs):
        # pylint: disable-next=fixme
        # TODO: Remove after optparse has been deprecated
        raise NotImplementedError

    def __init__(
        self,
        args,
        reporter=None,
        exit=True,
        do_exit=UNUSED_PARAM_SENTINEL,
    ):  # pylint: disable=redefined-builtin
        # Immediately exit if user asks for version
        if "--version" in args:
            print(full_version)
            sys.exit(0)

        self._rcfile: Optional[str] = None
        self._output = None
        self._plugins = []
        self.verbose = None
        try:
            preprocess_options(
                args,
                {
                    # option: (callback, takearg)
                    "init-hook": (cb_init_hook, True),
                    "rcfile": (self.cb_set_rcfile, True),
                    "load-plugins": (self.cb_add_plugins, True),
                    "enable-all-extensions": (self.cb_enable_all_extensions, False),
                    "verbose": (self.cb_verbose_mode, False),
                    "output": (self.cb_set_output, True),
                },
            )
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
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "Specify a configuration file to load.",
                    },
                ),
                (
                    "output",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "Specify an output file.",
                    },
                ),
                (
                    "init-hook",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "callback": Run._not_implemented_callback,
                        "help": "Python code to execute, usually for sys.path "
                        "manipulation such as pygtk.require().",
                    },
                ),
                (
                    "help-msg",
                    {
                        "action": _MessageHelpAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "Display a help message for the given message id and "
                        "exit. The value may be a comma separated list of message ids.",
                    },
                ),
                (
                    "list-msgs",
                    {
                        "action": _ListMessagesAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "Display a list of all pylint's messages divided by whether "
                        "they are emittable with the given interpreter.",
                    },
                ),
                (
                    "list-msgs-enabled",
                    {
                        "action": _ListMessagesEnabledAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "Display a list of what messages are enabled, "
                        "disabled and non-emittable with the given configuration.",
                    },
                ),
                (
                    "list-groups",
                    {
                        "action": _ListCheckGroupsAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "List pylint's message groups.",
                    },
                ),
                (
                    "list-conf-levels",
                    {
                        "action": _ListConfidenceLevelsAction,
                        "callback": Run._not_implemented_callback,
                        "kwargs": {"Run": self},
                        "group": "Commands",
                        "help": "Generate pylint's confidence levels.",
                    },
                ),
                (
                    "list-extensions",
                    {
                        "action": _ListExtensionsAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "List available extensions.",
                    },
                ),
                (
                    "full-documentation",
                    {
                        "action": _FullDocumentationAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "Generate pylint's full documentation.",
                    },
                ),
                (
                    "generate-rcfile",
                    {
                        "action": _GenerateRCFileAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "group": "Commands",
                        "help": "Generate a sample configuration file according to "
                        "the current configuration. You can put other options "
                        "before this one to get them in the generated "
                        "configuration.",
                    },
                ),
                (
                    "errors-only",
                    {
                        "action": _ErrorsOnlyModeAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "short": "E",
                        "help": "In error mode, checkers without error messages are "
                        "disabled and for others, only the ERROR messages are "
                        "displayed, and no reports are done by default.",
                    },
                ),
                (
                    "verbose",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "callback": Run._not_implemented_callback,
                        "short": "v",
                        "help": "In verbose mode, extra non-checker-related info "
                        "will be displayed.",
                    },
                ),
                (
                    "enable-all-extensions",
                    {
                        "action": _DoNothingAction,
                        "kwargs": {},
                        "callback": Run._not_implemented_callback,
                        "help": "Load and enable all available extensions. "
                        "Use --list-extensions to see a list all available extensions.",
                    },
                ),
                (
                    "long-help",
                    {
                        "action": _LongHelpAction,
                        "kwargs": {"Run": self},
                        "callback": Run._not_implemented_callback,
                        "help": "Show more verbose help.",
                        "group": "Commands",
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
            linter.check(args)
            score_value = linter.generate_reports()

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

    def cb_set_rcfile(self, name: Literal["rcfile"], value: str) -> None:
        """Callback for option preprocessing (i.e. before option parsing)."""
        self._rcfile = value

    def cb_set_output(self, name, value):
        """Callback for option preprocessing (i.e. before option parsing)."""
        self._output = value

    def cb_add_plugins(self, name, value):
        """Callback for option preprocessing (i.e. before option parsing)."""
        self._plugins.extend(utils._splitstrip(value))

    def cb_verbose_mode(self, *args, **kwargs):
        self.verbose = True

    def cb_enable_all_extensions(self, option_name: str, value: None) -> None:
        """Callback to load and enable all available extensions."""
        for filename in os.listdir(os.path.dirname(extensions.__file__)):
            if filename.endswith(".py") and not filename.startswith("_"):
                extension_name = f"pylint.extensions.{filename[:-3]}"
                if extension_name not in self._plugins:
                    self._plugins.append(extension_name)
