# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for deprecation warnings in the config module."""


import warnings

import pytest

from pylint.checkers import BaseChecker
from pylint.lint import PyLinter
from pylint.utils import get_global_option


class SampleChecker(BaseChecker):
    options = (("test-opt", {"action": "store_true", "help": "help message"}),)


class SampleCheckerTwo(BaseChecker):
    options = (
        ("test-opt-two", {"action": "store", "type": "string", "help": "help message"}),
    )


class SampleCheckerThree(BaseChecker):
    options = (
        (
            "test-opt-three",
            {"action": "store_true", "level": 1, "help": "help message"},
        ),
    )


class TestDeprecationArgumentsManager:
    """Tests for deprecation warnings in the ArgumentsManager class."""

    linter = PyLinter()

    @classmethod
    def setup_class(cls) -> None:
        checker = SampleChecker(cls.linter)
        cls.linter.register_checker(checker)
        with pytest.warns(DeprecationWarning):
            cls.linter.register_options_provider(checker)

    def test_load_configuration(self) -> None:
        """Test that load_configuration emits a DeprecationWarning."""

        with pytest.warns(DeprecationWarning):
            self.linter.load_configuration(test_opt=True)

    def test_load_configuration_from_config(self) -> None:
        """Test that load_configuration_from_config emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.load_configuration_from_config({"test_opt": True})

    def test_help_with_level(self) -> None:
        """Test that help with a level argument raises a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.help(1)

        with pytest.warns(DeprecationWarning):
            self.linter.help(level=1)

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            self.linter.help()

    def test_register_options_provider_load_defaults(self) -> None:
        """Test that register_options_provider and load_defaults emits a DeprecationWarning."""
        checker = BaseChecker(self.linter)
        with pytest.warns(DeprecationWarning):
            self.linter.register_options_provider(checker)
        with pytest.warns(DeprecationWarning):
            self.linter.load_defaults()

    def test_get_global_option(self) -> None:
        """Test that get_global_option emits a DeprecationWarning."""
        checker = BaseChecker(self.linter)
        with pytest.warns(DeprecationWarning):
            get_global_option(checker, "test-opt")  # type: ignore[call-overload]

    def test_read_config_file(self) -> None:
        """Test that read_config_file emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.read_config_file()

    def test_load_config_file(self) -> None:
        """Test that load_config_file emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.load_config_file()

    def test_load_command_line_configuration(self) -> None:
        """Test that load_command_line_configuration emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.load_command_line_configuration([])

    def test_cb_set_provider_option(self) -> None:
        """Test that cb_set_provider_option emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.cb_set_provider_option(None, "--test-opt", True, None)

    def test_level_attribute(self) -> None:
        """Test that the level attribute emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            self.linter.level = 1

        with pytest.warns(DeprecationWarning):
            assert self.linter.level is not None

    def test_no_default_in_optdict(self) -> None:
        """Test that not having a default value in a optiondict emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            SampleCheckerTwo(self.linter)

    def test_no_level_in_optdict(self) -> None:
        """Test that not having a level value in a optiondict emits a DeprecationWarning."""
        with pytest.warns(DeprecationWarning):
            SampleCheckerThree(self.linter)
