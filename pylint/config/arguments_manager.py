# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Arguments manager class used to handle command-line arguments and options."""

import argparse
import collections
import configparser
import copy
import optparse  # pylint: disable=deprecated-module
import os
import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TextIO, Tuple, Union

from pylint import utils
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
from pylint.config.option import Option
from pylint.config.option_parser import OptionParser
from pylint.config.options_provider_mixin import OptionsProviderMixIn
from pylint.config.utils import _convert_option_to_argument
from pylint.constants import MAIN_CHECKER_NAME
from pylint.typing import OptionDict

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

if sys.version_info <= (3, 7, 1):
    from typing_extensions import OrderedDict
else:
    from typing import OrderedDict

if TYPE_CHECKING:
    from pylint.config.arguments_provider import _ArgumentsProvider

ConfigProvider = Union["_ArgumentsProvider", OptionsProviderMixIn]


# pylint: disable-next=too-many-instance-attributes
class _ArgumentsManager:
    """Arguments manager class used to handle command-line arguments and options."""

    def __init__(self, prog: str, usage: Optional[str] = None) -> None:
        self.namespace = argparse.Namespace()
        """Namespace for all options."""

        self._arg_parser = argparse.ArgumentParser(
            prog=prog,
            usage=usage or "%(prog)s [options]",
            formatter_class=_HelpFormatter,
        )
        """The command line argument parser."""

        self._argument_groups_dict: Dict[str, argparse._ArgumentGroup] = {}
        """Dictionary of all the argument groups."""

        self._option_dicts: Dict[str, OptionDict] = {}
        """All option dictionaries that have been registered."""

        # pylint: disable=fixme
        # TODO: Optparse: Added to keep API parity with OptionsManger
        # They should be removed/deprecated when refactoring the copied methods
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.reset_parsers(usage or "")
        # list of registered options providers
        self.options_providers: List[ConfigProvider] = []
        # dictionary associating option name to checker
        self._all_options: OrderedDict[str, ConfigProvider] = collections.OrderedDict()
        self._short_options: Dict[str, str] = {}
        self._nocallback_options: Dict[ConfigProvider, str] = {}
        self._mygroups: Dict[str, optparse.OptionGroup] = {}
        # verbosity
        self._maxlevel: int = 0

    def _register_options_provider(self, provider: "_ArgumentsProvider") -> None:
        """Register an options provider and load its defaults."""
        for opt, optdict in provider.options:
            self._option_dicts[opt] = optdict
            argument = _convert_option_to_argument(opt, optdict)
            section = argument.section or provider.name.capitalize()

            section_desc = provider.option_groups_descs.get(section, None)

            # We exclude master since its docstring comes from PyLinter
            if provider.name != MAIN_CHECKER_NAME and provider.__doc__:
                section_desc = provider.__doc__.split("\n\n")[0]

            self._add_arguments_to_parser(section, section_desc, argument)

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

    def _parse_configuration_file(self, arguments: List[str]) -> None:
        """Parse the arguments found in a configuration file into the namespace."""
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

    def reset_parsers(self, usage: str = "") -> None:
        """DEPRECATED."""
        warnings.warn(
            "reset_parsers has been deprecated. Parsers should be instantiated "
            "once during initialization and do not need to be reset.",
            DeprecationWarning,
        )
        # configuration file parser
        self.cfgfile_parser = configparser.ConfigParser(
            inline_comment_prefixes=("#", ";")
        )
        # command line parser
        self.cmdline_parser = OptionParser(Option, usage=usage)
        self.cmdline_parser.options_manager = self  # type: ignore[attr-defined]
        self._optik_option_attrs = set(self.cmdline_parser.option_class.ATTRS)

    def register_options_provider(
        self, provider: ConfigProvider, own_group: bool = True
    ) -> None:
        """DEPRECATED: Register an options provider."""
        warnings.warn(
            "register_options_provider has been deprecated. Options providers and "
            "arguments providers should be registered by initializing ArgumentsProvider. "
            "This automatically registers the provider on the ArgumentsManager.",
            DeprecationWarning,
        )
        self.options_providers.append(provider)
        non_group_spec_options = [
            option for option in provider.options if "group" not in option[1]
        ]
        groups = getattr(provider, "option_groups", ())
        if own_group and non_group_spec_options:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                self.add_option_group(
                    provider.name.upper(),
                    provider.__doc__,
                    non_group_spec_options,
                    provider,
                )
        else:
            for opt, optdict in non_group_spec_options:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=DeprecationWarning)
                    self.add_optik_option(provider, self.cmdline_parser, opt, optdict)
        for gname, gdoc in groups:
            gname = gname.upper()
            goptions = [
                option
                for option in provider.options
                if option[1].get("group", "").upper() == gname  # type: ignore[union-attr]
            ]
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                self.add_option_group(gname, gdoc, goptions, provider)

    def add_option_group(
        self,
        group_name: str,
        _: Optional[str],
        options: List[Tuple[str, OptionDict]],
        provider: ConfigProvider,
    ) -> None:
        """DEPRECATED."""
        warnings.warn(
            "add_option_group has been deprecated. Option groups should be "
            "registered by initializing ArgumentsProvider. "
            "This automatically registers the group on the ArgumentsManager.",
            DeprecationWarning,
        )
        # add option group to the command line parser
        if group_name in self._mygroups:
            group = self._mygroups[group_name]
        else:
            group = optparse.OptionGroup(
                self.cmdline_parser, title=group_name.capitalize()
            )
            self.cmdline_parser.add_option_group(group)
            group.level = provider.level  # type: ignore[attr-defined]
            self._mygroups[group_name] = group
            # add section to the config file
            if (
                group_name != "DEFAULT"
                and group_name not in self.cfgfile_parser._sections  # type: ignore[attr-defined]
            ):
                self.cfgfile_parser.add_section(group_name)
        # add provider's specific options
        for opt, optdict in options:
            if not isinstance(optdict.get("action", "store"), str):
                optdict["action"] = "callback"
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                self.add_optik_option(provider, group, opt, optdict)

    def add_optik_option(
        self,
        provider: ConfigProvider,
        optikcontainer: Union[optparse.OptionParser, optparse.OptionGroup],
        opt: str,
        optdict: OptionDict,
    ) -> None:
        """DEPRECATED."""
        warnings.warn(
            "add_optik_option has been deprecated. Options should be automatically "
            "added by initializing an ArgumentsProvider.",
            DeprecationWarning,
        )
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            args, optdict = self.optik_option(provider, opt, optdict)
        option = optikcontainer.add_option(*args, **optdict)
        self._all_options[opt] = provider
        self._maxlevel = max(self._maxlevel, option.level or 0)

    def optik_option(
        self, provider: ConfigProvider, opt: str, optdict: OptionDict
    ) -> Tuple[List[str], OptionDict]:
        """DEPRECATED: Get our personal option definition and return a suitable form for
        use with optik/optparse
        """
        warnings.warn(
            "optik_option has been deprecated. Parsing of option dictionaries should be done "
            "automatically by initializing an ArgumentsProvider.",
            DeprecationWarning,
        )
        optdict = copy.copy(optdict)
        if "action" in optdict:
            self._nocallback_options[provider] = opt
        else:
            optdict["action"] = "callback"
            optdict["callback"] = self.cb_set_provider_option
        # default is handled here and *must not* be given to optik if you
        # want the whole machinery to work
        if "default" in optdict:
            if (
                "help" in optdict
                and optdict.get("default") is not None
                and optdict["action"] not in ("store_true", "store_false")
            ):
                optdict["help"] += " [current: %default]"  # type: ignore[operator]
            del optdict["default"]
        args = ["--" + str(opt)]
        if "short" in optdict:
            self._short_options[optdict["short"]] = opt  # type: ignore[index]
            args.append("-" + optdict["short"])  # type: ignore[operator]
            del optdict["short"]
        # cleanup option definition dict before giving it to optik
        for key in list(optdict.keys()):
            if key not in self._optik_option_attrs:
                optdict.pop(key)
        return args, optdict

    def generate_config(
        self, stream: Optional[TextIO] = None, skipsections: Tuple[str, ...] = ()
    ) -> None:
        """DEPRECATED: Write a configuration file according to the current configuration
        into the given stream or stdout
        """
        warnings.warn(
            "generate_config has been deprecated. It will be removed in pylint 3.0.",
            DeprecationWarning,
        )
        options_by_section: Dict[str, List[Tuple]] = {}
        sections = []
        for provider in self.options_providers:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                for section, options in provider.options_by_section():
                    if section is None:
                        section = provider.name
                    if section in skipsections:
                        continue
                    options = [  # type: ignore[misc]
                        (n, d, v)
                        for (n, d, v) in options
                        if d.get("type") is not None and not d.get("deprecated")
                    ]
                    if not options:
                        continue
                    if section not in sections:
                        sections.append(section)
                    all_options = options_by_section.setdefault(section, [])
                    all_options += options
        stream = stream or sys.stdout
        printed = False
        for section in sections:
            if printed:
                print("\n", file=stream)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                utils.format_section(
                    stream, section.upper(), sorted(options_by_section[section])
                )
            printed = True

    def load_provider_defaults(self) -> None:
        """DEPRECATED: Initialize configuration using default values."""
        warnings.warn(
            "load_provider_defaults has been deprecated. Parsing of option defaults should be done "
            "automatically by initializing an ArgumentsProvider.",
            DeprecationWarning,
        )
        for provider in self.options_providers:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                provider.load_defaults()

    def read_config_file(
        self, config_file: Optional[Path] = None, verbose: bool = False
    ) -> None:
        """DEPRECATED: Read the configuration file but do not load it (i.e. dispatching
        values to each option's provider)

        :raises OSError: Whem the specified config file doesn't exist
        """
        warnings.warn(
            "read_config_file has been deprecated. It will be removed in pylint 3.0.",
            DeprecationWarning,
        )
        if not config_file:
            if verbose:
                print(
                    "No config file found, using default configuration", file=sys.stderr
                )
            return
        config_file = Path(os.path.expandvars(config_file)).expanduser()
        if not config_file.exists():
            raise OSError(f"The config file {str(config_file)} doesn't exist!")
        parser = self.cfgfile_parser
        if config_file.suffix == ".toml":
            try:
                self._parse_toml(config_file, parser)
            except tomllib.TOMLDecodeError:
                pass
        else:
            # Use this encoding in order to strip the BOM marker, if any.
            with open(config_file, encoding="utf_8_sig") as fp:
                parser.read_file(fp)
            # normalize each section's title
            for sect, values in list(parser._sections.items()):  # type: ignore[attr-defined]
                if sect.startswith("pylint."):
                    sect = sect[len("pylint.") :]
                if not sect.isupper() and values:
                    parser._sections[sect.upper()] = values  # type: ignore[attr-defined]

        if verbose:
            print(f"Using config file '{config_file}'", file=sys.stderr)

    def _parse_toml(self, config_file: Path, parser: configparser.ConfigParser) -> None:
        """DEPRECATED: Parse and handle errors of a toml configuration file.

        TODO: Remove after read_config_file has been removed.
        """
        with open(config_file, mode="rb") as fp:
            content = tomllib.load(fp)
        try:
            sections_values = content["tool"]["pylint"]
        except KeyError:
            return
        for section, values in sections_values.items():
            section_name = section.upper()
            # TOML has rich types, convert values to
            # strings as ConfigParser expects.
            if not isinstance(values, dict):
                # This class is a mixin: add_message comes from the `PyLinter` class
                self.add_message(  # type: ignore[attr-defined] # pylint: disable=no-member
                    "bad-configuration-section", line=0, args=(section, values)
                )
                continue
            for option, value in values.items():
                if isinstance(value, bool):
                    values[option] = "yes" if value else "no"
                elif isinstance(value, list):
                    values[option] = ",".join(value)
                else:
                    values[option] = str(value)
            for option, value in values.items():
                try:
                    parser.set(section_name, option, value=value)
                except configparser.NoSectionError:
                    parser.add_section(section_name)
                    parser.set(section_name, option, value=value)

    def load_config_file(self) -> None:
        """DEPRECATED: Dispatch values previously read from a configuration file to each
        option's provider
        """
        warnings.warn(
            "load_config_file has been deprecated. It will be removed in pylint 3.0.",
            DeprecationWarning,
        )
        parser = self.cfgfile_parser
        for section in parser.sections():
            for option, value in parser.items(section):
                try:
                    self.global_set_option(option, value)
                except (KeyError, optparse.OptionError):
                    continue

    def load_configuration(self, **kwargs: Any) -> None:
        """DEPRECATED: Override configuration according to given parameters."""
        warnings.warn(
            "load_configuration has been deprecated. It will be removed in pylint 3.0.",
            DeprecationWarning,
        )
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            return self.load_configuration_from_config(kwargs)

    def load_configuration_from_config(self, config: Dict[str, Any]) -> None:
        warnings.warn(
            "DEPRECATED: load_configuration_from_config has been deprecated. It will be removed in pylint 3.0.",
            DeprecationWarning,
        )
        for opt, opt_value in config.items():
            opt = opt.replace("_", "-")
            provider = self._all_options[opt]
            provider.set_option(opt, opt_value)

    def load_command_line_configuration(
        self, args: Optional[List[str]] = None
    ) -> List[str]:
        """DEPRECATED: Override configuration according to command line parameters.

        return additional arguments
        """
        warnings.warn(
            "load_command_line_configuration has been deprecated. It will be removed in pylint 3.0.",
            DeprecationWarning,
        )
        args = sys.argv[1:] if args is None else list(args)
        (options, args) = self.cmdline_parser.parse_args(args=args)
        for provider in self._nocallback_options:
            config = provider.config
            for attr in config.__dict__.keys():
                value = getattr(options, attr, None)
                if value is None:
                    continue
                setattr(config, attr, value)
        return args

    def help(self, level: Optional[int] = None) -> str:
        """Return the usage string based on the available options."""
        if level is not None:
            warnings.warn(
                "Supplying a 'level' argument to help() has been deprecated."
                "You can call help() without any arguments.",
                DeprecationWarning,
            )
        return self._arg_parser.format_help()

    # pylint: disable-next=fixme
    # TODO: Optparse: Refactor and potentially deprecate cb_set_provider_option
    def cb_set_provider_option(self, option, opt, value, parser):
        """Optik callback for option setting."""
        if opt.startswith("--"):
            # remove -- on long option
            opt = opt[2:]
        else:
            # short option, get its long equivalent
            opt = self._short_options[opt[1:]]
        # trick since we can't set action='store_true' on options
        if value is None:
            value = 1
        self.global_set_option(opt, value)

    # pylint: disable-next=fixme
    # TODO: Optparse: Refactor and potentially deprecate global_set_option
    def global_set_option(self, opt, value):
        """Set option on the correct option provider."""
        self._all_options[opt].set_option(opt, value)
