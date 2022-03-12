# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Pylint [options] modules_or_packages.

  Check that module(s) satisfy a coding standard (and more !).

    pylint --help

  Display this help message and exit.

    pylint --help-msg <msg-id>[,<msg-id>]

  Display help messages about given message identifiers and exit.
"""
import sys

from pylint.lint.parallel import check_parallel
from pylint.lint.pylinter import PyLinter
from pylint.lint.report_functions import (
    report_messages_by_module_stats,
    report_messages_stats,
    report_total_messages_stats,
)
from pylint.lint.run import Run
from pylint.lint.utils import (
    ArgumentPreprocessingError,
    _patch_sys_path,
    fix_import_path,
    preprocess_options,
)

__all__ = [
    "check_parallel",
    "PyLinter",
    "report_messages_by_module_stats",
    "report_messages_stats",
    "report_total_messages_stats",
    "Run",
    "ArgumentPreprocessingError",
    "_patch_sys_path",
    "fix_import_path",
    "preprocess_options",
]

if __name__ == "__main__":
    Run(sys.argv[1:])
