# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Functional full-module tests for PyLint."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from _pytest.config import Config
from pytest_remaster import GoldenMaster  # type: ignore[import-not-found]

from pylint import testutils
from pylint.constants import PY312_PLUS
from pylint.lint.pylinter import MANAGER
from pylint.testutils.functional import (
    FunctionalTestFile,
    get_functional_test_files_from_directory,
)

if TYPE_CHECKING:
    from pylint.lint import PyLinter

FUNCTIONAL_DIR = Path(__file__).parent.resolve() / "functional"


TEST_WITH_EXPECTED_DEPRECATION = [
    "anomalous_backslash_escape",
    "anomalous_unicode_escape",
    "excess_escapes",
    "future_unicode_literals",
]


@pytest.fixture
def revert_stateful_config_changes(linter: PyLinter) -> Iterator[PyLinter]:
    yield linter
    # Revert any stateful configuration changes.
    MANAGER.brain["module_denylist"] = set()
    MANAGER.brain["prefer_stubs"] = False


@pytest.mark.usefixtures("revert_stateful_config_changes")
@pytest.mark.parametrize(
    "test_file",
    get_functional_test_files_from_directory(FUNCTIONAL_DIR),
    ids=lambda x: x.base,
)
def test_functional(
    test_file: FunctionalTestFile,
    pytestconfig: Config,
    golden_master: GoldenMaster,
) -> None:
    __tracebackhide__ = True  # pylint: disable=unused-variable
    lint_test = testutils.LintModuleTest(test_file, pytestconfig)
    lint_test.setUp()

    if test_file.base in TEST_WITH_EXPECTED_DEPRECATION:
        exception_type = SyntaxWarning if PY312_PLUS else DeprecationWarning
        with pytest.warns(exception_type, match="invalid escape sequence"):
            actual_output = lint_test.check_messages()
    else:
        actual_output = lint_test.check_messages()

    serialized_output = lint_test.serialize_output(actual_output)
    if test_file.expected_output_is_fallback:
        expected = Path(test_file.expected_output).read_text(encoding="utf-8")
        assert serialized_output.rstrip() == expected.rstrip()
    else:
        golden_master.check(
            serialized_output, test_file.expected_output
        )
