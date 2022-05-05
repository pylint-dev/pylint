# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import os
import pathlib
import pickle
import sys

__all__ = [
    "ConfigurationMixIn",  # Deprecated
    "find_default_config_files",
    "find_pylintrc",  # Deprecated
    "Option",  # Deprecated
    "OptionsManagerMixIn",  # Deprecated
    "OptionParser",  # Deprecated
    "OptionsProviderMixIn",  # Deprecated
    "UnsupportedAction",  # Deprecated
    "PYLINTRC",
    "USER_HOME",  # Compatibility with the old API
    "PYLINT_HOME",  # Compatibility with the old API
]

from pylint.config.arguments_provider import UnsupportedAction
from pylint.config.configuration_mixin import ConfigurationMixIn
from pylint.config.environment_variable import PYLINTRC
from pylint.config.find_default_config_files import (
    find_default_config_files,
    find_pylintrc,
)
from pylint.config.option import Option
from pylint.config.option_manager_mixin import OptionsManagerMixIn
from pylint.config.option_parser import OptionParser
from pylint.config.options_provider_mixin import OptionsProviderMixIn
from pylint.constants import PYLINT_HOME, USER_HOME
from pylint.utils import LinterStats


def _get_pdata_path(base_name: str, recurs: int) -> pathlib.Path:
    base_name = base_name.replace(os.sep, "_")
    return pathlib.Path(PYLINT_HOME) / f"{base_name}{recurs}.stats"


def load_results(base: str) -> LinterStats | None:
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, "rb") as stream:
            data = pickle.load(stream)
            if not isinstance(data, LinterStats):
                raise TypeError
            return data
    except Exception:  # pylint: disable=broad-except
        return None


def save_results(results: LinterStats, base: str) -> None:
    if not os.path.exists(PYLINT_HOME):
        try:
            os.makedirs(PYLINT_HOME)
        except OSError:
            print(f"Unable to create directory {PYLINT_HOME}", file=sys.stderr)
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, "wb") as stream:
            pickle.dump(results, stream)
    except OSError as ex:
        print(f"Unable to create file {data_file}: {ex}", file=sys.stderr)
