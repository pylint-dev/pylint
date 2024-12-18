# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from typing import Optional

class BaseProgressReporter:
    """Progress reporter.
    """

    def __init__(self) -> None:
        self.item_count = None
        self.current_count = 0

    def increment(self, filename: str) -> None:
        """Print the next filename."""
        self.current_count += 1
        msg = filename
        if self.item_count is not None:
            msg = f"{msg} ({self.current_count} of {self.item_count})"
        self.print_message(msg)

    def print_message(self, msg: str) -> None:
        """Display progress message."""
        raise NotImplementedError()


class StdoutProgressReporter(BaseProgressReporter):
    """Print progress to stdout."""

    def print_message(self, msg: str) -> None:
        """Display progress message."""
        print(msg, flush=True)


class NullProgressReporter(BaseProgressReporter):
    """Suppress progress output."""

    def print_message(self, msg: str) -> None:
        """Do nothing."""


def get_progress_reporter(verbose: bool, item_count: Optional[int] = None) -> BaseProgressReporter:
    """
    Get a progress reporter.

    Parameters:
        verbose (bool): Whether the reporter should display output.
        item_count (Optional[int]): total count of items.  If included, "(1 of n)" is printed.

    Returns:
        BaseProgressReporter: An instance of the progress reporter.
    """
    p: BaseProgressReporter = NullProgressReporter()
    if verbose:
        p = StdoutProgressReporter()
    p.item_count = item_count
    return p
