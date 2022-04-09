# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for deprecation warnings in the config module."""


import pytest

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class SampleChecker(BaseChecker):
    options = (("test-opt", {"action": "store_true"}),)


class TestDeprecationArgumentsManager:
    """Tests for deprecation warnings in the ArgumentsManager class."""

    linter = PyLinter()

    @classmethod
    def setup_class(cls) -> None:
        cls.linter.register_checker(SampleChecker(cls.linter))

    def test_load_configuration(self) -> None:
        """Test that load_configuration emits a DeprecationWarning."""

        with pytest.warns(DeprecationWarning):
            self.linter.load_configuration(test_opt=True)

    def test_load_configuration_from_config(self) -> None:
        """Test that load_configuration_from_config emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.load_configuration_from_config({"test_opt": True})
