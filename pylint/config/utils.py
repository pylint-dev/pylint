# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Utils for arguments/options parsing and handling."""


from typing import Any, Dict, Union

from pylint.config.argument import _Argument, _CallableArgument, _StoreTrueArgument
from pylint.config.callback_actions import _CallbackAction


def _convert_option_to_argument(
    opt: str, optdict: Dict[str, Any]
) -> Union[_Argument, _StoreTrueArgument, _CallableArgument]:
    """Convert an optdict to an Argument class instance."""
    # pylint: disable-next=fixme
    # TODO: Do something with the 'group', 'level' and 'hide' keys of optdicts

    # pylint: disable-next=fixme
    # TODO: Do something with the 'dest' key and deprecation of options

    # Get the long and short flags
    flags = [f"--{opt}"]
    if "short" in optdict:
        flags += [f"-{optdict['short']}"]

    # Get the action type
    action = optdict.get("action", "store")

    # pylint: disable-next=fixme
    # TODO: Remove this handling after we have deprecated multiple-choice arguments
    choices = optdict.get("choices", None)
    if opt == "confidence":
        choices = None

    if action == "store_true":
        return _StoreTrueArgument(
            flags=flags,
            action=action,
            default=optdict["default"],
            arg_help=optdict["help"],
        )
    if not isinstance(action, str) and issubclass(action, _CallbackAction):
        return _CallableArgument(
            flags=flags,
            action=action,
            arg_help=optdict["help"],
            kwargs=optdict["kwargs"],
        )
    return _Argument(
        flags=flags,
        action=action,
        default=optdict["default"],
        arg_type=optdict["type"],
        choices=choices,
        arg_help=optdict["help"],
        metavar=optdict["metavar"],
    )


def _parse_rich_type_value(value: Any) -> str:
    """Parse rich (toml) types into strings."""
    if isinstance(value, (list, tuple)):
        return ",".join(value)
    return str(value)
