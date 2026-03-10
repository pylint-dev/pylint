# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Configuration file parser class."""

from __future__ import annotations

import argparse
import configparser
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pylint.config.utils import _parse_rich_type_value

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

if TYPE_CHECKING:
    from pylint.lint import PyLinter

PylintConfigFileData = tuple[dict[str, str], list[str]]


class _RawConfParser:
    """Class to parse various formats of configuration files."""

    @staticmethod
    def parse_ini_file(file_path: Path) -> PylintConfigFileData:
        """Parse and handle errors of an ini configuration file.

        Raises ``configparser.Error``.
        """
        parser = configparser.ConfigParser(inline_comment_prefixes=("#", ";"))
        # Use this encoding in order to strip the BOM marker, if any.
        with open(file_path, encoding="utf_8_sig") as fp:
            parser.read_file(fp)

        config_content: dict[str, str] = {}
        options: list[str] = []
        ini_file_with_sections = _RawConfParser._ini_file_with_sections(file_path)
        for section in parser.sections():
            if ini_file_with_sections and not section.startswith("pylint"):
                continue
            for option, value in parser[section].items():
                config_content[option] = value
                options += [f"--{option}", value]
        return config_content, options

    @staticmethod
    def _ini_file_with_sections(file_path: Path) -> bool:
        """Return whether the file uses sections."""
        if "setup.cfg" in file_path.parts:
            return True
        if "tox.ini" in file_path.parts:
            return True
        return False

    @staticmethod
    def parse_toml_file(file_path: Path) -> PylintConfigFileData:
        """Parse and handle errors of a toml configuration file.

        Raises ``tomllib.TOMLDecodeError``.
        """
        with open(file_path, mode="rb") as fp:
            content = tomllib.load(fp)
        try:
            sections_values = content["tool"]["pylint"]
        except KeyError:
            return {}, []

        config_content: dict[str, str] = {}
        options: list[str] = []
        for opt, values in sections_values.items():
            if isinstance(values, dict):
                for config, value in values.items():
                    value = _parse_rich_type_value(value)
                    config_content[config] = value
                    options += [f"--{config}", value]
            else:
                values = _parse_rich_type_value(values)
                config_content[opt] = values
                options += [f"--{opt}", values]
        return config_content, options

    @staticmethod
    def parse_config_file(
        file_path: Path | None, verbose: bool
    ) -> PylintConfigFileData:
        """Parse a config file and return str-str pairs.

        Raises ``tomllib.TOMLDecodeError``, ``configparser.Error``.
        """
        if file_path is None:
            if verbose:
                print(
                    "No config file found, using default configuration", file=sys.stderr
                )
            return {}, []

        file_path = Path(os.path.expandvars(file_path)).expanduser()
        if not file_path.exists():
            raise OSError(f"The config file {file_path} doesn't exist!")

        if verbose:
            print(f"Using config file {file_path}", file=sys.stderr)

        if file_path.suffix == ".toml":
            return _RawConfParser.parse_toml_file(file_path)
        return _RawConfParser.parse_ini_file(file_path)


class _ConfigurationFileParser:
    """Class to parse various formats of configuration files."""

    def __init__(self, verbose: bool, linter: PyLinter) -> None:
        self.verbose_mode = verbose
        self.linter = linter

    def _fix_store_true_options(self, options: list[str]) -> list[str]:
        """Fix boolean values for store_true argparse actions.

        TOML files can express boolean values natively (true/false). When these
        are converted to strings and passed as ["--flag", "True"/"False"],
        argparse store_true actions ignore the value and always set True just
        from the flag's presence. This method removes the stringified value for
        store_true options, and drops the flag entirely when the value is False.
        """
        # Build a set of store_true option names from the linter's arg parser
        store_true_options: set[str] = set()
        for action in self.linter._arg_parser._actions:
            if isinstance(action, argparse._StoreTrueAction):
                store_true_options.update(action.option_strings)

        fixed: list[str] = []
        i = 0
        while i < len(options):
            opt = options[i]
            if opt in store_true_options and i + 1 < len(options):
                value = options[i + 1].lower()
                if value in ("true", "1", "yes"):
                    fixed.append(opt)
                # When False, omit the flag entirely so argparse uses the default.
                i += 2  # Skip the value in either case
            else:
                fixed.append(opt)
                i += 1
        return fixed

    def parse_config_file(self, file_path: Path | None) -> PylintConfigFileData:
        """Parse a config file and return str-str pairs."""
        try:
            config_content, options = _RawConfParser.parse_config_file(
                file_path, self.verbose_mode
            )
            options = self._fix_store_true_options(options)
            return config_content, options
        except (configparser.Error, tomllib.TOMLDecodeError) as e:
            self.linter.add_message("config-parse-error", line=0, args=str(e))
            return {}, []
