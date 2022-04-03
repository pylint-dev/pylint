# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Callback actions for various options."""

import abc
import argparse
from typing import Any, Optional, Sequence, Union


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
