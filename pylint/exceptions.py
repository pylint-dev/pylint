# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Exception classes raised by various operations within pylint."""


class InvalidMessageError(Exception):
    """Raised when a message creation, registration or addition is rejected."""


class UnknownMessageError(Exception):
    """Raised when an unregistered message id is encountered."""


class EmptyReportError(Exception):
    """Raised when a report is empty and so should not be displayed."""


class InvalidReporterError(Exception):
    """Raised when selected reporter is invalid (e.g. not found)."""


class InvalidArgsError(ValueError):
    """Raised when passed arguments are invalid, e.g., have the wrong length."""


class NoLineSuppliedError(Exception):
    """Raised when trying to disable a message on a next line without supplying a line number."""
