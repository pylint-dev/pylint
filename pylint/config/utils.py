# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Utils for arguments/options parsing and handling."""


import re
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

from pylint import extensions, utils
from pylint.config.argument import (
    _CallableArgument,
    _StoreArgument,
    _StoreNewNamesArgument,
    _StoreOldNamesArgument,
    _StoreTrueArgument,
)
from pylint.config.callback_actions import _CallbackAction
from pylint.config.exceptions import ArgumentPreprocessingError

if TYPE_CHECKING:
    from pylint.lint.run import Run


def _convert_option_to_argument(
    opt: str, optdict: Dict[str, Any]
) -> Union[
    _StoreArgument,
    _StoreTrueArgument,
    _CallableArgument,
    _StoreOldNamesArgument,
    _StoreNewNamesArgument,
]:
    """Convert an optdict to an Argument class instance."""
    if "level" in optdict and "hide" not in optdict:
        warnings.warn(
            "The 'level' key in optdicts has been deprecated. "
            "Use 'hide' with a boolean to hide an option from the help message.",
            DeprecationWarning,
        )

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
            default=optdict.get("default", True),
            arg_help=optdict.get("help", ""),
            hide_help=optdict.get("hide", False),
            section=optdict.get("group", None),
        )
    if not isinstance(action, str) and issubclass(action, _CallbackAction):
        return _CallableArgument(
            flags=flags,
            action=action,
            arg_help=optdict.get("help", ""),
            kwargs=optdict.get("kwargs", {}),
            hide_help=optdict.get("hide", False),
            section=optdict.get("group", None),
        )
    try:
        default = optdict["default"]
    except KeyError:
        warnings.warn(
            "An option dictionary should have a 'default' key to specify "
            "the option's default value. This key will be required in pylint "
            "3.0. It is not required for 'store_true' and callable actions.",
            DeprecationWarning,
        )
        default = None

    if "kwargs" in optdict:
        if "old_names" in optdict["kwargs"]:
            return _StoreOldNamesArgument(
                flags=flags,
                default=default,
                arg_type=optdict["type"],
                choices=choices,
                arg_help=optdict.get("help", ""),
                metavar=optdict.get("metavar", ""),
                hide_help=optdict.get("hide", False),
                kwargs=optdict.get("kwargs", {}),
                section=optdict.get("group", None),
            )
        if "new_names" in optdict["kwargs"]:
            return _StoreNewNamesArgument(
                flags=flags,
                default=default,
                arg_type=optdict["type"],
                choices=choices,
                arg_help=optdict.get("help", ""),
                metavar=optdict.get("metavar", ""),
                hide_help=optdict.get("hide", False),
                kwargs=optdict.get("kwargs", {}),
                section=optdict.get("group", None),
            )
    if "dest" in optdict:
        return _StoreOldNamesArgument(
            flags=flags,
            default=default,
            arg_type=optdict["type"],
            choices=choices,
            arg_help=optdict.get("help", ""),
            metavar=optdict.get("metavar", ""),
            hide_help=optdict.get("hide", False),
            kwargs={"old_names": [optdict["dest"]]},
            section=optdict.get("group", None),
        )
    return _StoreArgument(
        flags=flags,
        action=action,
        default=default,
        arg_type=optdict["type"],
        choices=choices,
        arg_help=optdict.get("help", ""),
        metavar=optdict.get("metavar", ""),
        hide_help=optdict.get("hide", False),
        section=optdict.get("group", None),
    )


def _parse_rich_type_value(value: Any) -> str:
    """Parse rich (toml) types into strings."""
    if isinstance(value, (list, tuple)):
        return ",".join(value)
    if isinstance(value, re.Pattern):
        return value.pattern
    return str(value)


# pylint: disable-next=unused-argument
def _init_hook(run: "Run", value: Optional[str]) -> None:
    """Execute arbitrary code from the init_hook.

    This can be used to set the 'sys.path' for example.
    """
    assert value is not None
    exec(value)  # pylint: disable=exec-used


def _set_rcfile(run: "Run", value: Optional[str]) -> None:
    """Set the rcfile."""
    assert value is not None
    run._rcfile = value


def _set_output(run: "Run", value: Optional[str]) -> None:
    """Set the output."""
    assert value is not None
    run._output = value


def _add_plugins(run: "Run", value: Optional[str]) -> None:
    """Add plugins to the list of loadable plugins."""
    assert value is not None
    run._plugins.extend(utils._splitstrip(value))


def _set_verbose_mode(run: "Run", value: Optional[str]) -> None:
    assert value is None
    run.verbose = True


def _enable_all_extensions(run: "Run", value: Optional[str]) -> None:
    """Enable all extensions."""
    assert value is None
    for filename in Path(extensions.__file__).parent.iterdir():
        if filename.suffix == ".py" and not filename.stem.startswith("_"):
            extension_name = f"pylint.extensions.{filename.stem}"
            if extension_name not in run._plugins:
                run._plugins.append(extension_name)


PREPROCESSABLE_OPTIONS: Dict[
    str, Tuple[bool, Callable[["Run", Optional[str]], None]]
] = {  # pylint: disable=consider-using-namedtuple-or-dataclass
    "--init-hook": (True, _init_hook),
    "--rcfile": (True, _set_rcfile),
    "--output": (True, _set_output),
    "--load-plugins": (True, _add_plugins),
    "--verbose": (False, _set_verbose_mode),
    "--enable-all-extensions": (False, _enable_all_extensions),
}


def _preprocess_options(run: "Run", args: List[str]) -> List[str]:
    """Preprocess options before full config parsing has started."""
    processed_args: List[str] = []

    i = 0
    while i < len(args):
        argument = args[i]
        if not argument.startswith("--"):
            processed_args.append(argument)
            i += 1
            continue

        try:
            option, value = argument.split("=", 1)
        except ValueError:
            option, value = argument, None

        if option not in PREPROCESSABLE_OPTIONS:
            processed_args.append(argument)
            i += 1
            continue

        takearg, cb = PREPROCESSABLE_OPTIONS[option]

        if takearg and value is None:
            i += 1
            if i >= len(args) or args[i].startswith("-"):
                raise ArgumentPreprocessingError(f"Option {option} expects a value")
            value = args[i]
        elif not takearg and value is not None:
            raise ArgumentPreprocessingError(f"Option {option} doesn't expects a value")

        cb(run, value)
        i += 1

    return processed_args
