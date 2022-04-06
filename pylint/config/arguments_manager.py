# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Arguments manager class used to handle command-line arguments and options."""

import argparse
import sys
from typing import TYPE_CHECKING, Dict, List, Optional

from pylint.config.argument import (
    _Argument,
    _CallableArgument,
    _StoreArgument,
    _StoreNewNamesArgument,
    _StoreOldNamesArgument,
    _StoreTrueArgument,
)
from pylint.config.exceptions import UnrecognizedArgumentAction
from pylint.config.help_formatter import _HelpFormatter
from pylint.config.utils import _convert_option_to_argument

if TYPE_CHECKING:
    from pylint import checkers


class _ArgumentsManager:
    """Arguments manager class used to handle command-line arguments and options."""

    def __init__(self) -> None:
        self.namespace = argparse.Namespace()
        """Namespace for all options."""

        self._arg_parser = argparse.ArgumentParser(
            prog="pylint",
            usage="%(prog)s [options]",
            formatter_class=_HelpFormatter,
        )
        """The command line argument parser."""

        self._argument_groups_dict: Dict[str, argparse._ArgumentGroup] = {}
        """Dictionary of all the argument groups."""

    def _register_options_provider(self, provider: "checkers.BaseChecker") -> None:
        """Register an options provider and load its defaults."""
        for opt, optdict in provider.options:
            argument = _convert_option_to_argument(opt, optdict)
            section = argument.section or provider.name.capitalize()

            # pylint: disable-next=fixme
            # TODO: Optparse: Always define option_groups_descs on ArgumentsProvider
            section_desc = None
            if hasattr(provider, "option_groups_descs"):
                section_desc = provider.option_groups_descs.get(section, None)  # type: ignore[attr-defined]
            self._add_arguments_to_parser(section, section_desc, argument)

        # pylint: disable-next=fixme
        # TODO: Investigate performance impact of loading default arguments on every call
        self._load_default_argument_values()

    def _add_arguments_to_parser(
        self, section: str, section_desc: Optional[str], argument: _Argument
    ) -> None:
        """Add an argument to the correct argument section/group."""
        try:
            section_group = self._argument_groups_dict[section]
        except KeyError:
            if section_desc:
                section_group = self._arg_parser.add_argument_group(
                    section, section_desc
                )
            else:
                section_group = self._arg_parser.add_argument_group(title=section)
            self._argument_groups_dict[section] = section_group
        self._add_parser_option(section_group, argument)

    @staticmethod
    def _add_parser_option(
        section_group: argparse._ArgumentGroup, argument: _Argument
    ) -> None:
        """Add an argument."""
        if isinstance(argument, _StoreArgument):
            section_group.add_argument(
                *argument.flags,
                action=argument.action,
                default=argument.default,
                type=argument.type,  # type: ignore[arg-type] # incorrect typing in typeshed
                help=argument.help,
                metavar=argument.metavar,
                choices=argument.choices,
            )
        elif isinstance(argument, _StoreOldNamesArgument):
            section_group.add_argument(
                *argument.flags,
                **argument.kwargs,
                action=argument.action,
                default=argument.default,
                type=argument.type,  # type: ignore[arg-type] # incorrect typing in typeshed
                help=argument.help,
                metavar=argument.metavar,
                choices=argument.choices,
            )
            # We add the old name as hidden option to make it's default value gets loaded when
            # argparse initializes all options from the checker
            assert argument.kwargs["old_names"]
            for old_name in argument.kwargs["old_names"]:
                section_group.add_argument(
                    f"--{old_name}",
                    action="store",
                    default=argument.default,
                    type=argument.type,  # type: ignore[arg-type] # incorrect typing in typeshed
                    help=argparse.SUPPRESS,
                    metavar=argument.metavar,
                    choices=argument.choices,
                )
        elif isinstance(argument, _StoreNewNamesArgument):
            section_group.add_argument(
                *argument.flags,
                **argument.kwargs,
                action=argument.action,
                default=argument.default,
                type=argument.type,  # type: ignore[arg-type] # incorrect typing in typeshed
                help=argument.help,
                metavar=argument.metavar,
                choices=argument.choices,
            )
        elif isinstance(argument, _StoreTrueArgument):
            section_group.add_argument(
                *argument.flags,
                action=argument.action,
                default=argument.default,
                help=argument.help,
            )
        elif isinstance(argument, _CallableArgument):
            section_group.add_argument(
                *argument.flags,
                **argument.kwargs,
                action=argument.action,
                help=argument.help,
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

    def _parse_command_line_configuration(
        self, arguments: Optional[List[str]] = None
    ) -> List[str]:
        """Parse the arguments found on the command line into the namespace."""
        arguments = sys.argv[1:] if arguments is None else arguments

        self.namespace, parsed_args = self._arg_parser.parse_known_args(
            arguments, self.namespace
        )

        return parsed_args
