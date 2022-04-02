# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Utils for arguments/options parsing and handling."""


from typing import Any, Dict

from pylint.config.argument import _Argument

IMPLEMENTED_OPTDICT_KEYS = {"action", "default", "type", "choices", "help", "metavar"}
"""This is used to track our progress on accepting all optdict keys."""


def _convert_option_to_argument(opt: str, optdict: Dict[str, Any]) -> _Argument:
    """Convert an optdict to an Argument class instance."""
    # See if the optdict contains any keys we don't yet implement
    # pylint: disable-next=fixme
    # TODO: This should be removed once the migration to argparse is finished
    for key, value in optdict.items():
        if key not in IMPLEMENTED_OPTDICT_KEYS:
            print("Unhandled key found in Argument creation:", key)  # pragma: no cover
            print("It's value is:", value)  # pragma: no cover

    return _Argument(
        flags=[f"--{opt}"],
        action=optdict.get("action", "store"),
        default=optdict["default"],
        arg_type=optdict["type"],
        choices=optdict.get("choices", None),
        arg_help=optdict["help"],
        metavar=optdict["metavar"],
    )


def _parse_rich_type_value(value: Any) -> str:
    """Parse rich (toml) types into strings."""
    if isinstance(value, (list, tuple)):
        return ",".join(value)
    return str(value)
