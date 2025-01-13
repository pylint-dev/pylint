# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import abc


class BaseProgressReporter:
    """Progress reporter."""

    def __init__(self) -> None:
        self._ast_count = 0
        self._lint_counter = 0

    def start_get_asts(self) -> None:
        self._print_message("Get ASTs.")

    def get_ast_for_file(self, filename: str) -> None:
        self._print_message(f"AST for {filename}")

    def start_linting(self, ast_count: int) -> None:
        self._ast_count = ast_count
        self._print_message(f"Linting {self._ast_count} modules.")

    def lint_file(self, filename: str) -> None:
        self._lint_counter += 1
        self._print_message(f"{filename} ({self._lint_counter} of {self._ast_count})")

    @abc.abstractmethod
    def _print_message(self, msg: str) -> None:
        """Display progress message."""
        raise NotImplementedError()


class StdoutProgressReporter(BaseProgressReporter):
    """Print progress to stdout."""

    def _print_message(self, msg: str) -> None:
        """Display progress message."""
        print(msg, flush=True)


class NullProgressReporter(BaseProgressReporter):
    """Suppress progress output."""

    def _print_message(self, msg: str) -> None:
        """Do nothing."""


def get_progress_reporter(verbose: bool) -> BaseProgressReporter:
    """
    Get a progress reporter.

    Parameters:
        verbose (bool): Whether the reporter should display output.

    Returns:
        BaseProgressReporter: An instance of the progress reporter.
    """
    if verbose:
        return StdoutProgressReporter()
    return NullProgressReporter()
