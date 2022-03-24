# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import sys
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Union

from pylint import reporters
from pylint.utils import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def _config_initialization(
    linter: "PyLinter",
    args_list: List[str],
    reporter: Union[reporters.BaseReporter, reporters.MultiReporter, None] = None,
    config_file: Union[None, str, Path] = None,
    verbose_mode: Optional[bool] = None,
) -> List[str]:
    """Parse all available options, read config files and command line arguments and
    set options accordingly.
    """

    # Read the config file. The parser is stored on linter.cfgfile_parser
    try:
        linter.read_config_file(config_file=config_file, verbose=verbose_mode)
    except OSError as ex:
        print(ex, file=sys.stderr)
        sys.exit(32)
    config_parser = linter.cfgfile_parser

    # Run init hook, if present, before loading plugins
    if config_parser.has_option("MASTER", "init-hook"):
        exec(  # pylint: disable=exec-used
            utils._unquote(config_parser.get("MASTER", "init-hook"))
        )

    # Load plugins if specified in the config file
    if config_parser.has_option("MASTER", "load-plugins"):
        plugins = utils._splitstrip(config_parser.get("MASTER", "load-plugins"))
        linter.load_plugin_modules(plugins)

    # Now we can load file config, plugins (which can
    # provide options) have been registered
    linter.load_config_file()

    if reporter:
        # If a custom reporter is provided as argument, it may be overridden
        # by file parameters, so re-set it here, but before command line
        # parsing, so it's still overridable by command line option
        linter.set_reporter(reporter)

    # Load command line arguments
    try:
        args_list = linter.load_command_line_configuration(args_list)
    except SystemExit as exc:
        if exc.code == 2:  # bad options
            exc.code = 32
        raise

    # args_list should now only be a list of files/directories to lint. All options have
    # been removed from the list
    if not args_list:
        print(linter.help())
        sys.exit(32)

    # We have loaded configuration from config file and command line. Now, we can
    # load plugin specific configuration.
    linter.load_plugin_configuration()

    # Now that plugins are loaded, get list of all fail_on messages, and enable them
    linter.enable_fail_on_messages()

    return args_list
