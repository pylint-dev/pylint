# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from argparse import Namespace


class BaseProgressReporter:
    """Progress reporter.

    NOTE: for discussion in draft PR.  This class keeps progress
    reporting separate from linting, and potentially allows for
    reporting to a filestream, etc.
    """

    def __init__(self) -> None:
        self.item_count = 0
        self.current_count = 0

    def increment(self, filename: str) -> None:
        """Print the next filename."""
        # NOTE: This currently just prints each increment, perhaps would
        # be better to output every, say 5 or 10% of the total count.
        self.current_count += 1
        msg = f"{filename} ({self.current_count} of {self.item_count})"
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


def get_progress_reporter(config: Namespace, item_count: int) -> BaseProgressReporter:
    """Get progress reporter as requested by command line args."""
    p: BaseProgressReporter = NullProgressReporter()
    if config.verbose:
        p = StdoutProgressReporter()
    p.item_count = item_count
    p.output_filenames = config.show_current_file
    return p
