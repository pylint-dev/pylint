# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for deprecation warnings in the config module."""


import pytest

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter
from pylint.utils import get_global_option


class SampleChecker(BaseChecker):
    options = (("test-opt", {"action": "store_true", "help": "help message"}),)


class TestDeprecationArgumentsManager:
    """Tests for deprecation warnings in the ArgumentsManager class."""

    linter = PyLinter()

    @classmethod
    def setup_class(cls) -> None:
        checker = SampleChecker(cls.linter)
        cls.linter.register_checker(checker)

    def test_get_global_option(self) -> None:
        """Test that get_global_option emits a DeprecationWarning."""
        checker = BaseChecker(self.linter)
        with pytest.warns(DeprecationWarning):
            get_global_option(checker, "test-opt")  # type: ignore[call-overload]
