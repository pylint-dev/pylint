# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Tests related to linting of namespace packages."""

from io import StringIO

from pylint.reporters.text import TextReporter
from pylint.testutils._run import _Run as Run


def test_namespace_package_sys_path() -> None:
    """Test that we do not append namespace packages to sys.path.

    The test package is based on https://github.com/PyCQA/pylint/issues/2648.
    """
    pylint_output = StringIO()
    reporter = TextReporter(pylint_output)
    runner = Run(
        ["tests/regrtest_data/namespace_import_self/"],
        reporter=reporter,
        exit=False,
    )
    assert not runner.linter.reporter.messages
