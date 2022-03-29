# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Definition of an Argument class and validators for various argument types.

An Argument instance represents a pylint option to be handled by an argparse.ArgumentParser
"""


from typing import Any, Callable, Dict, List, Optional, Union

from pylint import utils as pylint_utils

_ArgumentTypes = Union[str, List[str]]
"""List of possible argument types."""


def _csv_validator(value: Union[str, List[str]]) -> List[str]:
    """Validates a comma separated string."""
    return pylint_utils._check_csv(value)


_ASSIGNMENT_VALIDATORS: Dict[str, Callable[[Any], _ArgumentTypes]] = {
    "choice": str,
    "csv": _csv_validator,
}
"""Validators for all assignment types."""


class _Argument:
    """Class representing an argument to be passed by an argparse.ArgumentsParser.

    This is based on the parameters passed to argparse.ArgumentsParser.add_message.
    See:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
    """

    def __init__(
        self,
        flags: List[str],
        action: str,
        default: _ArgumentTypes,
        arg_type: str,
        choices: Optional[List[str]],
        arg_help: str,
        metavar: str,
    ) -> None:
        self.flags = flags
        """The name of the argument."""

        self.action = action
        """The action to perform with the argument."""

        self.type = _ASSIGNMENT_VALIDATORS[arg_type]
        """A validator function that returns and checks the type of the argument."""

        self.default = self.type(default)
        """The default value of the argument."""

        self.choices = choices
        """A list of possible choices for the argument.

        None if there are no restrictions.
        """

        # argparse uses % formatting on help strings, so a % needs to be escaped
        self.help = arg_help.replace("%", "%%")
        """The description of the argument."""

        self.metavar = metavar
        """The metavar of the argument.

        See:
        https://docs.python.org/3/library/argparse.html#metavar
        """
