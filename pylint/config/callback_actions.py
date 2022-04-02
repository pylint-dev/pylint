# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=too-many-arguments

"""Callback actions for various options."""

import abc
import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Sequence, Union

from pylint import extensions, interfaces, utils

if TYPE_CHECKING:
    from pylint.lint.run import Run


class _CallbackAction(argparse.Action):
    """Custom callback action."""

    @abc.abstractmethod
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        raise NotImplementedError


class _DoNothingAction(_CallbackAction):
    """Action that just passes.

    This action is used to allow pre-processing of certain options
    without erroring when they are then processed again by argparse.
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        return None


class _AccessRunObjectAction(_CallbackAction):
    """Action that has access to the Run object."""

    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        nargs: None = None,
        const: None = None,
        default: None = None,
        arg_type: None = None,
        choices: None = None,
        required: bool = False,
        help_msg: str = "",
        metavar: str = "",
        **kwargs: "Run",
    ) -> None:
        self.run = kwargs["Run"]

        super().__init__(
            option_strings,
            dest,
            0,
            const,
            default,
            arg_type,
            choices,
            required,
            help_msg,
            metavar,
        )

    @abc.abstractmethod
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        raise NotImplementedError


class _MessageHelpAction(_CallbackAction):
    """Display the help message of a message."""

    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        nargs: None = None,
        const: None = None,
        default: None = None,
        arg_type: None = None,
        choices: None = None,
        required: bool = False,
        help_msg: str = "",
        metavar: str = "",
        **kwargs: "Run",
    ) -> None:
        self.run = kwargs["Run"]
        super().__init__(
            option_strings,
            dest,
            "+",
            const,
            default,
            arg_type,
            choices,
            required,
            help_msg,
            metavar,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[str], None],
        option_string: Optional[str] = "--help-msg",
    ) -> None:
        if isinstance(values, (list, tuple)):
            self.run.linter.msgs_store.help_message(values)
        elif isinstance(values, str):
            self.run.linter.msgs_store.help_message(utils._splitstrip(values))
        else:
            raise argparse.ArgumentTypeError(f"{values} should be a string.")
        sys.exit(0)


class _ListMessagesAction(_AccessRunObjectAction):
    """Display all available messages."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--list-enabled",
    ) -> None:
        self.run.linter.msgs_store.list_messages()
        sys.exit(0)


class _ListMessagesEnabledAction(_AccessRunObjectAction):
    """Display all enabled messages."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--list-msgs-enabled",
    ) -> None:
        self.run.linter.list_messages_enabled()
        sys.exit(0)


class _ListCheckGroupsAction(_AccessRunObjectAction):
    """Display all the check groups that pylint knows about."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--list-groups",
    ) -> None:
        for check in self.run.linter.get_checker_names():
            print(check)
        sys.exit(0)


class _ListConfidenceLevelsAction(_AccessRunObjectAction):
    """Display all the confidence levels that pylint knows about."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--list-conf-levels",
    ) -> None:
        for level in interfaces.CONFIDENCE_LEVELS:
            print(f"%-18s: {level}")
        sys.exit(0)


class _ListExtensionsAction(_AccessRunObjectAction):
    """Display all extensions under pylint.extensions."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--list-extensions",
    ) -> None:
        for filename in Path(extensions.__file__).parent.iterdir():
            if filename.suffix == ".py" and not filename.stem.startswith("_"):
                extension_name, _, _ = filename.stem.partition(".")
                print(f"pylint.extensions.{extension_name}")
        sys.exit(0)


class _FullDocumentationAction(_AccessRunObjectAction):
    """Display the full documentation."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--full-documentation",
    ) -> None:
        utils.print_full_documentation(self.run.linter)
        sys.exit(0)


class _GenerateRCFileAction(_AccessRunObjectAction):
    """Generate a pylintrc file."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--generate-rcfile",
    ) -> None:
        self.run.linter.generate_config(skipsections=("COMMANDS",))
        sys.exit(0)


class _ErrorsOnlyModeAction(_AccessRunObjectAction):
    """Turn on errors-only mode.

    Error mode:
        * disable all but error messages
        * disable the 'miscellaneous' checker which can be safely deactivated in
          debug
        * disable reports
        * do not save execution information
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--errors-only",
    ) -> None:
        self.run.linter.error_mode()


class _VerboseModeAction(_AccessRunObjectAction):
    """Turn on verbose mode."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--verbose",
    ) -> None:
        self.run.verbose = True


class _EnableAllExtensionsAction(_AccessRunObjectAction):
    """Turn on all extensions."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--enable-all-extensions",
    ) -> None:
        for filename in Path(extensions.__file__).parent.iterdir():
            if filename.suffix == (".py") and not filename.stem.startswith("_"):
                extension_name = f"pylint.extensions.{filename.stem}"
                if extension_name not in self.run._plugins:
                    self.run._plugins.append(extension_name)


class _LongHelpAction(_AccessRunObjectAction):
    """Display the long help message."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = "--long-help",
    ) -> None:
        print(self.run.linter.help(1))
        sys.exit(0)
