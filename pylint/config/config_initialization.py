# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, List, Union

from pylint import config, reporters
from pylint.utils import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def _config_initialization(
    linter: "PyLinter",
    args_list: List[str],
    reporter: Union[reporters.BaseReporter, reporters.MultiReporter, None] = None,
    config_file: Union[None, str, Path] = None,
    verbose_mode: bool = False,
) -> List[str]:
    """Parse all available options, read config files and command line arguments and
    set options accordingly.
    """
    config_file = Path(config_file) if config_file else None

    # Set the current module to the configuration file
    # to allow raising messages on the configuration file.
    linter.set_current_module(str(config_file) if config_file else None)

    # Read the configuration file
    config_file_parser = config._ConfigurationFileParser(verbose_mode, linter)
    try:
        config_data, config_args = config_file_parser.parse_config_file(
            file_path=config_file
        )
    except OSError as ex:
        print(ex, file=sys.stderr)
        sys.exit(32)

    # Run init hook, if present, before loading plugins
    if "init-hook" in config_data:
        exec(utils._unquote(config_data["init-hook"]))  # pylint: disable=exec-used

    # Load plugins if specified in the config file
    if "load-plugins" in config_data:
        linter.load_plugin_modules(utils._splitstrip(config_data["load-plugins"]))

    # pylint: disable-next=fixme
    # TODO: Remove everything until set_reporter once the optparse
    # implementation is no longer needed
    # Load optparse command line arguments
    try:
        # The parser is stored on linter.cfgfile_parser
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            linter.read_config_file(config_file=config_file, verbose=verbose_mode)
    except OSError as ex:
        print(ex, file=sys.stderr)
        sys.exit(32)

    # Now we can load file config, plugins (which can
    # provide options) have been registered
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        linter.load_config_file()

    try:
        linter.load_command_line_configuration(args_list)
    except SystemExit as exc:
        if exc.code == 2:  # bad options
            exc.code = 32
        raise

    if reporter:
        # If a custom reporter is provided as argument, it may be overridden
        # by file parameters, so re-set it here, but before command line
        # parsing, so it's still overridable by command line option
        linter.set_reporter(reporter)

    # First we parse any options from a configuration file
    linter._parse_configuration_file(config_args)

    # Second we parse any options from the command line, so they can override
    # the configuration file
    parsed_args_list = linter._parse_command_line_configuration(args_list)

    # We have loaded configuration from config file and command line. Now, we can
    # load plugin specific configuration.
    linter.load_plugin_configuration()

    # parsed_args_list should now only be a list of files/directories to lint.
    # All other options have been removed from the list.
    if not parsed_args_list:
        linter._arg_parser.print_help()
        sys.exit(32)

    # Now that plugins are loaded, get list of all fail_on messages, and enable them
    linter.enable_fail_on_messages()

    linter._parse_error_mode()

    return parsed_args_list
