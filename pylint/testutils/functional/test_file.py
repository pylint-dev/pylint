# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import configparser
import sys
from os.path import basename, exists, join
from typing import Callable, Dict, List, Tuple, Union


def parse_python_version(ver_str: str) -> Tuple[int, ...]:
    """Convert python version to a tuple of integers for easy comparison."""
    return tuple(int(digit) for digit in ver_str.split("."))


class NoFileError(Exception):
    pass


if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class TestFileOptions(TypedDict):
    min_pyver: Tuple[int, ...]
    max_pyver: Tuple[int, ...]
    min_pyver_end_position: Tuple[int, ...]
    requires: List[str]
    except_implementations: List[str]
    exclude_platforms: List[str]


# mypy need something literal, we can't create this dynamically from TestFileOptions
POSSIBLE_TEST_OPTIONS = {
    "min_pyver",
    "max_pyver",
    "min_pyver_end_position",
    "requires",
    "except_implementations",
    "exclude_platforms",
}


class FunctionalTestFile:
    """A single functional test case file with options."""

    _CONVERTERS: Dict[str, Callable[[str], Union[Tuple[int, ...], List[str]]]] = {
        "min_pyver": parse_python_version,
        "max_pyver": parse_python_version,
        "min_pyver_end_position": parse_python_version,
        "requires": lambda s: [i.strip() for i in s.split(",")],
        "except_implementations": lambda s: [i.strip() for i in s.split(",")],
        "exclude_platforms": lambda s: [i.strip() for i in s.split(",")],
    }

    def __init__(self, directory: str, filename: str) -> None:
        self._directory = directory
        self.base = filename.replace(".py", "")
        self.options: TestFileOptions = {
            "min_pyver": (2, 5),
            "max_pyver": (4, 0),
            "min_pyver_end_position": (3, 8),
            "requires": [],
            "except_implementations": [],
            "exclude_platforms": [],
        }
        self._parse_options()

    def __repr__(self) -> str:
        return f"FunctionalTest:{self.base}"

    def _parse_options(self) -> None:
        cp = configparser.ConfigParser()
        cp.add_section("testoptions")
        try:
            cp.read(self.option_file)
        except NoFileError:
            pass

        for name, value in cp.items("testoptions"):
            conv = self._CONVERTERS.get(name, lambda v: v)

            assert (
                name in POSSIBLE_TEST_OPTIONS
            ), f"[testoptions]' can only contains one of {POSSIBLE_TEST_OPTIONS}"
            self.options[name] = conv(value)  # type: ignore[literal-required]

    @property
    def option_file(self) -> str:
        return self._file_type(".rc")

    @property
    def module(self) -> str:
        package = basename(self._directory)
        return ".".join([package, self.base])

    @property
    def expected_output(self) -> str:
        return self._file_type(".txt", check_exists=False)

    @property
    def source(self) -> str:
        return self._file_type(".py")

    def _file_type(self, ext: str, check_exists: bool = True) -> str:
        name = join(self._directory, self.base + ext)
        if not check_exists or exists(name):
            return name
        raise NoFileError(f"Cannot find '{name}'.")
