# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import configparser
import os
from pathlib import Path
from typing import Generator, List, Union

import toml
from toml.decoder import TomlDecodeError


def _toml_has_config(path):
    with open(path) as toml_handle:
        try:
            content = toml.load(toml_handle)
        except TomlDecodeError as error:
            print("Failed to load '{}': {}".format(path, str(error)))
            return False

        try:
            content["tool"]["pylint"]
        except KeyError:
            return False

    return True


def _cfg_has_config(path):
    parser = configparser.ConfigParser()
    parser.read(path)
    return any(section.startswith("pylint.") for section in parser.sections())


def _get_config_paths(curdir: Union[Path, str]) -> List[str]:
    paths = []
    config_names = ("pylintrc", ".pylintrc", "pyproject.toml", "setup.cfg")
    for config_name in config_names:
        config_path = os.path.join(curdir, config_name)
        if os.path.isfile(config_path):
            if config_name.endswith(".toml") and not _toml_has_config(config_path):
                continue
            if config_name.endswith(".cfg") and not _cfg_has_config(config_path):
                continue

            paths.append(config_path)

    return paths


def find_default_config_files() -> Generator:
    """Find all possible config files."""
    yield from _get_config_paths(os.path.abspath("."))

    if os.path.isfile("__init__.py"):
        curdir = os.path.abspath(os.getcwd())
        while os.path.isfile(os.path.join(curdir, "__init__.py")):
            curdir = os.path.abspath(os.path.join(curdir, ".."))
            yield from _get_config_paths(curdir)

    if "PYLINTRC" in os.environ and os.path.exists(os.environ["PYLINTRC"]):
        if os.path.isfile(os.environ["PYLINTRC"]):
            yield os.environ["PYLINTRC"]

    user_home = os.path.expanduser("~")
    if user_home not in ("~", "/root"):
        yield from _get_config_paths(user_home)
        yield from _get_config_paths(os.path.join(user_home, ".config"))

    curdir = os.path.abspath("/etc")
    yield from _get_config_paths(curdir)
