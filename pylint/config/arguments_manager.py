# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Arguments manager class used to handle command-line arguments and options."""

import argparse
from typing import TYPE_CHECKING, Dict, List

from pylint.config.argument import _Argument
from pylint.config.exceptions import UnrecognizedArgumentAction
from pylint.config.utils import _convert_option_to_argument

if TYPE_CHECKING:
    from pylint import checkers


class _ArgumentsManager:
    """Arguments manager class used to handle command-line arguments and options."""

    def __init__(self) -> None:
        self.namespace = argparse.Namespace()
        """Namespace for all options."""

        self._arg_parser = argparse.ArgumentParser(prog="pylint", allow_abbrev=False)
        """The command line argument parser."""

        self._argument_groups_dict: Dict[str, argparse._ArgumentGroup] = {}
        """Dictionary of all the argument groups."""

    def _register_options_provider(self, provider: "checkers.BaseChecker") -> None:
        """Register an options provider and load its defaults."""
        # pylint: disable-next=fixme
        # TODO: Do something own_group parameter (see OptionsManagerMixIn.register_options_provider)
        for opt, optdict in provider.options:
            argument = _convert_option_to_argument(opt, optdict)
            self._add_arguments_to_parser(provider.name, argument)

        # pylint: disable-next=fixme
        # TODO: Do something with option groups within optdicts (see OptionsManagerMixIn.register_options_provider)

        # pylint: disable-next=fixme
        # TODO: Investigate performance impact of loading default arguments on every call
        self._load_default_argument_values()

    def _add_arguments_to_parser(self, section: str, argument: _Argument) -> None:
        """Iterates over all argument sections and add them to the parser object."""
        try:
            section_group = self._argument_groups_dict[section]
        except KeyError:
            section_group = self._arg_parser.add_argument_group(title=section)
            self._argument_groups_dict[section] = section_group
        self._add_parser_option(section_group, argument)

    @staticmethod
    def _add_parser_option(
        section_group: argparse._ArgumentGroup, argument: _Argument
    ) -> None:
        """Add an argument."""
        if argument.action == "store":
            section_group.add_argument(
                *argument.flags,
                action=argument.action,
                default=argument.default,
                type=argument.type,  # type: ignore[arg-type] # incorrect typing in typeshed
                help=argument.help,
                metavar=argument.metavar,
                choices=argument.choices,
            )
        else:
            raise UnrecognizedArgumentAction

    def _load_default_argument_values(self) -> None:
        """Loads the default values of all registered options."""
        self.namespace = self._arg_parser.parse_args([], self.namespace)

    def _parse_configuration_file(self, config_data: Dict[str, str]) -> None:
        """Parse the arguments found in a configuration file into the namespace."""
        arguments = []
        for opt, value in config_data.items():
            arguments.extend([f"--{opt}", value])
        # pylint: disable-next=fixme
        # TODO: This should parse_args instead of parse_known_args
        self.namespace = self._arg_parser.parse_known_args(arguments, self.namespace)[0]

    def _parse_command_line_configuration(self, arguments: List[str]) -> None:
        """Parse the arguments found on the command line into the namespace."""
        # pylint: disable-next=fixme
        # TODO: This should parse_args instead of parse_known_args
        self.namespace = self._arg_parser.parse_known_args(arguments, self.namespace)[0]

        # pylint: disable-next=fixme
        # TODO: This should return a list of arguments with the option arguments removed
        # just as PyLinter.load_command_line_configuration does

    def _parse_plugin_configuration(self) -> None:
        # pylint: disable-next=fixme
        # TODO: This is not currently implemented.
        # Perhaps we should also change the name to distuingish it better?
        # See PyLinter.load_plugin_configuration
        pass
