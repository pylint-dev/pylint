# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Utils for the 'pylint-config' command."""

from __future__ import annotations

import sys
from collections.abc import Callable

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


SUPPORTED_FORMATS = {"t", "toml", "i", "ini"}


class InvalidUserInput(Exception):
    """Raised whenever a user input is invalid."""

    def __init__(self, valid_input: str, input_value: str, *args: object) -> None:
        self.valid = valid_input
        self.input = input_value
        super().__init__(*args)


def should_retry_after_invalid_input(func: Callable[[], str]) -> Callable[[], str]:
    """Decorator that handles InvalidUserInput exceptions and retries."""

    def inner_function() -> str:
        called_once = False
        while True:
            try:
                return func()
            except InvalidUserInput as exc:
                if called_once and exc.input == "exit()":
                    print("Stopping 'pylint-config'.")
                    sys.exit()
                print(f"Format should be one of {exc.valid}.")
                print("Type 'exit()' if you want to exit the program.")
                called_once = True

    return inner_function


@should_retry_after_invalid_input
def get_and_validate_format() -> Literal["toml", "ini"]:
    """Make sure that the output format is either .toml or .ini."""
    # pylint: disable-next=bad-builtin
    format_type = input(
        "Please choose the format of configuration, (T)oml or (I)ni (.cfg): "
    ).lower()

    if format_type not in SUPPORTED_FORMATS:
        raise InvalidUserInput(", ".join(sorted(SUPPORTED_FORMATS)), format_type)

    if format_type.startswith("t"):
        return "toml"
    return "ini"
