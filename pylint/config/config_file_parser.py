# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Configuration file parser class."""

import configparser
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from pylint.config.utils import _parse_rich_type_value

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class _ConfigurationFileParser:
    """Class to parse various formats of configuration files."""

    def __init__(self, verbose: bool, linter: "PyLinter") -> None:
        self.verbose_mode = verbose
        self.linter = linter

    @staticmethod
    def _parse_ini_file(file_path: Path) -> Tuple[Dict[str, str], List[str]]:
        """Parse and handle errors of a ini configuration file."""
        parser = configparser.ConfigParser(inline_comment_prefixes=("#", ";"))

        # Use this encoding in order to strip the BOM marker, if any.
        with open(file_path, encoding="utf_8_sig") as fp:
            parser.read_file(fp)

        config_content: Dict[str, str] = {}
        options: List[str] = []
        for section in parser.sections():
            for opt, value in parser[section].items():
                config_content[opt] = value
                options += [f"--{opt}", value]
        return config_content, options

    def _parse_toml_file(self, file_path: Path) -> Tuple[Dict[str, str], List[str]]:
        """Parse and handle errors of a toml configuration file."""
        try:
            with open(file_path, mode="rb") as fp:
                content = tomllib.load(fp)
        except tomllib.TOMLDecodeError as e:
            self.linter.add_message("config-parse-error", line=0, args=str(e))
            return {}, []

        try:
            sections_values = content["tool"]["pylint"]
        except KeyError:
            return {}, []

        config_content: Dict[str, str] = {}
        options: List[str] = []
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

    def parse_config_file(
        self, file_path: Optional[Path]
    ) -> Tuple[Dict[str, str], List[str]]:
        """Parse a config file and return str-str pairs."""
        if file_path is None:
            if self.verbose_mode:
                print(
                    "No config file found, using default configuration", file=sys.stderr
                )
            return {}, []

        file_path = Path(os.path.expandvars(file_path)).expanduser()
        if not file_path.exists():
            raise OSError(f"The config file {file_path} doesn't exist!")

        if self.verbose_mode:
            print(f"Using config file {file_path}", file=sys.stderr)

        if file_path.suffix == ".toml":
            return self._parse_toml_file(file_path)
        return self._parse_ini_file(file_path)
